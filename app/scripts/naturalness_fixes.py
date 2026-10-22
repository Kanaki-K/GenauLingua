# -*- coding: utf-8 -*-
"""
Правки базы по своду естественности (2.3) — по номеру, со сверкой «было».

    python -m app.scripts.naturalness_fixes app/data/naturalness/batch_01.json
    python -m app.scripts.naturalness_fixes app/data/naturalness/batch_01.json --apply
    python -m app.scripts.rebuild_word_groups          # если в блоке есть замены

Файл блока:

    {"edits": [{"id": 10, "col": "translation_ru", "old": "…", "new": "…", "why": "…"}],
     "replace": [{"id": 2676, "by": 542, "lang": "de", "why": "…"}],
     "unreplace": [{"id": 18268, "why": "…"}]}

ПОЧЕМУ ПО НОМЕРУ И СО СВЕРКОЙ «БЫЛО» (`REVIEW_CRITERIA.md`, «Порядок работы
с правкой»). Прежние правки адресовались по немецкому слову — при 382
немецких словах с дублями это попадание в чужую строку. Номер плюс прежнее
значение: если в базе уже не то, что вычитывалось, правка не пишется поверх
чужой, а прогон останавливается — «пропущено» обязано быть 0.

`replace` — книжное слово выключается в пользу разговорного: указание
`word_lemma_overrides` с языком (миграция b5d7f9a1c3e4). Ничего не
удаляется; после пересборки групп прогресс по книжному сливается на
разговорное.

`unreplace` — снять указание, если строка снова самостоятельна (например,
форму переименовали в лемму, а старое «форма от …» осталось). После записи
указания проверяются целиком: ни одно не ведёт на выключенную строку —
иначе цепочка или круг (22.10: unterbringen B2↔C1 и bezweifeln B1↔C1
указывали друг на друга, и обе строки пропали у людей). Нашлось — откат.

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


_STOP = set("""der die das den dem des ein eine einen einem einer ist sind war bin bist hat habe hast haben
ich du er sie es wir ihr mir dir mich dich uns euch und oder aber nicht kein keine mit auf aus bei nach von zu
zum zur im in am an für über unter vor sehr noch schon auch nur mal bitte heute ja nein so wie was wer wo dann
denn doch man mein meine meinen meinem meiner dein deine deinen deinem deiner unser unsere""".split())


def _words(text_: str) -> set[str]:
    """Смысловые слова примера — без служебных, иначе всё «похоже» на всё."""
    import re
    return {w for w in re.findall(r"[a-zäöüß]+", (text_ or "").lower()) if len(w) > 2 and w not in _STOP}


def near_twins(conn, ready: list[dict]) -> list[str]:
    """
    Почти-повторы: новый немецкий пример по словам похож на пример другой
    строки (общих слов ≥ 75%). Не запрет — подсказка: точные совпадения
    запрещены в `_check`, а «Der Boden ist nass» рядом с «Pass auf, der
    Boden ist nass!» вычитка 21.10 пропустила дважды.
    """
    new = [(e["id"], e["new"]) for e in ready if e["col"] == "example_de"]
    if not new:
        return []
    rows = conn.execute(text("select id, example_de from words where example_de is not null")).all()
    others = [(wid, _words(x)) for wid, x in rows]
    found = []
    for wid, x in new:
        mine = _words(x)
        if len(mine) < 2:
            continue
        for oid, theirs in others:
            if oid == wid or not theirs:
                continue
            # Доля смысловых слов нового примера, которые уже есть в чужом
            common = len(mine & theirs)
            if common / len(mine) >= 0.8:
                found.append(f"{wid}: «{x}» похоже на пример слова {oid}")
                break
            # Шаблон: та же фраза, другое одно слово — «Mir tut das Ohr weh» /
            # «Mir tut der Magen weh» (идея 15 в review/2.3-ideas.md)
            if common >= 2 and len(mine - theirs) == 1 and len(theirs - mine) == 1:
                found.append(f"{wid}: «{x}» — шаблон примера слова {oid}")
                break
    return found


def _check(conn, block: dict) -> tuple[list[dict], list[str]]:
    """Что запишется и что не сходится. Не сходится хоть одно — писать нельзя."""
    ready, problems = [], []
    seen = set()
    for e in block.get("edits", []):
        wid, col = e.get("id"), e.get("col")
        if col not in EDITABLE:
            problems.append(f"{wid}: колонку {col!r} править нельзя")
            continue
        # Битая кодировка: UTF-8, прочитанный как cp1251 («ü» → «Гј»). 22.10 так испортились
        # 69 немецких примеров — находки читались через консоль Windows
        import re as _re
        # не «Рі»: так начинается укр. «Різдво»
        if _re.search(r"Г[јЁ¤¶–ћњ„џ©]|Р[°±µё]|С[Ѓ‚ѓ€]", e.get("new") or ""):
            problems.append(f"{wid}.{col}: битая кодировка в новом тексте")
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
            # ОДИН ПРИМЕР — ОДНОМУ СЛОВУ. Проверка всей базы 21.10 нашла 28
            # фраз у разных слов, две из них внесла сама вычитка: человек
            # видит ту же фразу на разных карточках и перестаёт её читать
            if col == "example_de":
                twin = conn.execute(text(
                    "select id from words where example_de = :x and id <> :id limit 1"),
                    {"x": e.get("new"), "id": wid}).scalar()
                if twin is not None:
                    problems.append(f"{wid}.example_de: такой пример уже у слова {twin}")
                    continue
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
    for r in block.get("unreplace", []):
        has = conn.execute(text("select count(*) from word_lemma_overrides where word_id = :id"),
                           {"id": r.get("id")}).scalar()
        if not has and not any(x.get("id") == r.get("id") for x in block.get("replace", [])):
            problems.append(f"снятие замены {r.get('id')}: указания нет")
        elif not (r.get("why") or "").strip():
            problems.append(f"снятие замены {r.get('id')}: нет «зачем»")
    return ready, problems


def broken_overrides(conn) -> list[str]:
    """Указания, которые ведут на выключенную строку: цепочка или круг."""
    rows = conn.execute(text(
        "select o.word_id, o.lemma_word_id, o2.lemma_word_id from word_lemma_overrides o "
        "join word_lemma_overrides o2 on o2.word_id = o.lemma_word_id order by 1")).all()
    return [f"{a} → {b} → {c}" for a, b, c in rows]


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
        unreplaces = block.get("unreplace", [])
        print(f"правок к записи {len(ready)}, замен {len(replaces)}, пропущено {len(problems)}")
        for p in problems:
            print("  ПРОПУЩЕНО", p)
        for w in near_twins(conn, ready):
            print("  ПОХОЖЕ", w)
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
        for r in unreplaces:
            conn.execute(text("delete from word_lemma_overrides where word_id = :id"), {"id": r["id"]})
        if replaces or unreplaces:
            broken = broken_overrides(conn)
            if broken:
                print(f"СТОП: {len(broken)} указаний ведут на выключенную строку — откат")
                for b in broken[:20]:
                    print("  ЦЕПОЧКА", b)
                raise SystemExit(1)

        # Самопроверка чтением обратно — в той же транзакции
        wrong = [e for e in ready if (conn.execute(
            text(f"select {e['col']}::text from words where id = :id"), {"id": e["id"]}
        ).scalar() or "") != e["new"]]
        if wrong:
            print(f"СТОП: {len(wrong)} правок не прочитались обратно — откат")
            raise SystemExit(1)
    print(f"записано правок {len(ready)}, замен {len(replaces)}, снято {len(unreplaces)}")
    if replaces or unreplaces:
        print("теперь: python -m app.scripts.rebuild_word_groups")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
