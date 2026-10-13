"""
Откуда началось занятие: петлю возврата должно быть чем измерить.

ЗАЧЕМ. `start_source` у занятия существовал с самого начала, и в него
ВСЕГДА писалось «menu» — какой бы дверью человек ни вошёл. Замер по
рабочей копии: 2 295 занятий с пустым источником и 25 со «menu» на 2 320
всего. А в админке при этом жила метрика «Из напоминаний», искавшая
`start_source == 'notification'` — значение, которого не писал НИКТО, и
потому она не могла стать ненулевой никогда.

Это не мелочь учёта. Петля возврата — напоминание → занятие → итог →
«ещё круг» — то, что по замеру оказалось главным рычагом (6.85 дней
занятий у включивших напоминания против 1.59 у остальных). И прямой её
замер был невозможен.

Мешала и одна подробность: кнопка напоминания, кнопка домашнего экрана и
кнопка «ещё круг» несли ОДИН И ТОТ ЖЕ `callback_data` — «learn_now», —
то есть источник был неразличим даже в принципе. Теперь у каждой двери
своя пометка после двоеточия, а обработчик остался один: занятие с
напоминания не должно вести себя иначе, чем занятие с экрана.
"""

from sqlalchemy import select

from app.bot.handlers.quiz.game import (
    KNOWN_SOURCES, SOURCE_AGAIN, SOURCE_CHANNEL, SOURCE_HOME, SOURCE_MENU,
    SOURCE_REMINDER, SOURCE_REPEAT, source_from_callback,
)
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import QuizSession, UserWord, Word
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.conftest import build_groups, make_word

import pytest


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def _ready(session, user, *, channels="t", count=4) -> None:
    for i in range(40):
        session.add(make_word(f"Wort{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = count
    user.audio_enabled = "a" in channels or "s" in channels
    user.quiz_channels = channels
    await session.commit()


async def _source_of_last(session, user) -> str | None:
    return (await session.execute(
        select(QuizSession.start_source)
        .where(QuizSession.user_id == user.id)
        .order_by(QuizSession.id.desc()).limit(1)
    )).scalar()


# ============================================================================
# РАЗБОР ПОМЕТКИ
# ============================================================================

def test_tail_after_the_colon_is_the_door():
    assert source_from_callback("learn_now:reminder") == SOURCE_REMINDER
    assert source_from_callback("learn_now:again") == SOURCE_AGAIN


def test_a_button_without_a_tag_falls_back_to_the_default():
    """
    В переписке у людей живут кнопки, отправленные прежними версиями, —
    у них пометки нет. Такое нажатие обязано работать.
    """
    assert source_from_callback("learn_now") == SOURCE_HOME
    assert source_from_callback("learn_now", default=SOURCE_MENU) == SOURCE_MENU


def test_an_unknown_tag_does_not_break_the_lesson():
    """
    Незнакомая пометка сводится к двери по умолчанию МОЛЧА. Ронять занятие
    из-за неузнанной строки нельзя: виноват будет человек, а не строка.
    """
    assert source_from_callback("learn_now:whatever") == SOURCE_HOME
    assert source_from_callback("learn_now:") == SOURCE_HOME


def test_every_door_has_a_name():
    """Все пометки, которые пишет код, перечислены в одном месте."""
    for source in (SOURCE_MENU, SOURCE_HOME, SOURCE_CHANNEL, SOURCE_REMINDER,
                   SOURCE_AGAIN, SOURCE_REPEAT):
        assert source in KNOWN_SOURCES


# ============================================================================
# ПОМЕТКИ НА САМИХ КНОПКАХ
# ============================================================================

def test_the_reminder_button_carries_its_own_door():
    """
    Самая ценная кнопка в боте: единственная, которую человек нажимает,
    не заходя в бота. Если она неотличима от домашнего экрана, замерить
    напоминания нечем.
    """
    from app.bot.keyboards.notifications import get_reminder_keyboard

    data = [
        button.callback_data
        for row in get_reminder_keyboard("ru", count=15).inline_keyboard
        for button in row
    ]
    assert f"learn_now:{SOURCE_REMINDER}" in data, data


def test_the_result_button_says_another_round():
    from app.bot.handlers.quiz.game import get_results_keyboard

    data = [
        button.callback_data
        for row in get_results_keyboard(has_errors=False, lang="ru").inline_keyboard
        for button in row
    ]
    assert f"learn_now:{SOURCE_AGAIN}" in data, data


# ============================================================================
# ЧТО ПОПАДАЕТ В БАЗУ
# ============================================================================

async def test_a_lesson_from_the_reminder_is_recorded_as_such(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)

    await dp.feed_update(bot, press(user.id, f"learn_now:{SOURCE_REMINDER}"))

    assert await _source_of_last(session, user) == SOURCE_REMINDER


async def test_a_lesson_from_the_menu_button_is_recorded_as_menu(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    assert await _source_of_last(session, user) == SOURCE_MENU


async def test_a_lesson_from_the_home_screen_is_recorded_as_home(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)

    await dp.feed_update(bot, press(user.id, "learn_now"))

    assert await _source_of_last(session, user) == SOURCE_HOME


async def test_a_direct_channel_entry_is_recorded_as_channel(session, user, stage):
    """
    Прямой вход 🔤 с домашнего экрана — своя дверь: по ней видно, пользуются
    ли вообще прямыми входами или они стоят зря.
    """
    dp, bot, recorder = stage
    await _ready(session, user, channels="t")

    await dp.feed_update(bot, press(user.id, "home_learn_t"))

    assert await _source_of_last(session, user) == SOURCE_CHANNEL


async def test_another_round_after_the_result_is_recorded_as_again(session, user, stage):
    """
    Второй круг подряд — сам по себе признак вовлечения, и считать его
    надо отдельно от первого.
    """
    dp, bot, recorder = stage
    await _ready(session, user, count=3)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(3):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await dp.feed_update(bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))

    await dp.feed_update(bot, press(user.id, f"learn_now:{SOURCE_AGAIN}"))

    assert await _source_of_last(session, user) == SOURCE_AGAIN


async def test_the_error_repeat_round_is_recorded_as_repeat(session, user, stage):
    """
    Повтор ошибок — тоже занятие, но другого рода: в месячный зачёт он не
    идёт, и в замере дверей его надо видеть отдельно.
    """
    dp, bot, recorder = stage
    await _ready(session, user, count=3)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(3):
        data = await context.get_data()
        correct = data.get("correct_word_id")
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        wrong = next((o for o in options if o != f"answer_{correct}"), options[0])
        await dp.feed_update(bot, press(user.id, wrong))
        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))

    assert "repeat_errors" in recorder.all_buttons(), "ошибок не набралось"
    await dp.feed_update(bot, press(user.id, "repeat_errors"))

    assert await _source_of_last(session, user) == SOURCE_REPEAT
