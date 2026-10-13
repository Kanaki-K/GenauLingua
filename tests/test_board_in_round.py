"""
Доска внутри круга: баллы, точность, ошибки, репорт.

ЗАЧЕМ ОТДЕЛЬНЫЙ ФАЙЛ. Это проверки не того, что доска РАБОТАЕТ, а того,
что она ПОДКЛЮЧЕНА к кругу — к учёту, повтору ошибок и репорту. Разница
настоящая, и первая редакция доски её провалила.

Доска звала только `update_word_progress`: двигала три шкалы и ничего
больше. Следствий было четыре, и все тихие:

    баллов НЕТ         счёт берётся из `quiz_questions`, строк не было
    точности НЕТ       `answered_questions` не росло
    репорта НЕТ        жаловаться на перевод не на что
    повтора ошибок НЕТ промахи оставались внутри доски

Человек решал доску, видел «зачтено 5 из 5» и не получал ни балла. Снаружи
это выглядело бы обманом, а изнутри — ничем: ни одна прежняя проверка
такого не видела, потому что все они смотрели на саму доску.
"""

import pytest

from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, UserWord, Word
from app.services.match_service import BOARD_CHANNEL, BOARD_SIZE, board_slot
from tests.conftest import build_groups, make_word
from tests.scenario import make_bot, make_dispatcher, press, reset_state, text_update

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def stage(session):
    """Диспетчер, бот и запись вызовов — на один сценарий."""
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def _feed(dp, bot, update):
    await dp.feed_update(bot, update)


async def _ready(session, user) -> None:
    """Круг из 15, запас коротких знакомых слов, доска положена."""
    from sqlalchemy import select

    for i in range(60):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 15
    user.audio_enabled = False
    user.quiz_channels = "t"
    user.match_in_round = True
    user.quizzes_passed = 0          # чётное — доска положена
    await session.commit()

    # Знакомыми делаем половину: доске нужны отвеченные верно, кругу — ещё
    # и новые, иначе он упрётся в исчерпание
    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    for word in words[:30]:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=1, times_shown=2, times_correct=2, learned=False,
        ))
    await session.commit()


async def _play_to_board(dp, bot, recorder, user):
    """Довести круг до доски и вернуть контекст состояния."""
    from app.locales import get_text

    slot = board_slot(15)
    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(slot - 1):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        assert options, "вопрос до доски не показан"
        await _feed(dp, bot, press(user.id, options[0]))
        await _feed(dp, bot, press(user.id, "next_question"))

    assert [b for b in recorder.buttons() if b.startswith("mt:")], (
        f"на вопросе {slot} доски нет: {recorder.buttons()}"
    )
    return dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)


async def _solve_board(dp, bot, context, user, *, miss_first: bool = False) -> None:
    """Решить доску. `miss_first` — сперва промахнуться по паре 0."""
    if miss_first:
        data = await context.get_data()
        order = data["match_right"]
        wrong = next(row for row in range(BOARD_SIZE) if order[row] != 0)
        await _feed(dp, bot, press(user.id, f"mt:l:0:{data['match_version']}"))
        data = await context.get_data()
        await _feed(dp, bot, press(user.id, f"mt:r:{wrong}:{data['match_version']}"))

    for _ in range(BOARD_SIZE):
        data = await context.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left = next(i for i in range(BOARD_SIZE) if i not in matched)
        await _feed(dp, bot, press(user.id, f"mt:l:{left}:{data['match_version']}"))
        data = await context.get_data()
        await _feed(dp, bot, press(
            user.id, f"mt:r:{order.index(left)}:{data['match_version']}"
        ))


