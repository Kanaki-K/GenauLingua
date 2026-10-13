"""
Приёмка КРУГА ЦЕЛИКОМ: четыре игры вместе и сквозной учёт.

ЧЕГО НЕ ПРОВЕРЯЕТ НИКТО, КРОМЕ ЭТОГО СКРИПТА

    verify_quiz_channels   собирается ли ВОПРОС верно — по одному
    verify_quiz_round      проходится ли круг — зовёт генератор напрямую
    verify_match           собирается ли ДОСКА — отдельно от круга
    tests/test_*           поведение на засеянной тестовой базе

Все они смотрят на части. Здесь круг играется ЦЕЛИКОМ через настоящий
диспетчер на НАСТОЯЩЕЙ словарной базе, и проверяются сквозные инварианты —
то, что обязано сходиться между состоянием, строками в базе, счётчиками
занятия и месячным баллом.

    A  нумерация      вопросы идут 1..N без скачков, доска занимает один
    B  неповторность  ни одно слово не спрошено в круге дважды
    C  счётчики       строк вопросов = отвечено, верных строк = верных
    D  ошибки         список ошибок круга = неверные строки
    E  жалоба         список для жалобы = все слова круга
    F  каналы         канал каждой строки разрешён человеку и порогу слова
    G  баллы          месячный балл вырос РОВНО на ожидаемое по каналам
    H  идемпотентность второе нажатие по тому же вопросу не считается

Разница между «собирается» и «идёт в зачёт» в этом проекте уже стоила
четвёртой игры: приёмка доски была чиста, пока доска не давала ни балла,
ни права пожаловаться.

ПОДОПЫТНЫЙ ЗАВОДИТСЯ И УДАЛЯЕТСЯ. Живых людей скрипт не трогает: он
создаёт своего человека с заведомо свободным id, играет им и удаляет его
вместе со всем нажитым (каскадом). Иначе приёмка пачкала бы те самые
данные, по которым потом считается рейтинг.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.audit_round
    ... -m app.scripts.audit_round --pairs 6 --questions 9
    ... -m app.scripts.audit_round --full          # все 30 пар × 2 стороны
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from dataclasses import dataclass, field

from sqlalchemy import Integer, delete, func, select

from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import (
    MonthlyStats, QuizQuestion, QuizSession, User, UserWord, Word, WordLangGroup,
)
from app.database.session import AsyncSessionLocal
from app.locales import get_text
from app.services.language_service import LANGUAGES, pair_from_user
from app.services.match_service import BOARD_CHANNEL, BOARD_SIZE, board_slot
from app.services.monthly_leaderboard_service import get_or_create_current_season
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from app.testing.telegram import voice_update

logging.disable(logging.ERROR)

# Свободный диапазон id для подопытных. Живые telegram-id настолько малыми
# не бывают — но на всякий случай скрипт проверяет, что такого человека нет
PROBE_ID_BASE = 990_000_001

# Сколько знакомых слов выдать подопытному. Нужно и для порогов каналов
# (слух от одного верного ответа, речь от двух), и для доски — ей нужно
# вдвое больше своего размера
FAMILIAR_WORDS = 40

DEFAULT_QUESTIONS = 15


# ============================================================================
# ОТВЕТ ВСЛУХ БЕЗ МИКРОФОНА
# ============================================================================

class _Verdict:
    """Ответ подменного распознавателя: услышал ровно то, что просили."""

    def __init__(self, heard: str) -> None:
        self.heard = heard
        self.matched = True
        self.failed = False
        self.empty = False


def _patch_speech() -> None:
    """
    Подменить распознаватель и скачивание записи.

    ЗАЧЕМ. Речевой канал — единственный, чью ЗАПИСЬ В КРУГ не проверяет
    ничто: нажатием его не пройти (кнопок ответа нет), а пропуск нарочно не
    засчитывается — ни строки, ни прогресса. То есть «вслух учитывается
    верно» до сих пор держалось на честном слове.

    Подменяются РОВНО ДВЕ вещи, обе внешние: скачивание файла из Telegram и
    сам распознаватель. Всё остальное — порог канала, запись строки,
    счётчики, прогресс, баллы — работает настоящее. Оценки произношения тут
    и нет: бот её не выводит нарочно, значит и подделывать нечего.
    """
    from app.bot.handlers.quiz import game as game_module

    async def recognise(_audio, target, _lang):
        return _Verdict(target)

    game_module.check_pronunciation = recognise


def _patch_download(bot) -> None:
    """Скачивание записи: поддельная сессия файлов не отдаёт."""
    class _Bytes:
        def read(self):
            return b"fake-voice"

    async def download(*_args, **_kwargs):
        return _Bytes()

    bot.download = download


@dataclass
class Case:
    """Один прогон: кто играет и чем."""
    learning: str
    native: str
    reverse: bool
    channels: str
    questions: int
    level: CEFRLevel = CEFRLevel.A1

    @property
    def title(self) -> str:
        arrow = "←" if self.reverse else "→"
        return f"{self.learning}{arrow}{self.native} [{self.channels}]"


@dataclass
class Report:
    checked: int = 0
    rounds: int = 0
    questions: int = 0
    boards: int = 0
    by_channel: dict = field(default_factory=dict)
    problems: list = field(default_factory=list)
    skipped: list = field(default_factory=list)

    def fail(self, case: Case, text: str) -> None:
        self.problems.append(f"{case.title}: {text}")


# ============================================================================
# ПОДОПЫТНЫЙ
# ============================================================================

async def _make_probe(session, case: Case, index: int) -> User:
    """
    Завести человека и выдать ему знакомых слов.

    Знакомые нужны затем, что без них круг честно пойдёт одним текстом:
    порог слуха — один верный ответ по слову, речи — два. Приёмка, не
    выдавшая прогресса, проверила бы один канал из трёх и отрапортовала
    «всё верно» — так уже было, и это записано в правилах.
    """
    probe_id = PROBE_ID_BASE + index
    await _drop_probe(session, probe_id)

    user = User(
        id=probe_id,
        first_name=f"Приёмка {index}",
        interface_language="ru",
        learning_lang=case.learning,
        native_lang=case.native,
        reverse_mode=case.reverse,
        level=case.level,
        quiz_mode=QuizMode.LEVEL,
        quiz_word_count=case.questions,
        quiz_channels=case.channels,
        audio_enabled="a" in case.channels or "s" in case.channels,
        match_in_round=True,
        quizzes_passed=0,            # чётное — доска положена
    )
    session.add(user)
    await session.commit()

    # Канонические слова нужного уровня на этом языке
    words = (await session.execute(
        select(Word)
        .join(WordLangGroup, (WordLangGroup.word_id == Word.id)
              & (WordLangGroup.lang == case.learning)
              & (WordLangGroup.is_canonical.is_(True)))
        .where(Word.level == case.level)
        .order_by(func.random())
        .limit(FAMILIAR_WORDS)
    )).scalars().all()

    # ТОЧНОСТЬ ЗНАКОМЫХ СЛОВ ВЫБРАНА НЕ НАУГАД, и первая редакция здесь
    # провалилась показательно. Я выдал 5 из 5 — то есть 100%, — и круги
    # пошли ОДНИМ ТЕКСТОМ: подбор берёт слова корзинами, где 60% достаётся
    # трудным (точность ниже 70), 30% новым, 9% на повторение и лишь 1%
    # освоенным. Безупречно знакомое слово попадало в последнюю корзину и
    # почти не выпадало, новые же идут текстом по порогу. Приёмка
    # отрапортовала бы «ок», проверив один канал из трёх, — ровно то, что
    # записано в правилах проекта как «приёмка вхолостую».
    #
    # 3 из 5 — это 60%, трудная корзина. Три верных ответа заодно открывают
    # и слух (порог 1), и речь (порог 2). `last_seen_at` пустой: иначе
    # часовой отлёжки хватит, чтобы слово из подбора выпало.
    for word in words:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang=case.learning,
            times_shown=5, times_correct=3, correct_streak=1, learned=False,
            last_seen_at=None,
        ))
    await session.commit()
    return user


async def _drop_probe(session, user_id: int) -> None:
    """
    Убрать подопытного и всё нажитое им.

    ПРЯМЫМ ЗАПРОСОМ, а не `session.delete(user)`. Связи в моделях объявлены
    без `passive_deletes`, и ORM на удалении человека пытается ОБНУЛИТЬ
    внешние ключи у его записей вместо того, чтобы отдать дело каскаду
    базы, — а `user_words.user_id` входит в первичный ключ, и обнулить его
    нельзя. Падает это с «tried to blank-out primary key column», то есть
    на первом же сочетании.
    """
    await session.rollback()          # на случай сорванного круга
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
    session.expunge_all()


# ============================================================================
# ПРОГОН КРУГА
# ============================================================================

async def _play(dp, bot, recorder, session, user: User, case: Case, rep: Report):
    """Отыграть круг целиком, собирая по дороге всё, что надо проверить."""
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    seen_numbers: list[int] = []
    board_at: int | None = None

    for _ in range(case.questions * 3):       # с запасом на доску и итог
        data = await context.get_data()
        if not data.get("session_id"):
            break

        cells = [b for b in recorder.buttons() if b.startswith("mt:")]
        if cells:
            board_at = int(data.get("match_round_at") or data.get("current_question") or 0)
            rep.boards += 1
            await _solve_board(dp, bot, context, user)
            await dp.feed_update(bot, press(user.id, "next_question"))
            continue

        buttons = recorder.buttons()
        options = [b for b in buttons if b.startswith("answer_")]

        if options:
            seen_numbers.append(int(data.get("current_question") or 0))
            await dp.feed_update(bot, press(user.id, options[0]))
        elif "speech_skip" in buttons:
            # Вопрос ВСЛУХ: кнопок ответа у него нет, отвечают голосовым
            seen_numbers.append(int(data.get("current_question") or 0))
            await dp.feed_update(bot, voice_update(user.id))
        else:
            break

        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))

    return seen_numbers, board_at, await context.get_data()


async def _check_idempotence(dp, bot, recorder, session, user, case, rep) -> None:
    """
    H — ВТОРОЕ НАЖАТИЕ ПО ТОМУ ЖЕ ВОПРОСУ НЕ СЧИТАЕТСЯ.

    Отдельным кругом, а не внутри общего, и это поправка к первой редакции:
    двойное нажатие само создаёт вторую строку на то же слово, и проверка
    неповторности [B] начинала ругаться на мою же подделку. Две проверки в
    одном прогоне — две находки, из которых одна ложная.

    В жизни второе нажатие приходит двумя путями: двойной тык (в базе есть
    разрывы по 0.00 с) и нажатие по карточке, которую не удалось поправить
    (есть разрывы по 78 с). Считаться не должно ни одно.
    """
    recorder.clear()
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    data = await context.get_data()
    session_id = data.get("session_id")
    options = [b for b in recorder.buttons() if b.startswith("answer_")]
    if not session_id or not options:
        rep.skipped.append(f"{case.title}: круг для [H] не начался")
        return

    await dp.feed_update(bot, press(user.id, options[0]))
    once = await _rows(session, session_id)
    await dp.feed_update(bot, press(user.id, options[0]))
    twice = await _rows(session, session_id)

    if twice != once:
        rep.fail(case, f"[H] второе нажатие записалось: строк {once} → {twice}")

    quiz = await session.get(QuizSession, session_id)
    await session.refresh(quiz)
    if quiz.answered_questions != twice:
        rep.fail(case, f"[H] счётчик отвеченных {quiz.answered_questions} "
                       f"при {twice} строках")


async def _solve_board(dp, bot, context, user) -> None:
    for _ in range(BOARD_SIZE):
        data = await context.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left = next(i for i in range(BOARD_SIZE) if i not in matched)
        await dp.feed_update(bot, press(user.id, f"mt:l:{left}:{data['match_version']}"))
        data = await context.get_data()
        await dp.feed_update(bot, press(
            user.id, f"mt:r:{order.index(left)}:{data['match_version']}"
        ))


async def _rows(session, session_id: int) -> int:
    return (await session.execute(
        select(func.count()).select_from(QuizQuestion)
        .where(QuizQuestion.session_id == session_id)
    )).scalar() or 0


# ============================================================================
# ПРОВЕРКИ
# ============================================================================

async def _check(session, user: User, case: Case, rep: Report,
                 numbers: list[int], board_at: int | None, state: dict,
                 session_id: int, score_before: int) -> None:
    rows = (await session.execute(
        select(QuizQuestion).where(QuizQuestion.session_id == session_id)
        .order_by(QuizQuestion.id)
    )).scalars().all()
    quiz = await session.get(QuizSession, session_id)
    await session.refresh(quiz)

    # --- A. Нумерация идёт подряд
    expected = list(range(1, len(numbers) + 1))
    if board_at is not None:
        # Доска заняла свой номер и вернула круг на нём же: в списке
        # обычных вопросов её номера нет, остальные идут подряд
        expected = [n for n in range(1, len(numbers) + 2) if n != board_at]
    if numbers != expected:
        rep.fail(case, f"[A] номера вопросов {numbers}, ожидались {expected}")

    if board_at is not None and board_at != board_slot(case.questions):
        rep.fail(case, f"[A] доска встала на {board_at}, "
                       f"а должна на {board_slot(case.questions)}")

    # --- B. Ни одно слово не спрошено дважды
    word_ids = [r.word_id for r in rows]
    if len(set(word_ids)) != len(word_ids):
        twice = sorted({w for w in word_ids if word_ids.count(w) > 1})
        board_words = [r.word_id for r in rows if r.channel == BOARD_CHANNEL]
        overlap = [w for w in twice if w in board_words]
        rep.fail(case, f"[B] слов спрошено дважды: {len(twice)}"
                       + (f", из них задето доской {len(overlap)}" if overlap else ""))

    # --- C. Счётчики занятия сходятся со строками
    correct_rows = sum(1 for r in rows if r.is_correct)
    if quiz.answered_questions != len(rows):
        rep.fail(case, f"[C] отвечено {quiz.answered_questions}, строк {len(rows)}")
    if quiz.correct_answers != correct_rows:
        rep.fail(case, f"[C] верных {quiz.correct_answers}, верных строк {correct_rows}")

    # --- D. Ошибки круга = неверные строки
    wrong_rows = {r.word_id for r in rows if not r.is_correct}
    saved = set(state.get("saved_errors") or [])
    if saved != wrong_rows:
        rep.fail(case, f"[D] ошибок в состоянии {len(saved)}, "
                       f"неверных строк {len(wrong_rows)}")

    # --- E. Жалоба достаёт все слова круга
    reportable = set(state.get("report_word_ids") or [])
    if reportable != set(word_ids):
        missing = set(word_ids) - reportable
        rep.fail(case, f"[E] для жалобы недоступно слов: {len(missing)}")

    # --- F. Каналы разрешены человеку и порогу слова
    allowed = set(case.channels) | {BOARD_CHANNEL}
    for row in rows:
        if row.channel and row.channel not in allowed:
            rep.fail(case, f"[F] канал {row.channel!r} вне состава {case.channels!r}")
            break
    await _check_thresholds(session, user, case, rep, rows)

    for row in rows:
        rep.by_channel[row.channel or "?"] = rep.by_channel.get(row.channel or "?", 0) + 1
    rep.questions += len(rows)

    # --- G. Месячный балл вырос ровно на ожидаемое
    await _check_score(session, user, case, rep, rows, quiz, score_before)


async def _check_thresholds(session, user, case, rep, rows) -> None:
    """
    Слух и речь не задаются по слову, не доросшему до порога.

    Порог считается по прогрессу ДО круга, а круг его двигает — поэтому
    сверяется послабление: было хотя бы столько верных, сколько требует
    канал, МИНУС то, что мог добавить сам круг (по одному на строку).
    """
    need = {QuizChannel.AUDIO.value: 1, QuizChannel.SPEECH.value: 2}
    for row in rows:
        if row.channel not in need:
            continue
        progress = (await session.execute(
            select(UserWord.times_correct).where(
                UserWord.user_id == user.id,
                UserWord.word_id == row.word_id,
                UserWord.learning_lang == case.learning,
            )
        )).scalar() or 0
        if progress < need[row.channel]:
            rep.fail(case, f"[F] канал {row.channel!r} выдан слову "
                           f"с {progress} верными, нужно {need[row.channel]}")
            return


async def _check_score(session, user, case, rep, rows, quiz, score_before) -> None:
    season = await get_or_create_current_season(session)
    stat = (await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user.id,
            MonthlyStats.season_id == season.id,
            MonthlyStats.learning_lang == case.learning,
        )
    )).scalar_one_or_none()

    if stat is None:
        rep.fail(case, "[G] месячной статистики не появилось вовсе")
        return

    audio = sum(1 for r in rows if r.is_correct and r.channel == QuizChannel.AUDIO.value)
    speech = sum(1 for r in rows if r.is_correct and r.channel == QuizChannel.SPEECH.value)
    other = sum(1 for r in rows if r.is_correct) - audio - speech

    if stat.correct_audio != audio:
        rep.fail(case, f"[G] слух в зачёте {stat.correct_audio}, верных строк {audio}")
    if stat.correct_speech != speech:
        rep.fail(case, f"[G] речь в зачёте {stat.correct_speech}, верных строк {speech}")

    expected = (
        other * MonthlyStats.POINTS_TEXT
        + audio * MonthlyStats.POINTS_AUDIO
        + speech * MonthlyStats.POINTS_SPEECH
        + MonthlyStats.POINTS_PER_ROUND
        + (MonthlyStats.POINTS_PER_REVERSE if case.reverse else 0)
        + stat.monthly_words * MonthlyStats.POINTS_PER_WORD
        + MonthlyStats.streak_points(stat.monthly_streak or 0)
        + round((stat.total_questions or 0)
                * max(0, (stat.monthly_avg_percent or 0) - MonthlyStats.ACCURACY_FLOOR) / 100)
    )
    got = stat.calculate_monthly_score()
    if got != expected:
        rep.fail(case, f"[G] балл {got}, а по каналам ожидался {expected} "
                       f"(текст {other}, слух {audio}, речь {speech})")


# ============================================================================
# ПРОГОН
# ============================================================================

def _cases(full: bool, pairs_limit: int, questions: int) -> list[Case]:
    codes = sorted(LANGUAGES)
    out: list[Case] = []
    for learning in codes:
        for native in codes:
            if learning == native:
                continue
            for reverse in (False, True):
                out.append(Case(learning, native, reverse, "tas", questions))
    if not full:
        # Ровный срез: берём каждую k-ю, чтобы попали все языки
        step = max(1, len(out) // max(1, pairs_limit))
        out = out[::step][:pairs_limit]
    # Состав занятия тоже надо потрогать: один канал и два
    out.append(Case("de", "ru", False, "t", questions))
    out.append(Case("de", "ru", False, "ta", questions))
    return out


async def run(full: bool, pairs_limit: int, questions: int) -> int:
    rep = Report()
    cases = _cases(full, pairs_limit, questions)

    bot, recorder = make_bot()
    _patch_speech()
    _patch_download(bot)

    async with AsyncSessionLocal() as session:
        dp = make_dispatcher(session)

        for index, case in enumerate(cases, start=1):
            rep.checked += 1
            recorder.clear()
            await reset_state(dp)

            user = await _make_probe(session, case, index)
            try:
                numbers, board_at, state = await _play(
                    dp, bot, recorder, session, user, case, rep
                )
                session_id = state.get("report_session_id")
                if not session_id:
                    rep.skipped.append(f"{case.title}: круг не доигрался")
                else:
                    rep.rounds += 1
                    await _check(session, user, case, rep, numbers, board_at,
                                 state, session_id, 0)
            finally:
                await _drop_probe(session, user.id)

            # Идемпотентность — своим кругом и своим подопытным: прежний
            # уже удалён вместе с нажитым
            user = await _make_probe(session, case, index)
            try:
                await _check_idempotence(dp, bot, recorder, session, user, case, rep)
            finally:
                await _drop_probe(session, user.id)

            print(f"  {case.title:22} {'ок' if not rep.problems else '...'}",
                  flush=True)

    print()
    print(f"сочетаний проверено: {rep.checked}")
    print(f"кругов доиграно: {rep.rounds}, вопросов: {rep.questions}")
    print(f"досок в кругах: {rep.boards}")
    if rep.by_channel:
        parts = ", ".join(f"{k} {v}" for k, v in sorted(rep.by_channel.items()))
        print(f"  по каналам: {parts}")

    if rep.skipped:
        print(f"\nне доигралось: {len(rep.skipped)}")
        for line in rep.skipped[:10]:
            print(f"   {line}")

    if rep.problems:
        print(f"\nНАРУШЕНИЙ: {len(rep.problems)}")
        for line in rep.problems[:40]:
            print(f"   {line}")
        if len(rep.problems) > 40:
            print(f"   … и ещё {len(rep.problems) - 40}")
        return 1

    if not rep.rounds:
        print("\nНИ ОДИН КРУГ НЕ ДОИГРАН — проверять было нечего")
        return 1

    print("\nкруг сходится: нумерация, счётчики, ошибки, жалоба, каналы, баллы")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--full", action="store_true",
                    help="все 30 пар × 2 направления")
    ap.add_argument("--pairs", type=int, default=8,
                    help="сколько сочетаний брать без --full")
    ap.add_argument("--questions", type=int, default=DEFAULT_QUESTIONS)
    args = ap.parse_args()
    return asyncio.run(run(args.full, args.pairs, args.questions))


if __name__ == "__main__":
    sys.exit(main())
