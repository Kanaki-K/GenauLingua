"""
Круг: пять дефектов, найденных аудитом 14 октября, — каждый воспроизведён
и закреплён здесь.

ЗАЧЕМ ОТДЕЛЬНЫМ ФАЙЛОМ. Все пять жили в местах, которые прежние тесты
обходили: голос, который не разобран; круг, начатый поверх брошенного;
доска, открытая посреди круга; запись нажатого в «Вспоминаю»; повторное
завершение. Каждый из них оставлял человека без выхода или с чужим числом,
и ни одна приёмка этого не видела.

    застревал в «Говорю»      неразобранная запись занимала вопрос навсегда
    застревал в новом круге   от брошенного оставался «уже отвечено»
    /match писал в круг       шесть строк в занятии вместо одной
    «der Drink» → «Напиток»   в «Вспоминаю» записывалось не нажатое
    два итога, +2 круга       двойное «Далее» на последнем вопросе

ГОНКУ ЗДЕСЬ НЕ ИЗОБРАЗИТЬ: тесты ходят через одну сессию базы, и два
нажатия идут по очереди — второе отсекается фильтром состояния, и тест
остаётся зелёным даже без защиты (проверено поломкой). Поэтому защиты
проверяются на своём уровне: замок «Далее» — прямым вызовом дважды,
завершение — двумя вызовами `_finish_quiz`, где решает уже база.
"""

from sqlalchemy import func, select

import pytest

from app.bot.handlers.quiz import game as G
from app.bot.handlers.quiz import lesson_state as LS
from app.bot.handlers.quiz import summary as SM
from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, UserWord, Word
from app.locales import get_text
from app.services.language_service import pair_from_user
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from app.testing.telegram import voice_update
from tests.conftest import build_groups, make_word

LEARN = get_text("btn_learn_words", "ru")


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


def _ctx(dp, bot, user):
    return dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)


async def _ready(session, user, *, channels="t", questions=15, familiar=30) -> None:
    for i in range(60):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = questions
    user.audio_enabled = False
    user.quiz_channels = channels
    user.match_in_round = False
    user.quizzes_passed = 0
    await session.commit()

    rows = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    for word in rows[:familiar]:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            times_shown=5, times_correct=3, correct_streak=1, learned=False,
        ))
    await session.commit()


async def _rows(session, session_id, channel=None):
    query = (select(func.count()).select_from(QuizQuestion)
             .where(QuizQuestion.session_id == session_id))
    if channel:
        query = query.where(QuizQuestion.channel == channel)
    return (await session.execute(query)).scalar() or 0


def _force(monkeypatch, channel):
    original = G.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = channel
        return await original(*args, **kwargs)

    monkeypatch.setattr(G, "generate_question", forced)


def _first_option(recorder):
    return next(b for b in recorder.buttons() if b.startswith("answer_"))


# ============================================================================
# «ГОВОРЮ»: НЕРАЗОБРАННАЯ ЗАПИСЬ НЕ ЗАНИМАЕТ ВОПРОС
# ============================================================================

class _Verdict:
    def __init__(self, heard, matched, failed):
        self.heard, self.matched, self.failed = heard, matched, failed
        self.empty = not heard


async def test_an_unrecognised_voice_leaves_the_question_open(
    session, user, stage, monkeypatch
):
    dp, bot, recorder = stage
    await _ready(session, user, channels="ts")
    _force(monkeypatch, QuizChannel.SPEECH)

    calls = {"n": 0}

    async def judge(_audio, target, _lang):
        calls["n"] += 1
        if calls["n"] == 1:
            return _Verdict("", False, True)         # шум, тычок в микрофон
        return _Verdict(target, True, False)

    class _Downloaded:
        def read(self):
            return b"x"

    async def download(*_a, **_k):
        return _Downloaded()

    monkeypatch.setattr(G, "check_pronunciation", judge)
    monkeypatch.setattr(bot, "download", download, raising=False)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    session_id = (await _ctx(dp, bot, user).get_data())["session_id"]

    await dp.feed_update(bot, voice_update(user.id))
    assert await _rows(session, session_id) == 0, "неразобранное не ответ"

    # Вторая запись ОБЯЗАНА дойти до распознавателя и записаться. Прежде
    # она гасилась как повтор, и выйти из вопроса было нельзя
    await dp.feed_update(bot, voice_update(user.id))
    assert calls["n"] == 2
    assert await _rows(session, session_id) == 1


# ============================================================================
# НОВЫЙ КРУГ ПОВЕРХ БРОШЕННОГО
# ============================================================================

async def test_a_new_round_after_an_abandoned_one_accepts_its_first_answer(
    session, user, stage
):
    dp, bot, recorder = stage
    await _ready(session, user)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, press(user.id, _first_option(recorder)))
    first = (await _ctx(dp, bot, user).get_data())["session_id"]

    # Бросил после первого ответа и снова нажал «Учить»
    recorder.clear()
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    second = data["session_id"]
    assert second != first
    assert data.get(LS.S_ANSWERED) is None, "отметка брошенного круга пережила новый"

    await dp.feed_update(bot, press(user.id, _first_option(recorder)))
    assert await _rows(session, second) == 1


