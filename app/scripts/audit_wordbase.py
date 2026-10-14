#!/usr/bin/env python3
"""
Аудит качества словарной базы.

Читать 12 900 слов × 4 языка глазами бессмысленно: 51 600 переводов не
поместятся ни в один обзор, и внимание размажется. Поэтому сначала машина
подсвечивает подозрительное по формальным признакам, а разбирать вручную
нужно только то, что попало в отчёт.

Проверки и их важность выставлены по результатам сверки с прод-статистикой
(193 слова с не менее 15 показами, 28 082 ответа):

  ПОДТВЕРЖДЕНО данными:
  * служебные части речи с единственным значением — точность 71.0% против
    80.0% у остальных, и первым вопросом такое слово стоит в 24.2% сессий,
    брошенных за два вопроса, против 14.7% доигранных;
  * чужой алфавит в колонке и отсутствующий перевод — прямая поломка;
  * потерянные турецкие диакритики («ornek» вместо «örnek»).

  НЕ ПОДТВЕРЖДЕНО, важность понижена:
  * редкое для уровня слово — у таких слов точность ВЫШЕ (79.7% против
    76.5%), и они скорее удерживают, чем отпугивают. Частотный ранг считан
    по общему корпусу и плохо описывает учебную лексику;
  * совпадение перевода с немецким словом в en и tr — это интернационализмы
    (optimal, September, Pizza), а не ошибка.

  НЕ ПРОВЕРЯЕМО на текущих данных:
  * многозначность в одной ячейке — слов с достаточной выборкой всего три,
    вывода сделать нельзя. Замечание оставлено как сигнал для ручного разбора.

Usage:
  python -m app.scripts.audit_wordbase --csv path/to/words.csv
  python -m app.scripts.audit_wordbase --csv words.csv --difficulty a_word_difficulty.csv
  python -m app.scripts.audit_wordbase --csv words.csv --level A1 --out report.md
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

csv.field_size_limit(10_000_000)

LANGS = ("ru", "uk", "en", "tr")

# Алфавиты, ожидаемые в каждой колонке
CYRILLIC = re.compile(r"[а-яёіїєґА-ЯЁІЇЄҐ]")
LATIN = re.compile(r"[a-zA-Zäöüßàâçéèêëîïôûùüÿñæœğışçöü]", re.IGNORECASE)

# Турецкие буквы, которые чаще всего теряются при переносе данных
TURKISH_SPECIFIC = set("çğıöşüÇĞİÖŞÜ")

SEPARATORS = re.compile(r"[/;,]")

EN_VERB_PREFIX = re.compile(r"^to\s+", re.IGNORECASE)

GERMAN_ARTICLES = {"der", "die", "das"}


@dataclass
class Finding:
    kind: str
    severity: str  # high / medium / low
    word_id: str
    word_de: str
    level: str
    pos: str
    detail: str


@dataclass
class Audit:
    findings: list[Finding] = field(default_factory=list)
    counts: Counter = field(default_factory=Counter)

    def add(self, kind, severity, row, detail):
        self.counts[kind] += 1
        self.findings.append(Finding(
            kind=kind,
            severity=severity,
            word_id=str(row.get("id", "")),
            word_de=row.get("word_de", ""),
            level=row.get("level", ""),
            pos=row.get("pos", ""),
            detail=detail,
        ))


def _clean(value) -> str:
    return (value or "").strip()


def _has_script(text: str, pattern: re.Pattern) -> bool:
    return bool(pattern.search(text))


def _strip_diacritics(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


# ============================================================================
# ПРОВЕРКИ
# ============================================================================

def check_missing_or_echo(audit: Audit, row: dict) -> None:
    """Перевода нет либо он дословно повторяет исходное слово."""
    word_de = _clean(row.get("word_de")).lower()

    for lang in LANGS:
        value = _clean(row.get(f"translation_{lang}"))
        if not value:
            audit.add("missing_translation", "high", row, f"{lang}: пусто")
            continue
        if value.lower() == word_de:
            # Для английского и турецкого совпадение обычно законно:
            # optimal, Generation, September, Pizza, Kilo — интернационализмы.
            # Проверка по выгрузке: 648 таких в en и 214 в tr, почти все верны.
            # А вот в русском и украинском латиница означает, что перевода нет.
            severity = "low" if lang in ("en", "tr") else "high"
            kind = "cognate" if lang in ("en", "tr") else "translation_equals_source"
            audit.add(kind, severity, row, f"{lang}: «{value}» совпадает с немецким словом")


def check_wrong_script(audit: Audit, row: dict) -> None:
    """Кириллица в латинской колонке и наоборот — перепутаны языки."""
    for lang in ("ru", "uk"):
        value = _clean(row.get(f"translation_{lang}"))
        if value and not _has_script(value, CYRILLIC):
            audit.add(
                "wrong_script", "high", row,
                f"{lang}: «{value}» без кириллицы",
            )

    for lang in ("en", "tr"):
        value = _clean(row.get(f"translation_{lang}"))
        if value and _has_script(value, CYRILLIC):
            audit.add(
                "wrong_script", "high", row,
                f"{lang}: «{value}» содержит кириллицу",
            )


def check_turkish_diacritics(audit: Audit, row: dict) -> None:
    """
    Потерянные турецкие диакритики.

    В базе замечено «ornek» вместо «örnek»: признак того, что данные прошли
    через транслитерацию. Для турецкого это меняет слово, а не только вид.

    Образца «iyi» здесь намеренно НЕТ, хотя он тут был. «iyi» (хороший)
    пишется без диакритики вовсе, и проверка срабатывала на совершенно верном
    турецком: «daha iyi», «en iyi», «iyi kalpli insan». Из 15 замечаний 15
    были ложными.

    Попал он сюда из-за «Iyi» вместо «İyi» — а это настоящий и другой дефект:
    заглавная от «i» по-турецки «İ», и его ловит app/scripts/fix_turkish_i.py,
    где правило различает дотted и дотless основы и покрыто тестами.

    Смешивать их нельзя. Проверка, которая кричит на верный текст, учит
    не доверять и остальным её замечаниям.
    """
    value = _clean(row.get("translation_tr"))
    if not value:
        return

    # Слово из турецких букв, но ни одной специфической — подозрительно,
    # если в нём есть сочетания, которые по-турецки почти всегда с диакритикой
    if any(c in TURKISH_SPECIFIC for c in value):
        return

    suspicious = re.search(r"\b(ornek|ogren|gun|goz|soz|yuz|buyuk|kucuk|opmek|dusun)\w*",
                           value, re.IGNORECASE)
    if suspicious:
        audit.add(
            "turkish_diacritics", "medium", row,
            f"tr: «{value}» похоже на потерю диакритики",
        )


def check_polysemy(audit: Audit, row: dict) -> None:
    """
    Многозначность без разметки.

    Главная причина ошибок на A1: служебному слову присвоено одно значение
    из нескольких, и в тесте из четырёх вариантов ученик угадывает выбор базы,
    а не язык. Служебные части речи выделяем отдельно — там эффект сильнее.
    """
    pos = _clean(row.get("pos")).upper()
    functional = pos in {"PRONOUN", "PREPOSITION", "CONJUNCTION", "ADVERB", "OTHER"}

    for lang in LANGS:
        value = _clean(row.get(f"translation_{lang}"))
        if not value:
            continue
        variants = [v.strip() for v in SEPARATORS.split(value) if v.strip()]
        if len(variants) > 1:
            audit.add(
                "multi_variant", "medium" if functional else "low", row,
                f"{lang}: {len(variants)} значения — «{value}»",
            )

    # Служебное слово с единственным значением — тоже риск: оно почти
    # наверняка многозначно, но в базе размечено одним смыслом
    if functional:
        single = all(
            len([v for v in SEPARATORS.split(_clean(row.get(f"translation_{lang}"))) if v.strip()]) <= 1
            for lang in LANGS
        )
        if single:
            audit.add(
                "functional_word_single_meaning", "high", row,
                f"{pos} с одним значением: ru=«{_clean(row.get('translation_ru'))}»",
            )


def check_example_contains_word(audit: Audit, row: dict) -> None:
    """Немецкий пример должен содержать само слово, иначе он не к нему."""
    word = _clean(row.get("word_de"))
    example = _clean(row.get("example_de"))
    if not word or not example:
        return

    # Сравниваем по началу слова: словоформы отличаются окончаниями
    stem = word[:max(4, len(word) - 3)].lower()
    if stem and stem not in example.lower():
        audit.add(
            "example_missing_word", "medium", row,
            f"пример «{example}» не содержит «{word}»",
        )


def check_english_verb_prefix(audit: Audit, row: dict) -> None:
    """Несогласованность «to » у английских глаголов."""
    if _clean(row.get("pos")).upper() != "VERB":
        return
    value = _clean(row.get("translation_en"))
    if not value:
        return
    if not EN_VERB_PREFIX.match(value):
        audit.add(
            "en_verb_without_to", "low", row,
            f"en: «{value}» без «to»",
        )


def check_article(audit: Audit, row: dict) -> None:
    """Существительное без артикля либо артикль у не-существительного."""
    pos = _clean(row.get("pos")).upper()
    article = _clean(row.get("article")).lower()

    if pos == "NOUN":
        if not article or article == "-":
            audit.add("noun_without_article", "medium", row, "существительное без артикля")
        elif article not in GERMAN_ARTICLES:
            audit.add("bad_article", "medium", row, f"артикль «{article}»")
    elif article and article != "-" and article in GERMAN_ARTICLES:
        audit.add("article_on_non_noun", "low", row, f"{pos} с артиклем «{article}»")


def check_level_plausibility(audit: Audit, row: dict) -> None:
    """
    Редкое слово на начальном уровне.

    Пример с прода: Kichererbse (нут) размечено как A1 — в A1-лексику такое
    не входит. Частотный ранг даёт грубую, но работающую проверку.
    """
    level = _clean(row.get("level")).upper()
    rank_raw = _clean(row.get("frequency_rank"))

    if level not in {"A1", "A2"} or not rank_raw:
        return
    try:
        rank = int(float(rank_raw))
    except ValueError:
        return

    threshold = 3000 if level == "A1" else 6000
    if rank > threshold:
        # Важность низкая осознанно. Проверка по прод-данным: у «редких для
        # уровня» слов точность 79.7% против 76.5% у нормальных, а первым
        # вопросом они стоят в 22.4% брошенных сессий против 29.7%
        # доигранных — то есть они скорее УДЕРЖИВАЮТ. Частотный ранг считан
        # по общему корпусу и плохо описывает учебную лексику: Teelöffel и
        # Familienname редки в корпусе, но входят в любой курс для начинающих.
        # Замечание оставлено как сигнал о разметке, не о трудности.
        audit.add(
            "level_too_low_for_rarity", "low", row,
            f"{level} при частотном ранге {rank} (порог {threshold})",
        )


def check_length_anomaly(audit: Audit, row: dict) -> None:
    """Перевод сильно длиннее слова — вероятно, там определение, а не перевод."""
    word = _clean(row.get("word_de"))
    if not word:
        return
    for lang in LANGS:
        value = _clean(row.get(f"translation_{lang}"))
        if value and len(value) > max(40, len(word) * 4):
            audit.add(
                "translation_too_long", "low", row,
                f"{lang}: {len(value)} символов — «{value[:60]}…»",
            )


def check_lemma_form(audit: Audit, row: dict) -> None:
    """
    Слово записано не в словарной форме.

    В немецком существительные всегда с заглавной буквы — строчная означает,
    что в колонку попала не та форма либо неверная часть речи. Так в базе
    нашлись «lieblings» (несамостоятельная морфема) и «Alben» (множественное
    число вместо леммы «Album»).
    """
    word = _clean(row.get("word_de"))
    pos = _clean(row.get("pos")).upper()
    if not word:
        return

    if pos == "NOUN" and word[:1].islower():
        audit.add("noun_lowercase", "high", row, f"существительное «{word}» со строчной")

    if word.endswith("-") or word.startswith("-"):
        audit.add("bound_morpheme", "high", row, f"«{word}» не самостоятельное слово")


CHECKS = (
    check_missing_or_echo,
    check_lemma_form,
    check_wrong_script,
    check_turkish_diacritics,
    check_polysemy,
    check_example_contains_word,
    check_english_verb_prefix,
    check_article,
    check_level_plausibility,
    check_length_anomaly,
)


# ============================================================================
# ДУБЛИ
# ============================================================================

def check_duplicates(audit: Audit, rows: list[dict]) -> dict:
    """Строки, дающие один и тот же headword — по каждому языку."""
    summary = {}

    for lang in ("de",) + LANGS:
        column = "word_de" if lang == "de" else f"translation_{lang}"
        groups: dict[tuple, list[dict]] = defaultdict(list)

        for row in rows:
            value = _clean(row.get(column)).lower()
            if not value:
                continue
            first = SEPARATORS.split(value)[0].strip()
            if lang == "en":
                first = EN_VERB_PREFIX.sub("", first)
            key = (first, _clean(row.get("pos")).upper())
            groups[key].append(row)

        collisions = {k: v for k, v in groups.items() if len(v) > 1}
        extra = sum(len(v) - 1 for v in collisions.values())
        summary[lang] = {
            "unique": len(groups),
            "collision_groups": len(collisions),
            "extra_rows": extra,
        }

        # Крупные группы стоят внимания: обычно это ошибка разметки
        for (text, pos), members in sorted(collisions.items(), key=lambda x: -len(x[1]))[:15]:
            if len(members) >= 4:
                words = ", ".join(_clean(m.get("word_de")) for m in members[:6])
                audit.add(
                    "large_duplicate_group", "medium", members[0],
                    f"{lang}: «{text}» ({pos}) — {len(members)} слов: {words}",
                )

    return summary


# ============================================================================
# СВЯЗЬ С ПРОД-СТАТИСТИКОЙ
# ============================================================================

def load_difficulty(path: Path) -> dict[str, dict]:
    """Прод-данные по точности ответов — внешний сигнал качества перевода."""
    if not path or not path.exists():
        return {}

    stats = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            wid = _clean(row.get("word_id") or row.get("id"))
            if wid:
                stats[wid] = row
    return stats


# ============================================================================
# ОТЧЁТ
# ============================================================================

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

KIND_TITLES = {
    "missing_translation": "Перевод отсутствует",
    "translation_equals_source": "Перевод совпадает с исходным словом",
    "wrong_script": "Чужой алфавит в колонке",
    "turkish_diacritics": "Потеря турецких диакритиков",
    "functional_word_single_meaning": "Служебное слово с одним значением",
    "multi_variant": "Несколько значений в одной ячейке",
    "example_missing_word": "Пример не содержит слова",
    "en_verb_without_to": "Английский глагол без «to»",
    "noun_without_article": "Существительное без артикля",
    "bad_article": "Некорректный артикль",
    "article_on_non_noun": "Артикль не у существительного",
    "level_too_low_for_rarity": "Редкое слово на начальном уровне",
    "translation_too_long": "Перевод подозрительно длинный",
    "large_duplicate_group": "Крупная группа дублей",
    "cognate": "Совпадает с немецким (интернационализм, обычно верно)",
    "noun_lowercase": "Существительное со строчной буквы",
    "bound_morpheme": "Не самостоятельное слово",
}


def build_report(audit: Audit, rows: list[dict], dup_summary: dict,
                 difficulty: dict, level_filter: str | None) -> str:
    total = len(rows)
    lines = []

    lines.append("# Аудит словарной базы\n")
    lines.append(f"Проверено строк: **{total}**")
    if level_filter:
        lines.append(f"Фильтр уровня: **{level_filter}**")
    lines.append("")

    lines.append("## Сводка по проверкам\n")
    lines.append("| Проверка | Найдено | Важность |")
    lines.append("|---|---:|---|")

    by_kind = defaultdict(list)
    for f in audit.findings:
        by_kind[f.kind].append(f)

    ordered = sorted(
        by_kind.items(),
        key=lambda kv: (SEVERITY_ORDER.get(kv[1][0].severity, 9), -len(kv[1])),
    )
    for kind, items in ordered:
        title = KIND_TITLES.get(kind, kind)
        pct = len(items) * 100 / total if total else 0
        lines.append(f"| {title} | {len(items)} ({pct:.1f}%) | {items[0].severity} |")
    lines.append("")

    lines.append("## Дубли headword по языкам\n")
    lines.append("Сколько строк дают одно и то же слово на каждом языке.\n")
    lines.append("| Язык | Уникальных слов | Групп дублей | Лишних строк |")
    lines.append("|---|---:|---:|---:|")
    for lang, s in dup_summary.items():
        lines.append(
            f"| {lang} | {s['unique']} | {s['collision_groups']} | {s['extra_rows']} |"
        )
    lines.append("")

    # Детали по важным категориям
    for kind, items in ordered:
        if items[0].severity == "low" and len(items) > 50:
            continue

        title = KIND_TITLES.get(kind, kind)
        lines.append(f"## {title} — {len(items)}\n")

        shown = items[:40]
        lines.append("| id | Слово | Уровень | Часть речи | Что не так |")
        lines.append("|---|---|---|---|---|")
        for f in shown:
            detail = f.detail.replace("|", "\\|")
            lines.append(
                f"| {f.word_id} | {f.word_de} | {f.level} | {f.pos} | {detail} |"
            )
        if len(items) > len(shown):
            lines.append(f"\n_Показано {len(shown)} из {len(items)}._")
        lines.append("")

    if difficulty:
        lines.append("## Пересечение с прод-статистикой\n")
        flagged_ids = {f.word_id for f in audit.findings if f.severity == "high"}
        hit = [wid for wid in flagged_ids if wid in difficulty]
        lines.append(
            f"Слов с важными замечаниями, по которым есть статистика ответов: "
            f"**{len(hit)}** из {len(flagged_ids)}.\n"
        )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Выгрузка таблицы words")
    parser.add_argument("--difficulty", help="a_word_difficulty.csv с прод-статистикой")
    parser.add_argument("--level", help="Проверить только один уровень CEFR")
    parser.add_argument("--out", help="Файл отчёта (по умолчанию stdout)")
    args = parser.parse_args()

    path = Path(args.csv)
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if args.level:
        rows = [r for r in rows if _clean(r.get("level")).upper() == args.level.upper()]

    audit = Audit()
    for row in rows:
        for check in CHECKS:
            check(audit, row)

    dup_summary = check_duplicates(audit, rows)
    difficulty = load_difficulty(Path(args.difficulty)) if args.difficulty else {}

    report = build_report(audit, rows, dup_summary, difficulty, args.level)

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Отчёт записан: {args.out}")
        print(f"Всего замечаний: {len(audit.findings)}")
        for kind, count in audit.counts.most_common():
            print(f"  {KIND_TITLES.get(kind, kind)}: {count}")
    else:
        print(report)


if __name__ == "__main__":
    main()
