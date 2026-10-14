"""
Проверка качества переводов языковым суждением, а не правилами.

ЗАЧЕМ. Формальные проверки в этом проекте ловят много: гомоглифы, пропавшую
диакритику, точку в конце, слово, отсутствующее в примере. Но «естественно ли
это звучит», «то ли это слово», «не русизм ли в украинской колонке» правилами
не берётся. А именно это и есть качество знаний, за которым человек приходит.

Чтение глазами показало, чего стоит пропуск: в пятидесяти случайных рядах
нашлись «образжений» (такого слова нет), «тщательне розслідування» (русское
слово в украинском), «улики» вместо «докази», «sorgulyoruz» вместо
«sorguluyoruz», «çok ciddiye değil» вместо «çok ciddi değil». Формальные
проверки на всём этом молчат: буквы те, диакритика на месте, слово в примере
есть.

ЧТО СЧИТАЕТСЯ ДЕФЕКТОМ. Только то, что портит знания, — не вкусовщина.
Выдуманные слова, чужой язык в колонке, опечатки, неверный перевод, калька
вместо живой фразы, пример-перевод про другое. Сомнение трактуется в пользу
базы: лучше пропустить спорное, чем завалить отчёт шумом, в котором утонет
настоящее.

РАБОТА В ДВА ЭТАПА — скрипт ничего не правит сам:

    python -m app.scripts.quality_review run --batch --limit 4000
    python -m app.scripts.quality_review report --file quality_findings.jsonl
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("quality")

MODEL = "claude-opus-5"

# Слов в запросе. Меньше, чем в других прогонах: на каждое слово уходит шесть
# языков с переводами и примерами, это много входного текста.
#
# Было 25 при потолке 3000 — и первая же проба упёрлась в max_tokens, ответ
# обрезало на середине JSON. Дефектов в базе оказалось больше, чем я закладывал:
# на двадцати пяти рядах их набирается на несколько тысяч токенов. Поэтому
# порция вдвое меньше, а потолок втрое выше.
WORDS_PER_REQUEST = 12

# Выход — найденные дефекты с пояснением и предложением на каждый. Запас
# рассчитан на худший случай: все двенадцать рядов с замечаниями по трём
# языкам сразу.
MAX_TOKENS = 9000

LANGS = ("ru", "uk", "en", "tr", "pl")


def api_key() -> str:
    key = getattr(settings, "ANTHROPIC_API_KEY", None) or os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    env = Path(__file__).resolve().parents[2] / ".env.local"
    found = re.search(r"ANTHROPIC_API_KEY\s*=\s*(\S+)", env.read_text(encoding="utf-8"))
    if found:
        return found.group(1).strip().strip("\"'")
    sys.exit("не нашёл ANTHROPIC_API_KEY")


SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "description": "Только настоящие дефекты. Пусто — значит всё в порядке.",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "lang": {"type": "string", "enum": list(LANGS)},
                    "field": {"type": "string", "enum": ["translation", "example"]},
                    "kind": {
                        "type": "string",
                        "enum": [
                            "несуществующее слово",
                            "чужой язык в колонке",
                            "опечатка",
                            "неверный перевод",
                            "неестественная фраза",
                            "грамматическая ошибка",
                            "пример про другое",
                        ],
                    },
                    "problem": {"type": "string", "description": "В чём дело, одной фразой"},
                    "suggestion": {"type": "string", "description": "Как должно быть"},
                },
                "required": ["id", "lang", "field", "kind", "problem", "suggestion"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


SYSTEM_PROMPT = """\
Ты проверяешь словарную базу приложения, которое учит языкам. Человек учит по \
ней слова и верит тому, что видит. Твоя задача — найти то, что портит знания.

ЯЗЫКИ: русский, украинский, английский, турецкий, польский. Заголовок всегда \
немецкий, он эталон смысла.

ЧТО ИСКАТЬ

