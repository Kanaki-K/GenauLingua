#!/usr/bin/env python3
"""
Пересборка переводов словарной базы через Claude API + польский с нуля.

Зачем нужна модель, а не скрипт с правилами: «естественный разговорный
перевод» — языковое суждение. Правилами проверяются только формальные вещи
(артикль из списка, чужой алфавит, потерянная диакритика) — это делает
app/scripts/audit_wordbase.py. Всё остальное приходится генерировать.

Что решает по результатам аудита и прод-данных:
  * служебные многозначные слова получают ВСЕ значения, а не одно из них —
    это единственная подтверждённая данными проблема качества (точность 71%
    против 80%, и 24.2% против 14.7% как первое слово в брошенных сессиях);
  * артикль проверяется и исправляется;
  * латиница в русской/украинской колонке (Schlüpfer → «Slip») исправляется;
  * потерянные турецкие диакритики (Iyi → İyi) восстанавливаются;
  * «to» у английских глаголов приводится к единому виду;
  * польские перевод и пример создаются с нуля — колонок в базе не было;
  * примеры на пяти языках проверяются на то, что они вообще содержат
    само слово («подсобить» → «нужно помочь удаче» — негодный пример);
    негодные собираются в отдельный файл для переписывания;
  * неверная лемма и подозрительный уровень CEFR помечаются на ручной разбор.

РАБОТА В ДВА ЭТАПА — в боевую базу напрямую скрипт не пишет:

  1. propose — собрать предложения в JSONL-файл
       python -m app.scripts.retranslate_wordbase propose --level A1
       python -m app.scripts.retranslate_wordbase propose --all --batch

  2. apply — применить проверенное
       python -m app.scripts.retranslate_wordbase apply --file proposals.jsonl --dry-run
       python -m app.scripts.retranslate_wordbase apply --file proposals.jsonl

Пакетный режим (--batch) использует Batches API: вдвое дешевле, результат
в течение часа. Для 12 900 слов это примерно $10–25 единоразово.

Требуется ANTHROPIC_API_KEY либо активный профиль `ant auth login`.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv

# Тот же файл, что читает app.config — иначе локальный запуск
# подхватит боевые строки подключения из .env.
load_dotenv(os.environ.get("ENV_FILE", ".env"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("retranslate")

MODEL = "claude-opus-5"

# Сколько слов в одном запросе. Больше — дешевле за счёт общего системного
# промпта, но выше риск, что модель собьётся с нумерации на длинном списке.
WORDS_PER_REQUEST = 20

# Потолок на ответ, а не расход: платится фактический выход. Замер на живом
# прогоне — 8292 токена на запрос из 20 слов, так что 11 000 даёт треть запаса.
#
# Прежде стояло 14 000. Уменьшено не потому, что 14 000 мешало: пакет из 162
# таких запросов отработал полностью и отдал 3197 слов из 3237. Просто запас
# втрое от замеренного значения ничего не давал, а резерв пакета из max_tokens
# считается, и без нужды приближаться к квоте аккаунта незачем.
MAX_TOKENS = 11000

# Выходная квота аккаунта из anthropic-ratelimit-output-tokens-limit.
#
# Проверка перед отправкой добавлена как страховка, а НЕ как исправление
# известной поломки: пакет с резервом 2 268 000 при этой квоте отработал
# нормально, просто медленно — около трёх часов. Гипотеза, что превышение
# резерва блокирует пакет, не подтвердилась, и предупреждение здесь
# консервативное: оно советует разбить работу, но не утверждает, что иначе
# ничего не выйдет.
OUTPUT_TOKEN_QUOTA = 2_000_000


# ============================================================================
# СХЕМА ОТВЕТА
# ============================================================================

# Модель обязана вернуть ровно эту структуру — иначе разбирать ответ пришлось бы
# эвристиками, а на 12 900 словах любая эвристика где-нибудь да сломается.
WORD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "words": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "id слова из запроса"},
                    # Через anyOf, а не "type": ["string","null"] с enum:
                    # структурированный вывод отклоняет союзный тип вместе с enum
                    # («Enum value 'der' does not match declared type»).
                    "article": {
                        "anyOf": [
                            {"type": "string", "enum": ["der", "die", "das"]},
                            {"type": "null"},
                        ],
                        "description": "Артикль для существительных, иначе null",
                    },
                    "lemma_ok": {
                        "type": "boolean",
                        "description": "Слово в словарной форме (не форма слова, не морфема)",
                    },
                    "level_ok": {
                        "type": "boolean",
                        "description": "Уровень CEFR правдоподобен для этого слова",
                    },
                    "suggested_level": {
                        "anyOf": [
                            {"type": "string", "enum": ["A1", "A2", "B1", "B2", "C1", "C2"]},
                            {"type": "null"},
                        ],
                    },
                    "ru": {"$ref": "#/$defs/translation"},
                    "uk": {"$ref": "#/$defs/translation"},
                    "en": {"$ref": "#/$defs/translation"},
                    "tr": {"$ref": "#/$defs/translation"},
                    "pl": {"$ref": "#/$defs/translation"},
                    "example_pl": {
                        "type": "string",
                        "description": (
                            "Короткая бытовая фраза по-польски, содержащая это слово "
                            "и раскрывающая его основное значение"
                        ),
                    },
                    "examples_ok": {"$ref": "#/$defs/examples_ok"},
                    "note": {
                        "type": ["string", "null"],
                        "description": "Короткое пояснение, если со словом что-то не так",
                    },
                },
                "required": [
                    "id", "article", "lemma_ok", "level_ok", "suggested_level",
                    "ru", "uk", "en", "tr", "pl", "example_pl", "examples_ok", "note",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["words"],
    "additionalProperties": False,
    "$defs": {
        "translation": {
            "type": "object",
            "properties": {
                "primary": {
                    "type": "string",
                    "description": "Самый естественный повседневный перевод, одно слово или короткая фраза",
                },
                "meanings": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Все существенные значения, включая primary, от частого к редкому. "
                        "Для однозначного слова — один элемент."
                    ),
                },
            },
            "required": ["primary", "meanings"],
            "additionalProperties": False,
        },
        # Проверка примеров логическими полями, а не переписыванием: переписать
        # все примеры на пяти языках стоило бы вдвое дороже, а испорчена малая
        # часть. Помеченные переписываются отдельным дешёвым прогоном.
        "examples_ok": {
            "type": "object",
            "properties": {
                "de": {"type": "boolean"},
                "ru": {"type": "boolean"},
                "uk": {"type": "boolean"},
                "en": {"type": "boolean"},
                "tr": {"type": "boolean"},
            },
            "required": ["de", "ru", "uk", "en", "tr"],
            "additionalProperties": False,
            "description": (
                "По каждому языку: содержит ли существующий пример само это слово "
                "(в любой форме) и раскрывает ли его значение. false, если пример "
                "про другое слово, пустой или бессмысленный."
            ),
        },
    },
}


SYSTEM_PROMPT = """\
Ты — лексикограф словаря для приложения, которое учит словам через тест \
с четырьмя вариантами ответа. Твои переводы люди увидят как варианты выбора.

