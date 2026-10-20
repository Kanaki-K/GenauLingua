"""
Запись ошибок, 2.2.4: что показали, что выбрали, уровень вопроса.

Владелец 20.10: «нужно записывать неправильные ответы, чтобы понимать и иметь
возможность разобрать! как мы это упустили». Прод 20.10: до 2.0 текст ответа
пуст у всех 3156 ошибок, с 2.0 есть, но без вариантов и без номера
выбранного слова — перепутанные пары было не собрать.

Каждая проверка здесь ломается, если запись пропадёт: нарочно неверный ответ
обязан оставить строку с вариантами и выбранным словом.
"""
from sqlalchemy import select

from app.bot.handlers.quiz.lesson_state import S_SHOWN, shown_for, shown_state
from app.database.models import QuizQuestion, QuizSession, User, UserEvent
from app.services.match_service import BOARD_CHANNEL
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.test_board_in_round import _play_to_board, _ready, _solve_board
from tests.test_games_audit_oct14 import LEARN, _words

ADMIN = 1          # tests/conftest.py: ADMIN_USER=1


async def _rows(session, user):
    return (await session.execute(
        select(QuizQuestion).join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        .where(QuizSession.user_id == user.id).order_by(QuizQuestion.id)
    )).scalars().all()


async def _play(session, user, *, wrong_on=(1,), questions=4):
    """Ответить на несколько вопросов; на номерах `wrong_on` — нарочно неверно."""
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    ctx = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    chosen = {}
    for n in range(1, questions + 1):
        data = await ctx.get_data()
        correct = data["correct_word_id"]
        shown = data[S_SHOWN]
        assert shown["w"] == correct and len(shown["o"]) == 4, shown
        pick = correct
        if n in wrong_on:
            pick = next(o["id"] for o in shown["o"] if o["id"] != correct)
        chosen[correct] = (pick, [o["id"] for o in shown["o"]])
        await dp.feed_update(bot, press(user.id, f"answer_{pick}"))
        await dp.feed_update(bot, press(user.id, "next_question"))
    return chosen


async def test_a_wrong_answer_keeps_what_was_shown_and_what_was_chosen(session, user):
    await _words(session, user)
    chosen = await _play(session, user, wrong_on=(1, 3))
    rows = await _rows(session, user)
    assert len(rows) == 4
    wrong = [r for r in rows if not r.is_correct]
    assert len(wrong) == 2
    for row in wrong:
        pick, shown_ids = chosen[row.word_id]
        assert row.chosen_word_id == pick != row.word_id
        # Варианты — в том порядке, что видел человек, с надписями
        assert [o["id"] for o in row.options] == shown_ids
        assert all(o["t"] for o in row.options)
        assert row.word_id in shown_ids
        # Текст ответа — надпись выбранного варианта
        assert row.user_answer == next(o["t"] for o in row.options if o["id"] == pick)


async def test_a_right_answer_keeps_the_options_too(session, user):
    await _words(session, user)
    await _play(session, user, wrong_on=(), questions=2)
    for row in await _rows(session, user):
        assert row.is_correct and row.chosen_word_id == row.word_id
        assert len(row.options) == 4


def test_options_of_another_question_are_not_taken():
    data = shown_state(7, [(7, "дом"), (8, "кот"), (9, "лес"), (10, "сад")])
    assert [o["id"] for o in shown_for(data, 7)] == [7, 8, 9, 10]
    assert shown_for(data, 8) is None
    # У сборки номер кнопки — не слово, и он не пишется
    tiles = shown_state(7, [(0, "Ich"), (1, "bin")], ids=False)
    assert shown_for(tiles, 7) == [{"t": "Ich"}, {"t": "bin"}]


