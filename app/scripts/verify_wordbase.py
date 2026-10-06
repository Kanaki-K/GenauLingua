"""Приёмка базы: 100 раз по 100 случайных рядов, все проверки сразу.

Зачем, если каждая примета и так прогоняется по всей базе. Приметы
смотрят каждая в свою сторону и по очереди. Здесь по одному и тому же
ряду проходят ВСЕ проверки вместе, включая ту, которой ни у одной
приметы нет, — доходит ли дело до озвучки.

Главная проверка здесь последняя: **есть ли на диске тот клип, который
запросит карточка.** Она закрывает всю цепочку целиком —
`main_meaning` выбрал значение, `spoken_for` собрал произносимый текст,
хеш от текста дал имя файла, файл лежит. Если сходится, то показанное,
произнесённое и название клипа — одно и то же, а это и есть требование
владельца из HANDOVER §8.

ПОЧЕМУ 100 РАЗ ПО 100, А НЕ ОДИН РАЗ ПО 10 000. Разом по всей базе
каждая примета уже прогнана, и там ноль. Выборками видно другое:
РОВНО ли распределён остаток. Если бы дефекты сидели кучей в одном
месте базы, сто независимых выборок это показали бы — часть раундов
упала бы, остальные прошли. Один общий прогон такую кучу усреднил бы.

Зерно зафиксировано: прогон воспроизводим, и «у меня не падает»
означает то же самое у владельца.

НИ ОДНА ПРОВЕРКА ЗДЕСЬ НЕ НАПИСАНА ЗАНОВО. Все предикаты взяты из
примет и из рабочего кода бота. Это не вежливость, а дважды оплаченный
урок: своя копия расчёта расходится с оригиналом и начинает врать.
В последний раз такая копия объявила бы сиротами правильные клипы
озвучки на 5561 карточке.

    python -m app.scripts.verify_wordbase
    python -m app.scripts.verify_wordbase --rounds 10 --size 50
    python -m app.scripts.verify_wordbase --no-audio   # без проверки диска
"""

from __future__ import annotations

import argparse
import os
import pathlib
import random
import sys
from collections import Counter
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.audio_service import KIND_FULL, KIND_WORD, spoken_for
from app.services.audio_store import DEFAULT_ROOT, clip_path
from app.services.language_service import LANGUAGES
from app.services.tts_voices import default_voice

# Предикаты примет. Своих копий здесь нет и быть не должно.
from app.scripts import (  # noqa: E402
    scan_alien_letter,
    scan_de_colloquial,
    scan_formality_vs_de,
    scan_number_mismatch,
    scan_tr_number_suffix,
    scan_uk_copula_je,
)

LANGS = ("de", "en", "ru", "uk", "tr", "pl")
SEED = 20261006

# Столбцы, которые читаются у каждого ряда
COLS = ["id", "article", "word_de", "example_de"]
for _l in LANGS:
    _cfg = LANGUAGES[_l]
    for _a in (_cfg.word_attr, _cfg.example_attr):
        if _a not in COLS:
            COLS.append(_a)