Для каждого немецкого слова дай переводы на русский, украинский, английский, \
турецкий и польский.

ГЛАВНОЕ ТРЕБОВАНИЕ — ЕСТЕСТВЕННОСТЬ.
Пиши то слово, которым носитель пользуется в живой речи, а не словарный \
эквивалент и не калькированный подстрочник. Если немецкое слово обиходное, \
перевод тоже должен быть обиходным. Никаких канцеляризмов там, где их нет \
в оригинале.

МНОГОЗНАЧНОСТЬ — это самое важное для качества теста.
Поле meanings должно содержать ВСЕ существенные значения слова, а не одно. \
Служебные и частотные слова почти всегда многозначны: gleich — это и «сразу», \
и «одинаковый»; als — «чем», «когда», «в качестве»; man — безличное \
местоимение, а не «можно». Если в meanings окажется одно значение там, где \
их несколько, ученик будет угадывать, какое значение выбрал словарь, вместо \
того чтобы знать язык. В primary ставь самое частотное значение.

ПОЛЬСКИЙ ЗАПОЛНЯЕТСЯ С НУЛЯ — его в базе ещё нет.
Требования те же, что к остальным языкам, плюс:
- диакритика обязательна: «książka», «żółty», «ćwiczyć». Написание без \
хвостиков и точек («ksiazka») недопустимо.
- глагол давай инфинитивом без частиц: «robić», не «do robić».
- существительное — именительный падеж единственного числа, без артикля.
- слово этот язык озвучивает синтезатор, поэтому в переводе не должно быть \
пояснений в скобках, помет вроде «разг.» и косых черт — только сами значения.

