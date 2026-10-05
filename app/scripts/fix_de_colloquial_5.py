"""
Разговорное усечение в немецком эталоне, пятый проход.

Примета расширена после блока 40: добавлена основа `check` и новая
шестая примета — проглоченное `es`, приклеенное к глаголу (`ich mags`,
`ich habs`). После расширения сторож показал ещё два ряда.

Это пятый раз, когда класс «закрывался». Счёт проходов: 88, 15, 7, 7, 2.
Каждый раз примету расширяли по тому, что попалось глазами в очередном
блоке, — ещё одно подтверждение, что «примета показала 0» не закрывает
класс, а лишь говорит «того, что она умеет видеть, больше нет».

Переводы не трогаем: смысл не двигается, двигается только форма.

    python -m app.scripts.fix_de_colloquial_5            # показать
    python -m app.scripts.fix_de_colloquial_5 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [
    (2376, "example_de", "Ich check mich im Hotel ein",
     "Ich checke mich im Hotel ein",
     "усечённое «checke»"),
    (7934, "example_de", "Das Essen war sagenhaft gut, ich habs geliebt",
     "Das Essen war sagenhaft gut, ich habe es geliebt",
     "«habs» вместо «habe es»"),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
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