def checks(row, audio: bool, canonical: set[tuple[int, str]] | None = None) -> list[str]:
    """
    Все замечания по одному ряду. Пустой список — ряд чист.

    `canonical` — пары (id ряда, язык), которые участвуют в викторине
    (`word_lang_groups.is_canonical`). Озвучка проверяется только по ним,
    и это не послабление, а то же условие, по которому клипы вообще
    создаются: `expected_clips` берёт тот же фильтр, а `quiz_service`
    по нему же отбирает слова для показа. Неканоническому ряду карточка
    не строится, значит и клип ему не нужен — проверять его наличие
    означало бы ругаться на 2700–3700 рядов на язык без причины.

    Проверки текста (1–9) идут по ВСЕМ рядам: качество ячейки от
    каноничности не зависит.
    """
    bad: list[str] = []
    wid = row["id"]
    w = SimpleNamespace(**row)

    # 1. Все шесть языков заполнены: слово и пример
    for lang in LANGS:
        cfg = LANGUAGES[lang]
        if not (getattr(w, cfg.word_attr) or "").strip():
            bad.append(f"{lang}: пустое слово")
        if not (getattr(w, cfg.example_attr) or "").strip():
            bad.append(f"{lang}: пустой пример")

    # 2. Чужая буква в алфавите (гейт)
    for lang, cols in scan_alien_letter.COLUMNS.items():
        for col in cols:
            if (wid, col) in scan_alien_letter.LEGIT:
                continue
            found = scan_alien_letter.alien(lang, row.get(col))
            if found:
                bad.append(f"{col}: чужая буква {''.join(found)}")

    # 3. Числа во всех языках сходятся (гейт)
    others = {l: row.get(LANGUAGES[l].example_attr) for l in scan_number_mismatch.LANGS}
    for m in scan_number_mismatch.mismatches(row.get("example_de") or "", others):
        bad.append(f"числа расходятся: {m[0]}")

    # 4. Турецкий аффикс после цифры без апострофа (гейт)
    for col in scan_tr_number_suffix.COLUMNS:
        val = row.get(col) or ""
        if scan_tr_number_suffix.GLUED.search(val):
            bad.append(f"{col}: аффикс после цифры без апострофа")

    # 5. Разговорное усечение в немецком эталоне
    if scan_de_colloquial.hit(row.get("example_de") or ""):
        bad.append("example_de: разговорное усечение")

    # 6. Обращение расходится с эталоном
    if scan_formality_vs_de.flagged(
        row.get("example_de") or "", row.get("example_tr") or ""
    ):
        bad.append("example_tr: обращение расходится с эталоном")

    # 7. Книжная связка «є» в украинской ячейке
    for col in scan_uk_copula_je.COLUMNS:
        if scan_uk_copula_je.COPULA.search(row.get(col) or ""):
            bad.append(f"{col}: книжна зв'язка є")

    # 8. Артефакт с косой чертой между двумя вариантами
    for lang in LANGS:
        col = LANGUAGES[lang].example_attr
        val = row.get(col) or ""
        for i, ch in enumerate(val):
            if ch == "/" and 0 < i < len(val) - 1:
                if val[i - 1].isalpha() and val[i + 1].isalpha():
                    bad.append(f"{col}: вариант через косую черту")
                    break

    # 9. Точка в конце слова или примера — правило владельца
    for lang in LANGS:
        cfg = LANGUAGES[lang]
        for col in (cfg.word_attr, cfg.example_attr):
            val = (row.get(col) or "").strip()
            if val.endswith(".") and not val.endswith(".."):
                bad.append(f"{col}: точка в конце")

    if not audio:
        return bad

    # 10. ГЛАВНОЕ: клип, который запросит карточка, лежит на диске.
    # Проверяется вся цепочка — main_meaning, spoken_for, хеш, файл.
    for lang in LANGS:
        if canonical is not None and (wid, lang) not in canonical:
            continue  # ряд не показывается на этом языке, клип не нужен
        voice = default_voice(lang)
        for kind in (KIND_WORD, KIND_FULL):
            spoken = spoken_for(w, lang, kind)
            if not spoken:
                bad.append(f"{lang}/{kind}: нечего произносить")
                continue
            if not clip_path(lang, voice, kind, spoken).exists():
                bad.append(f"{lang}/{kind}: нет клипа для «{spoken[:40]}»")
    return bad


