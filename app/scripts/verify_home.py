# -*- coding: utf-8 -*-
"""
ПРИЁМКА ДОМАШНЕГО ЭКРАНА: три шкалы на живых людях и на всех шести языках.

    python -m app.scripts.verify_home
    python -m app.scripts.verify_home --per-lang 12

ЗАЧЕМ. Экран собирается из двух запросов, и беда у него ровно одна, зато
тихая: ЧИСЛИТЕЛЬ И ЗНАМЕНАТЕЛЬ МОГУТ ПРИЙТИ ИЗ РАЗНЫХ НАБОРОВ СЛОВ. Тогда
полоса уходит за край — «342 из 300», — и это не падение, а молчаливое
вранье: экран нарисуется, человек прочтёт неправду. Семь прежних дефектов
проекта были той же формы (`ROADMAP.md` §6), и ни один не нашёлся чтением
кода — все замером.

Поэтому замер идёт двумя проходами:

  живые люди   каждый пользователь базы со своим уровнем, режимом, парой
               языков и накопленным прогрессом. Это единственный способ
               поймать расхождение наборов: у подопытного пользователя
               прогресса нет, и у него ЛЮБАЯ формула даёт нули.
  языки        по паре языков на каждую локаль — чтобы подписи шкал не
               разъехались и ни один ключ не оказался пропущен.

ЧТО ПРОВЕРЯЕТСЯ В КАЖДОМ ЭКРАНЕ

  шкалы        число по каналу не больше числа слов набора;
               три полосы одной длины и начинаются в одном столбце —
               иначе сравнивать их взглядом нельзя, а в этом весь смысл
  допуск       допущенных к каналу не меньше освоенных им: порог допуска
               ниже порога освоения, и обратное означало бы, что считаются
               разные множества
  текст        ни одного «[MISSING:» и «[ERROR:» — пропущенный ключ
               локали уезжает человеку прямо в сообщение
  кнопки       главная кнопка и три прямых входа по каналам

Скрипт ТОЛЬКО ЧИТАЕТ: ни одной записи, ни одного commit.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

logging.disable(logging.INFO)

from sqlalchemy import select  # noqa: E402

from app.database.enums import CEFRLevel, QuizMode  # noqa: E402
from app.database.models import User  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.locales import LOCALES  # noqa: E402
from app.services.language_service import (  # noqa: E402
    INTERFACE_LANGS, LEARNABLE_LANGS,
)

# Подопытный пользователь: id заведомо не занят живыми людьми. Прогресса у
# него нет, поэтому шкалы выйдут нулевыми — он нужен только для проверки
# подписей и вёрстки на всех шести языках, а не содержательных чисел.
PROBE_USER_ID = -998


def _bar_start(line: str) -> int:
    """
    С какого столбца начинается полоса.

    Берётся первый из ДВУХ знаков полосы, а не первый пустой. Первая
    редакция искала `░` — и на живых людях дала два «нарушения»: у
    закрашенной полосы «▓▓▓░░░░» первый `░` стоит на четвёртом месте, и
    выравнивание выглядело сломанным там, где оно было в порядке. Это та же
    форма, что и семь прежних дефектов: проверка смотрела на соседнее поле.
    """
    marks = [i for i, ch in enumerate(line) if ch in "▓░"]
    return marks[0] if marks else -1


def _check(text: str, keyboard, progress: dict, total: int) -> list[str]:
    """Содержательные проверки одного экрана. Пустой список — всё верно."""
    problems: list[str] = []

    if "[MISSING:" in text or "[ERROR:" in text:
        problems.append("в тексте след незаполненного ключа локали")

    # Полоса рисуется от ВСТРЕЧЕННЫХ слов, и это та граница, которую нельзя
    # перейти: освоить канал можно только у слова, которое уже встречал.
    for field in ("text", "audio", "speech"):
        if progress[field] > progress["touched"]:
            problems.append(
                f"шкала {field}: {progress[field]} "
                f"при {progress['touched']} встреченных словах"
            )

    # А встреченных не может быть больше, чем слов в наборе занятия. Это
    # вторая половина той же проверки: разойдись наборы — сломается либо
    # первое неравенство, либо это.
    if progress["touched"] > total:
        problems.append(
            f"встречено {progress['touched']} при наборе из {total} слов"
        )

    # Порог допуска НИЖЕ порога освоения, значит допущенных не может быть
    # меньше освоенных. Обратное означало бы, что два числа посчитаны по
    # разным множествам слов, — та самая форма дефекта.
    if progress["ready_audio"] < progress["audio"]:
        problems.append(
            f"допущено к слуху {progress['ready_audio']}, "
            f"а освоено {progress['audio']}"
        )
    if progress["ready_speech"] < progress["speech"]:
        problems.append(
            f"допущено к речи {progress['ready_speech']}, "
            f"а освоено {progress['speech']}"
        )

    if "<code>" not in text:
        problems.append("блока шкал нет вовсе")
    else:
        block = text.split("<code>")[1].split("</code>")[0]
        lines = block.splitlines()
        if len(lines) != 3:
            problems.append(f"шкал {len(lines)}, а должно три")
        else:
            starts = {_bar_start(line) for line in lines}
            if len(starts) != 1:
                problems.append(f"полосы начинаются в разных столбцах: {starts}")

    rows = keyboard.inline_keyboard
    shape = [len(row) for row in rows]
    if shape != [1, 3, 1]:
        problems.append(
            f"клавиатура не «занятие · три канала · подробнее»: ряды {shape}"
        )
    elif rows[0][0].callback_data != "learn_now":
        problems.append(
            "первая кнопка домашнего экрана не ведёт к занятию: "
            f"{rows[0][0].callback_data}"
        )

    return problems


async def run(per_lang: int) -> int:
    from app.bot.handlers.quiz.home import _scope, build_home
    from app.services.language_service import pair_from_user
    from app.services.quiz_service import (
        get_channel_progress, get_user_progress_stats,
    )

    checked = collections.Counter()
    by_mode = collections.Counter()
    failures: list[str] = []
    skipped_no_level = 0
    gaps: list[tuple[int, int, int]] = []

    async def one(user: User, tag: str) -> None:
        pair = pair_from_user(user)
        level, category = _scope(user)
        progress = await get_channel_progress(
            user.id, session, pair, level=level, category=category
        )
        stats = await get_user_progress_stats(
            user.id, session, pair, level=level, category=category
        )
        text, keyboard = await build_home(user, session)

        for problem in _check(text, keyboard, progress, stats["total_words"]):
            failures.append(f"{tag}: {problem}")

        checked[tag.split()[0]] += 1
        by_mode[user.quiz_mode.value if user.quiz_mode else "—"] += 1
        if progress["text"] or progress["audio"] or progress["speech"]:
            gaps.append((progress["text"], progress["audio"], progress["speech"]))

    async with AsyncSessionLocal() as session:
        # ================= ПРОХОД 1: ЖИВЫЕ ЛЮДИ =========================
        users = (await session.execute(
            select(User).where(User.id > 0).order_by(User.id)
        )).scalars().all()

        for user in users:
            if not user.level:
                skipped_no_level += 1
                continue
            await one(user, f"люди id={user.id}")

        # ================= ПРОХОД 2: ВСЕ ШЕСТЬ ЯЗЫКОВ ===================
        probe = User(id=PROBE_USER_ID, level=CEFRLevel.B1, quiz_mode=QuizMode.LEVEL)
        probe.audio_enabled = True
        probe.quiz_channels = "tas"
        probe.streak_days = 7

        for lang in INTERFACE_LANGS:
            pairs = [c for c in LEARNABLE_LANGS if c != lang][:per_lang]
            for learning in pairs:
                probe.interface_language = lang
                probe.native_lang = lang
                probe.learning_lang = learning
                probe.reverse_mode = False
                await one(probe, f"язык {lang}→{learning}")

        await session.rollback()   # ничего не записываем, и это видно

    total_checked = sum(checked.values())

    print(f"\nживых людей проверено: {checked['люди']}"
          f" (без уровня пропущено: {skipped_no_level})")
    print(f"сочетаний языков проверено: {checked['язык']}"
          f" (локалей {len(LOCALES)})")
    print(f"ВСЕГО ЭКРАНОВ: {total_checked}")
    print("по режимам: " + ", ".join(f"{m} {n}" for m, n in by_mode.most_common()))

    if gaps:
        print(f"\nэкранов с непустыми шкалами: {len(gaps)}")
        widest = max(gaps, key=lambda g: g[0] - g[2])
        print(f"самый широкий разрыв глаз/речь: "
              f"написанное {widest[0]} · на слух {widest[1]} · вслух {widest[2]}")
    else:
        print("\nни одного экрана с непустыми шкалами — "
              "содержательные числа НЕ ПРОВЕРЕНЫ")

    # «Ок» без числа проверенного — не результат. Приёмка обязана падать на
    # холостом прогоне: дважды за один день приёмка трёх игр отрапортовала
    # «всё верно», не задав ни одного вопроса на слух (`ROADMAP.md` §6).
    if total_checked == 0:
        print("\nПРОВЕРЯТЬ БЫЛО НЕЧЕГО — это неудача, а не успех")
        return 1
    if checked["язык"] < len(LOCALES):
        print("\nпроверены не все локали — часть подписей осталась не глянута")
        return 1

    if failures:
        print(f"\nНАРУШЕНИЙ: {len(failures)}")
        for line in failures[:25]:
            print(f"   {line}")
        if len(failures) > 25:
            print(f"   … и ещё {len(failures) - 25}")
        return 1

    print("\nдомашний экран собирается верно: шкалы в своих границах, "
          "полосы выровнены, подписи на месте")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-lang", type=int, default=5,
                        help="сколько изучаемых языков брать на локаль")
    args = parser.parse_args()
    return asyncio.run(run(args.per_lang))


if __name__ == "__main__":
    raise SystemExit(main())
