"""
«Учить слова» при открытом занятии — продолжить или начать новое (2.2.1).

ЧТО БЫЛО. Кнопка «Учить слова» и все `learn_now:*` всегда начинали новое
занятие, а открытое помечали брошенным. Прод 14–18.10: 28 из 84 «брошенных»
занятий — человек нажал «Учить» и начал заново за две минуты; начатое
пропадало без итога, баллов за занятие и повтора ошибок.

ПРАВИЛО (владелец, 18.10). Было начато — предложить «Продолжить» или
«Начать новое». Не было начатого (ни одного ответа) — как сейчас: новое сразу.
"""

import pytest
from sqlalchemy import select

from app.bot.handlers.quiz.card import STATE_CARD_ID
from app.bot.handlers.quiz.lesson import CB_NEW, CB_RESUME
from app.core.clock import utcnow
from app.database.models import QuizSession
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.test_games_audit_oct14 import LEARN, _words

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def stage(session, user):
    await _words(session, user)
    user.onboarded_at = utcnow()      # не первый урок: обычный круг из 15
    await session.commit()
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


def _ctx(dp, bot, user):
    return dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)


async def _sessions(session, user):
    rows = (await session.execute(
        select(QuizSession).where(QuizSession.user_id == user.id).order_by(QuizSession.id)
    )).scalars().all()
    for row in rows:
        await session.refresh(row)
    return rows


async def _answer(dp, bot, user):
    data = await _ctx(dp, bot, user).get_data()
    await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))


def _offers(recorder):
    """Сообщения с кнопками «Продолжить / Начать новое»."""
    out = []
    for name, payload in recorder.calls:
        if name != "SendMessage":
            continue
        rows = (payload.get("reply_markup") or {}).get("inline_keyboard") or []
        data = [b.get("callback_data") for row in rows for b in row]
        if CB_RESUME in data:
            out.append((payload.get("text"), data))
    return out


async def test_without_answers_learn_starts_anew_as_before(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, text_update(user.id, LEARN))

    first, second = await _sessions(session, user)
    assert not _offers(recorder), "без ответов предлагать нечего"
    assert first.exit_reason == "restarted"
    assert second.exit_reason is None and not second.is_completed


async def test_with_an_answer_learn_offers_to_continue_and_closes_nothing(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    await dp.feed_update(bot, text_update(user.id, LEARN))

    offers = _offers(recorder)
    assert len(offers) == 1, offers
    text, buttons = offers[0]
    assert text == get_text("lesson_resume_prompt", "ru", done=1, total=15)
    assert buttons == [CB_RESUME, f"{CB_NEW}:menu"]
    (only,) = await _sessions(session, user)
    assert only.exit_reason is None, "занятие закрыто до решения человека"


async def test_continue_after_an_answered_question_goes_to_the_next(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    old_card = (await _ctx(dp, bot, user).get_data())[STATE_CARD_ID]
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, press(user.id, CB_RESUME, message_id=777))

    data = await _ctx(dp, bot, user).get_data()
    assert data["current_question"] == 2
    (only,) = await _sessions(session, user)
    assert data["session_id"] == only.id and only.exit_reason is None
    deleted = {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}
    assert old_card in deleted, "прежняя карточка осталась живой"


async def test_continue_on_an_unanswered_question_shows_the_same_number(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    await dp.feed_update(bot, press(user.id, "next_question"))       # вопрос 2 показан
    await dp.feed_update(bot, text_update(user.id, LEARN))

    (text, _), = _offers(recorder)
    assert text == get_text("lesson_resume_prompt", "ru", done=1, total=15)
    await dp.feed_update(bot, press(user.id, CB_RESUME, message_id=777))
    data = await _ctx(dp, bot, user).get_data()
    assert data["current_question"] == 2, "неотвеченный вопрос пропущен"
    await _answer(dp, bot, user)
    (only,) = await _sessions(session, user)
    assert only.answered_questions == 2


async def test_continue_clears_a_menu_screen_opened_mid_lesson(session, user, stage):
    """
    Прод 18.10, владелец: начал занятие, открыл «Статистику», нажал «Учить»
    → «Продолжить» — экран статистики остался висеть над вопросом.
    """
    from app.database.models import User

    dp, bot, recorder = stage
    rs = bot.session
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)

    before = rs._next_id
    await dp.feed_update(bot, text_update(user.id, get_text("btn_stats", "ru")))
    fresh = await session.get(User, user.id)
    await session.refresh(fresh)
    screens = set(range(before + 1, rs._next_id + 1)) - {fresh.anchor_message_id}
    assert screens, "экран статистики не показан"

    await dp.feed_update(bot, text_update(user.id, LEARN))
    prompt = rs._next_id
    await dp.feed_update(bot, press(user.id, CB_RESUME, message_id=prompt))

    deleted = {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}
    assert screens <= deleted, f"остались на экране: {sorted(screens - deleted)}"
    assert fresh.anchor_message_id not in deleted, "якорь с клавиатурой удалён"
    assert (await _ctx(dp, bot, user).get_data())["current_question"] == 2


async def test_double_continue_moves_the_lesson_once(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, press(user.id, CB_RESUME, message_id=777))
    await dp.feed_update(bot, press(user.id, CB_RESUME, message_id=777))

    data = await _ctx(dp, bot, user).get_data()
    assert data["current_question"] == 2


async def test_start_new_closes_the_old_as_abandoned(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, press(user.id, f"{CB_NEW}:menu", message_id=777))

    first, second = await _sessions(session, user)
    assert first.exit_reason == "abandoned" and first.exit_at_question == 1
    assert second.start_source == "menu" and second.exit_reason is None
    data = await _ctx(dp, bot, user).get_data()
    assert data["session_id"] == second.id and data["current_question"] == 1


async def test_a_resumed_lesson_ends_with_one_summary(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, press(user.id, CB_RESUME, message_id=777))
    for _ in range(20):
        data = await _ctx(dp, bot, user).get_data()
        if not data.get("session_id") or data.get("current_question", 99) > 15:
            break
        await _answer(dp, bot, user)
        await dp.feed_update(bot, press(user.id, "next_question"))

    (only,) = await _sessions(session, user)
    assert only.is_completed and only.answered_questions == 15
    summaries = [t for t in recorder.sent_texts() if t.startswith(get_text("quiz_completed", "ru"))]
    assert len(summaries) == 1, summaries


async def test_learn_now_from_a_reminder_offers_too(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await _answer(dp, bot, user)
    await dp.feed_update(bot, press(user.id, "learn_now:reminder", message_id=600))

    (_, buttons), = _offers(recorder)
    assert buttons == [CB_RESUME, f"{CB_NEW}:reminder"]