async def test_a_new_round_keeps_what_the_last_result_needs(session, user, stage):
    """Ошибки для повтора и слова для жалобы принадлежат прошлому итогу."""
    dp, bot, recorder = stage
    await _ready(session, user)
    ctx = _ctx(dp, bot, user)
    await ctx.update_data(saved_errors=[1, 2], report_session_id=7,
                          report_word_ids=[3], board_shown=True)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await ctx.get_data()
    assert data["saved_errors"] == [1, 2]
    assert data["report_session_id"] == 7 and data["report_word_ids"] == [3]
    assert not data.get("board_shown"), "доска прошлого круга убирала её из нового"


# ============================================================================
# ОТДЕЛЬНАЯ ДОСКА ПОСРЕДИ КРУГА
# ============================================================================

async def test_a_standalone_board_during_a_round_does_not_write_into_it(
    session, user, stage
):
    dp, bot, recorder = stage
    await _ready(session, user, familiar=40)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, press(user.id, _first_option(recorder)))
    ctx = _ctx(dp, bot, user)
    session_id = (await ctx.get_data())["session_id"]

    await dp.feed_update(bot, text_update(user.id, "/match"))
    data = await ctx.get_data()
    assert data.get("match_words"), "доска не собралась — тест ничего не проверит"

    for _ in range(len(data["match_words"])):
        data = await ctx.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left = next(i for i in range(len(order)) if i not in matched)
        await dp.feed_update(bot, press(user.id, f"mt:l:{left}:{data['match_version']}"))
        data = await ctx.get_data()
        await dp.feed_update(
            bot, press(user.id, f"mt:r:{order.index(left)}:{data['match_version']}")
        )

    assert await _rows(session, session_id) == 1, "доска вне круга записалась в круг"
    quiz = await session.get(QuizSession, session_id)
    await session.refresh(quiz)
    assert quiz.answered_questions == 1


# ============================================================================
# «ВСПОМИНАЮ»: ЗАПИСЫВАЕТСЯ НАЖАТОЕ
# ============================================================================

async def test_recall_records_the_word_that_was_pressed(
    session, user, stage, monkeypatch
):
    dp, bot, recorder = stage
    await _ready(session, user, channels="tr")
    _force(monkeypatch, QuizChannel.REVERSE)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    assert data["channel"] == QuizChannel.REVERSE.value

    await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
    row = (await session.execute(
        select(QuizQuestion).where(QuizQuestion.session_id == data["session_id"])
    )).scalar_one()
    word = await session.get(Word, data["correct_word_id"])
    # Варианты «Вспоминаю» — слова изучаемого языка; прежде писалось значение
    assert word.word_de in row.user_answer, row.user_answer
    assert "дом" not in row.user_answer


# ============================================================================
# ДВОЙНОЕ «ДАЛЕЕ» И ДВОЙНОЕ ЗАВЕРШЕНИЕ
# ============================================================================

async def test_next_advances_from_one_number_only_once(session, user, stage):
    dp, bot, _ = stage
    ctx = _ctx(dp, bot, user)
    await ctx.update_data(current_question=15)

    assert await LS._claim_advance(ctx, user.id) is True
    assert await LS._claim_advance(ctx, user.id) is False

    # Следующий номер продвигается снова
    await ctx.update_data(current_question=16)
    assert await LS._claim_advance(ctx, user.id) is True


async def test_a_round_is_finished_once_however_many_times_finish_is_called(
    session, user, stage
):
    dp, bot, recorder = stage
    await _ready(session, user, questions=2)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    ctx = _ctx(dp, bot, user)
    for _ in range(2):
        await dp.feed_update(bot, press(user.id, _first_option(recorder)))
        data = await ctx.get_data()
        if data["current_question"] < 2:
            await dp.feed_update(bot, press(user.id, "next_question"))
    data = await ctx.get_data()

    fresh = await session.get(User, user.id)
    pair = pair_from_user(fresh)

    class _Callback:
        """Достаточно для `_finish_quiz`: бот, сообщение, ответ."""
        def __init__(self):
            self.bot = bot
            # Сообщение не нужно: завершённый круг уходит раньше показа
            self.message = None
            self.from_user = fresh

        async def answer(self, *_a, **_k):
            return None

    # Первый вызов через настоящую кнопку, второй — напрямую, как сделал бы
    # второй экземпляр бота или повтор обновления после перезапуска
    await dp.feed_update(bot, press(user.id, "next_question"))
    await session.refresh(fresh)
    assert fresh.quizzes_passed == 1

    await SM._finish_quiz(_Callback(), ctx, session, fresh, pair, "ru", data)
    await session.refresh(fresh)
    assert fresh.quizzes_passed == 1, "второе завершение прибавило круг"


