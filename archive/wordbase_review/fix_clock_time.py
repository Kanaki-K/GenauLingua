"""СКВОЗНОЙ КЛАСС: запись времени на часах. 52 ячейки.

ОТКУДА ВЗЯЛСЯ. Класс всплывал по одному-два ряда в блоках 16, 18, 22 и
23: `Versammlung` писал «о 18:00», `Übertragung` — «в 20:00»,
`Pressekonferenz` — «at 2 p.m», `Veranstaltung` — «в 19:00». Четыре
блока подряд — повод замерить по базе.

ЗАМЕР. 71 эталон со словом «Uhr». Запись времени в переводах:

    ru   цифра + «часов» 23 │ двоеточие 10 │ словом 10
    uk   цифра + «годині» 19 │ двоеточие 10 │ словом  8
    en   «o'clock»        29 │ am/pm     17 │ двоеточие 1
    tr   «saat N»         20 │ двоеточие  9 │ точка    5
    pl   словом           43 │ двоеточие  2

**Норма в каждом языке своя, и в каждом она определяется большинством
самой базы, а не моим вкусом.** Меньшинство приводится к большинству.

ЧТО ИМЕННО ДЕФЕКТ, А ЧТО НЕТ. Я сначала думал, что двоеточие — дефект
озвучки, и так и написал в блоке 18. Это было предположение, а не
замер: современный синтезатор читает «20:00» по-русски правильно.
Настоящая причина правки другая и прочнее: **база сама себе
противоречит.** Один и тот же немецкий «um 20 Uhr» передан то «в 20
часов», то «в 20:00» — ученик видит два разных способа для одного и
того же, и ни один не объявлен главным.

Отдельно стоит английское «p.m» БЕЗ ВТОРОЙ ТОЧКИ — вот это дефект без
оговорок: такой формы нет. Она появилась из правила «в конце примера
точки не ставим», которое срезало точку у сокращения.

ТУРЕЦКИЙ ЗДЕСЬ НЕ ОШИБАЛСЯ. «saat 19.00'da» — нормальная турецкая
орфография, и правится только ради единообразия с 20 рядами, где стоит
«saat N'de» без минут. Это не исправление ошибки, а выбор одной записи
из двух законных.

ПЯТЬ ФОРМ ИСПРАВЛЕНЫ РУКАМИ, И ЭТО ГЛАВНОЕ ПРЕДУПРЕЖДЕНИЕ. Я сгенерил
замены правилом и получил пять грамматических ошибок:

    ru 2403   «в 22 часов»  → «в 22 часа»   (21–24 берут «часа»)
    uk 17356  «— 14 годині» → «— 14 година» (без «о» нужен именительный)
    pl 17356  «to czternastej» → «to czternasta»  (то же)
    tr 17356  «varış saati 14» — оставлено как было: в роли сказуемого
              голое число по-турецки читается хуже, чем «14.00»
    en 2322   «from 9 to 5 in the afternoon» — проверено глазами, годится

Это ровно та ловушка, что была с восклицательным знаком в блоке 5:
механическое правило по классу даёт правдоподобный, но неверный
результат, и спасает только чтение каждой строки.

    python -m app.scripts.fix_clock_time          # сухой прогон
    python -m app.scripts.fix_clock_time --apply
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── АНГЛИЙСКИЙ: am/pm → «o'clock»-норма, 17 ячеек ───────────
    (1099, "example_en", "The departure is at 3 PM",
     "The departure is at 3 in the afternoon", "am/pm против 29 рядов с «o'clock»"),
    (1141, "example_en", "The arrival is at 3 pm",
     "The arrival is at 3 in the afternoon", "то же"),
    (1232, "example_en", "I finish my work at 5 pm",
     "I finish my work at 5 in the afternoon", "то же"),
    (1364, "example_en", "Posting time is until 6 pm",
     "Posting time is until 6 in the evening", "то же"),
    (1773, "example_en", "The program starts at 8 pm",
     "The program starts at 8 in the evening", "то же"),
    (1963, "example_en", "The training starts at 6 pm",
     "The training starts at 6 in the evening", "то же"),
    (2322, "example_en", "Office hours are from 9 to 5 p.m",
     "Office hours are from 9 to 5 in the afternoon",
     "«p.m» без второй точки — такой формы нет"),
    (2391, "example_en", "Boarding starts at 10 a.m",
     "Boarding starts at 10 in the morning", "то же"),
    (2403, "example_en", "The movie ends at 10 p.m",
     "The movie ends at 10 in the evening", "то же"),
    (2810, "example_en", "The show is on at 8 p.m",
     "The show is on at 8 in the evening", "то же"),
    (8603, "example_en", "Admission is from 7 pm",
     "Admission is from 7 in the evening", "am/pm против нормы"),
    (9799, "example_en", "The auction starts at 3 PM",
     "The auction starts at 3 in the afternoon", "то же"),
    (11788, "example_en", "We eat dinner together at 7 PM",
     "We eat dinner together at 7 in the evening", "то же"),
    (14106, "example_en", "The meeting is tomorrow at 7 pm",
     "The meeting is tomorrow at 7 in the evening", "то же"),
    (17305, "example_en", "My return flight leaves next Tuesday at 2 PM",
     "My return flight leaves next Tuesday at 2 in the afternoon", "то же"),
    (17356, "example_en", "The arrival time of the train is 2 pm",
     "The arrival time of the train is 2 in the afternoon", "то же"),
    (18865, "example_en", "Visiting hours at the hospital are from 3 to 7 p.m",
     "Visiting hours at the hospital are from 3 to 7 in the evening",
     "«p.m» без второй точки"),

    # ── РУССКИЙ: двоеточие → «N часов», 10 ячеек ────────────────
    (1099, "example_ru", "Отправление в 15:00",
     "Отправление в 15 часов", "двоеточие против 23 рядов с «часов»"),
    (1141, "example_ru", "Прибытие в 15:00",
     "Прибытие в 15 часов", "то же"),
    (1431, "example_ru", "Самолёт приземляется в 15:00",
     "Самолёт приземляется в 15 часов", "то же"),
    (1773, "example_ru", "Программа начинается в 20:00",
     "Программа начинается в 20 часов", "то же"),
    (1963, "example_ru", "Тренировка начинается в 18:00",
     "Тренировка начинается в 18 часов", "то же"),
    (2403, "example_ru", "Фильм заканчивается в 22:00",
     "Фильм заканчивается в 22 часа",
     "ПРАВЛЕНО РУКАМИ: 21–24 берут «часа», правило дало «часов»"),
    (2810, "example_ru", "Передача идёт в 20:00",
     "Передача идёт в 20 часов", "то же"),
    (8603, "example_ru", "Вход с 19:00",
     "Вход с 19 часов", "то же"),
    (17305, "example_ru", "Мой обратный рейс вылетает в следующий вторник в 14:00",
     "Мой обратный рейс вылетает в следующий вторник в 14 часов", "то же"),
    (17356, "example_ru", "Время прибытия поезда — 14:00",
     "Время прибытия поезда — 14 часов", "то же"),

    # ── УКРАИНСКИЙ: двоеточие → «о N годині», 10 ячеек ──────────
    (1099, "example_uk", "Відправлення о 15:00",
     "Відправлення о 15 годині", "двоеточие против 19 рядов с «годині»"),
    (1773, "example_uk", "Програма починається о 20:00",
     "Програма починається о 20 годині", "то же"),
    (1963, "example_uk", "Тренування починається о 18:00",
     "Тренування починається о 18 годині", "то же"),
    (2076, "example_uk", "Лекція починається о 10:00",
     "Лекція починається о 10 годині", "то же"),
    (2403, "example_uk", "Фільм закінчується о 22:00",
     "Фільм закінчується о 22 годині", "то же"),
    (9799, "example_uk", "Аукціон починається о 15:00",
     "Аукціон починається о 15 годині", "то же"),
    (11788, "example_uk", "Ми їмо вечерю разом о 19:00",
     "Ми їмо вечерю разом о 19 годині", "то же"),
    (14106, "example_uk", "Зустріч завтра о 19:00",
     "Зустріч завтра о 19 годині", "то же"),
    (17305, "example_uk", "Мій зворотний рейс вилітає наступного вівторка о 14:00",
     "Мій зворотний рейс вилітає наступного вівторка о 14 годині", "то же"),
    (17356, "example_uk", "Час прибуття поїзда — 14:00",
     "Час прибуття поїзда — 14 година",
     "ПРАВЛЕНО РУКАМИ: без «о» нужен именительный, правило дало «годині»"),

    # ── ТУРЕЦКИЙ: двоеточие и точка → «saat N», 13 ячеек ────────
    (1099, "example_tr", "Kalkış saat 15:00'te",
     "Kalkış saat 15'te", "против 20 рядов с «saat N»; ошибкой не было"),
    (1963, "example_tr", "Antrenman saat 18:00'de başlıyor",
     "Antrenman saat 18'de başlıyor", "то же"),
    (2027, "example_tr", "Etkinlik saat 19:00'da başlıyor",
     "Etkinlik saat 19'da başlıyor", "то же"),
    (2076, "example_tr", "Ders saat 10:00'da başlıyor",
     "Ders saat 10'da başlıyor", "то же"),
    (2403, "example_tr", "Film 22:00'de bitiyor",
     "Film saat 22'de bitiyor", "то же, и добавлено «saat» как в остальных"),
    (2810, "example_tr", "Program saat 20:00'de",
     "Program saat 20'de", "то же"),
    (2904, "example_tr", "Yayın saat 20.00'de başlıyor",
     "Yayın saat 20'de başlıyor", "то же"),
    (9799, "example_tr", "Müzayede saat 15.00'te başlıyor",
     "Müzayede saat 15'te başlıyor", "то же"),
    (14002, "example_tr", "Basın toplantısı saat 14.00'te başlıyor",
     "Basın toplantısı saat 14'te başlıyor", "то же"),
    (14106, "example_tr", "Buluşma yarın saat 19:00'da",
     "Buluşma yarın saat 19'da", "то же"),
    (16105, "example_tr", "Toplantı yarın saat 18.00'de yapılacak",
     "Toplantı yarın saat 18'de yapılacak", "то же"),
    (17305, "example_tr", "Dönüş uçuşum önümüzdeki salı saat 14.00'te kalkıyor",
     "Dönüş uçuşum önümüzdeki salı saat 14'te kalkıyor", "то же"),
    (18865, "example_tr", "Hastanedeki ziyaret saati 15:00 ile 19:00 arasındadır",
     "Hastanedeki ziyaret saati 15 ile 19 arasındadır", "то же"),

    # ── ПОЛЬСКИЙ: двоеточие → словом, 2 ячейки ──────────────────
    (11788, "example_pl", "Kolację jemy razem o 19:00",
     "Kolację jemy razem o dziewiętnastej",
     "двоеточие против 43 рядов, где время написано словом"),
    (17356, "example_pl", "Godzina przyjazdu pociągu to 14:00",
     "Godzina przyjazdu pociągu to czternasta",
     "ПРАВЛЕНО РУКАМИ: нужен именительный, правило дало «czternastej»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
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