1. Несуществующее слово. «образжений» в украинском — такого слова нет, есть \
«ображений».
2. Чужой язык в колонке. В украинском «тщательне» вместо «ретельне», «улики» \
вместо «докази», «язвливість» вместо «ущипливість» — это русские слова, \
записанные как украинские. Ищи такое особенно внимательно: формальные \
проверки на этом молчат, буквы кириллические.
3. Опечатка. «sorgulyoruz» вместо «sorguluyoruz».
4. Неверный перевод. Немецкое слово значит не то, что написано в колонке. \
Или добавлено значение, которого у немецкого слова нет: у «Kran» это только \
подъёмный кран, водопроводный — «Wasserhahn», поэтому «tap» и «kran» лишние.
5. Грамматическая ошибка. «çok ciddiye değil» вместо «çok ciddi değil».
6. Неестественная фраза. Калька, которую живой носитель не скажет.
7. Пример про другое. Пример на языке перевода обязан переводить немецкий \
пример: те же лица, тот же предмет. «Der Konflikt eskaliert» и «Восени в неї \
загострюється алергія» — разные предложения, это дефект.

ЧЕГО НЕ ТРОГАТЬ

- Другая грамматическая форма слова в примере — это норма: «риба» → «люблю \
рибу».
- Перечисление нескольких значений через запятую — так устроена база.
- Отсутствие точки в конце — так принято здесь намеренно.
- Международные слова, совпадающие с немецким: «internet», «balkon», \
«chirurg» по-польски пишутся именно так.
- Стилистические предпочтения. Если фраза правильная, но ты сказал бы иначе — \
это не дефект.
- Пустая колонка — не дефект, её заполнят отдельно.

СОМНЕВАЕШЬСЯ — МОЛЧИ. Отчёт, забитый спорным, хуже пустого: в нём тонет \
настоящее. Лучше пропустить десять сомнительных, чем выдумать один дефект.

