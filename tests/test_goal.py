"""
Зачем учишь — опрос, встроенный в первое нажатие.

Двадцать категорий в базе есть, режим «по категории» работает — и им
пользуются ТРИ человека из 233. Не потому, что он плох, а потому, что
спрятан третьим уровнем настроек: 223 человека из 233 не меняли режим
викторины ни разу. Выбор — это работа, и её не делают.

ЧТО ЗДЕСЬ ГЛАВНОЕ. Тема подмешивается в НОВЫЕ слова и только в них, а
трудность по-прежнему задаёт уровень. Переключить режим на «по категории»
было бы вдвое дешевле, но замер это отменил: тот режим не смотрит на
уровень ВОВСЕ, и новичок, выбравший «для работы», получал бы C1
вперемешку с A1. А вместе с уровнем многие пары пусты — в «Wirtschaft»
слов уровня A1 всего ДВА.

Отсюда два условия, которые тесты и держат: тема соблюдается, пока слова
темы есть, и НЕ ДЕРЖИТ КРУГ, когда они кончились.
"""

import pytest

from app.database.enums import CEFRLevel, QuizMode, WordCategory
from app.database.models import User, Word
from app.services.goal_service import (
    GOAL_CATEGORIES,
    GOAL_ORDER,
    categories_for,
    is_goal,
)
from app.services.language_service import pair_from_user
from app.services.quiz_service import get_new_words
from tests.conftest import build_groups, make_word


# ============================================================================
# СОПОСТАВЛЕНИЕ ЦЕЛЕЙ И КАТЕГОРИЙ
# ============================================================================

def test_every_offered_goal_is_a_real_goal():
    """
    Кнопка, ведущая в несуществующую цель, молча не сохранила бы ничего.
    """
    for code in GOAL_ORDER:
        assert is_goal(code), f"кнопка {code} ведёт в несуществующую цель"


def test_every_goal_has_a_button():
    """Обратное: цель без кнопки недостижима, а значит мертва."""
    assert set(GOAL_ORDER) == set(GOAL_CATEGORIES), (
        f"цели и кнопки разошлись: {set(GOAL_CATEGORIES) ^ set(GOAL_ORDER)}"
    )


def test_goals_point_at_categories_that_exist():
    """
    Категория сверяется с перечислением, а не с текстом: опечатка в
    названии дала бы пустую тему, и подмешивание тихо перестало бы работать
    — круг при этом собирался бы как ни в чём не бывало.
    """
    known = {c.value for c in WordCategory}
    for goal, cats in GOAL_CATEGORIES.items():
        for cat in cats:
            assert cat.value in known, f"{goal}: нет такой категории {cat.value!r}"


def test_plain_learning_asks_for_no_theme():
    """«Просто учить слова» — честный ответ, а не отказ отвечать."""
    assert categories_for("any") == ()
    assert is_goal("any")


def test_no_goal_means_no_theme():
    """У тех, кого не спрашивали, цели нет, и подмешивать нечего."""
    assert categories_for(None) == ()
    assert categories_for("") == ()


def test_unknown_goal_does_not_crash_the_round():
    """
    В базе может лежать цель, которой больше нет в коде (переименовали,
    выкинули). Круг от этого собираться не перестанет.
    """
    assert categories_for("прошлогодняя_цель") == ()


# ============================================================================
# ПОДМЕШИВАНИЕ В НОВЫЕ СЛОВА
# ============================================================================

WORK = WordCategory.ARBEIT_BERUF
FAR = WordCategory.NATUR_WETTER       # ни в одной цели «work» не числится


async def _seed(session, themed: int, other: int, level=CEFRLevel.A1) -> None:
    for i in range(themed):
        session.add(make_word(f"Arbeit{i}", level=level, category=WORK.value))
    for i in range(other):
        session.add(make_word(f"Wetter{i}", level=level, category=FAR.value))
    await build_groups(session, ["de"])


@pytest.mark.asyncio
async def test_new_words_come_from_the_chosen_theme(session, user):
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.learning_goal = "work"
    await _seed(session, themed=5, other=5)

    pair = pair_from_user(user)
    picked = [
        (await get_new_words(user.id, session, pair, [], user=user)).category
        for _ in range(8)
    ]

    assert set(picked) == {WORK.value}, f"тема не соблюдена: {set(picked)}"