ПОЛЬСКИЙ ПРИМЕР (example_pl) — тоже с нуля.
Короткая бытовая фраза из 3–8 слов, в которой это слово стоит живьём и по \
которой видно, что оно значит. Фраза должна звучать как из разговора, а не \
как из учебника грамматики. Само слово обязано в ней присутствовать, пусть \
и в другой грамматической форме. Точку в конце не ставь.

ПРОВЕРКА СУЩЕСТВУЮЩИХ ПРИМЕРОВ (examples_ok).
По каждому из пяти языков ответь, годен ли уже имеющийся пример. Ставь false, \
если пример про другое слово (для «подсобить» дан «Иногда нужно помочь удаче» \
— там нет исходного слова), если он пустой, бессмысленный или не раскрывает \
значение. Иная грамматическая форма слова — это нормально, «рыба» → «люблю \
рыбу» годится, тут true. Если примера на этом языке нет вообще — false.

ОСТАЛЬНЫЕ ПРАВИЛА
- Английские глаголы — всегда с «to»: «to run», не «run».
- Турецкий — с диакритикой: «İyi», «örnek», «öğrenmek». Транслит недопустим.
- Русский и украинский — только кириллицей.
- Артикль указывай только для существительных: der, die или das. Для остальных \
частей речи — null.
- Строчная или заглавная буква в немецком слове значима: существительные \
пишутся с заглавной. Если слово размечено как существительное, но написано \
со строчной, поставь lemma_ok = false.
- lemma_ok = false, если это форма слова, а не лемма (Alben вместо Album), \
либо несамостоятельная морфема (lieblings-), либо разговорное усечение.
- level_ok = false, если уровень CEFR явно не соответствует слову. Учитывай, \
что учебная лексика для начинающих включает конкретные бытовые слова \
(Teelöffel, Familienname) — они уместны на A1, даже если редки в общем \
корпусе. А вот Hufeisen или Müllabfuhr на A1 не место.
- note заполняй только когда есть что сказать: неверная часть речи, \
испорченные данные, неоднозначная разметка. Иначе null.

