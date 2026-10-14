"""
Петля возврата: у каждого конца есть начало.

Замер на 233 людях (`MENU_CONCEPT.md`): 79% тех, кто вообще играл, ни разу
не занимались два дня подряд. Люди не теряются в меню — в четырёх кнопках
заблудиться нельзя, — они просто не приходят во второй раз.

Петля была разорвана в четырёх местах, и каждый разрыв выглядел одинаково:
**экран кончается, а следующего действия не предлагает.**

    напоминание          ни одной кнопки, хотя обе лежали в шести локалях
    итог круга           настройки и форма жалобы, «ещё раз» нет
    после выбора уровня  текст «нажми кнопку» вместо кнопки
    домашний экран       за /start, который набирают один раз в жизни

Эти тесты держат правило: **экран, которым кончается действие, обязан
предлагать следующее действие.** Проверяется наличие кнопки и её место, а
не текст: надпись переведут, порядок сломают молча.
"""

import pytest

from app.testing import starts_lesson

from app.bot.handlers.quiz.game import get_results_keyboard
from app.bot.handlers.reminders import get_reminder_offer_keyboard
from app.bot.keyboards.notifications import get_reminder_keyboard
from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import User
from app.locales import LOCALES
from app.services.reminder_service import (
    FALLBACK_HOUR_UTC,
    MIN_ROUNDS_FOR_OWN_TIME,
    should_offer_reminders,
    suggest_reminder_time,
)


def _data(keyboard) -> list[str]:
    return [b.callback_data for row in keyboard.inline_keyboard for b in row]


# ============================================================================
# НАПОМИНАНИЕ
# ============================================================================

def test_reminder_offers_a_way_to_start_and_a_way_to_stop():
    """
    Прежде напоминание приходило БЕЗ ЕДИНОЙ КНОПКИ: в тексте стояло «не
    прерывай серию», а нажать было нечего.

    Вторая кнопка не менее важна первой: выключить напоминания можно было
    только найдя их в настройках, а человек, которому они надоели, в
    настройки не идёт — он блокирует бота.
    """
    data = _data(get_reminder_keyboard("ru"))

    assert starts_lesson(data[0]), f"первая кнопка не ведёт к занятию: {data}"
    assert "notif_off" in data, f"нечем отказаться от напоминаний: {data}"


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_reminder_keyboard_speaks_every_language(lang):
    """Пропущенный ключ не падает — он уезжает человеку как «[MISSING: …]»."""
    texts = [b.text for row in get_reminder_keyboard(lang).inline_keyboard for b in row]

    assert len(texts) == 2
    for text in texts:
        assert "[MISSING:" not in text and "[ERROR:" not in text, f"{lang}: {text}"


# ============================================================================
# ИТОГ КРУГА
# ============================================================================

def test_round_result_offers_another_round_first():
    """
    Самый высокий момент мотивации за день. Прежде бот предлагал здесь
    «изменить режим викторины» и «сообщить об ошибке», а кнопки продолжить
    не было вовсе.
    """
    data = _data(get_results_keyboard(has_errors=False, lang="ru"))

    assert starts_lesson(data[0]), f"«ещё круг» не первым: {data}"


def test_complaint_never_outranks_continuing():
    """
    Жалоба нужна редко и не должна стоять выше того, зачем человек здесь.
    Проверяется на обоих видах круга: с ошибками и без.
    """
    for has_errors in (False, True):
        data = _data(get_results_keyboard(has_errors=has_errors, lang="ru"))
        lesson = next(i for i, d in enumerate(data) if starts_lesson(d))
        assert lesson < data.index("report_translation_error"), (
            f"жалоба выше продолжения при has_errors={has_errors}: {data}"
        )


def test_repeating_errors_stays_right_after_continuing():
    """Ошибки — про только что пройденное, им второе место, а не последнее."""
    data = _data(get_results_keyboard(has_errors=True, lang="ru"))

    assert data[1] == "repeat_errors", f"повтор ошибок не вторым: {data}"


# ============================================================================
# КОГДА ПРЕДЛАГАТЬ НАПОМИНАНИЯ
# ============================================================================

