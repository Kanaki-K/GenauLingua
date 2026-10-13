"""Правки по `example_person_mismatch` — проверке, которую я за 72 блока
НЕ ПРОГНАЛ НИ РАЗУ.

Она лежала в репозитории всё время и ищет ровно тот класс, который я
искал глазами: «пример-перевод не соответствует немецкому примеру,
разное лицо подлежащего». Прогнана по требованию владельца после
окончания обзора.

ЧТО ДАЛА. 83 расхождения на 3292 проверенных ряда по четырём языкам.
Из них настоящих **17**, остальные 66 — сдвиг конструкции при том же
смысле, и примета их не отличает:

    de  Meine Partnerin und ich haben große Pläne
    ru  Мы с моей партнёршей строим большие планы
        примета видит «1s против 1p», а смысл один

    de  Ich bezweifle, dass er die Wahrheit sagt
    pl  Wątpię, że on mówi prawdę
        «Wątpię» это и есть первое лицо, примета смотрит на «on»

Семнадцать настоящих — это подменённая фраза, а не сдвиг:

    de  Du kannst den Mantel ablegen        (можешь снять пальто)
    en  She successfully passed the exam    (она сдала экзамен)

ЧТО ЭТО ЗНАЧИТ ПРО ОБЗОР. Семнадцать дефектов такого рода прошли мимо
глаз за 72 блока. Не потому, что класс незнаком — я правил его
десятки раз, — а потому, что в блоке из 200 рядов и 1200 ячеек глаз
держит не всё. Готовая проверка нашла их за минуту.

Урок прямой: **прежде чем читать глазами, надо прогнать ВСЁ, что уже
написано.** У меня в репозитории лежали `example_person_mismatch`,
`example_number_mismatch` и `example_quality`, и я построил
`scan_number_mismatch` заново, не заметив, что второй уже есть.

Два ряда из семнадцати — `du` (1328) и `ich` (1687) — это известные
полные дубликаты, ждущие решения владельца (HANDOVER 1b). Примеры им
правятся всё равно: дубликат не повод учить неверному.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (13986, "example_en",
     "He denied taking the money",
     "He denies everything I say",
     "эталон «Er leugnet alles, was ich sage» — про отрицание моих слов"),
    (1104, "example_en",
     "She successfully passed the exam",
     "You can take off your coat",
     "эталон «Du kannst den Mantel ablegen» — снять пальто, а не сдать экзамен"),
    (1104, "example_uk",
     "Вона успішно склала іспит",
     "Ти можеш зняти пальто",
     "то же"),
    (1328, "example_uk",
     "Я бачу тебе",
     "Ти підеш з нами сьогодні ввечері?",
     "эталон «Kommst du heute Abend mit?»"),
    (1833, "example_uk",
     "Він високий і стрункий хлопець",
     "Ти дуже стрункий",
     "эталон «Du bist sehr schlank» — обращение на «ты», а не про него"),
    (1687, "example_en",
     "Do you see me",
     "I am already quite tired",
     "эталон «Ich bin schon ziemlich müde»"),
    (1687, "example_uk",
     "Ти мене бачиш",
     "Я вже досить втомлений",
     "то же"),
    (13461, "example_en",
     "It's raining, however we're going for a walk",
     "It's raining, however I'm going for a walk",
     "в эталоне «gehe ich» — я, а не мы"),
    (13461, "example_uk",
     "Йде дощ, однак ми йдемо гуляти",
     "Йде дощ, однак я йду гуляти",
     "то же"),
    (7092, "example_en",
     "He performed badly on the exam",
     "I want to cut off the label",
     "эталон «Ich will das Etikett abschneiden» — отрезать этикетку"),
    (7092, "example_uk",
     "Він погано виступив на іспиті",
     "Я хочу відрізати етикетку",
     "то же"),
    (8415, "example_en",
     "He's quitting the party because he no longer agrees",
     "I want to leave the club",
     "эталон «Ich will aus dem Verein austreten» — из клуба, и это я"),
    (8415, "example_uk",
     "Він виходить з партії, тому що більше не згоден",
     "Я хочу вийти з клубу",
     "то же"),
    (13775, "example_en",
     "She gets her hair styled in the morning before going to work",
     "I get my hair styled in the morning before going to work",
     "в эталоне «Ich lass mir» — я, а не она"),
    (13775, "example_uk",
     "Щоранку вона розчісується перед дзеркалом",
     "Щоранку я роблю укладку перед роботою",
     "то же; и про зеркало в эталоне нет"),
    (17395, "example_ru",
     "Я обычно заправляюсь на этой станции",
     "Нам нужно заправиться перед долгой поездкой",
     "эталон «Wir müssen auftanken, bevor wir eine lange Fahrt machen»"),
    (10775, "example_uk",
     "Він стояв безмовний від подиву",
     "Я був безмовний, коли побачив результат",
     "эталон «Ich war sprachlos, als ich das Ergebnis sah»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