Переводи по смыслу, который задают часть речи и пример употребления. \
Отвечай строго по схеме, по одному объекту на каждое слово из запроса, \
с тем же id.
"""


# ============================================================================
# ИСТОЧНИК СЛОВ
# ============================================================================

def load_words_from_db(
    levels: Optional[list[str]],
    ids: Optional[list[int]],
    limit: Optional[int],
    only_flagged: bool,
) -> list[dict]:
    from sqlalchemy import create_engine, text

    from app.config import settings

    conditions = []
    params: dict[str, Any] = {}

    if levels:
        # Уровнями целиком, а не частями: наполовину пересобранный уровень
        # дал бы ученику смесь проверенных и непроверенных слов
        conditions.append("level::text = ANY(:levels)")
        params["levels"] = [lv.upper() for lv in levels]
    if ids:
        conditions.append("id = ANY(:ids)")
        params["ids"] = ids
    if only_flagged:
        # Слова, по которым аудит и прод-статистика чаще всего расходятся
        # с ожиданием: служебные части речи и всё с единственным значением
        conditions.append(
            "(pos::text IN ('PRONOUN','PREPOSITION','CONJUNCTION','ADVERB','OTHER')"
            " OR translation_ru !~ '[,;/]')"
        )

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    limit_sql = f"LIMIT {int(limit)}" if limit else ""

    sql = text(
        f"""
        SELECT id, word_de, article, pos::text AS pos, level::text AS level,
               category, frequency_rank,
               translation_ru, translation_uk, translation_en, translation_tr,
               translation_pl,
               example_de, example_ru, example_uk, example_en, example_tr
        FROM words
        {where}
        ORDER BY frequency_rank NULLS LAST, id
        {limit_sql}
        """
    )

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(sql, params).mappings()]


def chunked(items: list, size: int) -> Iterator[list]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def build_user_message(words: list[dict]) -> str:
    lines = ["Слова для перевода:", ""]
    for w in words:
        lines.append(f"id: {w['id']}")
        lines.append(f"  слово: {w['word_de']}")
        lines.append(f"  часть речи: {w['pos']}")
        lines.append(f"  уровень: {w['level']}")
        if w.get("article"):
            lines.append(f"  текущий артикль: {w['article']}")
        if w.get("frequency_rank"):
            lines.append(f"  частотный ранг: {w['frequency_rank']}")
        lines.append("  текущие переводы (могут быть неточными):")
        for code in ("ru", "uk", "en", "tr"):
            lines.append(f"    {code}: {w.get(f'translation_{code}') or '—'}")
        # Примеры нужны и как контекст для перевода, и как предмет проверки
        # examples_ok — поэтому передаются все пять, а не только немецкий
        lines.append("  текущие примеры (их нужно оценить в examples_ok):")
        for code in ("de", "ru", "uk", "en", "tr"):
            lines.append(f"    {code}: {w.get(f'example_{code}') or '—'}")
        lines.append("")
    return "\n".join(lines)


# ============================================================================
# PROPOSE
# ============================================================================

def _request_params(words: list[dict]) -> dict:
    return {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        # Системный промпт одинаков во всех запросах — кешируем его,
        # иначе на 650 запросах платим за него каждый раз
        "system": [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "output_config": {"format": {"type": "json_schema", "schema": WORD_SCHEMA}},
        "messages": [{"role": "user", "content": build_user_message(words)}],
    }


def _parse_response(message, expected_ids: set[int]) -> tuple[list[dict], list[str]]:
    """Разобрать ответ модели. Возвращает (предложения, проблемы)."""
    problems: list[str] = []

    if getattr(message, "stop_reason", None) == "refusal":
        return [], ["модель отказалась обрабатывать запрос"]
    if getattr(message, "stop_reason", None) == "max_tokens":
        problems.append("ответ обрезан по max_tokens — уменьшить размер порции")

    text_block = next((b.text for b in message.content if b.type == "text"), None)
    if not text_block:
        return [], problems + ["в ответе нет текстового блока"]

    try:
        payload = json.loads(text_block)
    except json.JSONDecodeError as exc:
        return [], problems + [f"ответ не разобрался как JSON: {exc}"]

    proposals = payload.get("words", [])
    got_ids = {p.get("id") for p in proposals}

    missing = expected_ids - got_ids
    if missing:
        problems.append(f"модель пропустила id: {sorted(missing)}")
    extra = got_ids - expected_ids
    if extra:
        problems.append(f"модель вернула лишние id: {sorted(extra)}")
        proposals = [p for p in proposals if p.get("id") in expected_ids]

    return proposals, problems


def propose_sync(client, batches: list[list[dict]], out_path: Path) -> None:
    """Последовательные запросы. Медленно и вдвое дороже, зато результат сразу."""
    done = 0
    with out_path.open("a", encoding="utf-8") as out:
        for words in batches:
            expected = {w["id"] for w in words}
            try:
                message = client.messages.create(**_request_params(words))
            except Exception as exc:
                logger.error("запрос упал (%s): %s", sorted(expected)[:3], exc)
                continue

            proposals, problems = _parse_response(message, expected)
            for problem in problems:
                logger.warning("%s", problem)

            for proposal in proposals:
                out.write(json.dumps(proposal, ensure_ascii=False) + "\n")
            out.flush()

            done += len(proposals)
            usage = message.usage
            logger.info(
                "готово %d слов | вход %d, кеш-чтение %d, выход %d",
                done, usage.input_tokens, usage.cache_read_input_tokens or 0,
                usage.output_tokens,
            )


def _check_output_budget(request_count: int) -> None:
    """
    Предупредить, если резерв пакета превышает выходную квоту аккаунта.

    Только предупреждение, не отказ. Пакет с резервом 2 268 000 при квоте
    2 000 000 отработал нормально, просто медленно — около трёх часов. Так что
    превышение не означает поломки; оно означает, что прогресса придётся ждать
    долго и лучше разбить работу на части, чтобы видеть результат раньше.
    """
    reserved = request_count * MAX_TOKENS
    if reserved <= OUTPUT_TOKEN_QUOTA:
        logger.info("резерв пакета %d токенов из квоты %d",
                    reserved, OUTPUT_TOKEN_QUOTA)
        return

    fits = OUTPUT_TOKEN_QUOTA // MAX_TOKENS
    logger.warning(
        "резерв пакета %d токенов больше квоты аккаунта %d. Пакет отработает, "
        "но медленно: замеренный случай шёл около трёх часов при нулевом "
        "видимом прогрессе почти до самого конца. Чтобы видеть результат "
        "раньше, разбейте работу на части не больше %d запросов — например, "
        "по одному уровню CEFR.",
        reserved, OUTPUT_TOKEN_QUOTA, fits,
    )


def propose_batch(client, batches: list[list[dict]], out_path: Path) -> None:
    """
    Batches API: вдвое дешевле, результат в течение часа.
    Для полной базы это единственный разумный режим.
    """
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    id_map: dict[str, set[int]] = {}
    requests = []
    for index, words in enumerate(batches):
        custom_id = f"chunk-{index:05d}"
        id_map[custom_id] = {w["id"] for w in words}
        requests.append(
            Request(
                custom_id=custom_id,
                params=MessageCreateParamsNonStreaming(**_request_params(words)),
            )
        )

    _check_output_budget(len(requests))

    batch = client.messages.batches.create(requests=requests)
    logger.info("пакет создан: %s (%d запросов)", batch.id, len(requests))

    state_path = out_path.with_suffix(".batch")
    state_path.write_text(batch.id, encoding="utf-8")
    logger.info("id пакета сохранён в %s — можно прервать и вернуться позже", state_path)

    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        counts = batch.request_counts
        logger.info(
            "статус %s | в обработке %d, готово %d, ошибок %d",
            batch.processing_status, counts.processing, counts.succeeded, counts.errored,
        )
        time.sleep(30)

    logger.info("пакет завершён: успешно %d, с ошибкой %d",
                batch.request_counts.succeeded, batch.request_counts.errored)

    total = 0
    with out_path.open("a", encoding="utf-8") as out:
        for result in client.messages.batches.results(batch.id):
            expected = id_map.get(result.custom_id, set())
            kind = result.result.type

            if kind != "succeeded":
                logger.error("%s: %s", result.custom_id, kind)
                continue

            proposals, problems = _parse_response(result.result.message, expected)
            for problem in problems:
                logger.warning("%s: %s", result.custom_id, problem)
            for proposal in proposals:
                out.write(json.dumps(proposal, ensure_ascii=False) + "\n")
            total += len(proposals)

    logger.info("предложений записано: %d → %s", total, out_path)


def cmd_propose(args: argparse.Namespace) -> None:
    import anthropic

    words = load_words_from_db(args.levels, args.ids, args.limit, args.flagged)
    if not words:
        logger.error("под указанные условия не попало ни одного слова")
        return

    out_path = Path(args.out)

    # Возобновление: уже предложенные слова не переспрашиваем
    already: set[int] = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    already.add(json.loads(line)["id"])
                except (json.JSONDecodeError, KeyError):
                    continue
        if already:
            logger.info("в %s уже есть %d слов — пропускаю их", out_path, len(already))
            words = [w for w in words if w["id"] not in already]

    if not words:
        logger.info("всё уже обработано")
        return

    batches = list(chunked(words, args.chunk))
    logger.info(
        "слов к обработке: %d, запросов: %d, режим: %s",
        len(words), len(batches), "пакетный" if args.batch else "последовательный",
    )

    if args.estimate_only:
        _print_estimate(len(batches), args.batch)
        if args.batch:
            _check_output_budget(len(batches))
        return

    client = anthropic.Anthropic()
    if args.batch:
        propose_batch(client, batches, out_path)
    else:
        propose_sync(client, batches, out_path)


def _print_estimate(request_count: int, use_batch: bool) -> None:
    """
    Прикидка стоимости. Цены Opus 5: $5 за млн входных, $25 за млн выходных.

    Числа ниже — из замера на пробной партии, а не из головы: в запрос теперь
    уходят пять примеров на слово, а в ответ шесть языков и польский пример.
    """
    # Замерено на партии из 100 слов (5 запросов по 20): вход 3829,
    # чтение кеша 3842, выход 8292 на запрос. Выход и есть основная статья
    # расхода — шесть языков со всеми значениями плюс польский пример.
    input_per_request = 3829
    cache_read_per_request = 3842
    output_per_request = 8292

    input_tokens = request_count * input_per_request
    cache_tokens = request_count * cache_read_per_request
    output_tokens = request_count * output_per_request

    # Чтение кеша стоит 10% от входа
    cost = (
        input_tokens / 1e6 * 5
        + cache_tokens / 1e6 * 0.5
        + output_tokens / 1e6 * 25
    )
    if use_batch:
        cost /= 2

    print(f"\nзапросов: {request_count}  (слов ~{request_count * WORDS_PER_REQUEST})")
    print(f"входных токенов:  ~{input_tokens:,}")
    print(f"чтений кеша:      ~{cache_tokens:,}")
    print(f"выходных токенов: ~{output_tokens:,}")
    print(f"стоимость:        ~${cost:.2f}" + (" (со скидкой Batches)" if use_batch else ""))
    print("\nОценка из замера, а не из головы. Фактический расход смотреть\n"
          "в консоли Anthropic после прогона.\n")


# ============================================================================
# APPLY
# ============================================================================

# Похожие по виду буквы: латинская «a» и кириллическая «а» выглядят одинаково,
# но это разные символы. Модель их иногда путает, и на глаз это не видно:
# «удaритися» с латинской «a» выглядит как обычное украинское слово, а для
# базы, поиска и озвучки это другое слово.
#
# Найдено 8 таких случаев на 3237 предложений: «нареченa», «дорíжка»,
# «виставa», польское «babа» с кириллической «а».
_LATIN_TO_CYRILLIC = {
    "a": "а", "A": "А", "e": "е", "E": "Е", "o": "о", "O": "О",
    "c": "с", "C": "С", "p": "р", "P": "Р", "x": "х", "X": "Х",
    "y": "у", "Y": "У", "i": "і", "I": "І", "í": "і",
    "H": "Н", "K": "К", "M": "М", "T": "Т", "B": "В",
}
_CYRILLIC_TO_LATIN = {
    "а": "a", "А": "A", "е": "e", "Е": "E", "о": "o", "О": "O",
    "с": "c", "С": "C", "р": "p", "Р": "P", "х": "x", "Х": "X",
    "у": "y", "У": "Y", "і": "i", "І": "I",
    "Н": "H", "К": "K", "М": "M", "Т": "T", "В": "B",
}

CYRILLIC_LANGS = {"ru", "uk"}
LATIN_LANGS = {"en", "tr", "pl"}


_LETTER_RUN = re.compile(r"[^\W\d_]+", re.UNICODE)


def _fix_homoglyphs(value: str, lang: str) -> str:
    """
    Привести похожие буквы к письменности языка.

    Правится только буквенный отрезок, в котором смешаны обе письменности:
    такое написание всегда ошибка. Отрезок целиком из чужих букв не трогается —
    «ID-карта» и «HR-менеджер» законны, латиница там намеренная.

    Разбор идёт по буквенным отрезкам, а не по словам через пробел: «ID-карта»
    это одно слово из двух отрезков, и первая версия этой функции честно
    превращала его в «ІD-карта» с кириллической І.
    """
    table = _LATIN_TO_CYRILLIC if lang in CYRILLIC_LANGS else _CYRILLIC_TO_LATIN
    if not table:
        return value

    own = "CYRILLIC" if lang in CYRILLIC_LANGS else "LATIN"

    def fix_run(match: re.Match) -> str:
        run = match.group(0)
        kinds = {_script_of(ch) for ch in run if ch.isalpha()} - {""}
        # Смешаны обе письменности — значит чужие буквы внутри своего слова
        if kinds == {"LATIN", "CYRILLIC"}:
            return "".join(
                ch if _script_of(ch) == own else table.get(ch, ch) for ch in run
            )
        return run

    return _LETTER_RUN.sub(fix_run, value)


def _script_of(ch: str) -> str:
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return ""
    if "LATIN" in name:
        return "LATIN"
    if "CYRILLIC" in name:
        return "CYRILLIC"
    return ""


def _join_meanings(translation: dict, lang: str = "") -> str:
    """
    Собрать значения в одну строку. Разделитель — запятая: движок викторины
    разбирает по ней многозначные переводы (см. meaning_variants).

    Похожие буквы приводятся к письменности языка ДО снятия дублей: иначе
    «нареченa» с латинской «a» и «наречена» остаются двумя разными значениями
    и оба попадают в перевод.
    """
    meanings = translation.get("meanings") or []
    primary = translation.get("primary") or ""

    ordered = [primary] + [m for m in meanings if m != primary]
    if lang:
        ordered = [_fix_homoglyphs(m or "", lang) for m in ordered]

    seen, result = set(), []
    for meaning in ordered:
        key = (meaning or "").strip().lower()
        if key and key not in seen:
            seen.add(key)
            result.append(meaning.strip())

    return ", ".join(result)


def cmd_apply(args: argparse.Namespace) -> None:
    from sqlalchemy import create_engine, text

    from app.config import settings

    path = Path(args.file)
    proposals = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            proposals.append(json.loads(line))

    logger.info("предложений в файле: %d", len(proposals))

    engine = create_engine(settings.DATABASE_URL_SYNC)

    needs_review: list[dict] = []
    updates: list[dict] = []
    bad_examples: list[dict] = []

    for p in proposals:
        # Слова с сомнительной леммой или уровнем не применяем автоматически —
        # это разметка, а не перевод, и решать должен человек
        if not p.get("lemma_ok", True) or not p.get("level_ok", True) or p.get("note"):
            needs_review.append(p)
            if not args.include_flagged:
                continue

        updates.append({
            "id": p["id"],
            "article": p.get("article"),
            "ru": _join_meanings(p["ru"], "ru"),
            "uk": _join_meanings(p["uk"], "uk"),
            "en": _join_meanings(p["en"], "en"),
            "tr": _join_meanings(p["tr"], "tr"),
            "pl": _join_meanings(p["pl"], "pl"),
            # Пустую строку не пишем: лучше отсутствующий пример, чем пустой
            "example_pl": (p.get("example_pl") or "").strip() or None,
        })

        # Негодные примеры не переписываем здесь — собираем список для
        # отдельного прогона, иначе один проход отвечал бы за слишком многое
        bad = [code for code, ok in (p.get("examples_ok") or {}).items() if ok is False]
        if bad:
            bad_examples.append({"id": p["id"], "word_de": p.get("word_de"), "langs": bad})

    if needs_review:
        review_path = path.with_name(path.stem + "_needs_review.jsonl")
        with review_path.open("w", encoding="utf-8") as out:
            for p in needs_review:
                out.write(json.dumps(p, ensure_ascii=False) + "\n")
        logger.warning(
            "на ручной разбор: %d слов (неверная лемма, уровень или пометка) → %s",
            len(needs_review), review_path,
        )
        if not args.include_flagged:
            logger.warning("они НЕ будут применены; для применения — флаг --include-flagged")

    if bad_examples:
        bad_path = path.with_name(path.stem + "_bad_examples.jsonl")
        with bad_path.open("w", encoding="utf-8") as out:
            for b in bad_examples:
                out.write(json.dumps(b, ensure_ascii=False) + "\n")
        by_lang: dict[str, int] = {}
        for b in bad_examples:
            for code in b["langs"]:
                by_lang[code] = by_lang.get(code, 0) + 1
        logger.warning(
            "примеры не показывают слово: %d слов (%s) → %s",
            len(bad_examples),
            ", ".join(f"{c}: {n}" for c, n in sorted(by_lang.items())),
            bad_path,
        )

    if args.dry_run:
        print(f"\n--dry-run: применилось бы {len(updates)} слов\n")
        for u in updates[:15]:
            print(f"  id={u['id']:6} article={u['article'] or '—':4} "
                  f"ru={u['ru']}  |  pl={u['pl']}  |  {u['example_pl']}")
        if len(updates) > 15:
            print(f"  ... ещё {len(updates) - 15}")
        print()
        return

    if not updates:
        logger.info("применять нечего")
        return

    sql = text(
        """
        UPDATE words SET
            article = COALESCE(:article, article),
            translation_ru = :ru,
            translation_uk = :uk,
            translation_en = :en,
            translation_tr = :tr,
            translation_pl = :pl,
            example_pl = COALESCE(:example_pl, example_pl)
        WHERE id = :id
        """
    )

    with engine.begin() as conn:
        for chunk in chunked(updates, 500):
            conn.execute(sql, chunk)

    logger.info("обновлено слов: %d", len(updates))
    logger.warning(
        "ОБЯЗАТЕЛЬНО пересобрать группы — переводы изменились, а схлопывание "
        "дублей считается по ним:\n    python -m app.scripts.rebuild_word_groups"
    )


# ============================================================================
# CLI
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("propose", help="собрать предложения в файл")
    p.add_argument("--out", default="proposals.jsonl", help="файл с предложениями")
    p.add_argument("--levels", nargs="+", metavar="LEVEL",
                   help="уровни CEFR целиком, например: --levels A1 A2 B1")
    p.add_argument("--ids", type=int, nargs="*", help="только указанные id")
    p.add_argument("--limit", type=int, help="ограничить количество слов")
    p.add_argument("--all", action="store_true", help="вся база (равнозначно отсутствию фильтров)")
    p.add_argument("--flagged", action="store_true",
                   help="только подозрительные: служебные части речи и однозначные переводы")
    p.add_argument("--chunk", type=int, default=WORDS_PER_REQUEST,
                   help=f"слов в одном запросе (по умолчанию {WORDS_PER_REQUEST})")
    p.add_argument("--batch", action="store_true",
                   help="через Batches API: вдвое дешевле, результат в течение часа")
    p.add_argument("--estimate-only", action="store_true",
                   help="только посчитать стоимость, ничего не отправлять")
    p.set_defaults(func=cmd_propose)

    a = sub.add_parser("apply", help="применить предложения в БД")
    a.add_argument("--file", required=True, help="файл с предложениями")
    a.add_argument("--dry-run", action="store_true", help="показать, но не применять")
    a.add_argument("--include-flagged", action="store_true",
                   help="применять и слова с сомнительной леммой или уровнем")
    a.set_defaults(func=cmd_apply)

    args = parser.parse_args()

    if args.command == "propose" and not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")):
        logger.warning(
            "ANTHROPIC_API_KEY не задан — будет использован профиль `ant auth login`, "
            "если он активен (проверить: ant auth status)"
        )

    args.func(args)


if __name__ == "__main__":
    main()
