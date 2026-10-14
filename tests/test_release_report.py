"""
Отчёт о рассылке: каждая цифра — по известной истории пяти человек.

Владелец, 14.10: «хочу, чтобы бот мне сделал отчёты по этой теме после
рассылки». Отчёт должен отличать «дошло» от «вернулся» и «проснулся».
"""
from datetime import datetime, timedelta

from app.database.enums import CEFRLevel
from app.database.models import QuizQuestion, QuizSession, User
from app.scripts.release_report import build_report, format_report
from app.scripts.send_release_notes import read_journal
from tests.conftest import make_word

SINCE = datetime(2026, 10, 15, 6, 0)


def _lesson(uid, at, done=True, source=None):
    return QuizSession(user_id=uid, level=CEFRLevel.A1, learning_lang="de", native_lang="ru",
                       total_questions=15, answered_questions=15 if done else 3,
                       correct_answers=10, is_completed=done, started_at=at,
                       completed_at=at + timedelta(minutes=4) if done else None,
                       quiz_mode="level", start_source=source)


async def test_the_report_counts_reach_return_and_wake(session, tmp_path):
    # 1 — дошло, занимался вчера, занялся снова с кнопки рассылки
    # 2 — дошло, спал 2 месяца, проснулся, занятие не закончил
    # 3 — дошло, не вернулся;  4 — заблокировал бота;  5 — рассылки не было
    for uid, lang in ((1, "ru"), (2, "uk"), (3, "ru"), (4, "ru"), (5, "en")):
        session.add(User(id=uid, first_name=f"U{uid}", learning_lang="de",
                         native_lang="ru", interface_language=lang))
    await session.commit()
    session.add_all([
        _lesson(1, SINCE - timedelta(days=1)),
        _lesson(1, SINCE + timedelta(hours=2), source="release"),
        _lesson(2, SINCE - timedelta(days=60)),
        _lesson(2, SINCE + timedelta(hours=5), done=False),
        _lesson(5, SINCE + timedelta(hours=1)),
    ])
    await session.commit()
    after = (await session.execute(
        QuizSession.__table__.select().where(QuizSession.user_id == 1,
                                             QuizSession.started_at >= SINCE)
    )).first()
    word = make_word("Haus", level=CEFRLevel.A1, ru="дом")
    session.add(word)
    await session.flush()
    session.add_all([
        QuizQuestion(session_id=after.id, word_id=word.id, is_correct=True, channel="s"),
        QuizQuestion(session_id=after.id, word_id=word.id, is_correct=False, channel="b"),
    ])
    await session.commit()

    journal_file = tmp_path / "release.sent"
    journal_file.write_text("1 ok\n2 ok\n3\n4 blocked\n", encoding="utf-8")
    journal = read_journal(journal_file)
    assert journal == {1: "ok", 2: "ok", 3: "ok", 4: "blocked"}, "старый вид строки — «дошло»"

    r = await build_report(session, journal, SINCE, SINCE + timedelta(days=1))
    assert (r.delivered, r.blocked) == (3, 1)
    assert (r.returned, r.finished, r.via_button, r.woke) == (2, 1, 1, 1)
    assert (r.active_after, r.active_week_before, r.lessons) == (3, 1, 3)
    assert r.speech == (1, 1) and r.build == (1, 0)
    assert r.by_lang == {"ru": (2, 1), "uk": (1, 1)}

    text = format_report(r)
    assert "Начали занятие: 2 из 3 (66%)" in text
    assert "Проснулись" in text and "прошло 1 дн." in text
