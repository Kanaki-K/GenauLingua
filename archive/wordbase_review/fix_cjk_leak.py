"""
Класс: китайские иероглифы внутри русских ячеек.

«Помощница врача很 приветлива», «ограниченный, небольшой, 限»,
«требовать, 需要», «существо, 创творение», «упорядоченный, налаженный,
урегулированный, 規регулируемый». Пять ячеек, все русские — похоже на
один прогон перевода, куда подмешался чужой язык.

ЭТОТ КЛАСС БЫЛ ИЗВЕСТЕН И НИКОГДА НЕ ПРОВЕРЯЛСЯ СПЛОШНЯКОМ. В
REVIEW_CRITERIA, раздел 3, он записан с примером: «чужой алфавит внутри
слова: „коноtа“, „діш kürü“, „творець, 創創“». То есть его нашли глазами
ещё в первом круге, исправили тот случай — и не прошли поиском по
символам. За это время прочитано 2900 рядов, и четыре из пяти ячеек
лежали в непрочитанной части, где так и остались бы.

Вывод для журнала: **каждый класс из критериев обязан быть закрыт
сплошным поиском, а не только в том ряду, где попался глазами.**

Поиск шёл по диапазонам: китайский, японский, корейский, арабский,
иврит, греческий, тайский. Нашлись только китайские.

    python -m app.scripts.fix_cjk_leak            # показать
    python -m app.scripts.fix_cjk_leak --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

_CJK = "китайский иероглиф внутри русской ячейки"

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [
    (869, "example_ru", "Помощница врача很 приветлива",
     "Помощница врача приветлива", _CJK),
    (7372, "translation_ru", "ограниченный, небольшой, 限",
     "ограниченный, небольшой", _CJK),
    (7712, "translation_ru", "требовать, 需要",
     "требовать, нуждаться в", _CJK),
    (15570, "translation_ru", "существо, 创творение, создание",
     "существо, творение, создание", _CJK),
    (16106, "translation_ru",
     "упорядоченный, налаженный, урегулированный, 規регулируемый",
     "упорядоченный, налаженный, урегулированный, регулируемый", _CJK),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
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
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
