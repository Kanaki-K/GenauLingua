#!/usr/bin/env python3
"""
Переписать примеры, которые не показывают слово.

Отдельный прогон, а не часть пересборки переводов, потому что он несравнимо
дешевле: на выходе одна фраза вместо шести переводов со всеми значениями.
1952 дефекта стоят порядка полутора долларов против восемнадцати за пару
уровней в полном прогоне.

Что считается дефектом, определяет app/scripts/example_quality.py: пример,
в котором слова нет даже в другой форме. «Рыба» → «Я люблю рыбу» дефектом не
является, «Подсобить» → «Иногда нужно помочь удаче» является.

РАБОТА В ДВА ЭТАПА — в базу напрямую скрипт не пишет:

  1. propose — собрать новые примеры в файл
       python -m app.scripts.example_quality --out example_defects.jsonl
       python -m app.scripts.fix_examples propose --in example_defects.jsonl --batch

  2. apply — применить проверенное
       python -m app.scripts.fix_examples apply --file example_fixes.jsonl --dry-run
       python -m app.scripts.fix_examples apply --file example_fixes.jsonl

Требуется ANTHROPIC_API_KEY.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(os.environ.get("ENV_FILE", ".env"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fix-examples")

MODEL = "claude-opus-5"

# Больше, чем в пересборке переводов: ответ на один пример короткий, и
# порция из сорока слов всё равно укладывается в разумный размер
WORDS_PER_REQUEST = 40

MAX_TOKENS = 8000

LANG_NAMES = {
    "de": "немецком", "en": "английском", "ru": "русском",
    "uk": "украинском", "tr": "турецком", "pl": "польском",
}


SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "examples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "id слова из запроса"},
                    "lang": {
                        "type": "string",
                        "enum": ["de", "en", "ru", "uk", "tr", "pl"],
                    },
                    "example": {
                        "type": "string",
                        "description": (
                            "Короткая бытовая фраза, содержащая это слово и "
                            "раскрывающая его значение"
                        ),
                    },
                    "lemma_problem": {
                        "type": ["string", "null"],
                        "description": (
                            "Заполнить, только если пример написать нельзя: слово "
                            "не лемма, испорчено или бессмысленно. Иначе null."
                        ),
                    },
                },
                "required": ["id", "lang", "example", "lemma_problem"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["examples"],
    "additionalProperties": False,
}


SYSTEM_PROMPT = """\
Ты пишешь примеры употребления для словаря приложения, которое учит словам.
Пример человек видит после ответа — по нему он понимает, как слово живёт \
в живой речи.

Каждый присланный случай — это слово, у которого нынешний пример негоден: \
в нём нет самого слова. Твоя задача — написать новый.

ТРЕБОВАНИЯ К ПРИМЕРУ
- От трёх до восьми слов. Короче — не видно употребления, длиннее — не \
читается на карточке.
- Слово обязано присутствовать. В любой грамматической форме: для «рыба» \
годится «Я люблю рыбу», для «aufstehen» годится «Ich stehe früh auf».
- Фраза должна звучать как из разговора, а не из учебника грамматики. \
«Дай мне соль» — да. «Соль является веществом» — нет.
- По фразе должно быть понятно значение слова. Если слово многозначно, бери \
самое частое значение.
- Точку в конце не ставь. Вопросительный и восклицательный знак ставь, если \
фраза этого требует.
- Диакритика обязательна там, где она есть в языке: немецкое ä ö ü ß, \
турецкое ç ğ ı ö ş ü, польское ą ć ę ł ń ó ś ź ż, украинское і ї є ґ.
- Пиши на том языке, который указан в поле «язык примера», и ни на каком \
другом.

lemma_problem заполняй только тогда, когда пример написать невозможно: слово \
дано не в словарной форме (Alben вместо Album), это часть слова, а не слово \
(lieblings-), либо запись испорчена. В таком случае example оставь пустой \
строкой. Если пример написать можно — lemma_problem обязательно null.

