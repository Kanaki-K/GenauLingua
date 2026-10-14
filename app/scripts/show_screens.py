"""
ПОКАЗАТЬ ВСЕ ЭКРАНЫ так, как их видит человек.

ЗАЧЕМ. В проекте есть правило, выведенное болью: «экран надо ПОКАЗАТЬ, а
не вычитать». Приёмка на 262 экранах не увидела трёх дефектов вида — она
проверяла числа в блоках, а не то, как блок выглядит целиком.

СПИСОК ЭКРАНОВ НЕ ПИШЕТСЯ РУКАМИ, и это главное в скрипте. Первая его
редакция перечисляла экраны вручную — и пропустила ровно то, что потом
спросил владелец: жалобу на перевод, подробную статистику, рейтинг.
Поэтому кнопки берутся ИЗ КОДА (тем же сборщиком, что у `verify_buttons`),
а в конце печатается, какие из них не дали экрана. Пропустить молча больше
нельзя.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.show_screens
    ... --who new      путь нового человека
    ... --who old      экраны играющего
    ... --who round    круг целиком и жалоба на перевод
    ... --who reverse  пятая игра: вопрос значением, разбор, главная
    ... --who sweep    обход ВСЕХ кнопок из кода + отчёт о покрытии
    ... --who all      всё подряд
    ... --raw          не убирать html-разметку
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import re
import sys

from sqlalchemy import delete, func, select

from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import User, UserWord, Word, WordLangGroup
from app.database.session import AsyncSessionLocal
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update

logging.disable(logging.ERROR)

PROBE = 980_000_101

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF"
    "\U00002190-\U000021FF\U00002B00-\U00002BFF️⃣]"
)
TAGS = re.compile(r"</?[a-zA-Z][^>]*>")
WIDTH = 78

# Что в обходе не нажимаем: админка проверяется своим `audit_admin`,
# рассылка уходит живым людям, «noop» — заглушка.
SKIP = ("admin:", "broadcast", "noop")


def _plain(text: str, raw: bool) -> str:
    return text if raw else TAGS.sub("", text)


def _frame(title: str) -> None:
    print()
    print("┌" + "─" * WIDTH + "┐")
    print("│ " + title.ljust(WIDTH - 1) + "│")
    print("└" + "─" * WIDTH + "┘")


def _keyboard_rows(payload: dict) -> list[list[str]]:
    markup = payload.get("reply_markup")
    if not isinstance(markup, dict):
        return []
    rows = markup.get("inline_keyboard") or markup.get("keyboard") or []
    return [[str(b.get("text", "")) for b in row] for row in rows]


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


def _dump(recorder, raw: bool, title: str) -> bool:
    """Напечатать всё, что бот показал. False — если ничего."""
    _frame(title)
    shown = False
    for name, payload in recorder.calls:
        # EditMessageReplyMarkup — правка ОДНОЙ клавиатуры, без текста. Так
        # сделан весь путь жалобы на перевод: список слов подменяет кнопки
        # под итогом круга. Первая редакция такие вызовы пропускала, и
        # жалоба выглядела как «бот ничего не показал»
        if name == "EditMessageReplyMarkup":
            if shown:
                print("   " + "·" * (WIDTH - 4))
            _screen("(текста нет — меняются только кнопки)",
                    _keyboard_rows(payload), raw)
            shown = True
            continue
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
    return shown


# ============================================================================
# ПОДОПЫТНЫЙ
# ============================================================================

async def _drop(session) -> None:
    await session.rollback()
    await session.execute(delete(User).where(User.id == PROBE))
    await session.commit()
    session.expunge_all()


async def _probe(session, *, fresh: bool = False, channels: str = "tas",
                 count: int = 15, words: int = 60) -> User:
    """
    Подопытный. `fresh=True` — настоящий новичок: ни языка, ни уровня.

    Точность знакомых слов 60% (3 из 5), а не 100%, и это не мелочь: подбор
    берёт слова корзинами, где освоенным достаётся 1%, и у безупречно
    знакомых круг пошёл бы одним текстом. Та же ловушка уже сработала в
    приёмке круга.
    """
    await _drop(session)

    if fresh:
        user = User(
            id=PROBE, first_name="Новый", interface_language=None,
            learning_lang=None, native_lang=None, reverse_mode=False,
            level=None,
        )
        session.add(user)
        await session.commit()
        return user

    user = User(
        id=PROBE, first_name="Играющий", interface_language="ru",
        learning_lang="de", native_lang="ru", reverse_mode=False,
        level=CEFRLevel.B1, quiz_mode=QuizMode.LEVEL, quiz_word_count=count,
        quiz_channels=channels,
        audio_enabled=("a" in channels or "s" in channels),
        match_in_round=True, streak_days=7, quizzes_passed=42,
        words_learned=118, success_rate=84,
    )
    session.add(user)
    await session.commit()

    rows = (await session.execute(
        select(Word)
        .join(WordLangGroup, (WordLangGroup.word_id == Word.id)
              & (WordLangGroup.lang == "de")
              & (WordLangGroup.is_canonical.is_(True)))
        .where(Word.level == CEFRLevel.B1)
        .order_by(func.random()).limit(words)
    )).scalars().all()
    for index, word in enumerate(rows):
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            times_shown=5, times_correct=3, correct_streak=1,
            learned=index % 7 == 0, last_seen_at=None,
        ))
    await session.commit()
    return user


# ============================================================================
# ПУТЬ НОВОГО ЧЕЛОВЕКА
# ============================================================================

async def flow_new(dp, bot, rec, raw: bool, session) -> None:
    print("\n\n" + "=" * (WIDTH + 2))
    print("  НОВЫЙ ЧЕЛОВЕК: что он видит по порядку")
    print("=" * (WIDTH + 2))

    await reset_state(dp)
    user = await _probe(session, fresh=True)
    rec.clear()

    await dp.feed_update(bot, text_update(user.id, "/start"))
    _dump(rec, raw, "1. /start — первое, что видит человек")

    # ДВА ВОПРОСА, ДАЛЬШЕ ИГРА. Уровень и цель из знакомства убраны: уровень
    # ставит бот (A1 и выше по точности), цель осталась в настройках. Прежде
    # здесь нажимались `start_level_A1` и `goal_travel`, и после их снятия
    # показ печатал «бот ничего не показал» — обход жал кнопки, которых уже
    # нет, и этого не заметил бы никто, кроме глаз.
    start = None
    for data, title in (
        ("select_lang_uk", "2. выбрал язык бота"),
        ("onboard_learn_de", "3. выбрал, что учит — и может начать"),
    ):
        await dp.feed_update(bot, press(user.id, data))
        # Кнопка начала берётся из показанного, а не вписана: её адрес несёт
        # пометку двери (`learn_now:start`), и вписанный руками разошёлся бы.
        # Читается ДО печати: `_dump` чистит запись вызовов за собой
        start = next(
            (b for b in rec.all_buttons() if b.startswith("learn_now")), start
        )
        _dump(rec, raw, title)

    if start:
        await dp.feed_update(bot, press(user.id, start))
        _dump(rec, raw, "4. первый вопрос")
    else:
        _frame("4. первый вопрос")
        print("   (кнопки занятия на вступительном экране нет)")


# ============================================================================
# КРУГ ЦЕЛИКОМ И ЖАЛОБА НА ПЕРЕВОД
# ============================================================================

async def flow_round(dp, bot, rec, raw: bool, session) -> None:
    """
    Короткий круг — и вся жалоба на перевод за ним.

    Состав нарочно «t», только карточка: у вопроса ВСЛУХ кнопок ответа нет,
    отвечают голосовым, и обход вставал бы там. Первая редакция скрипта так
    и встала — жалоба, которую владелец потом спросил отдельно, в показ не
    попадала.
    """
    print("\n\n" + "=" * (WIDTH + 2))
    print("  КРУГ ЦЕЛИКОМ И ЖАЛОБА НА ПЕРЕВОД")
    print("=" * (WIDTH + 2))

    await reset_state(dp)
    user = await _probe(session, channels="t", count=4)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    rec.clear()

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    _dump(rec, raw, "1. вопрос карточкой")

    data = await context.get_data()
    if data.get("correct_word_id"):
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        _dump(rec, raw, "2. разбор после ВЕРНОГО ответа")
        await dp.feed_update(bot, press(user.id, "next_question"))

    data = await context.get_data()
    options = [b for b in rec.buttons() if b.startswith("answer_")]
    wrong = next((o for o in options
                  if o != f"answer_{data.get('correct_word_id')}"), None)
    rec.clear()
    if wrong:
        await dp.feed_update(bot, press(user.id, wrong))
        _dump(rec, raw, "3. разбор после НЕВЕРНОГО ответа")
        await dp.feed_update(bot, press(user.id, "next_question"))

    for _ in range(10):
        options = [b for b in rec.buttons() if b.startswith("answer_")]
        if not options:
            break
        rec.clear()
        await dp.feed_update(bot, press(user.id, options[0]))
        if "next_question" not in rec.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))
    _dump(rec, raw, "4. итог круга")

    await dp.feed_update(bot, press(user.id, "report_translation_error"))
    shown = _dump(rec, raw, "5. жалоба: список слов круга")

    toggles = [b for b in rec.all_buttons() if b.startswith("report_toggle_")]
    if not shown or not toggles:
        await dp.feed_update(bot, press(user.id, "report_translation_error"))
        toggles = [b for b in rec.all_buttons() if b.startswith("report_toggle_")]
        rec.clear()

    if toggles:
        await dp.feed_update(bot, press(user.id, toggles[0]))
        _dump(rec, raw, "6. жалоба: слово выбрано")
        await dp.feed_update(bot, press(user.id, "report_confirm"))
        _dump(rec, raw, "7. жалоба: что именно не так")
        await dp.feed_update(bot, press(user.id, "report_send_text"))
        _dump(rec, raw, "8. жалоба: отправлена")
    else:
        print("\n   жалоба не открылась: у круга нет слов для показа")

    await dp.feed_update(bot, press(user.id, "repeat_errors"))
    _dump(rec, raw, "9. повтор ошибок")


# ============================================================================
# ПЯТАЯ ИГРА
# ============================================================================

async def flow_reverse(dp, bot, rec, raw: bool, session) -> None:
    """
    Пятая игра — припоминание — своими экранами.

    ПОЧЕМУ ОТДЕЛЬНЫМ ПОТОКОМ, А НЕ ВНУТРИ КРУГА. В круге состав «tasr», и
    какая игра достанется вопросу, решает подбор. Показ, где пятая игра
    появляется «если повезёт», ничего не показывает: в прошлый раз её
    экраны так и не увидел никто, а тесты были зелёные.

    Состав «r» — ровно та игра и ничего кроме. Заодно это проверка, что
    круг целиком из припоминания собирается: кнопка «Вспомнить» на главной
    ведёт именно сюда.
    """
    print("\n\n" + "=" * (WIDTH + 2))
    print("  ПЯТАЯ ИГРА: СПРОСИЛИ ЗНАЧЕНИЕМ")
    print("=" * (WIDTH + 2))

    await reset_state(dp)
    user = await _probe(session, channels="r", count=3)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    rec.clear()

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    _dump(rec, raw, "1. вопрос значением — ответ словом")

    data = await context.get_data()
    if data.get("correct_word_id"):
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        _dump(rec, raw, "2. разбор: слово и значение рядом")
        await dp.feed_update(bot, press(user.id, "next_question"))

    for _ in range(10):
        options = [b for b in rec.buttons() if b.startswith("answer_")]
        if not options:
            break
        rec.clear()
        await dp.feed_update(bot, press(user.id, options[0]))
        if "next_question" not in rec.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))
    _dump(rec, raw, "3. итог круга: припоминание отдельной строкой")

    # Главная и прямой вход кнопкой: состав возвращается полным, иначе
    # полос было бы видно не четыре, а одна
    await _drop(session)
    user = await _probe(session, channels="tasr", count=15)
    rec.clear()
    await dp.feed_update(bot, text_update(user.id, "/home"))
    _dump(rec, raw, "4. главная: четыре полосы, четвёртая — припоминание")

    rec.clear()
    await dp.feed_update(bot, press(user.id, f"home_learn_{QuizChannel.REVERSE.value}"))
    _dump(rec, raw, "5. вход в пятую игру кнопкой с главной")


# ============================================================================
# ЭКРАНЫ ИГРАЮЩЕГО
# ============================================================================

async def flow_old(dp, bot, rec, raw: bool, session) -> None:
    print("\n\n" + "=" * (WIDTH + 2))
    print("  ЭКРАНЫ ИГРАЮЩЕГО ЧЕЛОВЕКА")
    print("=" * (WIDTH + 2))

    await reset_state(dp)
    user = await _probe(session)
    rec.clear()

    await dp.feed_update(bot, text_update(user.id, "/start"))
    _dump(rec, raw, "1. /start — вступительный блок")

    await dp.feed_update(bot, text_update(user.id, "/home"))
    _dump(rec, raw, "2. /home — прогресс")

    from app.bot.keyboards import get_main_menu_keyboard
    _frame("3. нижнее меню (видно всегда, живёт на якоре)")
    _screen("(реплай-клавиатура)",
            [[b.text for b in row]
             for row in get_main_menu_keyboard("ru").keyboard], raw)

    steps = [
        (text_update(user.id, get_text("btn_rating", "ru")), "4. рейтинг"),
        (text_update(user.id, get_text("btn_stats", "ru")), "5. прогресс по кнопке «Статистика»"),
        (press(user.id, "stats_full"), "6. подробная статистика"),
        (press(user.id, "settings_open"), "7. настройки — верх"),
        (press(user.id, "settings_group_what"), "8. настройки → что учу"),
        (press(user.id, "settings_group_how"), "9. настройки → как учу"),
        (press(user.id, "settings_group_bot"), "10. настройки → бот"),
        (press(user.id, "match_start"), "11. найди пары"),
    ]
    for update, title in steps:
        await dp.feed_update(bot, update)
        _dump(rec, raw, title)

    from app.bot.keyboards.notifications import get_reminder_keyboard
    from app.schedulers.reminder_scheduler import build_reminder_text
    async with AsyncSessionLocal() as fresh:
        person = await fresh.get(User, user.id)
        text = await build_reminder_text(person, fresh)
    _frame("12. напоминание — единственный экран вне бота")
    _screen(text, [[b.text for b in row]
                   for row in get_reminder_keyboard("ru", count=15).inline_keyboard],
            raw)


# ============================================================================
# ОБХОД ВСЕХ КНОПОК ИЗ КОДА
# ============================================================================

async def flow_sweep(dp, bot, rec, raw: bool, session) -> None:
    """
    Нажать КАЖДУЮ кнопку, которую бот рисует, и доложить о непокрытых.

    Список берётся сборщиком из `verify_buttons` — тем же, что проверяет,
    нет ли кнопок в пустоту. Руками список экранов писать нельзя: первая
    редакция этого скрипта так и пропустила жалобу, статистику и рейтинг.
    """
    from app.scripts.verify_buttons import collect_buttons

    everything: set[str] = set()
    for values in collect_buttons().values():
        everything |= values

    plain = sorted(
        data for data in everything
        if "<" not in data and not data.startswith(SKIP)
    )

    print("\n\n" + "=" * (WIDTH + 2))
    print(f"  ОБХОД ВСЕХ КНОПОК ИЗ КОДА: {len(plain)} из {len(everything)}")
    print("=" * (WIDTH + 2))

    await reset_state(dp)
    user = await _probe(session)

    empty: list[str] = []
    for data in plain:
        rec.clear()
        try:
            await dp.feed_update(bot, press(user.id, data))
        except Exception as exc:
            print(f"\n   {data}: СБОЙ — {type(exc).__name__}: {exc}")
            empty.append(f"{data} — сбой")
            continue
        if not _dump(rec, raw, f"кнопка · {data}"):
            empty.append(data)

    print("\n" + "=" * (WIDTH + 2))
    print("  ПОКРЫТИЕ")
    print("=" * (WIDTH + 2))
    print(f"  кнопок в коде:   {len(everything)}")
    print(f"  нажато:          {len(plain)}")
    print(f"  дали экран:      {len(plain) - len(empty)}")
    if empty:
        print(f"\n  НЕ ДАЛИ ЭКРАНА: {len(empty)}")
        print("  (ожидаемо для тех, кому нужно состояние: ответ в круге,")
        print("   выбранное слово в жалобе, ячейка доски)")
        for data in empty:
            print(f"     {data}")


# ============================================================================
# ПРОГОН
# ============================================================================

async def flow_scales(dp, bot, rec, raw: bool, session) -> None:
    """
    ОДНИ И ТЕ ЖЕ ЭКРАНЫ У ТРЁХ РАЗНЫХ ЛЮДЕЙ.

    Экран ломается не в середине, а на краях: у новичка делить нечего (ноль
    слов, ноль кругов, нет места в рейтинге), у заигравшего числа
    четырёхзначные и подписи длинные. Показывать только середину — значит
    не увидеть ни того, ни другого.

        пусто    ни одного слова, ни одного круга, ни серии
        обычный  40 знакомых слов, серия семь дней
        много    2 400 слов, 312 кругов, серия 180 дней
    """
    from app.services.monthly_leaderboard_service import get_or_create_current_season
    from app.database.models import MonthlyStats

    scales = (
        ("ПУСТО", dict(words=0, streak=0, rounds=0, learned=0, rank=False)),
        ("ОБЫЧНЫЙ", dict(words=40, streak=7, rounds=42, learned=118, rank=True)),
        ("МНОГО", dict(words=240, streak=180, rounds=312, learned=2417, rank=True)),
    )

    for title, cfg in scales:
        print()
        print("=" * (WIDTH + 2))
        print(f"  {title}: прогресс {cfg['learned']} слов, серия {cfg['streak']}, "
              f"кругов {cfg['rounds']}")
        print("=" * (WIDTH + 2))

        await reset_state(dp)
        user = await _probe(session, words=cfg["words"])
        user.streak_days = cfg["streak"]
        user.quizzes_passed = cfg["rounds"]
        user.words_learned = cfg["learned"]
        await session.commit()

        if cfg["rank"]:
            season = await get_or_create_current_season(session)
            stat = MonthlyStats(
                user_id=user.id, season_id=season.id, learning_lang="de",
                monthly_quizzes=cfg["rounds"], monthly_reverse=3,
                monthly_words=cfg["learned"] // 10,
                monthly_streak=min(cfg["streak"], 31),
                monthly_avg_percent=84,
                total_correct=cfg["rounds"] * 12,
                total_questions=cfg["rounds"] * 15,
                correct_audio=cfg["rounds"] * 3, correct_speech=cfg["rounds"],
            )
            stat.monthly_score = stat.calculate_monthly_score()
            session.add(stat)
            await session.commit()

        rec.clear()
        await dp.feed_update(bot, text_update(user.id, "/home"))
        _dump(rec, raw, f"{title} · прогресс")

        await dp.feed_update(bot, press(user.id, "stats_full"))
        _dump(rec, raw, f"{title} · подробная статистика")

        await dp.feed_update(bot, text_update(user.id, get_text("btn_rating", "ru")))
        _dump(rec, raw, f"{title} · рейтинг")

        from app.bot.keyboards.notifications import get_reminder_keyboard
        from app.schedulers.reminder_scheduler import build_reminder_text
        async with AsyncSessionLocal() as fresh:
            person = await fresh.get(User, user.id)
            text = await build_reminder_text(person, fresh)
        _frame(f"{title} · напоминание")
        _screen(text, [[b.text for b in row]
                       for row in get_reminder_keyboard("ru", count=15).inline_keyboard],
                raw)


FLOWS = {
    "new": flow_new,
    "old": flow_old,
    "round": flow_round,
    "reverse": flow_reverse,
    "sweep": flow_sweep,
    "scales": flow_scales,
}


async def run(who: str, raw: bool) -> int:
    chosen = (
        ["new", "old", "round", "reverse", "scales", "sweep"] if who == "all"
        else ["new", "old", "round"] if who == "both"
        else [who]
    )
    bot, rec = make_bot()
    async with AsyncSessionLocal() as session:
        dp = make_dispatcher(session)
        try:
            for name in chosen:
                await FLOWS[name](dp, bot, rec, raw, session)
        finally:
            await _drop(session)
    print()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--who", default="both",
                    choices=("new", "old", "round", "reverse", "sweep", "scales",
                             "both", "all"))
    ap.add_argument("--raw", action="store_true")
    args = ap.parse_args()
    return asyncio.run(run(args.who, args.raw))


if __name__ == "__main__":
    sys.exit(main())
