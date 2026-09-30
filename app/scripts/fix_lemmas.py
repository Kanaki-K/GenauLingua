#!/usr/bin/env python3
"""
Привести к словарной форме слова, у которых в базе стоит форма слова.

Найдено прогоном переводов: 328 слов, из них 227 уже показывались людям, и
кучно они на A1 — там, где учеников больше всего. Человек учит «jede» как
отдельное слово, хотя это форма от «jeder»; учит «soll», хотя лемма «sollen».

Отдельный прогон, потому что он несравнимо дешевле пересборки переводов: на
выходе одно слово, а не шесть переводов со значениями.

ОСТОРОЖНО СО СТОЛКНОВЕНИЯМИ. Лемма может уже быть в базе на том же уровне,
и тогда UPDATE упёрся бы в уникальность (word_de, level). Такие случаи не
применяются, а выписываются отдельно: это настоящие дубли, и решать, какую
строку оставить, должен человек — на одной из них может быть чужой прогресс.

    python -m app.scripts.fix_lemmas collect --out lemma_defects.jsonl
    python -m app.scripts.fix_lemmas propose --in lemma_defects.jsonl
    python -m app.scripts.fix_lemmas apply --file lemma_fixes.jsonl --dry-run
    python -m app.scripts.fix_lemmas apply --file lemma_fixes.jsonl
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(os.environ.get("ENV_FILE", ".env"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fix-lemmas")

MODEL = "claude-opus-5"
WORDS_PER_REQUEST = 40
MAX_TOKENS = 6000

# Части речи, которые есть в перечислении базы. Список берётся из кода, а не
# вписывается: иначе он разошёлся бы со схемой, и применение падало бы целиком.
def _valid_pos() -> frozenset[str]:
    from app.database.enums import PartOfSpeech

    return frozenset(p.name for p in PartOfSpeech)


VALID_POS = _valid_pos()


SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "words": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "is_lemma": {
                        "type": "boolean",
                        "description": (
                            "Слово уже в словарной форме. Тогда lemma повторяет "
                            "его, а article и pos остаются прежними."
                        ),
                    },
                    "lemma": {
                        "type": "string",
                        "description": (
                            "Словарная форма. Для существительного — именительный "
                            "падеж единственного числа с заглавной буквы, для "
                            "глагола — инфинитив, для прилагательного — краткая "
                            "несклонённая форма."
                        ),
                    },
                    "article": {
                        "anyOf": [
                            {"type": "string", "enum": ["der", "die", "das"]},
                            {"type": "null"},
                        ],
                        "description": "Артикль леммы, если это существительное",
                    },
                    # Значения ровно те, что есть в перечислении базы. Прежде
                    # здесь стоял NUMERAL, которого в базе нет, и применение
                    # падало целиком на первом же числительном.
                    "pos": {
                        "type": "string",
                        "enum": ["NOUN", "VERB", "ADJECTIVE", "ADVERB", "PHRASE",
                                 "PRONOUN", "PREPOSITION", "CONJUNCTION", "OTHER"],
                        "description": "Часть речи леммы: у формы она может отличаться",
                    },
                    "note": {
                        "type": ["string", "null"],
                        "description": "Короткое пояснение, если случай непростой",
                    },
                },
                "required": ["id", "is_lemma", "lemma", "article", "pos", "note"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["words"],
    "additionalProperties": False,
}


SYSTEM_PROMPT = """\
Ты приводишь немецкие слова к словарной форме для словаря приложения.

Каждое присланное слово помечено как возможная форма слова, а не лемма. \
Твоя задача — дать словарную форму.

ЧТО СЧИТАЕТСЯ СЛОВАРНОЙ ФОРМОЙ
- существительное: именительный падеж единственного числа, с заглавной буквы \
(«Eier» → «Ei», «Schwierigkeiten» → «Schwierigkeit»);
- глагол: инфинитив («soll» → «sollen», «verstanden» → «verstehen», \
«gibt» → «geben»);
- прилагательное: краткая несклонённая форма («echte» → «echt»);
- местоимение и определитель: основная форма («diesem» → «dieser», \
«jede» → «jeder», «seinem» → «sein»).

ЧАСТЬ РЕЧИ МОЖЕТ ИЗМЕНИТЬСЯ. «verstanden» размечено как прилагательное, но \
это причастие от глагола «verstehen» — pos должен стать VERB. Указывай часть \
речи леммы, а не присланной формы.

АРТИКЛЬ. Для существительного дай артикль леммы: у множественного числа он \
всегда «die», а у единственного может быть любым («Eier» это «die», но лемма \
«das Ei»). Для остальных частей речи — null.

ЕСЛИ СЛОВО УЖЕ ЛЕММА, поставь is_lemma = true и повтори его в lemma без \
изменений. Это нормальный ответ: пометка могла быть ошибочной.

