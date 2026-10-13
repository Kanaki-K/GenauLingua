"""ВТОРОЙ ПРОХОД, блок 2 (ряды 201–400): правки, найденные глазами.

Пятнадцать ячеек против двадцати шести в блоке 1, и разница объяснимая:
в первом блоке сидели служебные слова — артикли, местоимения, формы
«ist/hat/war», — а именно там жила путаница «артикль против
числительного» и подмена фраз в коротких примерах. Здесь уже
полнозначная лексика, и переводы в целом крепче.

Настоящих подмен смысла в блоке две:

    verlassen  de «Ich verlasse die Stadt»  uk «Я їду з міста»
               покидать город и ехать из города — разное, и первый
               вариант перевода как раз «покидати»

    Typ        de «Der Typ ist sehr nett»   ru «Этот ТИП очень милый»
               «тип» в русском пренебрежительно, а «nett» — нет;
               первый вариант перевода «парень», и его взяли
               украинский, английский и польский

Остальное — время глагола (`nehmen` будущее вместо настоящего,
`gefallen` прошедшее вместо настоящего), потерянное усиление
(`kam` без «zu spät»), добавленное (`nett` с «çok») и выбор дальнего
варианта из своего же списка (`glauben` uk «вірю» там, где немецкое
«ich glaube» значит «думаю»).

Чего в блоке НЕ оказалось, хотя в блоке 1 было много: путаницы
«артикль/числительное». Ряды `eines`, `einige`, `einmal` переведены
верно — там числительное и по-немецки числительное.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── подменённый смысл ─────────────────────────────────────────
    (2948, "example_uk",
     "Я їду з міста",
     "Я покидаю місто",
     "«verlassen» это покидать; «їду з міста» это про способ передвижения"),
    (14899, "example_ru",
     "Этот тип очень милый",
     "Этот парень очень милый",
     "«тип» по-русски пренебрежительно, а «nett» нет; первый перевод «парень»"),
    (345, "example_uk",
     "Я вірю, що він прийде",
     "Я думаю, що він прийде",
     "«ich glaube» здесь значит «думаю», а не «верю»; так и в ru, tr, pl"),

    # ── время глагола ─────────────────────────────────────────────
    (649, "example_ru",
     "Я возьму газету",
     "Я беру газету",
     "будущее против «Ich nehme»; в uk, tr, pl и en настоящее"),
    (316, "example_tr",
     "Bunu çok beğendim",
     "Bunu çok beğeniyorum",
     "прошедшее против «Das gefällt mir sehr»"),

    # ── потерянное и добавленное слово ────────────────────────────
    (6221, "example_uk",
     "Вона прийшла на роботу пізно",
     "Вона прийшла на роботу занадто пізно",
     "потеряно «zu»: «zu spät» это слишком поздно"),
    (6221, "example_en",
     "She came to work late",
     "She came to work too late",
     "то же"),
    (651, "example_tr",
     "O çok kibar",
     "O kibar",
     "«çok» в эталоне нет: «Sie ist nett»"),
    (2206, "example_uk",
     "Цікавий спосіб це зробити",
     "Це цікавий спосіб це зробити",
     "потеряно «Das ist»; в русском и польском оно есть"),
    (13829, "example_uk",
     "Е-е, як тебе звати?",
     "Е-е, як тебе звати, нагадай?",
     "потеряно «nochmal»: в русском и английском оно есть"),

    # ── форма и управление ────────────────────────────────────────
    (13354, "example_ru",
     "Нас четыре человека",
     "Нас четверо",
     "«нас четыре человека» так не говорят; в uk и pl стоит собирательное"),
    (882, "example_uk",
     "Постав сумку тут",
     "Постав сумку сюди",
     "«hier hin» это направление: сюда, а не тут"),
    (202, "example_ru",
     "Тогда сделаем это как раз завтра",
     "Тогда сделаем это просто завтра",
     "модальное «eben» это «просто», а не «как раз»"),
    (2049, "example_ru",
     "Это же сумасшествие!",
     "Это же сумасшествие",
     "восклицательного знака нет ни в эталоне, ни в четырёх других языках"),
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
