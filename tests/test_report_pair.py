"""
Жалоба знает пару языков (Н4–Н6, 16.10).

С десятью языками «перевод неверный» без пары не говорит, какую колонку
править, и в чей рейтинг класть балл. Три проверки:
  * пара пишется из занятия, где ошибку видели, а не нынешняя;
  * на то же слово можно пожаловаться в другой паре;
  * админ видит обе стороны ИМЕННО этой пары, балл — в ряд её языка.
"""
from sqlalchemy import select

from app.bot.handlers.admin import _build_reports_text_and_keyboard, admin_report_approve
from app.database.enums import CEFRLevel
from app.database.models import MonthlyStats, QuizSession, TranslationReport
from app.services.monthly_leaderboard_service import get_or_create_current_season
from tests.conftest import make_word
from tests.scenario import make_bot, make_dispatcher, press, reset_state

ADMIN_ID = 1


async def _quiz(session, user, learning, native):
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7,
                       learning_lang=learning, native_lang=native)
    session.add(quiz)
    await session.commit()
    return quiz


async def _send_report(session, user, word, quiz):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    state = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await state.update_data(report_selected=[word.id], report_session_id=quiz.id,
                            saved_errors=[])
    await dp.feed_update(bot, press(user.id, "report_send"))


async def test_pair_comes_from_the_lesson_not_from_the_current_settings(session, user):
    word = make_word("Haus", cs="dům", ru="дом")
    session.add(word)
    await session.commit()
    quiz = await _quiz(session, user, "de", "cs")     # человек сейчас учит de→ru

    await _send_report(session, user, word, quiz)
    report = (await session.execute(select(TranslationReport))).scalar_one()
    assert (report.learning_lang, report.native_lang) == ("de", "cs")


async def test_same_word_can_be_reported_in_another_pair(session, user):
    word = make_word("Haus", cs="dům", ru="дом")
    session.add(word)
    await session.commit()
    await _send_report(session, user, word, await _quiz(session, user, "de", "cs"))
    await _send_report(session, user, word, await _quiz(session, user, "de", "ru"))
    pairs = {(r.learning_lang, r.native_lang) for r in
             (await session.execute(select(TranslationReport))).scalars()}
    assert pairs == {("de", "cs"), ("de", "ru")}


async def test_admin_sees_both_sides_of_that_pair(session, user):
    word = make_word("Haus", cs="dům", ru="дом")
    session.add(word)
    await session.commit()
    session.add(TranslationReport(user_id=user.id, word_id=word.id, kind="text",
                                  status="pending", learning_lang="de", native_lang="cs"))
    await session.commit()
    text, _ = await _build_reports_text_and_keyboard(session)
    assert "Dům" in text, text
    assert "Чешский" in text


async def test_point_lands_in_the_rating_of_the_reports_language(session, user):
    season = await get_or_create_current_season(session)
    word = make_word("Haus", ru="дом", en="house")
    session.add(word)
    await session.commit()
    # Человек сейчас учит de, а жаловался, когда учил en (занятия нет)
    session.add(TranslationReport(user_id=user.id, word_id=word.id, kind="text",
                                  status="pending", learning_lang="en", native_lang="ru"))
    await session.commit()

    bot, _ = make_bot()
    callback = press(ADMIN_ID, f"admin:report_approve_text_{word.id}").callback_query.as_(bot)
    await admin_report_approve(callback, session)

    rows = (await session.execute(select(MonthlyStats).where(
        MonthlyStats.user_id == user.id, MonthlyStats.season_id == season.id))).scalars().all()
    assert [r.learning_lang for r in rows if r.report_bonus] == ["en"]