async def _finish_round(dp, bot, recorder, user) -> None:
    """Доиграть круг до итога после доски."""
    await _feed(dp, bot, press(user.id, "next_question"))
    for _ in range(20):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await _feed(dp, bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        await _feed(dp, bot, press(user.id, "next_question"))


# ============================================================================
# УЧЁТ: ПОДВОПРОСЫ ДОСКИ — ЭТО ОТВЕТЫ КРУГА
# ============================================================================

async def test_board_answers_are_recorded_as_round_questions(session, user, stage):
    from sqlalchemy import func, select

    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    session_id = (await context.get_data())["session_id"]

    before = (await session.execute(
        select(func.count()).select_from(QuizQuestion)
        .where(QuizQuestion.session_id == session_id)
    )).scalar()

    await _solve_board(dp, bot, context, user)

    rows = (await session.execute(
        select(QuizQuestion).where(
            QuizQuestion.session_id == session_id,
            QuizQuestion.channel == BOARD_CHANNEL,
        )
    )).scalars().all()

    assert len(rows) == BOARD_SIZE, (
        f"подвопросов записано {len(rows)}, а должно {BOARD_SIZE}"
    )
    assert all(row.is_correct for row in rows), "безошибочная доска дала неверные"

    total = (await session.execute(
        select(func.count()).select_from(QuizQuestion)
        .where(QuizQuestion.session_id == session_id)
    )).scalar()
    assert total == before + BOARD_SIZE


async def test_board_answers_move_the_round_counters(session, user, stage):
    """
    Без этих счётчиков не будет ни точности круга, ни месячного балла:
    оба считаются по ним.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    session_id = (await context.get_data())["session_id"]

    quiz = await session.get(QuizSession, session_id)
    answered_before = quiz.answered_questions or 0
    correct_before = quiz.correct_answers or 0

    await _solve_board(dp, bot, context, user)

    await session.refresh(quiz)
    assert quiz.answered_questions == answered_before + BOARD_SIZE
    assert quiz.correct_answers == correct_before + BOARD_SIZE


async def test_board_gives_up_to_five_points(session, user, stage):
    """
    Решение владельца: «за вопрос 7 можно 5 баллов получить».

    Проверяется тем же запросом, которым считает месячный балл: в нём из
    разбивки берутся только «a» и «s», а всё остальное попадает в текстовые
    ответы ВЫЧИТАНИЕМ — то есть по одному баллу за подвопрос.
    """
    from app.services.monthly_leaderboard_service import _correct_by_channel

    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    session_id = (await context.get_data())["session_id"]

    await _solve_board(dp, bot, context, user)

    by_channel = await _correct_by_channel(session, [session_id])

    assert by_channel.get(BOARD_CHANNEL) == BOARD_SIZE, (
        f"подвопросы доски не попали в разбивку: {by_channel}"
    )
    # И НЕ попали в слух с речью: там балл дороже, доска его не заслужила
    assert not by_channel.get(QuizChannel.AUDIO.value)
    assert not by_channel.get(QuizChannel.SPEECH.value)


async def test_a_miss_on_the_board_costs_the_point(session, user, stage):
    """
    Пара, найденная после промаха, записывается НЕВЕРНОЙ. Иначе доску
    выгодно перебирать наугад, а перебор ничему не учит.
    """
    from sqlalchemy import select

    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    session_id = (await context.get_data())["session_id"]

    await _solve_board(dp, bot, context, user, miss_first=True)

    rows = (await session.execute(
        select(QuizQuestion).where(
            QuizQuestion.session_id == session_id,
            QuizQuestion.channel == BOARD_CHANNEL,
        )
    )).scalars().all()

    assert len(rows) == BOARD_SIZE
    assert sum(1 for row in rows if not row.is_correct) >= 1, (
        "промах на доске не стоил ни одного балла"
    )


# ============================================================================
# ПОВТОР ОШИБОК И РЕПОРТ
# ============================================================================

async def test_board_miss_lands_in_the_round_errors(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)

    await _solve_board(dp, bot, context, user, miss_first=True)

    assert (await context.get_data())["errors"], (
        "промах на доске не попал в ошибки круга"
    )


async def test_repeat_errors_after_a_board_miss_really_runs(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    await _solve_board(dp, bot, context, user, miss_first=True)
    await _finish_round(dp, bot, recorder, user)

    assert "repeat_errors" in recorder.all_buttons(), (
        "круг с промахом на доске не предложил повтор"
    )

    recorder.clear()
    await _feed(dp, bot, press(user.id, "repeat_errors"))

    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"повтор ошибок после доски не дал вопроса: {recorder.buttons()}"
    )


async def test_board_words_can_be_reported(session, user, stage):
    """
    На слово с доски должно быть можно пожаловаться: ошибку в переводе,
    увиденную на доске, человеку иначе некуда девать. А подтверждённый
    репорт — это баллы (`MonthlyStats.report_bonus`).

    Список для репорта собирается из строк `quiz_questions` круга, так что
    это та же проверка, что и про баллы, только с другого конца.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)

    board_words = set((await context.get_data())["match_words"])
    await _solve_board(dp, bot, context, user)
    await _finish_round(dp, bot, recorder, user)

    reportable = set((await context.get_data()).get("report_word_ids", []))

    assert board_words, "доска не запомнила слов — проверка вхолостую"
    assert board_words <= reportable, (
        f"слова с доски нельзя отрепортить: не хватает "
        f"{sorted(board_words - reportable)}"
    )

    # Список репорта открывается ПРАВКОЙ КЛАВИАТУРЫ, без текста: смотреть на
    # `sent_texts()` здесь бессмысленно, и первая редакция этой проверки на
    # том и упала — объявила дефектом то, что работает
    recorder.clear()
    await _feed(dp, bot, press(user.id, "report_translation_error"))

    offered = set()
    for _ in range(10):
        buttons = recorder.buttons()
        offered |= {
            int(b.removeprefix("report_toggle_"))
            for b in buttons if b.startswith("report_toggle_")
        }
        forward = [b for b in buttons if b.startswith("report_page_")]
        if not forward:
            break
        await _feed(dp, bot, press(user.id, forward[-1]))

    assert board_words <= offered, (
        f"в списке для жалобы нет слов с доски: не хватает "
        f"{sorted(board_words - offered)}"
    )


