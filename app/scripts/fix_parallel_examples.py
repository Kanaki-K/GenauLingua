"""
Пример на языке перевода должен переводить немецкий пример, а не быть
отдельной фразой.

ЗАЧЕМ ЭТОТ ПРОГОН. Карточка после ответа показывает примеры стопкой, друг под
другом с флагами (app/bot/handlers/quiz/game.py). Человек читает их как пару:

    de: Seine Gedanken waren erhaben und tiefgründig
    pl: Jego słowa były wzniosłe i piękne          ← слова, а не мысли

Русский, украинский, английский и турецкий примеры — верные переводы немецкого.
Польский выбивается, и причина не в модели: запрос в retranslate_wordbase прямо
требовал написать польский пример «с нуля», короткой бытовой фразой. Модель
выполнила ровно это. На выборке из десяти слов несовпадающих пар оказалось
семь, на выборке из двадцати четырёх — двенадцать.

Запрос исправлен, но исправление касается будущих прогонов. Уже написанные
12 603 польских примера надо перевести заново — этим и занят этот скрипт.

ПОЧЕМУ ОТДЕЛЬНЫЙ СКРИПТ, А НЕ fix_examples. Тот пишет НОВЫЙ пример для слова,
у которого примера фактически нет. Здесь задача обратная: немецкий пример есть
и он хороший, нужен его точный перевод. Это разные запросы, и смешивать их
нельзя — получится то же самое сочинительство.

РАБОТА В ДВА ЭТАПА, в базу напрямую скрипт не пишет:

    python -m app.scripts.fix_parallel_examples propose --batch
    python -m app.scripts.fix_parallel_examples apply --file polish_examples.jsonl --dry-run
    python -m app.scripts.fix_parallel_examples apply --file polish_examples.jsonl
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Iterator

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("parallel_examples")

MODEL = "claude-opus-5"

# Выход — одна короткая фраза на слово, поэтому порция крупная.
WORDS_PER_REQUEST = 40

# Замер: сорок польских фраз по 3–8 слов укладываются примерно в 1600 токенов.
# 4000 даёт запас в два с половиной раза и держит резерв пакета далеко от квоты.
MAX_TOKENS = 4000

PL_DIACRITICS = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")

# Прогон начинался польским, но проверка качества показала то же самое в
# русском, украинском и турецком: пример на языке перевода оказывается
# самостоятельной фразой, а не переводом немецкой. На 36 случайных словах
# таких нашлось 11, и только четыре из них польские. Поэтому язык — параметр.
LANG_NAMES = {
    "ru": ("русский", "русском"),
    "uk": ("украинский", "украинском"),
    "en": ("английский", "английском"),
    "tr": ("турецкий", "турецком"),
    "pl": ("польский", "польском"),
}

DIACRITICS = {
    "pl": "ą ć ę ł ń ó ś ź ż",
    "tr": "ç ğ ı ö ş ü",
    "uk": "і ї є ґ",
    "ru": "ё",
    "en": "",
}


def api_key() -> str:
    """
    Ключ из настроек, а при их отсутствии — из .env.local напрямую.

    Так же устроен collect_batch: скрипты запускают руками и нередко без
    поднятого окружения, а `settings` поля ANTHROPIC_API_KEY не содержит вовсе.
    """
    import os
    import re

    key = getattr(settings, "ANTHROPIC_API_KEY", None) or os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    env = Path(__file__).resolve().parents[2] / ".env.local"
    if env.exists():
        found = re.search(r"ANTHROPIC_API_KEY\s*=\s*(\S+)", env.read_text(encoding="utf-8"))
        if found:
            return found.group(1).strip().strip("\"'")
    sys.exit("не нашёл ANTHROPIC_API_KEY ни в настройках, ни в .env.local")


SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "examples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "id слова из запроса"},
                    "example": {
                        "type": "string",
                        "description": "Перевод немецкого примера на целевой язык",
                    },
                    "changed": {
                        "type": "boolean",
                        "description": (
                            "true, если прежний польский пример говорил о другом "
                            "и его пришлось заменить; false, если он уже был "
                            "верным переводом и возвращён без изменений"
                        ),
                    },
                },
                "required": ["id", "example", "changed"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["examples"],
    "additionalProperties": False,
}


PROMPT_TEMPLATE = """\
Ты переводишь на {lang_acc} язык примеры употребления слов для словаря \
приложения, которое учит языкам.

Человек видит после ответа немецкую фразу и {lang_prep} одну под другой, с \
флагами. Он читает их как перевод друг друга. Поэтому {lang_prep} фраза \
обязана говорить ровно о том же, о чём немецкая.

ГЛАВНОЕ ТРЕБОВАНИЕ
Переведи немецкий пример. Те же действующие лица, тот же предмет, то же время, \
то же число. Не сочиняй свою фразу про это слово — именно переведи присланную.