@pytest.mark.asyncio
async def test_theme_never_starves_the_round(session, user):
    """
    Слова темы кончились — берём любые. Это не уступка, а необходимость:
    в «Wirtschaft» слов уровня A1 два, и держать тему до конца значило бы
    оставить человека без вопросов на третьем же круге.
    """
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.learning_goal = "work"
    await _seed(session, themed=1, other=5)

    from sqlalchemy import select

    themed_id = (await session.execute(
        select(Word.id).where(Word.category == WORK.value)
    )).scalar()

    pair = pair_from_user(user)
    # Единственное слово темы исключено — круг обязан продолжиться
    word = await get_new_words(user.id, session, pair, [themed_id], user=user)

    assert word is not None, "круг встал, когда кончились слова темы"
    assert word.category == FAR.value


@pytest.mark.asyncio
async def test_theme_does_not_override_the_level(session, user):
    """
    Тема стоит ПОВЕРХ уровня, а не вместо него. Это главное отличие от
    режима «по категории», который на уровень не смотрит вовсе.
    """
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.learning_goal = "work"
    # Слова темы есть, но все они ЧУЖОГО уровня
    await _seed(session, themed=4, other=0, level=CEFRLevel.C2)
    await _seed(session, themed=0, other=3, level=CEFRLevel.A1)

    pair = pair_from_user(user)
    picked = [
        await get_new_words(user.id, session, pair, [], user=user)
        for _ in range(5)
    ]

    assert all(w is not None for w in picked)
    assert {w.level for w in picked} == {CEFRLevel.A1}, (
        "тема протащила слова чужого уровня"
    )


@pytest.mark.asyncio
async def test_without_a_goal_nothing_changes(session, user):
    """
    У 233 нынешних пользователей цели нет, и отбор для них должен
    остаться в точности прежним.
    """
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.learning_goal = None
    await _seed(session, themed=3, other=3)

    pair = pair_from_user(user)
    picked = {
        (await get_new_words(user.id, session, pair, [], user=user)).category
        for _ in range(20)
    }

    assert picked == {WORK.value, FAR.value}, (
        f"без цели отбор перестал брать все слова уровня: {picked}"
    )


# ============================================================================
# ЦЕЛЬ ДОСТИЖИМА ИЗ НАСТРОЕК
#
# Опрос задаётся в онбординге, и этого МАЛО: у всех 233 нынешних
# пользователей он давно позади, и цель осталась бы у них пустой навсегда,
# а сменить свою они не смогли бы вовсе. Та же дыра, что была у состава
# занятия: колонка есть, экрана нет.
# ============================================================================

def test_goal_has_a_screen_in_settings():
    from app.bot.handlers.quiz.settings import _GROUPS, _PARENT_GROUP

    items = {data for _, _, group in _GROUPS.values() for _, data in group}
    assert "settings_goal" in items, "цель недостижима из настроек"
    assert _PARENT_GROUP["settings_goal"] == "settings_group_what", (
        "цель лежит не в группе «что учу»"
    )


def test_goal_line_shows_up_in_the_settings_state():
    from app.bot.handlers.quiz.settings import _STATE_LINES, _settings_state
    from app.database.enums import CEFRLevel, QuizMode
    from app.database.models import User as U

    person = U(id=1, interface_language="ru", learning_lang="de",
               native_lang="ru", reverse_mode=False,
               level=CEFRLevel.A1, quiz_mode=QuizMode.LEVEL)
    person.audio_enabled = True
    person.quiz_channels = "ta"

    assert "settings_goal" in _STATE_LINES

    person.learning_goal = None
    without = _settings_state(person, "ru", only=("settings_goal",))
    person.learning_goal = "work"
    with_goal = _settings_state(person, "ru", only=("settings_goal",))

    assert without != with_goal, "строка цели не меняется от самой цели"
    assert "[MISSING:" not in without and "[MISSING:" not in with_goal


@pytest.mark.parametrize("code", list(GOAL_ORDER))
def test_every_goal_is_nameable_in_every_language(code):
    """
    Экран настройки печатает названия целей; пропущенный ключ уехал бы
    человеку как «[MISSING: goal_work]».
    """
    from app.locales import LOCALES, get_text

    for lang in LOCALES:
        label = get_text(f"goal_{code}", lang)
        assert "[MISSING:" not in label, f"{lang}: нет названия цели {code}"
