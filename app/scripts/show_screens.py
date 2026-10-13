"""
ПОКАЗАТЬ ВСЕ ЭКРАНЫ так, как их видит человек.

ЗАЧЕМ. В проекте есть правило, выведенное болью: «экран надо ПОКАЗАТЬ, а
не вычитать». Приёмка на 262 экранах не увидела трёх дефектов вида —
потому что проверяла числа в блоках, а не то, как блок выглядит целиком.
Разговор о внешности без самих экранов на столе — разговор о домыслах.

Скрипт прогоняет настоящие обработчики через настоящий диспетчер и
печатает каждый экран: текст как есть (с разметкой или без) и клавиатуру
рядами. Плюс считает эмодзи — замер показал 75 РАЗНЫХ значков на 386
строк интерфейса, то есть системы нет, есть украшение.

ДВА ЧЕЛОВЕКА, и это главное в скрипте. Новый видит не то же, что
играющий: у новичка нет ни прогресса, ни серии, ни места в рейтинге, и
половина экранов у него выглядит иначе. Сравнивать их надо рядом.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.show_screens
    ... -m app.scripts.show_screens --who new
    ... -m app.scripts.show_screens --raw      # не убирать html-разметку
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import re
import sys

from sqlalchemy import delete, func, select

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User, UserWord, Word, WordLangGroup
from app.database.session import AsyncSessionLocal
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update

logging.disable(logging.ERROR)

PROBE_NEW = 980_000_101
PROBE_OLD = 980_000_102

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF"
    "\U00002190-\U000021FF\U00002B00-\U00002BFF️⃣]"
)
TAGS = re.compile(r"</?[a-zA-Z][^>]*>")

WIDTH = 78


def _plain(text: str, raw: bool) -> str:
    return text if raw else TAGS.sub("", text)


def _frame(title: str) -> None:
    print()
    print("┌" + "─" * WIDTH + "┐")
    print("│ " + title.ljust(WIDTH - 1) + "│")
    print("└" + "─" * WIDTH + "┘")


def _screen(text: str, rows: list[list[str]], raw: bool) -> None:
    body = _plain(text, raw)
    for line in body.split("\n"):
        print("   " + line)
    if rows:
        print()
        for row in rows:
            print("   [ " + " ] [ ".join(row) + " ]")
    marks = EMOJI.findall(body) + [
        m for row in rows for cell in row for m in EMOJI.findall(cell)
    ]
    if marks:
        print()
        print(f"   ·· значков: {len(marks)} — {' '.join(dict.fromkeys(marks))}")


def _keyboard_rows(payload: dict) -> list[list[str]]:
    markup = payload.get("reply_markup")
    if not isinstance(markup, dict):
        return []
    rows = markup.get("inline_keyboard") or markup.get("keyboard") or []
    out = []
    for row in rows:
        out.append([str(b.get("text", "")) for b in row])
    return out


def _dump(recorder, raw: bool, title: str) -> None:
    """Напечатать всё, что бот показал с прошлого сброса."""
    _frame(title)
    shown = False
    for name, payload in recorder.calls:
        if name not in ("SendMessage", "EditMessageText", "SendAudio",
                        "EditMessageCaption", "EditMessageMedia"):
            continue
        text = payload.get("text") or payload.get("caption") or ""
        if not text and name == "EditMessageMedia":
            text = (payload.get("media") or {}).get("caption") or ""
        if not text:
            continue
        if shown:
            print("   " + "·" * (WIDTH - 4))
        _screen(text, _keyboard_rows(payload), raw)
        shown = True
    if not shown:
        print("   (бот ничего не показал)")
    recorder.clear()


# ============================================================================
# ПОДОПЫТНЫЕ
# ============================================================================

async def _drop(session, user_id: int) -> None:
    await session.rollback()
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
    session.expunge_all()


async def _new_person(session) -> User:
    """Человек, который только что нашёл бота: ни уровня, ни прогресса."""
    await _drop(session, PROBE_NEW)
    # ВСЁ ПУСТОЕ, как у настоящего новичка: ни языка бота, ни изучаемого,
    # ни уровня. Первая редакция подопытного уже имела «ru» и «de» — и
    # выбор языка проскочил, то есть скрипт показывал не тот путь.
    user = User(
        id=PROBE_NEW, first_name="Новый", interface_language=None,
        learning_lang=None, native_lang=None, reverse_mode=False,
        level=None,
    )
    session.add(user)
    await session.commit()
    return user


async def _old_person(session) -> User:
    """Человек, который играет давно: серия, прогресс по трём каналам."""
    await _drop(session, PROBE_OLD)
    user = User(
        id=PROBE_OLD, first_name="Играющий", interface_language="ru",
        learning_lang="de", native_lang="ru", reverse_mode=False,
        level=CEFRLevel.B1, quiz_mode=QuizMode.LEVEL, quiz_word_count=15,
        quiz_channels="tas", audio_enabled=True, match_in_round=True,
        streak_days=7, quizzes_passed=42, words_learned=118, success_rate=84,
    )
    session.add(user)
    await session.commit()

    words = (await session.execute(
        select(Word)
        .join(WordLangGroup, (WordLangGroup.word_id == Word.id)
              & (WordLangGroup.lang == "de")
              & (WordLangGroup.is_canonical.is_(True)))
        .where(Word.level == CEFRLevel.B1)
        .order_by(func.random()).limit(60)
    )).scalars().all()
    for index, word in enumerate(words):
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            times_shown=5, times_correct=3 if index % 3 else 2,
            correct_streak=1, learned=index % 7 == 0, last_seen_at=None,
        ))
    await session.commit()
    return user


# ============================================================================
# ПРОГОН
# ============================================================================

async def _walk_new(dp, bot, recorder, user, raw: bool) -> None:
    print("\n\n" + "=" * (WIDTH + 2))
    print("  НОВЫЙ ЧЕЛОВЕК: что он видит по порядку")
    print("=" * (WIDTH + 2))

    recorder.clear()
    await dp.feed_update(bot, text_update(user.id, "/start"))
    _dump(recorder, raw, "1. /start — первое, что видит человек")

    for data, title in (
        ("select_lang_ru", "2. выбрал язык бота"),
        ("onboard_learn_de", "3. выбрал, что учит"),
        ("start_level_A1", "4. выбрал уровень"),
        ("goal_travel", "5. выбрал, зачем учит"),
    ):
        await dp.feed_update(bot, press(user.id, data))
        _dump(recorder, raw, title)


async def _walk_old(dp, bot, recorder, user, raw: bool) -> None:
    print("\n\n" + "=" * (WIDTH + 2))
    print("  ИГРАЮЩИЙ ЧЕЛОВЕК: все экраны, куда он может попасть")
    print("=" * (WIDTH + 2))

    recorder.clear()
    await dp.feed_update(bot, text_update(user.id, "/start"))
    _dump(recorder, raw, "1. /start — вступительный блок")

    await dp.feed_update(bot, text_update(user.id, "/home"))
    _dump(recorder, raw, "2. /home — домашний экран")

    # Главное меню — реплай-клавиатура
    from app.bot.keyboards import get_main_menu_keyboard
    _frame("3. главное меню (кнопки внизу экрана)")
    kb = get_main_menu_keyboard("ru")
    rows = [[b.text for b in row] for row in kb.keyboard]
    _screen("(реплай-клавиатура, видна всегда)", rows, raw)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    _dump(recorder, raw, "4. вопрос карточкой")

    options = [b for b in recorder.buttons() if b.startswith("answer_")] \
        if recorder.calls else []
    # Ответ на первый вопрос: карточку надо показать после ответа
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    data = await context.get_data()
    if data.get("correct_word_id"):
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        _dump(recorder, raw, "5. разбор после верного ответа")

    for data_cb, title in (
        ("settings_open", "6. настройки — верхний уровень"),
        ("settings_group_what", "7. настройки → что учу"),
        ("settings_group_how", "8. настройки → как учу"),
        ("settings_group_bot", "9. настройки → бот"),
    ):
        await dp.feed_update(bot, press(user.id, data_cb))
        _dump(recorder, raw, title)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_stats", "ru")))
    _dump(recorder, raw, "10. статистика")

    await dp.feed_update(bot, text_update(user.id, get_text("btn_leaderboard", "ru")))
    _dump(recorder, raw, "11. рейтинг")

    await dp.feed_update(bot, press(user.id, "match_start"))
    _dump(recorder, raw, "12. доска сопоставления")

    # Напоминание — единственный экран вне бота
    from app.schedulers.reminder_scheduler import build_reminder_text
    from app.bot.keyboards.notifications import get_reminder_keyboard
    async with AsyncSessionLocal() as fresh:
        person = await fresh.get(User, user.id)
        text = await build_reminder_text(person, fresh)
    _frame("13. напоминание — единственный экран вне бота")
    kb = get_reminder_keyboard("ru", count=15)
    _screen(text, [[b.text for b in row] for row in kb.inline_keyboard], raw)


async def run(who: str, raw: bool) -> int:
    bot, recorder = make_bot()

    async with AsyncSessionLocal() as session:
        dp = make_dispatcher(session)

        if who in ("new", "both"):
            await reset_state(dp)
            user = await _new_person(session)
            try:
                await _walk_new(dp, bot, recorder, user, raw)
            finally:
                await _drop(session, PROBE_NEW)

        if who in ("old", "both"):
            await reset_state(dp)
            user = await _old_person(session)
            try:
                await _walk_old(dp, bot, recorder, user, raw)
            finally:
                await _drop(session, PROBE_OLD)

    print()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--who", choices=("new", "old", "both"), default="both")
    ap.add_argument("--raw", action="store_true",
                    help="не убирать html-разметку")
    args = ap.parse_args()
    return asyncio.run(run(args.who, args.raw))


if __name__ == "__main__":
    sys.exit(main())
