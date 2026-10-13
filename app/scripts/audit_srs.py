"""
ПРИЁМКА ПОДБОРА СЛОВ: возвращается ли слово, и чем наполнен круг.

ЗАЧЕМ. До 13 октября 2026 подбор ключевался на точности, и слово,
отвеченное верно с первого раза, не попадало ни в одну корзину — 18 664
слова из 21 306 (87.6%) не могли вернуться никогда. Разбор —
`ROADMAP.md` §5б.

Дефект прожил незамеченным ровно потому, что ни одна приёмка не проверяла
СУДЬБУ СЛОВА: каждая смотрела на свой экран — собрался ли вопрос, цел ли
круг, сходятся ли счётчики. Этот скрипт смотрит на слово.

ЧТО ПРОВЕРЯЕТСЯ

    A  слово, отвеченное ВЕРНО, возвращается, когда выйдет срок
    B  и НЕ возвращается раньше срока
    C  круг из 15 содержит ровно столько новых, сколько обещано
    D  просроченные разбираются с самого старого
    E  выученное слово тоже возвращается — на поддержание
    F  у человека без прогресса круг собирается целиком из новых

Подопытные заводятся и удаляются; живых людей скрипт не трогает.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.audit_srs
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from datetime import timedelta

from sqlalchemy import delete, func, select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User, UserWord, Word, WordLangGroup
from app.database.session import AsyncSessionLocal
from app.services.language_service import pair_from_user
from app.services.quiz_service import (
    DEFAULT_ROUND_LENGTH, NEW_WORDS_PER_ROUND, REVIEW_SCHEDULE,
    count_due_words, get_due_words, select_word_by_priority, wants_new_word,
)

logging.disable(logging.ERROR)

PROBE = 950_000_501
LEVEL = CEFRLevel.A1


class Report:
    def __init__(self) -> None:
        self.problems: list[str] = []
        self.checked = 0

    def check(self, ok: bool, title: str, detail: str = "") -> None:
        self.checked += 1
        mark = "ок  " if ok else "СБОЙ"
        print(f"  [{mark}] {title}" + (f" — {detail}" if detail else ""))
        if not ok:
            self.problems.append(f"{title}: {detail}")


async def _reset(session) -> User:
    await session.rollback()
    await session.execute(delete(User).where(User.id == PROBE))
    await session.commit()
    session.expunge_all()

    user = User(
        id=PROBE, first_name="Подбор", interface_language="ru",
        learning_lang="de", native_lang="ru", reverse_mode=False,
        level=LEVEL, quiz_mode=QuizMode.LEVEL, quiz_word_count=15,
        quiz_channels="t", audio_enabled=False,
    )
    session.add(user)
    await session.commit()
    return user


async def _words(session, limit: int) -> list[Word]:
    return list((await session.execute(
        select(Word)
        .join(WordLangGroup, (WordLangGroup.word_id == Word.id)
              & (WordLangGroup.lang == "de")
              & (WordLangGroup.is_canonical.is_(True)))
        .where(Word.level == LEVEL)
        .order_by(func.random()).limit(limit)
    )).scalars().all())


async def _seen(session, word: Word, *, streak: int, ago: timedelta) -> None:
    """Записать, что слово видели `ago` назад с такой серией верных."""
    session.add(UserWord(
        user_id=PROBE, word_id=word.id, learning_lang="de",
        times_shown=max(1, streak), times_correct=streak,
        correct_streak=streak, learned=streak >= 3,
        last_seen_at=utcnow() - ago,
    ))
    await session.commit()


# ============================================================================
# ПРОВЕРКИ
# ============================================================================

async def check_returns(session, rep: Report) -> None:
    """A и B: слово возвращается по сроку и не раньше."""
    print("\nA. Слово, отвеченное ВЕРНО, возвращается когда выйдет срок")

    for streak, delay in sorted(REVIEW_SCHEDULE.items()):
        user = await _reset(session)
        pair = pair_from_user(user)
        word = (await _words(session, 1))[0]

        # Раньше срока — не должно вернуться
        await _seen(session, word, streak=streak, ago=delay / 2)
        early = await get_due_words(PROBE, session, pair, [], user=user)
        rep.check(
            early is None,
            f"серия {streak}: НЕ возвращается раньше срока",
            f"срок {delay}, прошло вдвое меньше"
            + (f", а вернулось «{early.word_de}»" if early else ""),
        )

        # После срока — должно
        await session.execute(delete(UserWord).where(UserWord.user_id == PROBE))
        await session.commit()
        await _seen(session, word, streak=streak, ago=delay + timedelta(minutes=5))
        due = await get_due_words(PROBE, session, pair, [], user=user)
        rep.check(
            due is not None and due.id == word.id,
            f"серия {streak}: возвращается после срока",
            f"срок {delay}" + ("" if due else ", а не вернулось"),
        )


async def check_composition(session, rep: Report) -> None:
    """C: сколько новых слов в круге."""
    print("\nC. Состав круга: новые слова по месту, а не жребием")

    user = await _reset(session)
    pair = pair_from_user(user)
    # Двадцать знакомых, всем пора — значит повторений хватит на весь круг
    for word in await _words(session, 20):
        await _seen(session, word, streak=1, ago=timedelta(days=2))

    known = {
        row.word_id for row in (await session.execute(
            select(UserWord).where(UserWord.user_id == PROBE)
        )).scalars().all()
    }

    picked: list[int] = []
    new_count = 0
    for _ in range(DEFAULT_ROUND_LENGTH):
        word = await select_word_by_priority(
            PROBE, session, pair, picked, user=user,
            round_length=DEFAULT_ROUND_LENGTH,
        )
        if word is None:
            break
        picked.append(word.id)
        if word.id not in known:
            new_count += 1

    rep.check(
        len(picked) == DEFAULT_ROUND_LENGTH,
        "круг собрался целиком",
        f"слов {len(picked)} из {DEFAULT_ROUND_LENGTH}",
    )
    rep.check(
        new_count == NEW_WORDS_PER_ROUND,
        f"новых в круге ровно {NEW_WORDS_PER_ROUND}",
        f"вышло {new_count}",
    )
    rep.check(
        len(set(picked)) == len(picked),
        "ни одно слово не повторилось внутри круга",
        f"уникальных {len(set(picked))} из {len(picked)}",
    )


async def check_oldest_first(session, rep: Report) -> None:
    """D: долг разбирается с самого старого."""
    print("\nD. Просроченные идут с самого залежавшегося")

    user = await _reset(session)
    pair = pair_from_user(user)
    words = await _words(session, 3)
    ages = (timedelta(days=30), timedelta(days=10), timedelta(days=2))
    for word, ago in zip(words, ages):
        await _seen(session, word, streak=1, ago=ago)

    order = []
    taken: list[int] = []
    for _ in range(3):
        word = await get_due_words(PROBE, session, pair, taken, user=user)
        if word is None:
            break
        order.append(word.id)
        taken.append(word.id)

    rep.check(
        order == [w.id for w in words],
        "порядок — от самого старого к свежему",
        f"ожидалось {[w.word_de for w in words]}",
    )


async def check_learned_returns(session, rep: Report) -> None:
    """E: выученное возвращается на поддержание."""
    print("\nE. Выученное слово тоже возвращается")

    user = await _reset(session)
    pair = pair_from_user(user)
    word = (await _words(session, 1))[0]
    await _seen(session, word, streak=4, ago=timedelta(days=22))

    due = await get_due_words(PROBE, session, pair, [], user=user)
    rep.check(
        due is not None and due.id == word.id,
        "выученное слово вернулось через 21 день",
        "" if due else "не вернулось — забудется тихо",
    )

    count = await count_due_words(PROBE, session, pair, user=user)
    rep.check(count == 1, "счётчик просроченных видит его", f"насчитал {count}")


async def check_fresh_user(session, rep: Report) -> None:
    """F: у человека без прогресса круг целиком из новых."""
    print("\nF. Первый день: повторять нечего, круг из новых")

    user = await _reset(session)
    pair = pair_from_user(user)

    picked: list[int] = []
    for _ in range(DEFAULT_ROUND_LENGTH):
        word = await select_word_by_priority(
            PROBE, session, pair, picked, user=user,
            round_length=DEFAULT_ROUND_LENGTH,
        )
        if word is None:
            break
        picked.append(word.id)

    rep.check(
        len(picked) == DEFAULT_ROUND_LENGTH,
        "круг собрался целиком и у новичка",
        f"слов {len(picked)}",
    )
    rep.check(
        len(set(picked)) == len(picked),
        "без повторов",
        f"уникальных {len(set(picked))}",
    )


async def check_second_day(session, rep: Report) -> None:
    """
    Второй день — самый дорогой случай: 56.6% возвратов приходятся на него,
    и 112 человек из 199 занимались ровно один день.
    """
    print("\nG. Второй день: круг построен из слов первого дня")

    user = await _reset(session)
    pair = pair_from_user(user)
    yesterday = await _words(session, 15)
    for index, word in enumerate(yesterday):
        # Как после первого дня: большинство верно, три промаха
        await _seen(session, word, streak=0 if index < 3 else 1,
                    ago=timedelta(days=1, hours=2))

    known = {w.id for w in yesterday}
    picked: list[int] = []
    from_yesterday = 0
    for _ in range(DEFAULT_ROUND_LENGTH):
        word = await select_word_by_priority(
            PROBE, session, pair, picked, user=user,
            round_length=DEFAULT_ROUND_LENGTH,
        )
        if word is None:
            break
        picked.append(word.id)
        if word.id in known:
            from_yesterday += 1

    expected = DEFAULT_ROUND_LENGTH - NEW_WORDS_PER_ROUND
    rep.check(
        from_yesterday == expected,
        f"слов первого дня в круге {expected} из {DEFAULT_ROUND_LENGTH}",
        f"вышло {from_yesterday}",
    )


async def run() -> int:
    rep = Report()
    print("Приёмка подбора слов\n" + "=" * 62)

    async with AsyncSessionLocal() as session:
        try:
            await check_returns(session, rep)
            await check_composition(session, rep)
            await check_oldest_first(session, rep)
            await check_learned_returns(session, rep)
            await check_fresh_user(session, rep)
            await check_second_day(session, rep)
        finally:
            await session.rollback()
            await session.execute(delete(User).where(User.id == PROBE))
            await session.commit()

    print("\n" + "=" * 62)
    print(f"проверок: {rep.checked}")
    if rep.problems:
        print(f"СБОЕВ: {len(rep.problems)}")
        for line in rep.problems:
            print(f"   {line}")
        return 1
    print("подбор работает: слово возвращается по сроку, состав круга держится")
    return 0


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    return asyncio.run(run())


if __name__ == "__main__":
    sys.exit(main())