Не выдумывай слов. Если присланное испорчено или не является немецким словом, \
поставь is_lemma = false, в lemma повтори присланное как есть и объясни в note.

Отвечай строго по схеме, по одному объекту на каждое слово, с тем же id.
"""


def chunked(items: list, size: int) -> Iterator[list]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def cmd_collect(args: argparse.Namespace) -> None:
    """
    Собрать помеченные слова из файлов прежних прогонов.

    Источники два: пересборка переводов сообщает lemma_ok = false, а прогон
    примеров отдельно сообщает, что пример написать нельзя, потому что слово
    не лемма. Наборы пересекаются, поэтому объединяются по id.
    """
    from sqlalchemy import create_engine, text

    from app.config import settings

    notes: dict[int, str] = {}

    for name in args.sources:
        path = Path(name)
        if not path.exists():
            logger.warning("нет файла %s — пропущен", path)
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            wid = row.get("id")
            if wid is None:
                continue
            note = row.get("note") or row.get("lemma_problem") or ""
            # Из пересборки переводов берём только помеченные как не-лемма
            if "lemma_ok" in row and row.get("lemma_ok") is not False:
                continue
            notes.setdefault(wid, note)

    if not notes:
        logger.error("помеченных слов не найдено")
        return

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, word_de, article, pos::text AS pos, level::text AS level,
                   translation_ru, example_de, times_shown
            FROM words WHERE id = ANY(:ids)
        """), {"ids": list(notes)}).mappings().all()

    out_path = Path(args.out)
    with out_path.open("w", encoding="utf-8") as out:
        for row in rows:
            item = dict(row)
            item["note"] = notes.get(row["id"], "")
            out.write(json.dumps(item, ensure_ascii=False) + "\n")

    shown = sum(1 for r in rows if r["times_shown"])
    logger.info("собрано %d слов → %s (уже показывались людям: %d)",
                len(rows), out_path, shown)


def build_user_message(items: list[dict]) -> str:
    lines = ["Слова, которые нужно привести к словарной форме:", ""]
    for item in items:
        lines.append(f"id: {item['id']}")
        lines.append(f"  слово: {item['word_de']}")
        lines.append(f"  часть речи в базе: {item['pos']}")
        if item.get("article"):
            lines.append(f"  артикль в базе: {item['article']}")
        lines.append(f"  уровень: {item['level']}")
        if item.get("translation_ru"):
            lines.append(f"  перевод: {item['translation_ru']}")
        if item.get("example_de"):
            lines.append(f"  пример: {item['example_de']}")
        if item.get("note"):
            lines.append(f"  замечание прошлого прогона: {item['note']}")
        lines.append("")
    return "\n".join(lines)


def cmd_propose(args: argparse.Namespace) -> None:
    import anthropic

    items = [
        json.loads(line)
        for line in Path(args.input).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if args.limit:
        items = items[:args.limit]
    if not items:
        logger.error("в файле нет записей")
        return

    out_path = Path(args.out)
    already: set[int] = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    already.add(json.loads(line)["id"])
                except (json.JSONDecodeError, KeyError):
                    continue
        if already:
            logger.info("уже есть %d — пропускаю", len(already))
            items = [i for i in items if i["id"] not in already]

    if not items:
        logger.info("всё обработано")
        return

    batches = list(chunked(items, args.chunk))
    logger.info("слов %d, запросов %d", len(items), len(batches))

    client = anthropic.Anthropic()
    done = 0
    with out_path.open("a", encoding="utf-8") as out:
        for batch in batches:
            expected = {i["id"] for i in batch}
            try:
                message = client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=[{"type": "text", "text": SYSTEM_PROMPT,
                             "cache_control": {"type": "ephemeral"}}],
                    output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
                    messages=[{"role": "user", "content": build_user_message(batch)}],
                )
            except Exception as exc:
                logger.error("запрос упал: %s", exc)
                continue

            block = next((b.text for b in message.content if b.type == "text"), None)
            if not block:
                logger.warning("в ответе нет текста")
                continue
            try:
                payload = json.loads(block)
            except json.JSONDecodeError as exc:
                logger.warning("ответ не разобрался: %s", exc)
                continue

            results = [r for r in payload.get("words", []) if r.get("id") in expected]
            missing = expected - {r["id"] for r in results}
            if missing:
                logger.warning("пропущены id: %s", sorted(missing)[:5])

            for result in results:
                out.write(json.dumps(result, ensure_ascii=False) + "\n")
            out.flush()
            done += len(results)
            logger.info("готово %d | выход %d токенов", done, message.usage.output_tokens)


