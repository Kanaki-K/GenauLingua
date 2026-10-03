"""
Два разных апострофа в одной базе — 243 ячейки.

В базе живут оба начертания: прямой U+0027 и типографский U+2019.
Распределение показывает, что норма сложилась прямая, а типографский
затесался прогонами:

    example_en   1586 прямых против  135 типографских
    example_uk    474 против   57
    example_tr     50 против   44

Для турецкого и украинского прямой апостроф — это ещё и орфографическая
норма: «Almanya'da», «здоров'я». Для английского он просто преобладает
втрое.

ПОЧЕМУ ЗАМЕНА БЕЗОПАСНА. U+2019 бывает не только апострофом, но и
закрывающей одинарной кавычкой — и тогда менять его нельзя. Проверено:
открывающей кавычки U+2018 в базе нет ни в одной колонке, то есть парных
кавычек нет, и каждый U+2019 — апостроф. Скрипт проверяет это сам перед
работой и отказывается работать, если открывающая кавычка появится.

    python -m app.scripts.fix_apostrophes            # показать
    python -m app.scripts.fix_apostrophes --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

TYPOGRAPHIC = "’"
DIRECT = "'"
OPENING_QUOTE = "‘"

COLUMNS = ["word_de", "example_de"] + [
    f"{part}_{lang}"
    for part in ("translation", "example")
    for lang in ("en", "ru", "uk", "tr", "pl")
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    with engine.connect() as conn:
        # Самопроверка: парных кавычек быть не должно
        guards = []
        for col in COLUMNS:
            n = conn.execute(text(
                f"SELECT COUNT(*) FROM words WHERE {col} LIKE :p"
            ), {"p": f"%{OPENING_QUOTE}%"}).scalar()
            if n:
                guards.append((col, n))
        if guards:
            for col, n in guards:
                print(f"  ТРЕВОГА: в {col} есть открывающая кавычка, {n} ячеек")
            sys.exit("в базе появились парные кавычки — замена небезопасна")
        print("=== самопроверка: открывающих кавычек нет, "
              "каждый знак — апостроф ===\n")

        found: list[tuple[str, int]] = []
        samples: list[tuple[str, int, str]] = []
        for col in COLUMNS:
            n = conn.execute(text(
                f"SELECT COUNT(*) FROM words WHERE {col} LIKE :p"
            ), {"p": f"%{TYPOGRAPHIC}%"}).scalar()
            if not n:
                continue
            found.append((col, n))
            for row in conn.execute(text(
                f"SELECT id, {col} FROM words WHERE {col} LIKE :p LIMIT 2"
            ), {"p": f"%{TYPOGRAPHIC}%"}):
                samples.append((col, row[0], row[1]))

    total = sum(n for _, n in found)
    print(f"=== ячеек с типографским апострофом: {total} ===")
    for col, n in found:
        print(f"  {col}: {n}")
    print()
    for col, wid, val in samples:
        print(f"  {col} {wid}: {val!r}")
        print(f"      → {val.replace(TYPOGRAPHIC, DIRECT)!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for col, _ in found:
            conn.execute(text(
                f"UPDATE words SET {col} = replace({col}, :old, :new) "
                f"WHERE {col} LIKE :p"
            ), {"old": TYPOGRAPHIC, "new": DIRECT, "p": f"%{TYPOGRAPHIC}%"})
    print(f"\nприменено: {total}")

    with engine.connect() as conn:
        left = 0
        for col in COLUMNS:
            left += conn.execute(text(
                f"SELECT COUNT(*) FROM words WHERE {col} LIKE :p"
            ), {"p": f"%{TYPOGRAPHIC}%"}).scalar()
        print(f"самопроверка: осталось ячеек с типографским апострофом {left}")


if __name__ == "__main__":
    main()
