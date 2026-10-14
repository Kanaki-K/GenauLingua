"""
Подбор слов и игр, расписание, речь: дефекты аудита 14 октября (вечер).

Каждый найден исполнением против копии базы и закреплён здесь.

    «сложные» обрывались     счёт сложных не знал часовой паузы, подбор
                             знал: круг из 6 кончался на 4-м вопросе
                             «Не удалось подготовить…», без итога
    слова кончились — обрыв  занятие очищалось молча, без итога и баллов
    речь трижды за круг      место отработки давало игру мимо правил
                             состава: потолок речи, «не последней»,
                             «не две подряд»
    «nein» засчитан за «Ei»  сверка речи подстрокой; короткие слова
                             проходили порог долей совпадения
    пауза отработки пуста    досрочный ответ не двигает `last_seen_at`, а
                             пауза смотрела на него
    короткий круг без игр    у круга из 5 все места отработки занимали
                             новые слова
    мелочь                   лишнее голосовое висело в чате; двойной
                             «повторить ошибки» заводил два занятия;
                             доска «сложных» брала любые слова; упавший
                             прогресс оставлял сессию базы сломанной;
                             мёртвый file_id медленного эталона
"""

from collections import Counter
from datetime import timedelta

import pytest
from sqlalchemy import func, select, text

from app.bot.handlers.quiz import lesson as LN
from app.bot.handlers.quiz import lesson_state as LS
from app.bot.handlers.quiz import listen as L
from app.bot.handlers.quiz import speech as SP
from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, UserWord, Word
from app.locales import get_text
from app.services import quiz_service as qs
from app.services import speech_check as sc
from app.services.language_service import LanguagePair
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from app.testing.telegram import voice_update
from tests.conftest import build_groups, make_word

LEARN = get_text("btn_learn_words", "ru")
PAIR = LanguagePair(learning="de", native="ru")


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


def _ctx(dp, bot, user):
    return dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)


async def _words(session, user, n=60, *, mode=QuizMode.LEVEL, channels="t"):
    for i in range(n):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = mode
    user.quiz_word_count = 15
    user.audio_enabled = False
    user.quiz_channels = channels
    user.match_in_round = False
    await session.commit()
    return (await session.execute(select(Word).order_by(Word.id))).scalars().all()


def _progress(user, word, **kw):
    row = dict(user_id=user.id, word_id=word.id, learning_lang="de",
               times_shown=4, times_correct=1, correct_streak=0, learned=False,
               last_seen_at=utcnow() - timedelta(hours=2))
    row.update(kw)
    return UserWord(**row)


# ============================================================================
# «СЛОЖНЫЕ СЛОВА»: СЧЁТ И ПОДБОР — ОДНО УСЛОВИЕ
# ============================================================================

async def test_difficult_count_sees_only_what_can_be_asked(session, user):
    words = await _words(session, user, mode=QuizMode.DIFFICULT)
    hot = words[:3]
    for w in hot:      # промахнулся десять минут назад
        session.add(_progress(user, w, last_seen_at=utcnow() - timedelta(minutes=10)))
    for w in words[3:6]:
        session.add(_progress(user, w))
    await session.commit()

    assert await qs.count_difficult_words(user.id, session, PAIR) == 3
    hot_ids = {w.id for w in hot}
    for _ in range(10):
        word = await qs.get_difficult_word(user.id, session, PAIR, [])
        assert word is not None and word.id not in hot_ids


async def test_a_round_that_runs_out_of_words_ends_with_a_result(session, user, stage):
    dp, bot, recorder = stage
    words = await _words(session, user, mode=QuizMode.DIFFICULT)
    for w in words[:8]:
        session.add(_progress(user, w))
    await session.commit()

    await dp.feed_update(bot, text_update(user.id, LEARN))
    ctx = _ctx(dp, bot, user)
    data = await ctx.get_data()
    session_id = data["session_id"]
    assert data["total_questions"] == 8

    for number in range(1, 9):
        data = await ctx.get_data()
        if not data.get("session_id"):
            break
        if number == 4:
            # Остальные сложные стали «только что отвечены» — слова кончились
            await session.execute(
                text("update user_words set last_seen_at = :now where user_id = :u"),
                {"now": utcnow(), "u": user.id},
            )
            await session.commit()
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        await dp.feed_update(bot, press(user.id, "next_question"))

    quiz_session = await session.get(QuizSession, session_id)
    await session.refresh(quiz_session)
    assert quiz_session.is_completed, "занятие оборвано, а не завершено итогом"
    assert quiz_session.answered_questions == 4
    texts = recorder.sent_texts()
    assert any(t.startswith(get_text("quiz_completed", "ru")) for t in texts), "итога нет"
    # Прежний обрыв: «✗ Не удалось подготовить следующий вопрос.» — ключ
    # удалён вместе с последним показом, сверяем по тексту
    assert not any("Не удалось подготовить следующий вопрос" in t for t in texts)