def cmd_apply(args: argparse.Namespace) -> None:
    from sqlalchemy import create_engine, text

    from app.config import settings

    proposals = [
        json.loads(line)
        for line in Path(args.file).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    logger.info("предложений: %d", len(proposals))

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        current = {r["id"]: dict(r) for r in conn.execute(text(
            "SELECT id, word_de, article, pos::text AS pos, level::text AS level, "
            "times_shown FROM words WHERE id = ANY(:ids)"),
            {"ids": [p["id"] for p in proposals]}).mappings()}
        # Карта «слово на уровне» → id: по ней ищутся столкновения
        occupied = {
            (r["word_de"].lower(), r["level"]): r["id"]
            for r in conn.execute(text(
                "SELECT id, word_de, level::text AS level FROM words")).mappings()
        }

    updates: list[dict] = []
    unchanged = 0
    collisions: list[dict] = []
    skipped: list[dict] = []

    for p in proposals:
        row = current.get(p["id"])
        if row is None:
            continue

        lemma = (p.get("lemma") or "").strip()
        if not lemma:
            skipped.append({**p, "reason": "пустая лемма"})
            continue

        if p.get("is_lemma") or lemma.lower() == row["word_de"].lower():
            # Пометка была ошибочной — слово и так лемма
            unchanged += 1
            continue

        # Лемма уже занята на этом уровне: это настоящий дубль, и решать,
        # какую строку оставить, должен человек — на одной может быть прогресс
        other = occupied.get((lemma.lower(), row["level"]))
        if other is not None and other != p["id"]:
            collisions.append({
                **p, "current": row["word_de"], "level": row["level"],
                "occupied_by": other, "times_shown": row["times_shown"],
            })
            continue

        # Часть речи проверяется по перечислению базы: неизвестное значение
        # уронило бы весь прогон одним оператором UPDATE, а не одну строку
        pos = p.get("pos") or row["pos"]
        if pos not in VALID_POS:
            logger.warning("часть речи %r не из перечисления, оставляю прежнюю "
                           "для %r", pos, row["word_de"])
            pos = row["pos"]

        updates.append({
            "id": p["id"],
            "word_de": lemma,
            "article": p.get("article"),
            "pos": pos,
        })

    logger.info("к применению %d, уже леммы %d, столкновений %d, пропущено %d",
                len(updates), unchanged, len(collisions), len(skipped))

    for name, items in (("collisions", collisions), ("skipped", skipped)):
        if items:
            path = Path(args.file).with_name(Path(args.file).stem + f"_{name}.jsonl")
            with path.open("w", encoding="utf-8") as fh:
                for item in items:
                    fh.write(json.dumps(item, ensure_ascii=False) + "\n")
            logger.warning("%s: %d → %s", name, len(items), path)

    if args.dry_run:
        print(f"\n--dry-run: применилось бы {len(updates)}\n")
        for u in updates[:20]:
            was = current[u["id"]]
            article = f"{u['article']} " if u["article"] else ""
            print(f"  {was['word_de']!r:<24} → {article}{u['word_de']!r}"
                  f"   [{was['pos']} → {u['pos']}]  показов {was['times_shown']}")
        if len(updates) > 20:
            print(f"  ... ещё {len(updates) - 20}")
        print()
        return

    if not updates:
        logger.info("применять нечего")
        return

    with engine.begin() as conn:
        for chunk in chunked(updates, 200):
            conn.execute(text("""
                UPDATE words SET
                    word_de = :word_de,
                    article = :article,
                    pos = CAST(:pos AS partofspeech)
                WHERE id = :id
            """), chunk)

    logger.info("приведено к словарной форме: %d", len(updates))
    logger.warning(
        "ОБЯЗАТЕЛЬНО после этого:\n"
        "  1. python -m app.scripts.rebuild_word_groups  — немецкие слова "
        "изменились, схлопывание дублей считается по ним\n"
        "  2. python -m app.scripts.tts_synthesize       — озвучка этих слов "
        "устарела, нужен новый клип\n"
        "  3. python -m app.scripts.tts_trim_store       — новые клипы приходят "
        "необрезанными\n"
        "Прогресс пользователей не затронут: он привязан к id, а id не менялись."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    c = sub.add_parser("collect", help="собрать помеченные слова из прежних прогонов")
    c.add_argument("--sources", nargs="+", default=[
        "wordbase_a1a2_needs_review.jsonl",
        "example_fixes_rejected.jsonl",
    ])
    c.add_argument("--out", default="lemma_defects.jsonl")
    c.set_defaults(func=cmd_collect)

    p = sub.add_parser("propose", help="получить словарные формы")
    p.add_argument("--in", dest="input", default="lemma_defects.jsonl")
    p.add_argument("--out", default="lemma_fixes.jsonl")
    p.add_argument("--limit", type=int)
    p.add_argument("--chunk", type=int, default=WORDS_PER_REQUEST)
    p.set_defaults(func=cmd_propose)

    a = sub.add_parser("apply", help="применить словарные формы")
    a.add_argument("--file", required=True)
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
