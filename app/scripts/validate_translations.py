#!/usr/bin/env python3
"""
Проверить предложения переводов ДО применения. Бесплатно, без обращения к модели.

Зачем второй слой, если то же самое сказано в запросе. Потому что сказанного
в запросе недостаточно: про турецкую «İ» в запросе было написано прямо, и всё
равно вышло 429 строк с латинской «I». Инструкция снижает долю поломок, но не
даёт гарантии, а эта проверка даёт — она не спрашивает модель, а смотрит текст.

Проверяются ровно те поломки, за исправление которых я уже платил:

  1. Перевод не в словарной форме: «смотрели» вместо «смотреть», турецкое
     «Anlıyorum» вместо «anlamak». Ловится по окончаниям: если немецкое слово
     глагол, перевод обязан быть инфинитивом.
  2. Пояснение в скобках внутри перевода: «щит (der Schild)».
  3. Немецкий текст в переводе — читающему он ничего не говорит.
  4. Украинское слово в русской колонке: оба языка кириллические, и путаница
     не видна проверкой алфавита.
  5. Турецкая «I» там, где нужна «İ».
  6. Повторы и склейки внутри massива значений.
  7. Пометы вместо значения: «Вы вежливое обращение».

Вывод — отчёт и файл с id, которые стоит переспросить. Ничего не правит:
решение применять или переспрашивать остаётся за человеком.

    python -m app.scripts.validate_translations --files wordbase_c1.jsonl
    python -m app.scripts.validate_translations --files *.jsonl --out suspect.txt
    python -m app.scripts.validate_translations --db          # уже применённое
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import LANGUAGES

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("validate")

LANGS = ("ru", "uk", "en", "tr", "pl")

# Окончания инфинитива. Проверяются только когда немецкое слово — глагол:
# у существительных и прилагательных формы другие
INFINITIVE = {
    "ru": re.compile(r"(ть|ти|ться|тись|чь|чься)$", re.IGNORECASE),
    "uk": re.compile(r"(ти|тися|тись|чи)$", re.IGNORECASE),
    "en": re.compile(r"^to\s+\w", re.IGNORECASE),
    "tr": re.compile(r"(mak|mek)$", re.IGNORECASE),
    "pl": re.compile(r"(ć|c|ąc)$", re.IGNORECASE),
}

# Спрягаемые окончания, по которым видно личную форму. Нужны, чтобы не
# ругаться на отглагольные существительные и устойчивые обороты, у которых
# инфинитивного окончания нет по делу
CONJUGATED = {
    "ru": re.compile(r"(ю|ешь|ет|ем|ете|ут|ют|ит|ят|ил|ила|или|ло|ла|ли)$",
                     re.IGNORECASE),
    "uk": re.compile(r"(ю|єш|є|ємо|єте|ють|ить|ать|в|ла|ли|ло)$", re.IGNORECASE),
    "en": re.compile(r"(ed|ing|s)$", re.IGNORECASE),
    "tr": re.compile(r"(yorum|yor|yordu|ıyor|iyor|dı|di|du|dü|lar|ler|ım|im)$",
                     re.IGNORECASE),
    "pl": re.compile(r"(am|asz|a|amy|acie|ają|em|esz|ę|ł|ła|li)$", re.IGNORECASE),
}

# Немецкий внутри перевода. Требуем связку из служебного слова и следующего
# за ним, иначе английское «an» и турецкое «an» дадут ложные срабатывания
GERMAN = re.compile(
    r"\b(es kommt|sich \w+|der \w+|die \w+|das \w+|dem \w+|den \w+|"
    r"einen \w+|einem \w+|zu \w+en|jemandem|jemanden|jmdm|jmdn|etw\.)\b",
    re.IGNORECASE,
)

# Пометы и подписи вместо значения
GLOSS = re.compile(
    r"(вежлив\w*\s+(обращени|форм)|ввічлив\w*\s+(звертанн|форм)|"
    r"nazik hitap|polite form|formal form|форма\s+обращени)",
    re.IGNORECASE,
)

# Буквы, которые есть только в украинском. Русский их не знает, поэтому в
# русской колонке они означают чужой язык, а не опечатку
UKRAINIAN_ONLY = set("іїєґІЇЄҐ")

# Турецкая заглавная I: правило и исключения совпадают с fix_turkish_i,
# который и будет её править
DOTLESS_RESTS = (
    "şı", "sı", "sla", "slı", "slah", "rk", "rmak", "rgat", "rz",
    "lık", "lıman", "lım", "zgara", "zdırap", "hlamur", "spanak",
    "stakoz", "stırap", "skarta", "skala", "ssız", "smarla", "tır", "vır",
)
TURKISH_I = re.compile(r"(?<!\w)I(\w+)", re.UNICODE)
KEEP_LATIN = ("intercity", "inline")


# Возвратная частица стоит ПОСЛЕ инфинитива и отдельным словом: польское
# «znajdować się», «spotykać się». Первая версия проверки смотрела конец строки
# целиком и объявляла эти безупречные инфинитивы личными формами — шесть
# случаев из шести оказались ложными. Правило, которое кричит на верный текст,
# обесценивает остальные его замечания.
REFLEXIVE_TAIL = {
    "pl": re.compile(r"\s+si[ęe]$", re.IGNORECASE),
    "ru": re.compile(r"\s+себя$", re.IGNORECASE),
    "uk": re.compile(r"\s+себе$", re.IGNORECASE),
    "en": re.compile(r"\s+(oneself|itself|himself|herself)$", re.IGNORECASE),
    "tr": re.compile(r"$"),
}


def strip_reflexive(value: str, lang: str) -> str:
    pattern = REFLEXIVE_TAIL.get(lang)
    return pattern.sub("", value) if pattern else value


def has_german(value: str) -> bool:
    return bool(GERMAN.search(value))


def turkish_i_wrong(value: str) -> list[str]:
    bad = []
    for match in TURKISH_I.finditer(value):
        rest = match.group(1)
        if rest[:1].isupper():
            continue
        lowered = rest.lower()
        if any(("i" + lowered).startswith(w) for w in KEEP_LATIN):
            continue
        if any(lowered.startswith(stem) for stem in DOTLESS_RESTS):
            continue
        bad.append(match.group(0))
    return bad


def script_of(value: str) -> set[str]:
    kinds = set()
    for char in value:
        if not char.isalpha():
            continue
        try:
            name = unicodedata.name(char)
        except ValueError:
            continue
        if "LATIN" in name:
            kinds.add("LATIN")
        elif "CYRILLIC" in name:
            kinds.add("CYRILLIC")
    return kinds


def language_payloads(row: dict) -> dict[str, dict]:
    """
    Достать переводы из записи предложения.

    Языки лежат верхними ключами: {"id": .., "ru": {...}, "uk": {...}}. Первая
    версия искала их под ключом "translations", не находила ничего и молча
    пропускала все 1092 записи, отвечая «придраться нечему». Проверка, которая
    не видит входа и всё равно говорит «чисто», опаснее отсутствия проверки —
    поэтому ниже пустой результат считается замечанием, а не успехом.
    """
    found = {}
    nested = row.get("translations")
    source = nested if isinstance(nested, dict) else row
    for lang in LANGS:
        payload = source.get(lang)
        if isinstance(payload, dict) and (payload.get("primary")
                                          or payload.get("meanings")):
            found[lang] = payload
    return found


def check_entry(word_de: str, pos: str, row: dict) -> list[str]:
    """Что не так с переводами одного слова. Пустой список — придраться нечему."""
    problems: list[str] = []
    payloads = language_payloads(row)

    if not payloads:
        return ["переводов в записи не найдено — проверять нечего, "
                "форма записи не та, что ожидалась"]

    for lang, payload in payloads.items():
        meanings = [m for m in (payload.get("meanings") or []) if m]
        primary = (payload.get("primary") or "").strip()
        # primary по устройству и есть первый элемент meanings, поэтому
        # значения берутся из meanings, а primary добавляется только если его
        # там нет
        values = list(meanings)
        if primary and primary not in values:
            values.insert(0, primary)
        if not values:
            continue

        for value in values:
            if "(" in value or ")" in value:
                problems.append(f"{lang}: пояснение в скобках — {value!r}")
            if "/" in value:
                problems.append(f"{lang}: косая черта — {value!r}")
            if has_german(value):
                problems.append(f"{lang}: немецкий текст — {value!r}")
            if GLOSS.search(value):
                problems.append(f"{lang}: помета вместо значения — {value!r}")
            if "," in value or ";" in value:
                problems.append(f"{lang}: несколько значений в одном элементе — {value!r}")

        # Чужой язык в кириллической колонке
        if lang == "ru":
            for value in values:
                if set(value) & UKRAINIAN_ONLY:
                    problems.append(f"ru: украинские буквы — {value!r}")
        if lang in ("ru", "uk") and any("LATIN" in script_of(v) for v in values):
            problems.append(f"{lang}: латиница в переводе — {values!r}")
        if lang in ("en", "tr", "pl") and any("CYRILLIC" in script_of(v) for v in values):
            problems.append(f"{lang}: кириллица в переводе — {values!r}")

        # Турецкая заглавная I
        if lang == "tr":
            for value in values:
                wrong = turkish_i_wrong(value)
                if wrong:
                    problems.append(f"tr: нужна İ вместо I — {wrong} в {value!r}")

        # Повтор одного значения внутри meanings. Совпадение primary с первым
        # элементом повтором не считается: так задумано
        folded = [v.strip().lower() for v in meanings]
        if len(folded) != len(set(folded)):
            problems.append(f"{lang}: значение повторено — {meanings!r}")

        # Словарная форма: только для глаголов, и только по primary
        if pos == "VERB" and primary:
            head = strip_reflexive(primary.strip(), lang)
            if not INFINITIVE[lang].search(head) and CONJUGATED[lang].search(head):
                problems.append(f"{lang}: не инфинитив — {primary!r}")

    return problems


def load_proposals(paths: list[str]) -> list[dict]:
    rows = []
    for path in paths:
        file = pathlib.Path(path)
        if not file.exists():
            logger.warning("нет файла %s", path)
            continue
        for line in file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_from_db() -> list[dict]:
    """Уже применённые переводы — в том же виде, что предложения."""
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(LANGUAGES[l].word_attr for l in LANGS)
    with engine.connect() as conn:
        rows = conn.execute(text(
            f"SELECT id, word_de, pos::text AS pos, {cols} FROM words"
        )).mappings().all()

    out = []
    for row in rows:
        entry = {"id": row["id"], "word_de": row["word_de"], "pos": row["pos"]}
        for lang in LANGS:
            value = (row[LANGUAGES[lang].word_attr] or "").strip()
            if not value:
                continue
            parts = [p.strip() for p in re.split(r"\s*,\s*", value) if p.strip()]
            # В базе значения лежат одной строкой через запятую; primary —
            # первое из них, и в meanings он входит законно
            entry[lang] = {"primary": parts[0] if parts else "", "meanings": parts}
        out.append(entry)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--db", action="store_true",
                    help="проверять уже применённое в базе, а не предложения")
    ap.add_argument("--out", default="translations_suspect.txt",
                    help="файл с id для переспроса")
    ap.add_argument("--show", type=int, default=25)
    args = ap.parse_args()

    if args.db:
        rows = load_from_db()
        # Части речи в базе есть; у предложений её нет, подставим из базы
        pos_by_id = {r["id"]: r["pos"] for r in rows}
    else:
        if not args.files:
            ap.error("нужен --files или --db")
        rows = load_proposals(args.files)
        engine = create_engine(settings.DATABASE_URL_SYNC)
        with engine.connect() as conn:
            pos_by_id = {
                r["id"]: r["pos"]
                for r in conn.execute(text(
                    "SELECT id, pos::text AS pos FROM words WHERE id = ANY(:ids)"
                ), {"ids": [r["id"] for r in rows]}).mappings()
            }

    if not rows:
        logger.error("проверять нечего")
        return 1

    kinds: dict[str, int] = {}
    suspect: list[tuple[int, str, list[str]]] = []

    for row in rows:
        pos = row.get("pos") or pos_by_id.get(row["id"], "")
        problems = check_entry(row.get("word_de", ""), pos, row)
        if not problems:
            continue
        suspect.append((row["id"], row.get("word_de", ""), problems))
        for problem in problems:
            key = problem.split(" — ")[0]
            kinds[key] = kinds.get(key, 0) + 1

    print(f"=== проверено записей: {len(rows)} ===")
    print(f"  с замечаниями: {len(suspect)} ({len(suspect) / len(rows) * 100:.2f}%)")
    print()
    if kinds:
        print("  по видам:")
        for key, count in sorted(kinds.items(), key=lambda kv: -kv[1]):
            print(f"    {count:>5}  {key}")
        print()

    for word_id, word, problems in suspect[:args.show]:
        print(f"  id={word_id} {word!r}")
        for problem in problems[:4]:
            print(f"      {problem}")

    if suspect:
        path = pathlib.Path(args.out)
        path.write_text(" ".join(str(i) for i, _, _ in suspect), encoding="utf-8")
        print()
        print(f"  id для переспроса: {len(suspect)} → {path}")
        print("  Турецкую İ и склейки значений править деньгами не нужно:")
        print("    python -m app.scripts.fix_turkish_i --apply")
    else:
        print("  придраться нечему")
    return 0


if __name__ == "__main__":
    sys.exit(main())