async def test_a_board_miss_keeps_the_word_it_was_confused_with(session, user):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    data = await context.get_data()
    board_ids = list(data["match_words"])
    order = data["match_right"]
    wrong_row = next(row for row in range(len(order)) if order[row] != 0)
    await _solve_board(dp, bot, context, user, miss_first=True)

    rows = [r for r in await _rows(session, user) if r.channel == BOARD_CHANNEL]
    by_word = {r.word_id: r for r in rows}
    first = by_word[board_ids[0]]
    assert not first.is_correct
    assert first.chosen_word_id == board_ids[order[wrong_row]]
    assert sorted(o["id"] for o in first.options) == sorted(board_ids)
    # Задетая промахом вторая пара — с первым словом
    assert by_word[board_ids[order[wrong_row]]].chosen_word_id == board_ids[0]
    # Сошедшиеся с первой попытки ни с чем не путали
    assert any(r.is_correct and r.chosen_word_id is None for r in rows)


async def test_a_question_carries_its_word_level_and_the_persons(session, user):
    await _words(session, user)
    await _play(session, user, wrong_on=(), questions=2)
    events = (await session.execute(
        select(UserEvent).where(UserEvent.user_id == user.id, UserEvent.kind == "question")
    )).scalars().all()
    assert events and all(e.data["lvl"] == "A1" and e.data["ulvl"] == "A1" for e in events), \
        [e.data for e in events]


async def test_the_mistakes_screen_shows_what_was_chosen(session, user):
    await _words(session, user)
    chosen = await _play(session, user, wrong_on=(1,))
    session.add(User(id=ADMIN, first_name="Владелец", interface_language="ru",
                     learning_lang="de", native_lang="ru"))
    await session.commit()

    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(ADMIN, "admin:ins_mist:7", message_id=700))
    edits = [p.get("text") or "" for n, p in recorder.calls if n == "EditMessageText"]
    assert edits, "экран не показан"
    screen = edits[-1]
    assert "Ошибки людей" in screen and "Последние ошибки" in screen
    wrong_row = next(r for r in await _rows(session, user) if not r.is_correct)
    assert wrong_row.user_answer in screen
    assert "с выбором" in screen
    assert chosen


async def test_strangers_do_not_see_the_mistakes(session, user):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(user.id, "admin:ins_mist:7"))
    assert not [n for n, _ in recorder.calls if n == "EditMessageText"]


async def test_a_voice_answer_leaves_its_time_split(session, user, monkeypatch):
    """Куда уходит время ответа голосом: до скачивания, скачивание, распознавание, хвост."""
    from app.bot.handlers.quiz import lesson as LN
    from app.bot.handlers.quiz import speech as SP
    from app.database.enums import QuizChannel
    from app.services import speech_check as sc
    from app.testing.telegram import voice_update
    from tests.test_journal import _download

    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _words(session, user, channels="ts")
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    async def judge(_audio, target, _lang):
        return sc.SpeechVerdict(heard=target, matched=True, similarity=1.0)

    monkeypatch.setattr(LN, "generate_question", forced)
    monkeypatch.setattr(bot, "download", _download, raising=False)
    monkeypatch.setattr(SP, "check_pronunciation", judge)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, voice_update(user.id))

    (timing,) = (await session.execute(
        select(UserEvent).where(UserEvent.user_id == user.id, UserEvent.kind == "speech_time")
    )).scalars().all()
    parts = ("before_s", "download_s", "recognize_s", "reply_s", "total_s")
    assert all(timing.data[k] >= 0 for k in parts), timing.data
    assert timing.data["total_s"] >= timing.data["download_s"]
    # Попытки голосом по-прежнему отдельно: «время» их счёт не раздувает
    speech = (await session.execute(
        select(UserEvent).where(UserEvent.user_id == user.id, UserEvent.kind == "speech")
    )).scalars().all()
    assert [e.action for e in speech] == ["matched"]
    # У «Говорю» вариантов на экране нет — и в строке ответа их нет
    (row,) = await _rows(session, user)
    assert row.options is None and row.chosen_word_id is None