def _user(**kwargs) -> User:
    base = dict(
        id=1, interface_language="ru", learning_lang="de", native_lang="ru",
        reverse_mode=False,
    )
    base.update(kwargs)
    user = User(**base)
    # Значения по умолчанию из модели проставляются только при записи в БД,
    # а проверяем мы чистую функцию — задаём явно
    user.notifications_enabled = kwargs.get("notifications_enabled", False)
    user.reminder_offered_at = kwargs.get("reminder_offered_at")
    user.quizzes_passed = kwargs.get("quizzes_passed", 0)
    return user


def test_not_offered_before_the_first_round_is_finished():
    """
    В онбординге спрашивать нельзя: человек ещё не знает, нужен ли ему бот,
    и ответит «нет» — а второго раза правило уже не даст.
    """
    assert not should_offer_reminders(_user(quizzes_passed=0))


def test_offered_right_after_the_first_round():
    assert should_offer_reminders(_user(quizzes_passed=1))


def test_never_offered_twice():
    """
    Второе предложение того же самого человек воспринимает не как заботу, а
    как навязывание, и уходит не от напоминаний, а от бота.
    """
    asked = _user(quizzes_passed=5, reminder_offered_at=utcnow())

    assert not should_offer_reminders(asked)


def test_not_offered_when_already_on():
    assert not should_offer_reminders(
        _user(quizzes_passed=1, notifications_enabled=True)
    )


def test_old_users_with_many_rounds_are_still_offered_once():
    """
    112 человек с выключенными напоминаниями и десятками кругов за спиной —
    ровно те, кого мы потеряли. Условие «после первого круга» не должно
    читаться как «только новичкам».
    """
    veteran = _user(quizzes_passed=40)

    assert should_offer_reminders(veteran), "ветеран не получит предложения"


def test_offer_keyboard_lets_you_say_no_in_one_tap():
    """
    Предложение, от которого нельзя отказаться одним нажатием, читается как
    навязывание.
    """
    data = _data(get_reminder_offer_keyboard("ru"))

    assert data == ["reminder_offer_yes", "reminder_offer_no"], data


# ============================================================================
# НА КАКОЙ ЧАС СТАВИТЬ
# ============================================================================

@pytest.mark.asyncio
async def test_time_without_history_falls_back_to_the_measured_hour(session, user):
    """
    У человека без кругов своего расписания нет. Запасной час не выдуман:
    замерен по всем 2 318 кругам базы.
    """
    user.timezone = "UTC"
    await session.commit()

    assert await suggest_reminder_time(user, session) == f"{FALLBACK_HOUR_UTC:02d}:00"


@pytest.mark.asyncio
async def test_a_single_round_is_not_a_habit(session, user):
    """
    Один круг — это случай, а не привычка: ткнул в обеденный перерыв, и
    напоминание навсегда село бы на этот час.
    """
    from app.database.models import QuizSession

    user.timezone = "UTC"
    for _ in range(MIN_ROUNDS_FOR_OWN_TIME - 1):
        session.add(QuizSession(
            user_id=user.id, learning_lang="de", total_questions=15,
            level=CEFRLevel.A1,
            started_at=utcnow().replace(hour=3, minute=0, second=0, microsecond=0),
        ))
    await session.commit()

    assert await suggest_reminder_time(user, session) == f"{FALLBACK_HOUR_UTC:02d}:00"


@pytest.mark.asyncio
async def test_own_schedule_wins_once_there_is_enough_of_it(session, user):
    from app.database.models import QuizSession

    user.timezone = "UTC"
    for _ in range(MIN_ROUNDS_FOR_OWN_TIME):
        session.add(QuizSession(
            user_id=user.id, learning_lang="de", total_questions=15,
            level=CEFRLevel.A1,
            started_at=utcnow().replace(hour=6, minute=30, second=0, microsecond=0),
        ))
    await session.commit()

    assert await suggest_reminder_time(user, session) == "06:00"


@pytest.mark.asyncio
async def test_measured_hour_is_translated_into_the_persons_timezone(session, user):
    """
    Планировщик сравнивает `notification_time` с МЕСТНЫМ временем человека.
    Забудь перевод — и напоминание приходит со сдвигом на пару часов, молча:
    оно ведь всё равно приходит.
    """
    from app.database.models import QuizSession

    user.timezone = "Europe/Kyiv"      # UTC+2 зимой, +3 летом
    for _ in range(MIN_ROUNDS_FOR_OWN_TIME):
        session.add(QuizSession(
            user_id=user.id, learning_lang="de", total_questions=15,
            level=CEFRLevel.A1,
            started_at=utcnow().replace(hour=6, minute=0, second=0, microsecond=0),
        ))
    await session.commit()

    local = await suggest_reminder_time(user, session)

    assert local != "06:00", "час не переведён в часовой пояс человека"
    assert local in ("08:00", "09:00"), f"перевод дал неправдоподобный час: {local}"