# ============================================================================
# ЖИВОЙ ТЕСТ ВЛАДЕЛЬЦА, ВЕЧЕР 14 ОКТЯБРЯ: ЧИСТОТА ЧАТА И КНОПКИ «ГОВОРЮ»
# ============================================================================

async def _speech_round(session, user, stage, monkeypatch, verdicts):
    dp, bot, recorder = stage
    await _ready(session, user, channels="ts")
    _force(monkeypatch, QuizChannel.SPEECH)
    queue = list(verdicts)

    async def judge(_audio, target, _lang):
        heard, ok, failed = queue.pop(0)
        return _Verdict(target if heard is True else heard, ok, failed)

    class _Downloaded:
        def read(self):
            return b"x"

    async def download(*_a, **_k):
        return _Downloaded()

    monkeypatch.setattr(G, "check_pronunciation", judge)
    monkeypatch.setattr(bot, "download", download, raising=False)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    return dp, bot, recorder


async def test_voices_are_swept_when_the_round_moves_on(session, user, stage, monkeypatch):
    """«После голосового ответа новый вопрос не удаляет сообщения юзера»."""
    dp, bot, recorder = await _speech_round(
        session, user, stage, monkeypatch,
        [("", False, True), (True, True, False)],
    )
    first, second = voice_update(user.id), voice_update(user.id)
    await dp.feed_update(bot, first)
    await dp.feed_update(bot, second)

    recorder.clear()
    await dp.feed_update(bot, press(user.id, "next_question"))
    deleted = {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}
    assert first.message.message_id in deleted, "неразобранное голосовое осталось в чате"
    assert second.message.message_id in deleted, "голосовое ответа осталось в чате"


async def test_the_reference_button_sends_a_slow_clip(session, user, stage, monkeypatch):
    """Обычная озвучка уже на карточке — кнопка присылает медленную."""
    from app.services import audio_service as svc

    dp, bot, recorder = await _speech_round(session, user, stage, monkeypatch, [])
    asked = []

    async def clip(_session, _user, _word, _lang, kind):
        asked.append(kind)
        return None

    monkeypatch.setattr(G, "clip_for_user", clip)
    await dp.feed_update(bot, press(user.id, "speech_reference"))
    assert asked == [svc.KIND_SLOW], f"кнопка просит не медленный клип: {asked}"


async def test_back_from_round_settings_returns_to_the_result(session, user, stage):
    """«Почему не возвращает на прошлое сообщение круга?»"""
    from app.bot.handlers.quiz.settings import BACK_FROM_RESULT, RESULT_SETTINGS

    dp, bot, recorder = stage
    await _ready(session, user)

    recorder.clear()
    await dp.feed_update(bot, press(user.id, RESULT_SETTINGS, message_id=777))
    sent = [(n, p) for n, p in recorder.calls if n in ("SendMessage", "EditMessageText")]
    assert sent and sent[0][0] == "SendMessage", "экран настроек заменил итог круга правкой"
    back = [b for row in sent[0][1]["reply_markup"]["inline_keyboard"] for b in row
            if b.get("callback_data") == BACK_FROM_RESULT]
    assert back, "у экрана из итога нет «Назад» к итогу"

    recorder.clear()
    await dp.feed_update(bot, press(user.id, BACK_FROM_RESULT, message_id=778))
    deleted = {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}
    assert deleted == {778}, f"«Назад» удалил не только экран настроек: {deleted}"


async def test_speech_gives_three_tries_and_counts_the_third(session, user, stage, monkeypatch):
    """
    «Почему бы не дать возможность перезаписать? … на 3-тий раз точно
    правильно засчитываем, он ведь старался!» — владелец, 14 октября.
    """
    dp, bot, recorder = await _speech_round(
        session, user, stage, monkeypatch,
        [("Verstrahlt!", False, False)] * 3,
    )
    session_id = (await _ctx(dp, bot, user).get_data())["session_id"]

    await dp.feed_update(bot, voice_update(user.id))
    await dp.feed_update(bot, voice_update(user.id))
    assert await _rows(session, session_id) == 0, "неудачная попытка записалась ответом"

    await dp.feed_update(bot, voice_update(user.id))
    row = (await session.execute(
        select(QuizQuestion).where(QuizQuestion.session_id == session_id)
    )).scalar_one()
    assert row.is_correct, "третья попытка не засчитана"


async def test_a_good_second_try_is_recorded_once(session, user, stage, monkeypatch):
    dp, bot, recorder = await _speech_round(
        session, user, stage, monkeypatch,
        [("Verstrahlt!", False, False), (True, True, False)],
    )
    session_id = (await _ctx(dp, bot, user).get_data())["session_id"]
    await dp.feed_update(bot, voice_update(user.id))
    await dp.feed_update(bot, voice_update(user.id))

    rows = (await session.execute(
        select(QuizQuestion).where(QuizQuestion.session_id == session_id)
    )).scalars().all()
    assert len(rows) == 1 and rows[0].is_correct
