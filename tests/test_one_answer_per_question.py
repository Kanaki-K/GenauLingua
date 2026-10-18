"""
Один вопрос — один ответ. И слово в круге одно, а не два.

ЗАЧЕМ. Оба дефекта найдены приёмкой круга (`app.scripts.audit_round`) и
оба подтверждены замером по рабочей копии — то есть это не умозрительные
гонки, а то, что уже случилось с живыми людьми.

ДВОЙНОЙ ОТВЕТ. 31 вопрос получил по две строки и больше, 50 лишних строк в
30 занятиях. Разрыв между двойными ответами — от 0.00 с до 78 с, и это два
разных пути к одной беде:

    0.00 с   двойной тык: оба нажатия пришли раньше, чем карточка успела
             перерисоваться и спрятать варианты
    78 с     правка карточки не удалась, варианты остались на экране, и
             человек нажал снова

Следствие одно: балл за вопрос начисляется дважды, прогресс по слову
двигается дважды, а отвеченных в занятии больше, чем было запланировано —
таких занятий в базе 14.

СЛОВО ДВАЖДЫ В КРУГЕ. Доска брала слова, не глядя на уже заданные, и не
пополняла список задействованных. Приёмка поймала это на первом же
сочетании: слово с доски приходило обычным вопросом через два хода.
Прогресс по нему двигался в одном круге дважды — «выучено» приходило бы
вдвое быстрее заслуженного.
"""

from sqlalchemy import func, select

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import QuizQuestion, QuizSession, UserWord, Word
from app.locales import get_text
from app.services.match_service import BOARD_CHANNEL, BOARD_SIZE, board_slot
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.conftest import build_groups, make_word

import pytest


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def _ready(session, user, *, questions=15, familiar=30, words=60) -> None:
    for i in range(words):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = questions
    user.audio_enabled = False
    user.quiz_channels = "t"
    user.match_in_round = True
    user.quizzes_passed = 2  # чётное — доска положена; не 0: у новичка первое занятие короче (7)
    await session.commit()

    rows = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    for word in rows[:familiar]:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            times_shown=5, times_correct=3, correct_streak=1, learned=False,
        ))
    await session.commit()


async def _rows(session, session_id):
    return (await session.execute(
        select(func.count()).select_from(QuizQuestion)
        .where(QuizQuestion.session_id == session_id)
    )).scalar() or 0


# ============================================================================
# ОДИН ВОПРОС — ОДИН ОТВЕТ
# ============================================================================

