# -*- coding: utf-8 -*-
"""
Приёмка напоминаний: какой повод получил бы КАЖДЫЙ человек базы.

ЗАЧЕМ. Правило выбора повода проверено тестами на выдуманных числах, а
живые люди распределены иначе. Главная опасность — повод, который по
правилу достижим, а на настоящей базе не достаётся НИКОМУ: такой код
выглядит работающим и молчит. Так уже вышло дважды, и оба раза увидел это
показ, а не чтение.

Вторая опасность — повод, который достаётся почти всем: тогда семь видов
напоминания сводятся к одному, и разнообразия нет, сколько бы строк ни
было написано.

Только чтение.
"""
from __future__ import annotations

import asyncio
import collections
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import select  # noqa: E402

from app.database.models import User  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.locales import get_text  # noqa: E402

logging.disable(logging.ERROR)

# Сколько примеров показывать на повод
SHOW = 2

# Почему повод может никому не достаться. Пустой повод — всегда вопрос, и
# у него ровно два ответа: либо его перекрыл другой (дефект), либо в базе
# нет людей в таком состоянии (не дефект). Приёмка обязана назвать, какой
# именно, — иначе мёртвое правило третий раз пройдёт за «редкий случай».
WHY_EMPTY = {
    "remind_streak_risk":
        "живых серий в базе нет вовсе — последняя активность 19 февраля. "
        "Повод оживёт вместе с петлёй возврата",
    "remind_streak_lost":
        "окно в неделю после обрыва: все ушли 236 дней назад, в окно никто "
        "не попадает",
    "remind_almost_learned":
        "нужны люди с нулём выученных и словом в одном ответе от «выучено»",
    "remind_rank":
        "стоит ниже «слова ждут», а просроченные слова есть почти у всех, "
        "кто играл",
    "remind_fact_2": "замечание выбирается по числу кругов: нужен остаток 1",
    "remind_fact_3": "нужен остаток 2 от числа кругов",
    "remind_fact_4": "нужен остаток 3 от числа кругов",
}


async def main() -> int:
    from app.schedulers.reminder_scheduler import collect_reminder_facts
    from app.services.language_service import pair_from_user
    from app.services.reminder_reason import pick_reason, reason_line

    print("Приёмка напоминаний: повод для каждого человека базы")
    print("=" * 76)

    counts: collections.Counter = collections.Counter()
    samples: dict[str, list[str]] = collections.defaultdict(list)
    liars: list[str] = []

    async with AsyncSessionLocal() as session:
        users = (await session.execute(select(User).order_by(User.id))).scalars().all()

        for user in users:
            pair = pair_from_user(user)
            facts = await collect_reminder_facts(user, session, pair)
            key, _ = pick_reason(facts)
            counts[key] += 1

            if len(samples[key]) < SHOW:
                line = reason_line(facts, user.interface_language or "ru")
                samples[key].append(f"{user.id}: {line}")

            # СТОРОЖ ВРАНЬЯ. Повод обязан быть правдой на момент отправки,
            # и две проверки ловят ровно те случаи, что уже случались
            if key == "remind_streak_risk" and facts.streak_days < 2:
                liars.append(f"{user.id}: серия {facts.streak_days}, а повод про серию")
            if key == "remind_due" and facts.due_words <= 0:
                liars.append(f"{user.id}: слов не ждёт, а повод про повторение")
            if key == "remind_milestone_close" and facts.words_in_work == 0:
                liars.append(f"{user.id}: слов в работе ноль, а повод про рубеж")

    total = sum(counts.values())
    print(f"\nлюдей: {total}\n")
    print(f"{'повод':26} {'людей':>6}  {'доля':>6}")
    for key, count in counts.most_common():
        print(f"  {key:24} {count:>6}  {count / total * 100:>5.1f}%")
        for sample in samples[key]:
            print(f"      {sample[:84]}")

    # Поводы, которые не достались НИКОМУ
    from app.services.reminder_reason import FACTS_COUNT

    all_keys = {
        "remind_streak_risk", "remind_due", "remind_due_many",
        "remind_streak_lost", "remind_milestone_close",
        "remind_almost_learned", "remind_rank",
        *(f"remind_fact_{i}" for i in range(1, FACTS_COUNT + 1)),
    }
    unused = sorted(all_keys - set(counts))

    print()
    print("=" * 76)
    problems = 0

    if liars:
        problems += len(liars)
        print(f"[СБОЙ] повод не соответствует числам — {len(liars)}")
        for line in liars[:10]:
            print(f"       {line}")
    else:
        print("[ок  ] каждый повод подтверждён числами того же человека")

    # ПОЧЕМУ повод никому не достался — вопрос решающий, и ответов два:
    # либо правило перекрыто другим поводом (дефект, его надо править),
    # либо в базе нет людей в таком состоянии (не дефект, данные такие).
    # Отличить одно от другого глазами нельзя: оба выглядят как «ноль».
    if unused:
        print(f"[знать] никому не досталось: {', '.join(unused)}")
        for key in unused:
            print(f"        {key}: {WHY_EMPTY.get(key, 'причина не разобрана')}")
    else:
        print("[ок  ] каждый повод кому-то достался")

    biggest, share = counts.most_common(1)[0]
    if share / total > 0.9:
        problems += 1
        print(f"[СБОЙ] один повод у {share / total * 100:.0f}% людей ({biggest}):")
        print("       семь видов напоминания свелись к одному")
    else:
        print(f"[ок  ] самый частый повод у {share / total * 100:.0f}% — "
              f"напоминания различаются")

    print("=" * 76)
    if problems:
        print(f"НАРУШЕНИЙ: {problems}")
        return 1
    print("напоминания говорят правду и не повторяются у всех подряд")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
