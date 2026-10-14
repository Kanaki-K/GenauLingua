"""Правки по замеру ранних блоков (срезы 301–330, 1801–1830, 3901–3930).

Это НЕ блок обзора. Это три срезa по 30 рядов, взятые из блоков 4, 17 и
28, чтобы ответить числом на вопрос «насколько ранние блоки хуже
поздних». Замер дал 19 рядов с замечанием из 90 (21%), см. журнал.

Найденное надо исправить — иначе замер превращается в список известных
и оставленных дефектов. Здесь ровно эти 19 рядов и ничего больше:
остальные 5910 рядов ранней части не перечитаны, и их состояние
по-прежнему оценка, а не факт.

Самая показательная находка — ряд 13351, `fünf`:

    de  Ich habe fünf Äpfel      (у меня пять яблок)
    pl  Kupiłem pięć bułek       (я купил пять булок)

Фраза подменена целиком, и гейт на числа её не видит: оба числительных
написаны словами, а такие ячейки он пропускает сознательно.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── срез 301–330 (блок 4) ─────────────────────────────────────
    (1874, "example_uk",
     "Навіть моя бабуся має телефон",
     "Навіть моя бабуся має мобільний телефон",
     "«ein Handy» это мобильный; русский и польский его держат"),
    (13346, "example_pl",
     "Nikogo nie ma w domu",
     "Nikogo tu nie ma w domu",
     "потеряно «hier»"),
    (871, "example_ru",
     "Уже слишком поздно",
     "Слишком поздно",
     "«уже» в эталоне нет: «Es ist zu spät»"),
    (6241, "translation_uk",
     "досить, доволі, дуже",
     "досить, доволі, відносно",
     "«дуже» это «sehr», а ziemlich — «довольно»"),
    (8735, "example_en",
     "I really enjoy my job",
     "I enjoy my job",
     "«really» в эталоне нет"),
    (8735, "example_tr",
     "İşim eğlenceli",
     "İşim bana keyif veriyor",
     "«eğlenceli» это забавный; «macht mir Spaß» — доставляет удовольствие"),
    (6245, "example_pl",
     "Weź ze sobą tę książkę",
     "Weź ze sobą tę książkę!",
     "восклицательный знак есть во всех пяти остальных языках"),
    (14896, "example_pl",
     "Mama gotuje obiad",
     "Mama gotuje jedzenie",
     "«obiad» это обед; в эталоне «das Essen» — еда"),
    (13351, "example_pl",
     "Kupiłem pięć bułek",
     "Mam pięć jabłek",
     "фраза подменена целиком: «я купил пять булок» вместо «у меня пять яблок»"),

    # ── срез 1801–1830 (блок 17) ──────────────────────────────────
    (18657, "example_tr",
     "Seni sonsuz zamandır bekliyorum",
     "Seni asırlardır bekliyorum",
     "«sonsuz zamandır» так не говорят; идиома — asırlardır"),
    (1915, "example_uk",
     "Є перешкода",
     "Сталася несправність",
     "«перешкода» это третий вариант перевода; первый — «несправність»"),
    (1200, "example_en",
     "Please show your ID",
     "Please show me your ID",
     "потеряно «mir»"),
    (1200, "example_tr",
     "Lütfen kimliğini göster",
     "Lütfen kimliğini bana göster",
     "то же"),
    (1829, "example_ru",
     "Вывеска большая",
     "Табличка большая",
     "в переводе первым «табличка», и так же в четырёх остальных языках"),
    (6652, "example_en",
     "Turn around",
     "Turn around!",
     "восклицательный знак есть во всех пяти остальных языках"),

    # ── срез 3901–3930 (блок 28) ──────────────────────────────────
    (7144, "example_tr",
     "Dün hava tamamen güzeldi, mükemmeldi",
     "Dün hava adeta harikaydı, kusursuzdu",
     "«tamamen» это «полностью», а geradezu — «прямо-таки»"),
    (9787, "example_uk",
     "Давай обміняємось: ти даси мені свій сендвіч, а я дам тобі свої чипси",
     "Давай обміняємось: ти даси мені свій сендвіч, а я дам тобі свої чіпси",
     "«чипси» написано по-русски; в базе принято «чіпси»"),
    (1166, "example_uk",
     "Бідність — серйозна проблема",
     "Бідність — велика проблема",
     "«großes» это большая; «серйозна» в эталоне нет"),
    (7146, "example_pl",
     "Silnik buczy, kiedy samochód jedzie",
     "Silnik buczy, kiedy samochód pracuje",
     "«läuft» о моторе это работает, а не едет"),
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
            print(f"  зачем: {why}")
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
