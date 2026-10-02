"""
Скобки в примерах: пояснения и варианты формы, попавшие в саму фразу.

Третий класс следов правки, найденный сплошным поиском после того, как
вычитка показала два предыдущих (стрелки и слеши). Всего девять строк.

Почему это дефект, а не мелочь. Пример должен читаться как живая фраза —
его и произносит голос. «The government is meeting. (or: The government is
in session.)» голос прочитает целиком, со словом «or» и скобками. А
«Обпік(ла) собі язик» человек просто не поймёт: это две формы сразу,
мужская и женская.

Три вида:

  1. Пояснение в скобках: «below the belt (an unfair blow)», «Goodbye (on
     the phone)». Пояснение полезно в словарной статье, но не во фразе.
  2. Вариант формы: «liebenswert(er)», «Обпік(ла)». Выбираю одну форму.
  3. Второй вариант фразы целиком: «(or: The government is in session.)».
     То же, что было со слешами.

Исключение. У `ihr/ihre` скобка несёт смысл: «Das ist ihre Tasche (von
meiner Schwester)» поясняет, чьё именно «ihre» — без этого немецкое
местоимение неоднозначно, и пример теряет назначение. Эту строку не трогаю,
но переписываю без скобок, чтобы смысл остался, а скобка ушла.

    python -m app.scripts.fix_paren_examples            # показать
    python -m app.scripts.fix_paren_examples --apply    # применить
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [

    # --- вариант формы в скобках --------------------------------------------
    (10868, "example_de",
     "Dein Sohn ist wirklich ein liebenswert(er) Junge, alle mögen ihn",
     "Dein Sohn ist wirklich ein liebenswerter Junge, alle mögen ihn",
     "вариант окончания в скобках"),
    (14951, "example_uk",
     "Обпік(ла) собі язик",
     "Я обпекла собі язик",
     "две формы рода сразу; немецкий пример от первого лица"),

    # --- пояснение в скобках -------------------------------------------------
    (12410, "example_en",
     "The boxer landed a punch below the belt (an unfair blow)",
     "The boxer landed a punch below the belt",
     "пояснение приклеено к фразе"),
    (2726, "example_en",
     "Delivery is free of charge (no postage)",
     "Delivery is free of charge",
     "пояснение приклеено к фразе"),
    (2635, "example_tr",
     "Bu gastronomik bir zirve (özel bir lezzet)",
     "Bu, mutfak sanatının bir başyapıtı",
     "пояснение в скобках, и фраза далека от немецкой"),
    (2645, "example_en",
     "I eat lactose-free (food)",
     "I eat lactose-free",
     "пояснение приклеено к фразе"),
    (13968, "example_en",
     "Goodbye (on the phone)",
     "Goodbye for now",
     "пояснение «по телефону» — это словарная помета, не часть фразы"),

    # --- второй вариант фразы -------------------------------------------------
    (2750, "example_en",
     "The government is meeting. (or: The government is in session.)",
     "The government is in session",
     "два варианта фразы разом, как было со слешами"),

    # --- скобка со смыслом: переписываю без скобки ----------------------------
    (428, "example_de",
     "Das ist ihre Tasche (von meiner Schwester)",
     "Das ist die Tasche meiner Schwester",
     "скобка поясняла, чьё «ihre»; смысл сохранён без неё"),
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

    # Самопроверка: скобок с пояснением в примерах остаться не должно
    cols = [f"example_{l}" for l in ("de", "ru", "uk", "en", "tr", "pl")]
    pat = re.compile(r"\([^)]{2,}\)")
    with engine.connect() as conn:
        rows = conn.execute(text(f"SELECT {', '.join(cols)} FROM words")).all()
    left = sum(1 for r in rows for v in r if v and pat.search(v))
    print(f"самопроверка: примеров со скобками осталось {left}")


if __name__ == "__main__":
    main()