# ============================================================================
# СОСТАВ КРУГА: МЕСТА ОТРАБОТКИ ПОДЧИНЯЮТСЯ ТЕМ ЖЕ ПРАВИЛАМ
# ============================================================================

def _person(channels="tasr", length=15):
    return User(id=1, quiz_channels=channels, audio_enabled=True, quiz_word_count=length)


def test_practice_slot_respects_the_speech_cap():
    # Место 8 (с нуля 7): отработка, не под новое. Речь уже была дважды —
    # потолок круга из 15
    recent = ["t", "s", "t", "r", "t", "s", "a"]
    games = qs._rotation(_person(), [0] * 7, recent, position=7, round_length=15)
    assert games, "место отработки пусто"
    assert QuizChannel.SPEECH not in games


def test_practice_slot_never_repeats_the_previous_game():
    games = qs._rotation(_person(), [0] * 3, ["t", "s", "r"], position=3, round_length=15)
    assert QuizChannel.REVERSE not in games


def test_practice_slot_does_not_ask_speech_last():
    # Круг из 16: последнее место (с нуля 15) — место отработки, не под новое
    recent = ["t", "r", "t", "a", "t", "r", "t", "a", "t", "r", "t", "a", "t", "r", "t"]
    games = qs._rotation(_person(length=16), [0] * 15, recent,
                         position=15, round_length=16)
    assert games and QuizChannel.SPEECH not in games


def test_a_short_round_keeps_places_for_the_games():
    """Круг из 5: новое одно, и места отработки остаются."""
    assert [i + 1 for i in range(5) if qs.wants_new_word(i, 5)] == [5]
    assert [i + 1 for i in range(15) if qs.wants_new_word(i, 15)] == [5, 10, 15]
    games = qs._rotation(_person(length=5), [0], ["t"], position=1, round_length=5)
    assert games, "в коротком круге нет места другим играм"


def test_place_in_round_counts_the_board_as_a_question():
    """После доски номер по истории отстаёт на один — круг передаёт свой."""
    recent = ["t", "r", "t", "a", "t", "r", "t", "a", "t", "r", "t", "a", "t"]  # 13 + доска
    picked = qs.place_in_round(
        [QuizChannel.TEXT, QuizChannel.SPEECH], enabled=list(QuizChannel),
        recent=recent, round_length=15, position=15,
    )
    assert picked is QuizChannel.TEXT, "речь на последнем вопросе"


async def test_an_advanced_round_holds_the_speech_cap(session, user):
    words = await _words(session, user, n=80, channels="tasr")
    user.audio_enabled = True
    for w in words[:60]:
        session.add(_progress(user, w, times_shown=4, times_correct=4, correct_streak=1,
                              last_seen_at=utcnow() - timedelta(days=2)))
    await session.commit()

    for _ in range(3):
        used, recent = [], []
        for number in range(1, 16):
            q = await qs.generate_question(
                session, user, exclude_ids=used, recent_channels=recent,
                round_length=15, question_number=number,
            )
            assert q is not None
            used.append(q["correct_word"].id)
            recent.append(q["channel"].value)
        shape = "".join(recent)
        assert Counter(recent)["s"] <= qs.speech_cap(15), shape
        assert recent[-1] != "s", shape


# ============================================================================
# ПАУЗА ОТРАБОТКИ — ОТ ПОСЛЕДНЕГО ОТВЕТА
# ============================================================================

async def _answered(session, user, word, ago):
    quiz_session = QuizSession(user_id=user.id, level=CEFRLevel.A1,
                               learning_lang="de", native_lang="ru",
                               total_questions=15, answered_questions=1, correct_answers=1)
    session.add(quiz_session)
    await session.flush()
    session.add(QuizQuestion(session_id=quiz_session.id, word_id=word.id, is_correct=True,
                             answered_at=utcnow() - ago, channel="r"))
    await session.commit()


