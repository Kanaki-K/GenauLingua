#!/usr/bin/env python3
"""
Записать переводы it, es, fr, cs из archive/new_langs/out в таблицу words.

Блок записывается только целиком и только без ошибок new_langs_check:
наполовину годный блок в базе потом не найти. Каждый ряд сверяется по
номеру И немецкому слову — номер без слова пропустил бы чужой ряд.
Повторный запуск ничего не меняет.

    python -m app.scripts.new_langs_apply            # вхолостую: что изменится
    python -m app.scripts.new_langs_apply --apply
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(os.environ.get("ENV_FILE", ".env"))

from app.scripts.new_langs_check import LANGS, check_file, load_jsonl  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent.parent / "archive" / "new_langs" / "out"


def main() -> None:
    from sqlalchemy import create_engine, text

    from app.config import settings

    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        db = {r.id: r for r in conn.execute(text(
            "SELECT id, word_de, "
            + ", ".join(f"translation_{c}, example_{c}" for c in LANGS)
            + " FROM words"
        ))}

    updates: list[dict] = []
    rejected: list[str] = []
    for path in sorted(OUT_DIR.glob("block_*.jsonl")):
        with contextlib.redirect_stdout(io.StringIO()):
            errors, _ = check_file(path)
        if errors:
            rejected.append(f"{path.name}: ошибок проверки {errors}")
            continue
        rows = load_jsonl(path)
        bad = [r["id"] for r in rows if r["id"] not in db or db[r["id"]].word_de != r["de"]]
        if bad:
            rejected.append(f"{path.name}: ряды не сходятся с базой по номеру и слову: {bad[:10]}")
            continue
        for r in rows:
            cur = db[r["id"]]
            new = {f"translation_{c}": r[c] for c in LANGS} | {f"example_{c}": r["ex_" + c] for c in LANGS}
            if any(getattr(cur, k) != v for k, v in new.items()):
                updates.append({"id": r["id"], **new})

    for line in rejected:
        print("НЕ ЗАПИСАН —", line)
    filled = sum(1 for r in db.values() if r.translation_it)
    print(f"блоков: {len(list(OUT_DIR.glob('block_*.jsonl')))}, отклонено {len(rejected)}; "
          f"рядов к записи: {len(updates)}; в базе заполнено сейчас: {filled} из {len(db)}")

    if not args.apply or not updates:
        if updates:
            print("вхолостую; запись — с --apply")
        return

    cols = [f"translation_{c}" for c in LANGS] + [f"example_{c}" for c in LANGS]
    sql = text("UPDATE words SET " + ", ".join(f"{c} = :{c}" for c in cols) + " WHERE id = :id")
    with engine.begin() as conn:
        conn.execute(sql, updates)
    print(f"записано рядов: {len(updates)}")


if __name__ == "__main__":
    main()