Нельзя (примеры настоящие, из этой базы):
  de «Seine Gedanken waren erhaben»  →  «Jego słowa były wzniosłe»
      (в немецком мысли, в переводе слова — это разные предложения)
  de «Der Konflikt eskaliert»  →  «Восени в неї загострюється алергія»
      (конфликт превратился в осеннюю аллергию)
  de «Ich muss den Termin absagen»  →  «Я мушу скасувати поїздку через дощ»
      (встреча превратилась в поездку из-за дождя)

Нужно:
  de «Seine Gedanken waren erhaben und tiefgründig»  →  «Jego myśli były wzniosłe i głębokie»
  de «Der Hund jault nachts»  →  «Pies wyje w nocy»

ПЕРЕВОД ЖИВОЙ, А НЕ ДОСЛОВНЫЙ
Фраза должна звучать естественно, как сказал бы носитель. Порядок слов, \
предлоги и устойчивые обороты бери {lang_prep}. Менять можно форму, но не \
содержание.

САМО СЛОВО ОБЯЗАНО ПРИСУТСТВОВАТЬ
В переводе должно стоять то самое слово, которое прислано в поле «слово» — \
пусть и в другой грамматической форме. Если точный перевод немецкой фразы его \
не содержит, подбери такой вариант перевода, который содержит.

ОСТАЛЬНОЕ
- Точку в конце не ставь. Вопросительный и восклицательный знак ставь, если \
фраза этого требует.
- Диакритика обязательна: {diacritics}
- Пиши только на {lang_prep} языке, ни на каком другом.
- Если присланный пример УЖЕ верно переводит немецкий, верни его без изменений \
и поставь changed = false. Не переписывай исправное.