async def test_a_report_on_a_board_word_goes_through(session, user, stage):
    """
    Жалобу на слово с доски можно ДОВЕСТИ до записи в базе.

    Награда за подтверждённую жалобу — `report_bonus` в месячном зачёте, и
    начисляет её админ при подтверждении. Значит всё, что требуется от игры,
    — чтобы её слово дошло до этой записи. Проверка идёт до конца, а не до
    открытия списка: открыть можно и пустой.
    """
    from sqlalchemy import select
    from app.database.models import TranslationReport

    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)

    board_words = list((await context.get_data())["match_words"])
    await _solve_board(dp, bot, context, user)
    await _finish_round(dp, bot, recorder, user)

    await _feed(dp, bot, press(user.id, "report_translation_error"))
    await _feed(dp, bot, press(user.id, f"report_toggle_{board_words[0]}"))
    await _feed(dp, bot, press(user.id, "report_confirm"))
    await _feed(dp, bot, press(user.id, "report_send_text"))

    reports = (await session.execute(
        select(TranslationReport).where(
            TranslationReport.user_id == user.id,
            TranslationReport.word_id == board_words[0],
        )
    )).scalars().all()

    assert reports, (
        "жалоба на слово с доски не записалась — награждать будет нечего"
    )


async def test_board_is_marked_in_the_round_breakdown(session, user, stage):
    """
    В разборе круга подвопросы доски помечены: иначе пять строк подряд
    выглядят как пять обычных карточек.

    ПОМЕТКА СМЕНИЛАСЬ ВМЕСТЕ С УСТАВОМ ВНЕШНОСТИ. Было `🧩`; в разрешённом
    наборе знака доски нет, а сам `🧩` ушёл и из её заголовка — название
    сказано словами. Взят `▸`: это СОБСТВЕННЫЙ знак доски, которым она
    помечает выбранную ячейку, и он же в наборе типографики. Разбор
    перенимает её язык, а не вводит восьмой значок.

    Проверка берёт пометку из кода, а не вписывает её второй копией: иначе
    следующая смена знака прошла бы молча.
    """
    from app.bot.handlers.quiz.game import _CHANNEL_MARKS

    dp, bot, recorder = stage
    await _ready(session, user)
    context = await _play_to_board(dp, bot, recorder, user)
    await _solve_board(dp, bot, context, user)
    await _finish_round(dp, bot, recorder, user)

    mark = _CHANNEL_MARKS[BOARD_CHANNEL]
    assert mark, "у доски нет пометки — её строки не отличить от карточек"

    everything = "\n".join(recorder.sent_texts())
    assert everything.count(mark) >= BOARD_SIZE, (
        f"в разборе круга доска не помечена: {mark!r} встречается "
        f"{everything.count(mark)} раз"
    )
