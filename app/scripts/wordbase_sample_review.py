# -*- coding: utf-8 -*-
"""
Выборочная проверка словарной базы: случайные ряды на разбор глазами.

Зачем не автоматическая проверка. Формальные вещи — диакритику, чужой алфавит,
артикль из списка, наличие слова в примере — уже проверяют другие скрипты, и
их выводы в этом отчёте показаны рядом. Но «естественный ли перевод» и «так ли
говорят живые люди» формальными правилами не берётся: это языковое суждение.
Поэтому задача скрипта — вытащить честно случайную выборку, привести её к виду,
в котором ряд читается за секунды, и не мешать судить.

Выборка случайная, но воспроизводимая: зерно печатается в заголовке. Одну и ту
же выборку можно вызвать повторно и сверить оценку.

Выборка расслоена по уровням CEFR пропорционально их доле в базе. Без этого
случайные 100 рядов пришли бы в основном с B2 и C1 — их в базе больше всего, —
и качество A1, который видит большинство учеников, осталось бы непроверенным.

    python -m app.scripts.wordbase_sample_review --rounds 10 --size 100
    python -m app.scripts.wordbase_sample_review --round 3 --size 100
    python -m app.scripts.wordbase_sample_review --rounds 1 --size 40 --lang pl
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import random
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS

# Зерно по умолчанию: выборка должна быть воспроизводимой, чтобы к оценке
# можно было вернуться и сверить её
BASE_SEED = 20260930

LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")

# Формальные признаки, которые стоит показать рядом с рядом: они не решают
# за проверяющего, но экономят его внимание
LATIN_LANGS = {"de", "en", "tr", "pl"}
CYRILLIC_LANGS = {"ru", "uk"}

# Подсказки про диакритику здесь нет намеренно. Она была, и соврала на первом
# же ряду: «Seine Aufrichtigkeit in der Beziehung war bewundernswert» —
# безупречный немецкий без единого умлаута. Украинская фраза «Чи можемо ми
# трохи прискорити темп?» — то же самое. Подсказка, которая врёт, учит
# игнорировать все остальные, поэтому она убрана. Транслит вместо турецкой
# диакритики ловит app/scripts/audit_wordbase.py — там проверка точная,
# по конкретным буквам.


def script_of(value: str) -> set[str]:
    kinds = set()
    for ch in value:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if "LATIN" in name:
            kinds.add("LATIN")
        elif "CYRILLIC" in name:
            kinds.add("CYRILLIC")
    return kinds


def formal_notes(row: dict, langs: list[str]) -> list[str]:
    """
    Что видно без языкового суждения.

    Это подсказки проверяющему, а не приговор: пустой список не означает
    «перевод хороший», он означает «формально придраться не к чему».
    """
    notes: list[str] = []

    for lang in langs:
        cfg = LANGUAGES[lang]
        word = (row.get(cfg.word_attr) or "").strip()
        example = (row.get(cfg.example_attr) or "").strip()

        if not word:
            # Отсутствие перевода — вопрос покрытия, а не качества, и оно
            # считается отдельно в заголовке. Иначе частично заполненный язык
            # затопляет отчёт: польский есть только на A1 и A2, и «перевода
            # нет» давало 78% замечаний на выборке по всем уровням.
            continue
        if not example:
            notes.append(f"{lang}: примера нет")

        kinds = script_of(word)
        if lang in LATIN_LANGS and "CYRILLIC" in kinds:
            notes.append(f"{lang}: кириллица в переводе — {word!r}")
        if lang in CYRILLIC_LANGS and "LATIN" in kinds:
            notes.append(f"{lang}: латиница в переводе — {word!r}")

        # Пометки в скобках и косые черты мешают и озвучке, и вариантам ответа
        if "(" in word:
            notes.append(f"{lang}: пояснение в скобках — {word!r}")
        # Косая черта здесь не проверяется: она не дефект. И разбор значений
        # в викторине (meaning_variants), и озвучка (word_clip_text) режут
        # по «,;/» одинаково, так что «Darn / blast» работает как надо.

    # Артикль осмыслен только у существительных
    article = (row.get("article") or "").strip()
    if row["pos"] == "NOUN" and article in ("", "-"):
        notes.append("существительное без артикля")
    if row["pos"] != "NOUN" and article not in ("", "-"):
        notes.append(f"артикль у не-существительного: {article}")

    # Немецкие существительные пишутся с заглавной
    word_de = (row.get("word_de") or "").strip()
    if row["pos"] == "NOUN" and word_de and word_de[0].islower():
        notes.append(f"существительное со строчной: {word_de!r}")

    return notes


async def filled_languages(langs: list[str]) -> list[str]:
    """
    Какие языки в базе вообще заполнены.

    Пустая колонка иначе помечала бы каждый ряд замечанием «перевода нет», и
    в этом шуме утонули бы настоящие находки. Польский до прогона переводов
    именно такой.
    """
    async with AsyncSessionLocal() as s:
        filled = []
        for lang in langs:
            cfg = LANGUAGES[lang]
            count = await s.scalar(text(
                f"SELECT COUNT(*) FROM words "
                f"WHERE {cfg.word_attr} IS NOT NULL "
                f"AND btrim({cfg.word_attr}) <> ''"
            ))
            if count:
                filled.append(lang)
    return filled


async def load_pool(lang_filter: str | None) -> list[dict]:
    attrs = []
    for lang in SUPPORTED_LANGS:
        cfg = LANGUAGES[lang]
        attrs.append(f"w.{cfg.word_attr}")
        attrs.append(f"w.{cfg.example_attr}")
    columns = ", ".join(dict.fromkeys(attrs))

    where = ""
    params: dict = {}
    if lang_filter:
        cfg = LANGUAGES[lang_filter]
        where = (f"WHERE w.{cfg.word_attr} IS NOT NULL "
                 f"AND btrim(w.{cfg.word_attr}) <> ''")

    async with AsyncSessionLocal() as s:
        rows = (await s.execute(text(f"""
            SELECT w.id, w.article, w.pos::text AS pos, w.level::text AS level,
                   w.frequency_rank, {columns}
            FROM words w
            {where}
            ORDER BY w.id
        """), params)).mappings().all()
    return [dict(r) for r in rows]


def stratified_sample(pool: list[dict], size: int, seed: int) -> list[dict]:
    """
    Выборка, расслоенная по уровням пропорционально их доле в базе.

    Иначе случайные 100 рядов пришли бы в основном с B2 и C1, которых в базе
    больше всего, и качество A1 — того, что видит большинство — осталось бы
    непроверенным.
    """
    rng = random.Random(seed)
    by_level: dict[str, list[dict]] = {}
    for row in pool:
        by_level.setdefault(row["level"], []).append(row)

    chosen: list[dict] = []
    for level in LEVELS:
        bucket = by_level.get(level, [])
        if not bucket:
            continue
        share = len(bucket) / len(pool)
        want = max(1, round(size * share))
        chosen.extend(rng.sample(bucket, min(want, len(bucket))))

    rng.shuffle(chosen)
    return chosen[:size]


def render(row: dict, langs: list[str], index: int) -> str:
    article = (row.get("article") or "").strip()
    head = row.get("word_de") or ""
    if article and article != "-":
        head = f"{article} {head}"

    lines = [
        f"─── {index}. {head}   [{row['pos']}, {row['level']}"
        + (f", ранг {row['frequency_rank']}" if row.get("frequency_rank") else "")
        + f", id={row['id']}]"
    ]
    for lang in langs:
        cfg = LANGUAGES[lang]
        word = (row.get(cfg.word_attr) or "—").strip() or "—"
        example = (row.get(cfg.example_attr) or "").strip()
        lines.append(f"    {lang}  {word}")
        if example:
            lines.append(f"        · {example}")

    for note in formal_notes(row, langs):
        lines.append(f"    ! {note}")
    return "\n".join(lines)


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rounds", type=int, default=1,
                    help="сколько выборок подряд (для 10 × 100)")
    ap.add_argument("--round", type=int, dest="single_round",
                    help="только одна конкретная выборка по номеру")
    ap.add_argument("--size", type=int, default=100, help="рядов в выборке")
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS),
                    help="проверять один язык, а не все")
    ap.add_argument("--seed", type=int, default=BASE_SEED)
    ap.add_argument("--only-flagged", action="store_true",
                    help="печатать только ряды с формальными замечаниями")
    args = ap.parse_args()

    requested = [args.lang] if args.lang else list(SUPPORTED_LANGS)
    langs = await filled_languages(requested)
    skipped = [c for c in requested if c not in langs]

    pool = await load_pool(args.lang)
    if not pool or not langs:
        print("в базе нет подходящих слов")
        return 1

    rounds = [args.single_round] if args.single_round else list(range(1, args.rounds + 1))

    print(f"база: {len(pool)} слов, языки: {' '.join(langs)}")
    if skipped:
        print(f"пропущены незаполненные языки: {' '.join(skipped)}")
    print(f"зерно {args.seed} — выборка воспроизводима")
    print()

    grand_flagged = 0
    grand_shown = 0

    for number in rounds:
        seed = args.seed + number
        sample = stratified_sample(pool, args.size, seed)
        flagged = [r for r in sample if formal_notes(r, langs)]
        grand_flagged += len(flagged)
        grand_shown += len(sample)

        by_level: dict[str, int] = {}
        for row in sample:
            by_level[row["level"]] = by_level.get(row["level"], 0) + 1

        coverage = {}
        for lang in langs:
            cfg = LANGUAGES[lang]
            have = sum(1 for r in sample if (r.get(cfg.word_attr) or "").strip())
            coverage[lang] = have

        print("=" * 72)
        print(f"ВЫБОРКА {number}: {len(sample)} рядов, зерно {seed}")
        print("  покрытие: " + ", ".join(
            f"{lang} {coverage[lang]}" for lang in langs
        ) + "  (это покрытие, не качество)")
        print("  по уровням: " + ", ".join(f"{lv} {by_level.get(lv, 0)}" for lv in LEVELS))
        print(f"  с формальными замечаниями: {len(flagged)} "
              f"({len(flagged) / len(sample) * 100:.0f}%)")
        print("=" * 72)
        print()

        shown = flagged if args.only_flagged else sample
        for index, row in enumerate(shown, 1):
            print(render(row, langs, index))
            print()

    if len(rounds) > 1:
        print("=" * 72)
        print(f"ИТОГО по {len(rounds)} выборкам: рядов {grand_shown}, "
              f"с формальными замечаниями {grand_flagged} "
              f"({grand_flagged / grand_shown * 100:.1f}%)")
        print("Формальные замечания — это подсказки, а не оценка качества.")
        print("Естественность перевода они не проверяют: это разбор глазами.")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