Отвечай строго по схеме, по одному объекту на каждый присланный случай, с тем \
же id.
"""


def system_prompt(lang: str) -> str:
    acc, prep = LANG_NAMES[lang]
    dia = DIACRITICS[lang]
    return PROMPT_TEMPLATE.format(
        lang_acc=acc, lang_prep=prep,
        diacritics=dia if dia else "в этом языке особой диакритики нет",
    )


def chunked(items: list, size: int) -> Iterator[list]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def load_rows(lang: str, limit: int | None, only_ids: list[int] | None) -> list[dict]:
    """Слова, у которых есть и немецкий пример, и перевод на целевой язык."""
    sql = f"""
        SELECT id, word_de, level,
               translation_{lang} AS word, example_de, example_{lang} AS example
        FROM words
        WHERE COALESCE(btrim(example_de), '') <> ''
          AND COALESCE(btrim(translation_{lang}), '') <> ''
    """
    params: dict[str, Any] = {}
    if only_ids:
        sql += " AND id = ANY(:ids)"
        params["ids"] = only_ids
    sql += " ORDER BY id"
    if limit:
        sql += f" LIMIT {int(limit)}"
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        return [dict(r) for r in conn.execute(text(sql), params).mappings()]


def build_user_message(items: list[dict], lang: str) -> str:
    acc, prep = LANG_NAMES[lang]
    lines = [f"Переведи немецкие примеры на {acc}:", ""]
    for it in items:
        lines.append(f"id: {it['id']}")
        lines.append(f"  слово ({lang}): {it['word']}")
        lines.append(f"  немецкий пример: {it['example_de']}")
        lines.append(f"  нынешний пример: {it.get('example') or '—'}")
        lines.append("")
    return "\n".join(lines)


def _request_params(items: list[dict], lang: str) -> dict:
    return {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": [
            {"type": "text", "text": system_prompt(lang),
             "cache_control": {"type": "ephemeral"}}
        ],
        "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}},
        "messages": [{"role": "user", "content": build_user_message(items, lang)}],
    }


def _parse(message, expected: set[int]) -> tuple[list[dict], list[str]]:
    problems = []
    if getattr(message, "stop_reason", None) == "max_tokens":
        problems.append("ответ обрезан по max_tokens — уменьшить порцию")

    block = next((b.text for b in message.content if b.type == "text"), None)
    if not block:
        return [], problems + ["в ответе нет текстового блока"]
    try:
        payload = json.loads(block)
    except json.JSONDecodeError as exc:
        return [], problems + [f"ответ не разобрался как JSON: {exc}"]

    rows = payload.get("examples", [])
    got = {r.get("id") for r in rows}
    if missing := expected - got:
        problems.append(f"модель пропустила id: {sorted(missing)[:10]}")
    if extra := got - expected:
        problems.append(f"модель вернула лишние id: {sorted(extra)[:10]}")
        rows = [r for r in rows if r.get("id") in expected]
    return rows, problems


def cmd_propose(args: argparse.Namespace) -> None:
    import anthropic

    ids = None
    if args.ids_file:
        ids = [int(x) for x in Path(args.ids_file).read_text().split()]
    rows = load_rows(args.lang, args.limit, ids)
    batches = list(chunked(rows, args.chunk))
    logger.info("слов %d, запросов %d, режим %s",
                len(rows), len(batches), "пакетный" if args.batch else "синхронный")
    reserved = len(batches) * MAX_TOKENS
    logger.info("резерв пакета %d токенов из квоты 2 000 000", reserved)
    if reserved > 2_000_000:
        logger.warning("резерв больше квоты — пакет пойдёт медленно, "
                       "разумнее разбить на части через --limit")
    if args.estimate_only:
        return

    out = Path(args.out)
    client = anthropic.Anthropic(api_key=api_key())

    if not args.batch:
        with out.open("a", encoding="utf-8") as fh:
            for items in batches:
                msg = client.messages.create(**_request_params(items, args.lang))
                proposals, problems = _parse(msg, {i["id"] for i in items})
                for p in problems:
                    logger.warning("%s", p)
                for p in proposals:
                    fh.write(json.dumps(p, ensure_ascii=False) + "\n")
                fh.flush()
                logger.info("готово %d", len(proposals))
        return

    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    requests, id_map = [], {}
    for index, items in enumerate(batches):
        cid = f"chunk-{index:05d}"
        id_map[cid] = {i["id"] for i in items}
        requests.append(Request(custom_id=cid,
                                params=MessageCreateParamsNonStreaming(**_request_params(items, args.lang))))

    batch = client.messages.batches.create(requests=requests)
    logger.info("пакет создан: %s (%d запросов)", batch.id, len(requests))
    state = out.with_suffix(".batch")
    state.write_text(batch.id, encoding="utf-8")
    logger.info("id пакета в %s — можно прервать и вернуться", state.name)

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
                logger.warning("%s: %s", result.custom_id, result.result.type)
                continue
            proposals, problems = _parse(result.result.message,
                                         id_map.get(result.custom_id, set()))
            for p in problems:
                logger.warning("%s: %s", result.custom_id, p)
            for p in proposals:
                fh.write(json.dumps(p, ensure_ascii=False) + "\n")
                written += 1
    logger.info("предложений записано: %d → %s", written, out)


def cmd_apply(args: argparse.Namespace) -> None:
    rows = [json.loads(l) for l in Path(args.file).read_text(encoding="utf-8").splitlines() if l.strip()]
    logger.info("предложений в файле: %d", len(rows))

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        current = {
            r[0]: (r[1], r[2], r[3])
            for r in conn.execute(
                text(f"SELECT id, word_de, example_de, example_{args.lang} FROM words WHERE id = ANY(:i)"),
                {"i": [r["id"] for r in rows]},
            )
        }

    updates, skipped = [], {"пусто": 0, "нет в базе": 0, "без изменений": 0,
                            "нет диакритики там, где она нужна": 0, "точка в конце": 0}
    for r in rows:
        wid = r["id"]
        new = (r.get("example") or "").strip()
        if wid not in current:
            skipped["нет в базе"] += 1
            continue
        if not new:
            skipped["пусто"] += 1
            continue
        if new == (current[wid][2] or "").strip():
            skipped["без изменений"] += 1
            continue
        if new.endswith("."):
            # Точка в конце в этой базе не ставится — снимаем, а не бракуем
            new = new.rstrip(".")
        updates.append((wid, new))

    logger.info("к применению %d, пропущено %s", len(updates), skipped)

    for wid, new in updates[:20]:
        de, old = current[wid][1], current[wid][2]
        logger.info("  %s\n      de:    %s\n      было:  %s\n      стало: %s",
                    current[wid][0], de, old, new)
    if len(updates) > 20:
        logger.info("  ... ещё %d", len(updates) - 20)

    if args.dry_run:
        logger.info("--dry-run: применилось бы %d", len(updates))
        return

    with engine.begin() as conn:
        for wid, new in updates:
            conn.execute(text(f"UPDATE words SET example_{args.lang} = :v WHERE id = :i"),
                         {"v": new, "i": wid})
    logger.info("применено: %d", len(updates))
    logger.warning("ОБЯЗАТЕЛЬНО после этого:\n"
                   "  python -m app.scripts.tts_synthesize --lang pl   — примеры изменились\n"
                   "  python -m app.scripts.tts_prune_orphans --delete")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("propose", help="перевести немецкие примеры на польский")
    p.add_argument("--lang", choices=sorted(LANG_NAMES), default="pl")
    p.add_argument("--out", default="polish_examples.jsonl")
    p.add_argument("--limit", type=int)
    p.add_argument("--ids-file", help="файл с id через пробел")
    p.add_argument("--chunk", type=int, default=WORDS_PER_REQUEST)
    p.add_argument("--batch", action="store_true", help="через Batches API: вдвое дешевле")
    p.add_argument("--estimate-only", action="store_true")
    p.set_defaults(func=cmd_propose)

    a = sub.add_parser("apply", help="применить переводы")
    a.add_argument("--lang", choices=sorted(LANG_NAMES), default="pl")
    a.add_argument("--file", required=True)
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_apply)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