Отвечай строго по схеме. Нашёл чисто — верни пустой список findings.
"""


def chunked(items: list, size: int) -> Iterator[list]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def load_rows(limit: int | None, offset: int, level: str | None) -> list[dict]:
    cols = ["id", "word_de", "article", "pos", "level", "example_de"]
    for code in LANGS:
        cols += [f"translation_{code}", f"example_{code}"]
    sql = f"SELECT {', '.join(cols)} FROM words"
    params: dict[str, Any] = {}
    if level:
        sql += " WHERE level = :lvl"
        params["lvl"] = level
    sql += " ORDER BY id"
    if limit:
        sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        return [dict(r) for r in conn.execute(text(sql), params).mappings()]


def build_user_message(items: list[dict]) -> str:
    lines = ["Проверь эти ряды:", ""]
    for it in items:
        art = f"{it['article']} " if it.get("article") else ""
        lines.append(f"id: {it['id']}  [{it.get('pos') or '?'}, {it['level']}]")
        lines.append(f"  de: {art}{it['word_de']}")
        lines.append(f"      · {it.get('example_de') or '—'}")
        for code in LANGS:
            lines.append(f"  {code}: {it.get(f'translation_{code}') or '—'}")
            lines.append(f"      · {it.get(f'example_{code}') or '—'}")
        lines.append("")
    return "\n".join(lines)


def _request_params(items: list[dict]) -> dict:
    return {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": [
            {"type": "text", "text": SYSTEM_PROMPT,
             "cache_control": {"type": "ephemeral"}}
        ],
        "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}},
        "messages": [{"role": "user", "content": build_user_message(items)}],
    }


def _parse(message) -> tuple[list[dict], list[str]]:
    problems = []
    if getattr(message, "stop_reason", None) == "max_tokens":
        problems.append("ответ обрезан по max_tokens — часть дефектов потеряна")
    block = next((b.text for b in message.content if b.type == "text"), None)
    if not block:
        return [], problems + ["в ответе нет текстового блока"]
    try:
        return json.loads(block).get("findings", []), problems
    except json.JSONDecodeError as exc:
        return [], problems + [f"ответ не разобрался: {exc}"]


def cmd_run(args: argparse.Namespace) -> None:
    import anthropic

    rows = load_rows(args.limit, args.offset, args.level)
    batches = list(chunked(rows, args.chunk))
    reserved = len(batches) * MAX_TOKENS
    logger.info("слов %d, запросов %d, резерв %d токенов из квоты 2 000 000",
                len(rows), len(batches), reserved)
    if reserved > 2_000_000:
        logger.warning("резерв больше квоты — разбейте на части через --limit/--offset")
    if args.estimate_only:
        return

    out = Path(args.out)
    client = anthropic.Anthropic(api_key=api_key())

    if not args.batch:
        with out.open("a", encoding="utf-8") as fh:
            for items in batches:
                msg = client.messages.create(**_request_params(items))
                found, problems = _parse(msg)
                for p in problems:
                    logger.warning("%s", p)
                for f in found:
                    fh.write(json.dumps(f, ensure_ascii=False) + "\n")
                fh.flush()
                logger.info("дефектов в порции: %d", len(found))
        return

    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    requests = [
        Request(custom_id=f"chunk-{i:05d}",
                params=MessageCreateParamsNonStreaming(**_request_params(items)))
        for i, items in enumerate(batches)
    ]
    batch = client.messages.batches.create(requests=requests)
    logger.info("пакет создан: %s (%d запросов)", batch.id, len(requests))
    out.with_suffix(".batch").write_text(batch.id, encoding="utf-8")

    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        c = batch.request_counts
        logger.info("статус %s | в работе %d, готово %d, ошибок %d",
                    batch.processing_status, c.processing, c.succeeded, c.errored)
        time.sleep(30)

    written = 0
    with out.open("a", encoding="utf-8") as fh:
        for result in client.messages.batches.results(batch.id):
            if result.result.type != "succeeded":
                continue
            found, problems = _parse(result.result.message)
            for p in problems:
                logger.warning("%s: %s", result.custom_id, p)
            for f in found:
                fh.write(json.dumps(f, ensure_ascii=False) + "\n")
                written += 1
    logger.info("дефектов записано: %d → %s", written, out)


def cmd_report(args: argparse.Namespace) -> None:
    rows = [json.loads(l) for l in Path(args.file).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"=== дефектов: {len(rows)} ===\n")
    print("по языкам:", dict(Counter(r["lang"] for r in rows)))
    print("по видам: ", dict(Counter(r["kind"] for r in rows)))
    print("по полям: ", dict(Counter(r["field"] for r in rows)))
    print()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        words = {r[0]: (r[1], r[2]) for r in conn.execute(
            text("SELECT id, word_de, level FROM words WHERE id = ANY(:i)"),
            {"i": [r["id"] for r in rows]})}

    for kind in sorted({r["kind"] for r in rows}):
        items = [r for r in rows if r["kind"] == kind]
        print(f"--- {kind}: {len(items)} ---")
        for r in items[:args.show]:
            de, lvl = words.get(r["id"], ("?", "?"))
            print(f"  {r['id']:>6} [{lvl}] {de} / {r['lang']} {r['field']}")
            print(f"         {r['problem']}")
            print(f"         → {r['suggestion']}")
        if len(items) > args.show:
            print(f"  ... ещё {len(items) - args.show}")
        print()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="проверить базу")
    r.add_argument("--out", default="quality_findings.jsonl")
    r.add_argument("--limit", type=int)
    r.add_argument("--offset", type=int, default=0)
    r.add_argument("--level", choices=["A1", "A2", "B1", "B2", "C1", "C2"])
    r.add_argument("--chunk", type=int, default=WORDS_PER_REQUEST)
    r.add_argument("--batch", action="store_true")
    r.add_argument("--estimate-only", action="store_true")
    r.set_defaults(func=cmd_run)

    p = sub.add_parser("report", help="свести найденное")
    p.add_argument("--file", default="quality_findings.jsonl")
    p.add_argument("--show", type=int, default=12)
    p.set_defaults(func=cmd_report)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