async def test_a_word_answered_early_a_minute_ago_waits(session, user):
    words = await _words(session, user)
    word = words[0]
    # Досрочный ответ минуту назад: якорь расписания старый, ответ свежий
    session.add(_progress(user, word, times_correct=2, correct_streak=1,
                          last_seen_at=utcnow() - timedelta(hours=2)))
    await session.commit()
    await _answered(session, user, word, timedelta(minutes=1))

    assert await qs.get_practice_words(user.id, session, PAIR, [], user=user) is None
    assert await qs.get_ready_for(QuizChannel.REVERSE, user.id, session, PAIR, [],
                                  user=user, gap=qs.PRACTICE_GAP) is None


async def test_a_word_answered_long_ago_comes_back(session, user):
    words = await _words(session, user)
    word = words[0]
    session.add(_progress(user, word, times_correct=2, correct_streak=1,
                          last_seen_at=utcnow() - timedelta(hours=2)))
    await session.commit()
    await _answered(session, user, word, timedelta(minutes=10))

    found = await qs.get_practice_words(user.id, session, PAIR, [], user=user)
    assert found is not None and found.id == word.id


# ============================================================================
# РЕЧЬ: СВЕРКА ПО ГРАНИЦАМ СЛОВ
# ============================================================================

def _matched(target, heard):
    want = sc._strip_article(sc._normalize(target, "de"), "de")
    got = sc._strip_article(sc._normalize(heard, "de"), "de")
    return sc._similarity(want, got) >= sc._threshold(want)


@pytest.mark.parametrize("target, heard", [
    ("das Ei", "nein"), ("das Ei", "Bleistift"), ("in", "Kino"),
    ("die Uhr", "Fuhrmann"), ("das Eis", "Reise"), ("an", "Mann"),
    ("das Ohr", "Rohr"), ("der Arm", "warm"),
])
def test_a_foreign_word_is_not_counted(target, heard):
    assert not _matched(target, heard)


@pytest.mark.parametrize("target, heard", [
    ("der Streit", "der Streit"), ("der Streit", "Derstreit"), ("der Streit", "Streit"),
    ("der Krieg", "das ist ein Krieg"), ("das Ei", "Ei."), ("das Ei", "dasei"),
    ("die Straße", "Stra ße"), ("der Kühlschrank", "Kühlschrang"),
])
def test_the_right_word_is_counted(target, heard):
    assert _matched(target, heard)


class _Audio:
    size = 10 ** 6


async def _check(monkeypatch, target, first, hinted):
    from app.services import mp3_trim

    monkeypatch.setattr(mp3_trim, "decode", lambda _data: _Audio())

    async def model():
        return object()

    def transcribe(_model, _audio, _lang, hint=None):
        return hinted if hint else first

    monkeypatch.setattr(sc, "_get_model", model)
    monkeypatch.setattr(sc, "_transcribe_blocking", transcribe)
    return await sc.check_pronunciation(b"x", target, "de")


async def test_the_hinted_second_pass_still_rescues_a_soundalike(monkeypatch):
    verdict = await _check(monkeypatch, "der Streit", "Verstrahlt!", "der Streit")
    assert verdict.matched


async def test_the_hint_does_not_rescue_a_foreign_short_word(monkeypatch):
    verdict = await _check(monkeypatch, "das Ohr", "Rohr", "Rohr")
    assert not verdict.matched


# ============================================================================
# МЕЛОЧЬ
# ============================================================================

async def test_a_surplus_voice_is_swept_away(session, user, stage, monkeypatch):
    dp, bot, recorder = stage
    await _words(session, user, channels="ts")
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    monkeypatch.setattr(LN, "generate_question", forced)

    async def judge(_audio, target, _lang):
        return sc.SpeechVerdict(heard=target, matched=True, similarity=1.0)

    class _Downloaded:
        def read(self):
            return b"x"

    async def download(*_a, **_k):
        return _Downloaded()

    monkeypatch.setattr(SP, "check_pronunciation", judge)
    monkeypatch.setattr(bot, "download", download, raising=False)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, voice_update(user.id))
    surplus = voice_update(user.id)            # после засчитанного ответа
    await dp.feed_update(bot, surplus)

    stray = (await _ctx(dp, bot, user).get_data()).get(LS.S_STRAY) or []
    assert surplus.message.message_id in stray, "лишнее голосовое останется в чате"


