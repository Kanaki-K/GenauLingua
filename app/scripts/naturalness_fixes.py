# -*- coding: utf-8 -*-
"""
Правки базы по своду естественности (2.3) — по номеру, со сверкой «было».

    python -m app.scripts.naturalness_fixes app/data/naturalness/batch_01.json
    python -m app.scripts.naturalness_fixes app/data/naturalness/batch_01.json --apply
    python -m app.scripts.rebuild_word_groups          # если в блоке есть замены

Файл блока:

    {"edits": [{"id": 10, "col": "translation_ru", "old": "…", "new": "…", "why": "…"}],
     "replace": [{"id": 2676, "by": 542, "lang": "de", "why": "…"}]}

ПОЧЕМУ ПО НОМЕРУ И СО СВЕРКОЙ «БЫЛО» (`REVIEW_CRITERIA.md`, «Порядок работы
с правкой»). Прежние правки адресовались по немецкому слову — при 382
немецких словах с дублями это попадание в чужую строку. Номер плюс прежнее
значение: если в базе уже не то, что вычитывалось, правка не пишется поверх
чужой, а прогон останавливается — «пропущено» обязано быть 0.

`replace` — книжное слово выключается в пользу разговорного: указание
`word_lemma_overrides` с языком (миграция b5d7f9a1c3e4). Ничего не
удаляется; после пересборки групп прогресс по книжному сливается на
разговорное.

Звук перестраивается сам: клип в кэше сверяется с произносимым текстом.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text  # noqa: E402

from app.config import settings  # noqa: E402
from app.services.language_service import LANGUAGES  # noqa: E402

# Править можно только текст слова, переводы и примеры — не счётчики и не id
EDITABLE = {"word_de", "article", "level"} | {
    attr for lang in LANGUAGES.values() for attr in (lang.word_attr, lang.example_attr)
}


def _check(conn, block: dict) -> tuple[list[dict], list[str]]:
    """Что запишется и что не сходится. Не сходится хоть одно — писать нельзя."""
    ready, problems = [], []
    seen = set()
    for e in block.get("edits", []):
        wid, col = e.get("id"), e.get("col")
        if col not in EDITABLE:
            problems.append(f"{wid}: колонку {col!r} править нельзя")
            continue
        if (wid, col) in seen:
            problems.append(f"{wid}.{col}: правка повторяется в блоке")
            continue
        seen.add((wid, col))
        if not (e.get("why") or "").strip():
            problems.append(f"{wid}.{col}: нет «зачем»")
            continue
        current = conn.execute(text(f"select {col}::text from words where id = :id"),
                               {"id": wid}).first()
        if current is None:
            problems.append(f"{wid}: слова нет")
        elif (e.get("new") or "") == (current[0] or ""):
            continue                        # уже записано — повторный прогон
        elif (current[0] or "") != (e.get("old") or ""):
            problems.append(f"{wid}.{col}: в базе {current[0]!r}, ждали {e.get('old')!r}")
        else:
            ready.append(e)
    for r in block.get("replace", []):
        ids = [r.get("id"), r.get("by")]
        found = conn.execute(text("select count(*) from words where id = any(:ids)"),
                             {"ids": ids}).scalar()
        if found != 2 or ids[0] == ids[1]:
            problems.append(f"замена {ids}: слов нет или ссылка на себя")
        elif r.get("lang") not in LANGUAGES:
            problems.append(f"замена {ids}: язык {r.get('lang')!r} неизвестен")
        elif not (r.get("why") or "").strip():
            problems.append(f"замена {ids}: нет «зачем»")
    return ready, problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("block")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    block = json.loads(pathlib.Path(args.block).read_text(encoding="utf-8"))
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.begin() as conn:
        ready, problems = _check(conn, block)
        replaces = block.get("replace", [])
        print(f"правок к записи {len(ready)}, замен {len(replaces)}, пропущено {len(problems)}")
        for p in problems:
            print("  ПРОПУЩЕНО", p)
        for e in ready[:200]:
            print(f"  {e['id']:>6} {e['col']:<15} {e['old']!r} → {e['new']!r}")
        if problems:
            print("СТОП: «пропущено» должно быть 0 — в базе не то, что вычитывалось")
            return 1
        if not args.apply:
            print("\nвхолостую; записать — --apply")
            return 0

        for e in ready:
            conn.execute(text(f"update words set {e['col']} = :new where id = :id"),
                         {"new": e["new"], "id": e["id"]})
        for r in replaces:
            conn.execute(text(
                "insert into word_lemma_overrides (word_id, lemma_word_id, reason, lang, created_at) "
                "values (:id, :by, :why, :lang, now()) on conflict (word_id) do update set "
                "lemma_word_id = excluded.lemma_word_id, reason = excluded.reason, lang = excluded.lang"),
                {"id": r["id"], "by": r["by"], "why": f"2.3 замена: {r['why']}", "lang": r["lang"]})

        # Самопроверка чтением обратно — в той же транзакции
        wrong = [e for e in ready if (conn.execute(
            text(f"select {e['col']}::text from words where id = :id"), {"id": e["id"]}
        ).scalar() or "") != e["new"]]
        if wrong:
            print(f"СТОП: {len(wrong)} правок не прочитались обратно — откат")
            raise SystemExit(1)
    print(f"записано правок {len(ready)}, замен {len(replaces)}")
    if replaces:
        print("теперь: python -m app.scripts.rebuild_word_groups")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