def selfcheck() -> None:
    """
    Каждое из правил обязано сработать на заведомо испорченном ряде.

    Без этого приёмка бесполезна: молчание нельзя отличить от того, что
    проверка просто не подключена. За этот сеанс такое случилось трижды —
    у приметы на усечения дважды и у приметы на артикль один раз, и
    каждый раз её ноль был честным только для того, что она умела видеть.
    """
    base = {
        "id": -1, "article": "das",
        "word_de": "Haus", "example_de": "Das ist ein Haus",
        "translation_en": "house", "example_en": "This is a house",
        "translation_ru": "дом", "example_ru": "Это дом",
        "translation_uk": "дім", "example_uk": "Це дім",
        "translation_tr": "ev", "example_tr": "Bu bir ev",
        "translation_pl": "dom", "example_pl": "To jest dom",
    }
    assert not checks(base, audio=False), f"чистый ряд дал {checks(base, False)}"

    cases = {
        "пустой пример": {"example_ru": ""},
        "чужая буква": {"example_pl": "To jest piosenečka"},
        "числа": {"example_de": "Es kostet 5 Euro",
                  "example_ru": "Это стоит 7 евро"},
        "турецкая цифра": {"example_tr": "Saat 8de geliyor"},
        "усечение": {"example_de": "Ich hab keine Zeit"},
        "обращение": {"example_de": "Zeig mir deinen Ausweis",
                      "example_tr": "Kimlik kartınızı gösterin"},
        "связка є": {"example_uk": "Це є домом"},
        "косая черта": {"example_tr": "Bu ev/bina"},
        "точка в конце": {"example_pl": "To jest dom."},
    }
    broken = []
    for name, patch in cases.items():
        row = dict(base) | patch
        if not checks(row, audio=False):
            broken.append(name)
    if broken:
        print("САМОПРОВЕРКА НЕ ПРОШЛА: правила не сработали —")
        for name in broken:
            print(f"  {name}")
        sys.exit(1)
    print(f"самопроверка: чистый ряд чист, {len(cases)} видов порчи "
          f"пойманы все\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=100)
    ap.add_argument("--size", type=int, default=100)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--show", type=int, default=15)
    args = ap.parse_args()
    audio = not args.no_audio

    selfcheck()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT {', '.join(COLS)} FROM words ORDER BY id")
        ).mappings().all()
        canon_rows = conn.execute(text(
            "SELECT word_id, lang FROM word_lang_groups WHERE is_canonical"
        )).all()
    by_id = {r["id"]: r for r in rows}
    ids = sorted(by_id)
    canonical = {(r[0], r[1]) for r in canon_rows}

    print(f"рядов в базе: {len(ids)}")
    print(f"пар (ряд, язык) в викторине: {len(canonical)}")
    print(f"хранилище озвучки: {pathlib.Path(DEFAULT_ROOT).resolve()}")
    print(f"проверка: {args.rounds} раундов по {args.size} рядов, "
          f"зерно {SEED}, озвучка {'да' if audio else 'нет'}\n")

    rng = random.Random(SEED)
    bad_rounds = 0
    seen_ids: set[int] = set()
    problems: Counter[str] = Counter()
    examples: list[tuple[int, list[str]]] = []
    total_draws = 0

    for rnd in range(1, args.rounds + 1):
        sample = rng.sample(ids, min(args.size, len(ids)))
        seen_ids.update(sample)
        total_draws += len(sample)
        failed = 0
        for wid in sample:
            bad = checks(by_id[wid], audio, canonical)
            if bad:
                failed += 1
                for b in bad:
                    problems[b.split(":")[1].strip() if ":" in b else b] += 1
                if len(examples) < args.show:
                    examples.append((wid, bad))
        if failed:
            bad_rounds += 1
            print(f"раунд {rnd:>3}: рядов с замечанием {failed} из {len(sample)}")

    print()
    for wid, bad in examples:
        print(f"id={wid}")
        for b in bad:
            print(f"  {b}")

    print()
    print(f"всего взятий: {total_draws}")
    print(f"разных рядов задето: {len(seen_ids)} из {len(ids)} "
          f"({100 * len(seen_ids) / len(ids):.0f}%)")
    print(f"раундов с замечаниями: {bad_rounds} из {args.rounds}")
    if problems:
        print("\nпо видам:")
        for name, n in problems.most_common():
            print(f"  {n:>6}  {name}")
        print("\nПРИЁМКА НЕ ПРОЙДЕНА")
        sys.exit(1)
    print("\nПРИЁМКА ПРОЙДЕНА: ни одного замечания ни в одном раунде")


if __name__ == "__main__":
    main()
