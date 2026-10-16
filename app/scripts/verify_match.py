# -*- coding: utf-8 -*-
"""
ПРИЁМКА ДОСКИ СОПОСТАВЛЕНИЯ: все 30 пар, оба направления.

    python -m app.scripts.verify_match
    python -m app.scripts.verify_match --boards 5

ЗАЧЕМ. Доска собирается из пяти слов сразу, и беды у неё свои, которых у
обычного вопроса не бывает:

  направление   слева должен стоять язык ВОПРОСА, справа язык ОТВЕТА. В
                обратном режиме они меняются местами, и первая редакция
                доски этого не делала вовсе: ставила изучаемый язык слева
                жёстко. Доска при этом собиралась и решалась, ничем не
                выдавая, что человек просил обратный порядок
  подсказка     ни одна пара не стоит напротив себя, иначе ответ дан
  неразрешимость  две одинаковые подписи в колонке означают два верных
                ответа, а засчитан будет один: человек увидит «не пара» на
                совершенно верном выборе
  ширина        подпись должна влезать в кнопку на половину экрана вместе
                со значком состояния

Проверяется ЖИВОЙ отбор `pick_words` на настоящей базе, а не выдуманные
слова: длина подписи считается по ВЫБРАННОМУ значению, и подделать её
значило бы проверить не то.

ЧТО ПИШЕТСЯ В БАЗУ. Прогресс подопытного пользователя — без него доска не
соберётся, порог допуска требует верных ответов. Пользователь свой, с
отрицательным id, и в конце удаляется вместе со следами.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import logging
import os
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

logging.disable(logging.INFO)

from sqlalchemy import delete, select  # noqa: E402

from app.database.enums import CEFRLevel, QuizMode  # noqa: E402
from app.database.models import User, UserWord, Word, WordLangGroup  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.services.language_service import (  # noqa: E402
    LEARNABLE_LANGS, LanguagePair, option_label,
)
from app.services.match_service import (  # noqa: E402
    BOARD_SIZE, LABEL_LIMIT, deranged_order, pick_words,
)

PROBE_ID = -1002

# Сколько слов засеять прогрессом. Доске нужно пять годных, а годность
# решается длиной подписи — на иных парах её проходит две трети, поэтому
# запас кратный.
SEED_WORDS = 300


async def _probe(session, learning: str, native: str, reverse: bool) -> User:
    user = await session.get(User, PROBE_ID)
    if user is None:
        user = User(id=PROBE_ID, first_name="приёмка доски")
        session.add(user)
    user.level = CEFRLevel.B1
    user.quiz_mode = QuizMode.LEVEL
    user.learning_lang = learning
    user.native_lang = native
    user.reverse_mode = reverse
    user.interface_language = "ru"
    await session.commit()
    return user


async def _seed(session, learning: str) -> None:
    """Прогресс по части слов: без него порог допуска не пустит ни одного."""
    rows = await session.execute(
        select(Word.id)
        .join(
            WordLangGroup,
            (WordLangGroup.word_id == Word.id)
            & (WordLangGroup.lang == learning)
            & (WordLangGroup.is_canonical.is_(True)),
        )
        .where(Word.level == CEFRLevel.B1)
        .limit(SEED_WORDS)
    )
    for (word_id,) in rows.all():
        session.add(UserWord(
            user_id=PROBE_ID, word_id=word_id, learning_lang=learning,
            correct_streak=1, times_shown=2, times_correct=2, learned=False,
        ))
    await session.commit()


def _check(words: list[Word], pair: LanguagePair, order: list[int]) -> list[str]:
    """Содержательные проверки одной доски. Пустой список — всё верно."""
    problems: list[str] = []

    if len(words) != BOARD_SIZE:
        problems.append(f"пар {len(words)}, а должно {BOARD_SIZE}")
        return problems

    left = [option_label(w, pair.prompt_lang) for w in words]
    right = [option_label(w, pair.answer_lang) for w in words]

    for side, labels in (("слева", left), ("справа", right)):
        if any(not text.strip() for text in labels):
            problems.append(f"{side} есть пустая подпись")
        if len(set(t.casefold() for t in labels)) != len(labels):
            problems.append(f"{side} подписи повторяются: {labels}")
        for text in labels:
            if len(text) > LABEL_LIMIT:
                problems.append(f"{side} подпись длиннее {LABEL_LIMIT}: {text!r}")

    # НАПРАВЛЕНИЕ. В обратном режиме слева должен стоять язык значения, а
    # не изучаемый — иначе доска не отличается от прямого порядка
    if pair.reverse:
        straight = [option_label(w, pair.learning) for w in words]
        if left == straight:
            problems.append("обратный режим: слева по-прежнему изучаемый язык")

    # Ни одна пара не стоит напротив себя
    for position, index in enumerate(order):
        if position == index:
            problems.append(f"пара {index} стоит напротив себя")

    return problems


async def run(boards: int) -> int:
    cases = [
        (learning, native, reverse)
        for learning in LEARNABLE_LANGS
        for native in LEARNABLE_LANGS
        if learning != native
        for reverse in (False, True)
    ]

    built = 0
    too_thin = collections.Counter()
    failures: list[str] = []
    rng = random.Random(20261012)

    async with AsyncSessionLocal() as session:
        try:
            for learning, native, reverse in cases:
                user = await _probe(session, learning, native, reverse)
                await _seed(session, learning)
                pair = LanguagePair(learning=learning, native=native, reverse=reverse)
                arrow = "←" if reverse else "→"
                case = f"{learning}{arrow}{native}"

                for _ in range(boards):
                    words = await pick_words(user, session, pair)
                    if len(words) < BOARD_SIZE:
                        # Не нарушение: на иных парах коротких подписей
                        # мало. Но считаем и печатаем — молчать о том, чего
                        # не проверили, нельзя
                        too_thin[case] += 1
                        continue

                    order = deranged_order(len(words), rng)
                    built += 1
                    for problem in _check(words, pair, order):
                        failures.append(f"{case}: {problem}")

                await session.execute(
                    delete(UserWord).where(UserWord.user_id == PROBE_ID)
                )
                await session.commit()
        finally:
            await session.execute(delete(UserWord).where(UserWord.user_id == PROBE_ID))
            await session.execute(delete(User).where(User.id == PROBE_ID))
            await session.commit()

    print(f"\nсочетаний проверено: {len(cases)} (пар {len(cases) // 2} × 2 направления)")
    print(f"досок собрано: {built} из {len(cases) * boards} попыток")
    if too_thin:
        total = sum(too_thin.values())
        print(f"не хватило коротких подписей: {total} попыток "
              f"({100 * total / max(len(cases) * boards, 1):.1f}%)")
        print("  чаще всего: " + ", ".join(
            f"{case} ({n})" for case, n in too_thin.most_common(5)
        ))

    if built == 0:
        print("\nНИ ОДНОЙ ДОСКИ НЕ СОБРАНО — проверять было нечего, это неудача")
        return 1

    if failures:
        print(f"\nНАРУШЕНИЙ: {len(failures)}")
        for line in failures[:25]:
            print(f"   {line}")
        if len(failures) > 25:
            print(f"   … и ещё {len(failures) - 25}")
        return 1

    print("\nдоска собирается верно на всех парах и в оба направления")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boards", type=int, default=3,
                        help="досок на каждое сочетание (по умолчанию 3)")
    args = parser.parse_args()
    return asyncio.run(run(args.boards))


if __name__ == "__main__":
    raise SystemExit(main())