async def test_double_repeat_errors_makes_one_repeat(session, user, stage):
    dp, bot, recorder = stage
    await _words(session, user)
    user.quiz_word_count = 5
    await session.commit()

    await dp.feed_update(bot, text_update(user.id, LEARN))
    ctx = _ctx(dp, bot, user)
    for _ in range(5):
        await dp.feed_update(bot, press(user.id, "answer_-1"))     # мимо
        await dp.feed_update(bot, press(user.id, "next_question"))

    await dp.feed_update(bot, press(user.id, "repeat_errors"))
    await dp.feed_update(bot, press(user.id, "repeat_errors"))
    repeats = (await session.execute(
        select(func.count()).select_from(QuizSession)
        .where(QuizSession.user_id == user.id, QuizSession.quiz_mode == "error_repeat")
    )).scalar()
    assert repeats == 1
    assert (await ctx.get_data()).get("is_error_repeat")


async def test_board_of_the_difficult_mode_takes_difficult_words(session, user):
    from app.services.match_service import pick_words

    words = await _words(session, user, mode=QuizMode.DIFFICULT)
    difficult = words[:6]
    for w in difficult:
        session.add(_progress(user, w))
    for w in words[6:20]:          # знакомые, но не сложные
        session.add(_progress(user, w, times_shown=3, times_correct=3, correct_streak=1))
    await session.commit()

    picked = await pick_words(user, session, PAIR, size=10)
    assert picked and {w.id for w in picked} <= {w.id for w in difficult}


async def test_a_failed_progress_write_leaves_the_session_usable(
    session, user, stage, monkeypatch
):
    dp, bot, recorder = stage
    await _words(session, user)

    async def broken(*, session, **_kw):
        # Падение посреди транзакции: Postgres помечает её прерванной
        await session.execute(text("select 1/0"))

    monkeypatch.setattr(LN, "update_word_progress", broken)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))

    # Без отката любой следующий запрос падал бы «transaction is aborted»
    assert (await session.execute(text("select 1"))).scalar() == 1
    assert await session.get(QuizSession, data["session_id"]) is not None


async def test_a_dead_slow_clip_is_forgotten_and_resent(session, user, stage, monkeypatch):
    from aiogram.exceptions import TelegramBadRequest
    from app.services.audio_service import AudioClip

    dp, bot, recorder = stage
    await _words(session, user, channels="ts")
    user.audio_enabled = True
    await session.commit()
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    monkeypatch.setattr(LN, "generate_question", forced)

    dead = AudioClip(kind="slow", voice="v", spoken_text="x", title="t",
                     filename="t.mp3", file_id="D" * 40)

    async def clip(_s, _u, _w, _l, kind):
        return dead if kind == "slow" else None

    forgotten = []

    async def forget(_s, word_id, _l, kind, _v):
        forgotten.append((word_id, kind))

    async def reobtain(c, _l):
        return AudioClip(kind=c.kind, voice=c.voice, spoken_text=c.spoken_text,
                         title=c.title, filename=c.filename, data=b"y" * 600)

    monkeypatch.setattr(SP, "clip_for_user", clip)
    monkeypatch.setattr(L, "clip_for_user", clip)
    monkeypatch.setattr(LN, "clip_for_user", clip)
    monkeypatch.setattr(SP, "forget", forget)
    monkeypatch.setattr(SP, "reobtain", reobtain)

    real = recorder.make_request

    async def make_request(bot_, method, timeout=None):
        if type(method).__name__ == "SendAudio" and method.audio == dead.file_id:
            raise TelegramBadRequest(method=method, message="wrong remote file identifier")
        return await real(bot_, method, timeout)

    monkeypatch.setattr(recorder, "make_request", make_request)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    recorder.clear()
    await dp.feed_update(bot, press(user.id, "speech_reference"))

    assert forgotten and forgotten[0][1] == "slow", "мёртвая запись не выброшена"
    assert any(name == "SendAudio" for name, _ in recorder.calls), "эталон не пришёл"


# ============================================================================
# ТРЕТЬЯ ПОПЫТКА «ГОВОРЮ»: ВЕРНО И С БАЛЛАМИ, НО СРОК НЕ ДВИГАЕТ
# ============================================================================

