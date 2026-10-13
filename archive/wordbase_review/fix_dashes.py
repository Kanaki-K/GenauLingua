"""
Дефис вместо тире — 120 ячеек.

Дефис в окружении пробелов не бывает верным ни в одном из шести языков: это
всегда тире. В базе он затесался прогонами, и видно это по тому, какой знак
в каждом языке преобладает:

    example_ru   275 длинных тире против  24 дефисов
    example_uk   188 против  65
    example_de    17 средних тире против   7
    example_en    22 против  15
    example_tr    15 против   6
    example_pl    13 против   3

Поэтому замена идёт по сложившейся в каждом языке норме, а не по одной
общей: в русском и украинском ставится длинное тире «—», в остальных
четырёх — среднее «–», потому что именно так в них уже написано
большинство строк.

ПОЧЕМУ ЗАМЕНА БЕЗОПАСНА. Ищется только дефис, с двух сторон окружённый
пробелами. Дефис внутри слова — «Не-а», «по-другому», «кто-нибудь»,
«Wi-Fi» — под шаблон не попадает и остаётся на месте. Скрипт проверяет это
на таких строках перед работой.

    python -m app.scripts.fix_dashes            # показать
    python -m app.scripts.fix_dashes --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

EM = "—"   # длинное тире: русский, украинский
EN = "–"   # среднее тире: немецкий, английский, турецкий, польский

# колонка → знак, принятый в этом языке
RULE = {
    "example_ru": EM,
    "example_uk": EM,
    "example_de": EN,
    "example_en": EN,
    "example_tr": EN,
    "example_pl": EN,
}

# Строки, где дефис внутри слова и трогать его нельзя
MUST_KEEP = [
    "Ты идёшь с нами? - Не-а, нет настроения",
    "Я сделаю это по-другому",
    "Кто-нибудь звонил",
    "Wi-Fi не работает",
    "Mein Vater ist Meister - er arbeitet dort",
]


def replace_spaced_hyphen(s: str, dash: str) -> str:
    return s.replace(" - ", f" {dash} ")


def selfcheck() -> None:
    print("=== самопроверка шаблона ===")
    bad = False
    for s in MUST_KEEP:
        out = replace_spaced_hyphen(s, EM)
        # Дефисы внутри слов должны остаться на месте
        inner_before = s.count("-") - s.count(" - ")
        inner_after = out.count("-") - out.count(" - ")
        if inner_before != inner_after:
            print(f"  ПРОВАЛ: внутренний дефис пострадал в {s!r} → {out!r}")
            bad = True
    if bad:
        sys.exit("шаблон ненадёжен — работать с ним нельзя")
    print("  дефис внутри слова шаблон не трогает\n")


def main() -> None:
    apply_mode = "--apply" in sys.argv
    selfcheck()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    planned: list[tuple[int, str, str, str]] = []

    with engine.connect() as conn:
        for col, dash in RULE.items():
            rows = conn.execute(text(
                f"SELECT id, {col} FROM words WHERE {col} LIKE :p"
            ), {"p": "% - %"}).all()
            for wid, value in rows:
                planned.append((wid, col, value, replace_spaced_hyphen(value, dash)))

    print(f"=== ячеек с дефисом вместо тире: {len(planned)} ===")
    by_col: dict[str, int] = {}
    for _, col, _, _ in planned:
        by_col[col] = by_col.get(col, 0) + 1
    for col, n in by_col.items():
        print(f"  {col}: {n} → знак «{RULE[col]}»")
    print()
    for wid, col, was, now in planned[:10]:
        print(f"  {wid} {col}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    if len(planned) > 10:
        print(f"  ... ещё {len(planned) - 10}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now in planned:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(planned)}")

    with engine.connect() as conn:
        left = 0
        for col in RULE:
            left += conn.execute(text(
                f"SELECT COUNT(*) FROM words WHERE {col} LIKE :p"
            ), {"p": "% - %"}).scalar()
        print(f"самопроверка: осталось ячеек с дефисом вместо тире {left}")


if __name__ == "__main__":
    main()