async def test_pressing_the_same_answer_twice_counts_once(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    options = [b for b in recorder.buttons() if b.startswith("answer_")]
    assert options, "вопрос не показан"
    session_id = (await context.get_data())["session_id"]

    await dp.feed_update(bot, press(user.id, options[0]))
    once = await _rows(session, session_id)
    await dp.feed_update(bot, press(user.id, options[0]))
    twice = await _rows(session, session_id)

    assert once == 1
    assert twice == 1, f"второе нажатие записалось: строк {twice}"


async def test_the_second_press_does_not_move_the_counters(session, user, stage):
    """
    Счётчики занятия — то, из чего считаются и точность, и месячный балл.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    data = await context.get_data()
    correct = f"answer_{data['correct_word_id']}"
    session_id = data["session_id"]

    await dp.feed_update(bot, press(user.id, correct))
    await dp.feed_update(bot, press(user.id, correct))

    quiz = await session.get(QuizSession, session_id)
    await session.refresh(quiz)
    assert quiz.answered_questions == 1
    assert quiz.correct_answers == 1, (
        f"верных {quiz.correct_answers} после двух нажатий по одной кнопке"
    )


async def test_the_second_press_does_not_move_word_progress(session, user, stage):
    """
    Прогресс по слову — три шкалы и «выучено». Двойной ответ двигал их
    дважды, то есть слово переходило в выученные вдвое быстрее.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    data = await context.get_data()
    word_id = data["correct_word_id"]

    await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
    after_one = (await session.execute(
        select(UserWord.times_shown).where(
            UserWord.user_id == user.id, UserWord.word_id == word_id,
            UserWord.learning_lang == "de",
        )
    )).scalar()

    await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
    await session.commit()
    after_two = (await session.execute(
        select(UserWord.times_shown).where(
            UserWord.user_id == user.id, UserWord.word_id == word_id,
            UserWord.learning_lang == "de",
        )
    )).scalar()

    assert after_two == after_one, (
        f"показов {after_one} → {after_two} от второго нажатия по той же кнопке"
    )


async def test_a_different_option_after_answering_is_also_refused(session, user, stage):
    """
    Второе нажатие по ДРУГОМУ варианту — тот же случай.

    Он даже опаснее: разбор уже на экране, то есть верный ответ виден, и
    нажатие по нему было бы даровым баллом.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    data = await context.get_data()
    session_id, correct_id = data["session_id"], data["correct_word_id"]
    options = [b for b in recorder.buttons() if b.startswith("answer_")]
    wrong = next(o for o in options if o != f"answer_{correct_id}")

    await dp.feed_update(bot, press(user.id, wrong))
    await dp.feed_update(bot, press(user.id, f"answer_{correct_id}"))

    rows = (await session.execute(
        select(QuizQuestion).where(QuizQuestion.session_id == session_id)
    )).scalars().all()
    assert len(rows) == 1, f"строк {len(rows)}, а должна одна"
    assert rows[0].is_correct is False, (
        "исправление ответа после разбора зачлось верным"
    )


async def test_the_next_question_accepts_an_answer_again(session, user, stage):
    """
    Отметка снимается на следующем вопросе — иначе круг встал бы после
    первого ответа. Это и есть главная опасность такой защиты.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    session_id = (await context.get_data())["session_id"]

    for expected in (1, 2, 3):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        assert options, f"вопрос {expected} не показан"
        await dp.feed_update(bot, press(user.id, options[0]))
        assert await _rows(session, session_id) == expected, (
            f"после {expected}-го ответа строк не {expected}"
        )
        await dp.feed_update(bot, press(user.id, "next_question"))


# ============================================================================
# СЛОВО В КРУГЕ ОДНО
# ============================================================================

async def test_no_word_is_asked_twice_in_one_round(session, user, stage):
    """
    Круг с доской: ни одно слово не спрошено дважды.

    Доска читает список задействованных при сборке и пополняет его после —
    поэтому запрет работает в обе стороны: и доска не берёт уже
    спрошенное, и остаток круга не берёт то, что было на доске.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    board_seen = False
    for _ in range(60):
        data = await context.get_data()
        if not data.get("session_id"):
            break
        if [b for b in recorder.buttons() if b.startswith("mt:")]:
            board_seen = True
            for _ in range(BOARD_SIZE):
                data = await context.get_data()
                order, matched = data["match_right"], data["match_matched"]
                left = next(i for i in range(BOARD_SIZE) if i not in matched)
                await dp.feed_update(bot, press(
                    user.id, f"mt:l:{left}:{data['match_version']}"))
                data = await context.get_data()
                await dp.feed_update(bot, press(
                    user.id, f"mt:r:{order.index(left)}:{data['match_version']}"))
            await dp.feed_update(bot, press(user.id, "next_question"))
            continue

        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await dp.feed_update(bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))

    assert board_seen, "доска в круге не встала — проверка вхолостую"

    session_id = (await context.get_data()).get("report_session_id")
    assert session_id, "круг не доигрался"

    rows = (await session.execute(
        select(QuizQuestion.word_id, QuizQuestion.channel)
        .where(QuizQuestion.session_id == session_id)
    )).all()
    ids = [word_id for word_id, _ in rows]
    repeats = sorted({w for w in ids if ids.count(w) > 1})

    assert not repeats, (
        f"слов спрошено дважды: {repeats}; "
        f"из них на доске: {[w for w, ch in rows if ch == BOARD_CHANNEL and w in repeats]}"
    )


async def test_board_words_enter_the_used_list(session, user, stage):
    """
    Разбор того же правила с другого конца — прямо по состоянию.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    slot = board_slot(15)
    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(slot - 1):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        assert options
        await dp.feed_update(bot, press(user.id, options[0]))
        await dp.feed_update(bot, press(user.id, "next_question"))

    data = await context.get_data()
    board_words = set(data["match_words"])
    used_before = set(data.get("used_word_ids") or [])

    assert not (board_words & used_before), (
        f"доска взяла уже спрошенное: {sorted(board_words & used_before)}"
    )

    for _ in range(BOARD_SIZE):
        data = await context.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left = next(i for i in range(BOARD_SIZE) if i not in matched)
        await dp.feed_update(bot, press(user.id, f"mt:l:{left}:{data['match_version']}"))
        data = await context.get_data()
        await dp.feed_update(bot, press(
            user.id, f"mt:r:{order.index(left)}:{data['match_version']}"))

    used_after = set((await context.get_data()).get("used_word_ids") or [])
    assert board_words <= used_after, (
        f"слова доски не попали в задействованные: "
        f"{sorted(board_words - used_after)}"
    )