async def _speech_round(session, user, stage, monkeypatch, verdicts):
    dp, bot, recorder = stage
    words = await _words(session, user, channels="ts")
    user.audio_enabled = True
    for w in words[:30]:     # к речи готовы, и всем пора
        session.add(_progress(user, w, times_shown=3, times_correct=3, correct_streak=1,
                              last_seen_at=utcnow() - timedelta(days=2)))
    await session.commit()

    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    async def no_clip(*_a, **_k):
        return None

    plan = list(verdicts)

    async def judge(_audio, target, _lang):
        if plan.pop(0):
            return sc.SpeechVerdict(heard=target, matched=True, similarity=1.0)
        return sc.SpeechVerdict(heard="Katze", matched=False, similarity=0.1)

    class _Downloaded:
        def read(self):
            return b"x"

    async def download(*_a, **_k):
        return _Downloaded()

    monkeypatch.setattr(LN, "generate_question", forced)
    monkeypatch.setattr(SP, "clip_for_user", no_clip)
    monkeypatch.setattr(L, "clip_for_user", no_clip)
    monkeypatch.setattr(LN, "clip_for_user", no_clip)
    monkeypatch.setattr(SP, "check_pronunciation", judge)
    monkeypatch.setattr(bot, "download", download, raising=False)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    word_id = data["correct_word_id"]
    before = (await session.execute(select(UserWord).where(
        UserWord.user_id == user.id, UserWord.word_id == word_id))).scalar_one()
    streak, seen = before.correct_streak, before.last_seen_at
    for _ in verdicts:
        await dp.feed_update(bot, voice_update(user.id))
    uid = user.id
    session.expire_all()
    after = (await session.execute(select(UserWord).where(
        UserWord.user_id == uid, UserWord.word_id == word_id))).scalar_one()
    row = (await session.execute(select(QuizQuestion).where(
        QuizQuestion.session_id == data["session_id"]))).scalar_one_or_none()
    return streak, seen, after, row


async def test_two_failed_tries_are_a_skip_not_a_free_point(
    session, user, stage, monkeypatch
):
    """
    Живой тест 14.10: третью попытку владелец «обматерил — и засчитало».
    Теперь попыток две, и вторая неудача — пропуск: ни строки ответа, ни
    балла за речь, ни сдвига расписания.
    """
    streak, seen, after, row = await _speech_round(
        session, user, stage, monkeypatch, [False, False]
    )
    assert row is None, "неудача голосом записалась ответом"
    assert (after.correct_speech or 0) == 0, "за неразобранную речь дан балл"
    assert after.correct_streak == streak, "пропуск сдвинул серию"
    assert after.last_seen_at == seen, "пропуск сдвинул якорь срока"


async def test_a_heard_answer_still_moves_the_schedule(session, user, stage, monkeypatch):
    streak, seen, after, row = await _speech_round(
        session, user, stage, monkeypatch, [False, True]
    )
    assert row.is_correct
    assert after.correct_streak == streak + 1, "услышанный ответ должен двигать срок"


# ============================================================================
# «+0» НА СМЕНЕ МЕСЯЦА
# ============================================================================

async def test_round_points_are_counted_in_the_season_of_the_round(
    session, user, stage, monkeypatch
):
    """
    Активен ещё ПРОШЛЫЙ сезон (смена не прошла), а занятие кончается в
    новом месяце — как круг, законченный 1-го в 00:01. Прирост баллов —
    разность в сезоне занятия, а не «новый минус прошлый».
    """
    from datetime import date

    from app.database.models import MonthlySeason, MonthlyStats
    from app.services import praise_service

    dp, bot, recorder = stage
    await _words(session, user)
    user.quiz_word_count = 5
    today = utcnow().date()
    prev_end = date(today.year, today.month, 1) - timedelta(days=1)
    old = MonthlySeason(year=prev_end.year, month=prev_end.month,
                        start_date=prev_end.replace(day=1), end_date=prev_end,
                        is_active=True, winners_finalized=False)
    session.add(old)
    await session.flush()
    session.add(MonthlyStats(user_id=user.id, season_id=old.id, learning_lang="de",
                             monthly_score=100))
    await session.commit()

    seen = {}
    real = praise_service.build_lines

    def spy(facts, *args, **kwargs):
        seen["points"] = facts.points
        return real(facts, *args, **kwargs)

    monkeypatch.setattr(praise_service, "build_lines", spy)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    ctx = _ctx(dp, bot, user)
    for _ in range(5):
        data = await ctx.get_data()
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        await dp.feed_update(bot, press(user.id, "next_question"))

    fresh = (await session.execute(
        select(MonthlyStats.monthly_score)
        .join(MonthlySeason, MonthlySeason.id == MonthlyStats.season_id)
        .where(MonthlyStats.user_id == user.id, MonthlySeason.month == today.month)
    )).scalar()
    assert fresh and fresh > 0, "занятие не засчиталось в новый сезон"
    assert seen.get("points") == fresh, f"итог показал +{seen.get('points')} вместо +{fresh}"