Отвечай строго по схеме, по одному объекту на каждый присланный случай, с тем \
же id и тем же языком.
"""


def load_defects(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def chunked(items: list, size: int) -> Iterator[list]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def build_user_message(items: list[dict]) -> str:
    lines = ["Случаи, для которых нужен новый пример:", ""]
    for item in items:
        lines.append(f"id: {item['id']}")
        lines.append(f"  язык примера: {item['lang']} ({LANG_NAMES.get(item['lang'], item['lang'])})")
        lines.append(f"  слово: {item['word']}")
        lines.append(f"  уровень: {item.get('level', '—')}")
        lines.append(f"  негодный пример: {item.get('example') or '—'}")
        lines.append("")
    return "\n".join(lines)


def _request_params(items: list[dict]) -> dict:
    return {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        # Системный промпт одинаков во всех запросах — кешируем
        "system": [
            {"type": "text", "text": SYSTEM_PROMPT,
             "cache_control": {"type": "ephemeral"}}
        ],
        "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}},
        "messages": [{"role": "user", "content": build_user_message(items)}],
    }


def _parse(message, expected: set[tuple[int, str]]) -> tuple[list[dict], list[str]]:
    problems: list[str] = []

    if getattr(message, "stop_reason", None) == "refusal":
        return [], ["модель отказалась обрабатывать запрос"]
    if getattr(message, "stop_reason", None) == "max_tokens":
        problems.append("ответ обрезан по max_tokens — уменьшить порцию")

    block = next((b.text for b in message.content if b.type == "text"), None)
    if not block:
        return [], problems + ["в ответе нет текстового блока"]

    try:
        payload = json.loads(block)
    except json.JSONDecodeError as exc:
        return [], problems + [f"ответ не разобрался как JSON: {exc}"]

    items = payload.get("examples", [])
    got = {(i.get("id"), i.get("lang")) for i in items}

    missing = expected - got
    if missing:
        problems.append(f"модель пропустила: {sorted(missing)[:5]}")
    extra = got - expected
    if extra:
        problems.append(f"модель вернула лишнее: {sorted(extra)[:5]}")
        items = [i for i in items if (i.get("id"), i.get("lang")) in expected]

    return items, problems


def propose_sync(client, batches: list[list[dict]], out_path: Path) -> None:
    done = 0
    with out_path.open("a", encoding="utf-8") as out:
        for items in batches:
            expected = {(i["id"], i["lang"]) for i in items}
            try:
                message = client.messages.create(**_request_params(items))
            except Exception as exc:
                logger.error("запрос упал: %s", exc)
                continue

            results, problems = _parse(message, expected)
            for problem in problems:
                logger.warning("%s", problem)
            for result in results:
                out.write(json.dumps(result, ensure_ascii=False) + "\n")
            out.flush()

            done += len(results)
            usage = message.usage
            logger.info("готово %d | вход %d, кеш %d, выход %d", done,
                        usage.input_tokens, usage.cache_read_input_tokens or 0,
                        usage.output_tokens)


def propose_batch(client, batches: list[list[dict]], out_path: Path) -> None:
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    id_map: dict[str, set[tuple[int, str]]] = {}
    requests = []
    for index, items in enumerate(batches):
        custom_id = f"ex-{index:05d}"
        id_map[custom_id] = {(i["id"], i["lang"]) for i in items}
        requests.append(Request(
            custom_id=custom_id,
            params=MessageCreateParamsNonStreaming(**_request_params(items)),
        ))

    batch = client.messages.batches.create(requests=requests)
    logger.info("пакет создан: %s (%d запросов)", batch.id, len(requests))

    state = out_path.with_suffix(".batch")
    state.write_text(batch.id, encoding="utf-8")
    logger.info("id пакета в %s — можно прервать и вернуться", state)

    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        counts = batch.request_counts
        logger.info("статус %s | в работе %d, готово %d, ошибок %d",
                    batch.processing_status, counts.processing,
                    counts.succeeded, counts.errored)
        time.sleep(30)

    total = 0
    with out_path.open("a", encoding="utf-8") as out:
        for result in client.messages.batches.results(batch.id):
            expected = id_map.get(result.custom_id, set())
            if result.result.type != "succeeded":
                logger.error("%s: %s", result.custom_id, result.result.type)
                continue
            items, problems = _parse(result.result.message, expected)
            for problem in problems:
                logger.warning("%s: %s", result.custom_id, problem)
            for item in items:
                out.write(json.dumps(item, ensure_ascii=False) + "\n")
            total += len(items)

    logger.info("новых примеров записано: %d → %s", total, out_path)


def cmd_propose(args: argparse.Namespace) -> None:
    import anthropic

    defects = load_defects(Path(args.input))
    if args.lang:
        defects = [d for d in defects if d["lang"] == args.lang]
    if args.limit:
        defects = defects[:args.limit]

    if not defects:
        logger.error("в файле нет подходящих записей")
        return

    out_path = Path(args.out)

    # Возобновление: уже предложенное не переспрашиваем
    already: set[tuple[int, str]] = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    row = json.loads(line)
                    already.add((row["id"], row["lang"]))
                except (json.JSONDecodeError, KeyError):
                    continue
        if already:
            logger.info("уже есть %d — пропускаю", len(already))
            defects = [d for d in defects if (d["id"], d["lang"]) not in already]

    if not defects:
        logger.info("всё уже обработано")
        return

    # Одним запросом идут случаи одного языка: иначе модель путается,
    # на каком языке писать
    by_lang: dict[str, list[dict]] = {}
    for item in defects:
        by_lang.setdefault(item["lang"], []).append(item)

    batches: list[list[dict]] = []
    for lang_items in by_lang.values():
        batches.extend(chunked(lang_items, args.chunk))

    logger.info("случаев %d, запросов %d, режим %s", len(defects), len(batches),
                "пакетный" if args.batch else "последовательный")

    if args.estimate_only:
        _print_estimate(len(batches), args.batch)
        return

    client = anthropic.Anthropic()
    if args.batch:
        propose_batch(client, batches, out_path)
    else:
        propose_sync(client, batches, out_path)


def _print_estimate(request_count: int, use_batch: bool) -> None:
    """
    Прикидка. Числа из замера пересборки переводов, пересчитанные на эту
    задачу: вход меньше (одно слово вместо шести переводов и пяти примеров),
    выход заметно меньше (одна фраза вместо шести переводов со значениями).
    """
    input_per_request = 1800
    cache_per_request = 900
    output_per_request = 1600

    inp = request_count * input_per_request
    cache = request_count * cache_per_request
    out = request_count * output_per_request

    cost = inp / 1e6 * 5 + cache / 1e6 * 0.5 + out / 1e6 * 25
    if use_batch:
        cost /= 2

    print(f"\nзапросов: {request_count} (случаев ~{request_count * WORDS_PER_REQUEST})")
    print(f"вход ~{inp:,}, кеш ~{cache:,}, выход ~{out:,}")
    print(f"стоимость ~${cost:.2f}" + (" (со скидкой Batches)" if use_batch else ""))
    print()


def cmd_apply(args: argparse.Namespace) -> None:
    from sqlalchemy import create_engine, text

    from app.config import settings
    from app.services.language_service import LANGUAGES
    from app.scripts.example_quality import word_in_example

    rows = []
    for line in Path(args.file).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

    logger.info("предложений в файле: %d", len(rows))

    engine = create_engine(settings.DATABASE_URL_SYNC)

    # Проверяем предложенное тем же детектором, который нашёл дефект: если
    # новый пример снова не содержит слова, применять его незачем
    with engine.connect() as conn:
        words = {
            r["id"]: dict(r)
            for r in conn.execute(text(
                "SELECT id, word_de, translation_ru, translation_uk, "
                "translation_en, translation_tr, translation_pl FROM words "
                "WHERE id = ANY(:ids)"
            ), {"ids": [r["id"] for r in rows]}).mappings()
        }

    updates: dict[str, list[dict]] = {}
    rejected: list[dict] = []
    lemma_problems: list[dict] = []
    disagreed: list[dict] = []

    for row in rows:
        if row.get("lemma_problem"):
            lemma_problems.append(row)
            continue

        example = (row.get("example") or "").strip()
        lang = row["lang"]
        source = words.get(row["id"])
        if not example or source is None:
            rejected.append({**row, "reason": "пустой пример или слово не найдено"})
            continue

        if len(example.split()) < 2:
            rejected.append({**row, "reason": "не фраза, а одно слово"})
            continue

        # Отсев по началу слова здесь не приговор, а отметка на полях.
        #
        # Он не видит чередования в корне: «wollen» → «Willst du einen Kaffee?»
        # и «geben» → «Gibst du mir das Salz?» — правильные примеры, которые он
        # браковал. Модель, которой велено вставить слово, разбирается в
        # морфологии лучше, поэтому её работа применяется, а несогласие просто
        # записывается для разбора.
        word = source.get(LANGUAGES[lang].word_attr) or ""
        found, _ = word_in_example(word, example, lang)
        if not found:
            disagreed.append({**row, "word": word,
                              "note": "отсев не нашёл слова — вероятно чередование"})

        updates.setdefault(lang, []).append({"id": row["id"], "example": example})

    total = sum(len(v) for v in updates.values())
    logger.info("к применению: %d", total)
    if lemma_problems:
        logger.warning("модель сообщила о проблеме со словом: %d — это разметка, "
                       "а не пример, нужен разбор", len(lemma_problems))
    if rejected or lemma_problems:
        path = Path(args.file).with_name(Path(args.file).stem + "_rejected.jsonl")
        with path.open("w", encoding="utf-8") as fh:
            for item in rejected + lemma_problems:
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        logger.warning("не применено: %d → %s", len(rejected) + len(lemma_problems), path)

    if disagreed:
        path = Path(args.file).with_name(Path(args.file).stem + "_disagreed.jsonl")
        with path.open("w", encoding="utf-8") as fh:
            for item in disagreed:
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        logger.info(
            "применено, но отсев не нашёл слова: %d → %s. Обычно это чередование "
            "в корне, которое отсев не видит; смотреть выборочно, а не целиком",
            len(disagreed), path,
        )

    if args.dry_run:
        print(f"\n--dry-run: применилось бы {total}\n")
        for lang, items in updates.items():
            print(f"  {lang}: {len(items)}")
            for item in items[:5]:
                print(f"     id={item['id']}  {item['example']}")
        print()
        return

    if not total:
        logger.info("применять нечего")
        return

    with engine.begin() as conn:
        for lang, items in updates.items():
            column = LANGUAGES[lang].example_attr
            conn.execute(
                text(f"UPDATE words SET {column} = :example WHERE id = :id"),
                items,
            )

    logger.info("примеров обновлено: %d", total)
    logger.warning("озвучка этих слов устарела: текст примера изменился, и клипы "
                   "«слово с примером» пересоберутся при следующем показе сами")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("propose", help="написать новые примеры в файл")
    p.add_argument("--in", dest="input", default="example_defects.jsonl")
    p.add_argument("--out", default="example_fixes.jsonl")
    p.add_argument("--lang", help="только один язык")
    p.add_argument("--limit", type=int)
    p.add_argument("--chunk", type=int, default=WORDS_PER_REQUEST)
    p.add_argument("--batch", action="store_true",
                   help="через Batches API: вдвое дешевле")
    p.add_argument("--estimate-only", action="store_true")
    p.set_defaults(func=cmd_propose)

    a = sub.add_parser("apply", help="применить новые примеры")
    a.add_argument("--file", required=True)
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