# ============================================================================
# НАПОМИНАНИЕ СО ШКАЛАМИ
#
# Прежде там висели четыре счётчика: «Викторин пройдено: 12 · Слов изучено:
# 47 · Точность: 88%». Ни одно из этих чисел не говорит, ЧЕГО человеку не
# хватает. Три шкалы говорят.
# ============================================================================

@pytest.mark.asyncio
async def test_reminder_shows_the_scales_when_there_is_progress(session, user):
    from app.database.enums import QuizMode
    from app.schedulers.reminder_scheduler import build_reminder_text
    from tests.test_home import _progress, _seed

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.streak_days = 3
    await _seed(session, user, words_a1=3, words_b1=0)

    from sqlalchemy import select
    from app.database.models import Word

    word = (await session.execute(select(Word))).scalars().first()
    session.add(_progress(user.id, word.id, times_shown=5, times_correct=3))
    await session.commit()

    text = await build_reminder_text(user, session)

    assert "<code>" in text, "шкал в напоминании нет"
    assert "▓" in text, "ни одна полоса не закрашена"


@pytest.mark.asyncio
async def test_reminder_without_progress_shows_no_empty_bars(session, user):
    """
    У новичка все три полосы пусты, и показывать их — значит встретить его
    тремя нулями. Напоминание пришло звать заниматься, а не отчитываться.
    """
    from app.database.enums import QuizMode
    from app.schedulers.reminder_scheduler import build_reminder_text
    from tests.test_home import _seed

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await _seed(session, user, words_a1=2, words_b1=0)
    await session.commit()

    text = await build_reminder_text(user, session)

    assert "░" not in text, "новичку показали пустые полосы"
    assert "<code>" not in text
    assert len(text.strip()) > 20, "осталось пустое сообщение"


# ============================================================================
# ВСТУПИТЕЛЬНЫЙ БЛОК НЕ ПЕРЕСКАЗЫВАЕТ МЕНЮ
# ============================================================================

@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_intro_does_not_promise_a_button_that_is_not_in_the_menu(lang):
    """
    Прежнее вступление обещало «❓ Помощь» среди кнопок меню, а она уехала
    в настройки ещё накануне. Текст про интерфейс живёт отдельно от самого
    интерфейса и расходится с ним молча — поэтому проверка сверяет их.
    """
    from app.bot.buttons import BTN_HELP, menu_texts
    from app.locales import get_text

    help_label = get_text(BTN_HELP, lang)
    assert help_label not in menu_texts_of_keyboard(lang), (
        "«Помощь» вернулась в меню — проверку надо переписать"
    )

    intro = " ".join(
        get_text(key, lang)
        # `intro_title` больше нет: ключ со значением «<b>GenauLingua</b>»
        # не читала ни одна строка кода — его держали только тесты.
        # `intro_three_games` переименован в `intro_games`: игр стало
        # четыре, и «three» в имени лгало бы.
        for key in ("intro_games", "intro_numbers")
    )
    # Сверяется не слово «помощь», а ИМЕННО надпись кнопки: слово само по
    # себе в тексте появиться может и ничего не обещает
    assert help_label not in intro, f"{lang}: вступление обещает {help_label!r}"
    assert menu_texts, "надписи меню не читаются — проверка вхолостую"


def menu_texts_of_keyboard(lang: str) -> set[str]:
    """Надписи кнопок, которые ДЕЙСТВИТЕЛЬНО стоят в главном меню."""
    from app.bot.keyboards import get_main_menu_keyboard

    keyboard = get_main_menu_keyboard(lang)
    return {button.text for row in keyboard.keyboard for button in row}


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_intro_keyboard_offers_learning_first(lang):
    from app.bot.handlers.start import _intro_keyboard
    from app.database.enums import CEFRLevel as L
    from app.database.models import User as U

    person = U(id=1, interface_language=lang, learning_lang="de",
               native_lang="ru", reverse_mode=False, level=L.B1)
    person.quiz_word_count = 15

    data = _data(_intro_keyboard(person, lang))
    assert starts_lesson(data[0]), (
        f"{lang}: вступление не зовёт заниматься: {data}"
    )
