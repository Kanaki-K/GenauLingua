"""
Ищет словарную статью во МНОЖЕСТВЕННОМ числе при существительном
в единственном.

Зачем. Блок 54 дал ряд `der Partisan` со статьями «партизаны,
повстанцы» / «partisans, guerrillas» / «partizanlar, gerillalar» /
«partyzanci». Слово ряда в единственном, а ученику показывают
множественное во всех пяти языках: карточка учит не тому, что
написано в заголовке.

Чем это ловится. Турецкий — агглютинативный: множественное там всегда
суффикс `-lar`/`-ler`, и других способов нет. Значит первая статья
турецкой колонки, кончающаяся на `-lar`/`-ler`, это всегда
множественное — без словаря и без морфологии. Это и есть примета.

Чего примета НЕ умеет. Отличить настоящее множественное от немецких
pluralia tantum: `die Gezeiten`, `die Einsen`, `die Seeleute`,
`die Windpocken`, `die Lebzeiten` — у них артикль `die`, как у любого
женского слова в единственном, а слово при этом множественное, и
множественная статья там законна. Артикль этого не различает.

Поэтому примета не чинит, а СУЖАЕТ базу до списка, который можно
прочесть глазами. Законные случаи вынесены в LEGIT: их видно по
немецкому слову, и каждый внесён руками после прочтения.

Самопроверка: на заведомо правильных строках срабатывать не должно, на
заведомо испорченных — должно. Если хоть одна не сошлась, скрипт падает
и ничего не печатает.

    python -m app.scripts.scan_plural_gloss
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Турецкое множественное: только «-lar»/«-ler», других способов нет.
TR_PLURAL = re.compile(r"(lar|ler)$", re.IGNORECASE)

# Турецкие слова, у которых «-ler» входит в КОРЕНЬ, а не суффикс.
# Первый проход дал `die Speisekammer` → `kiler` (кладовка, слово
# единственного числа): примета приняла корень за окончание. Список
# ведётся руками, другого способа нет.
TR_ROOT_LER = {"kiler", "iller", "miller", "haller"}

# Немецкие pluralia tantum и слова, у которых множественная статья
# законна: само слово ряда множественного числа. Артикль их не
# отличает, поэтому список ведётся руками.
LEGIT = {
    "Gezeiten", "Einsen", "Seeleute", "Windpocken", "Lebzeiten",
    "Eltern", "Geschwister", "Ferien", "Leute", "Kosten", "Möbel",
    "Menschenrecht", "Finanzen", "Daten", "Lebensmittel", "Schulden",
    "Trümmer", "Pocken", "Masern", "Flitterwochen", "Gliedmaßen",
}


def first_gloss(s: str) -> str:
    return (s or "").split(",")[0].strip()


def hit(word_de: str, translation_tr: str) -> bool:
    if word_de in LEGIT:
        return False
    g = first_gloss(translation_tr)
    if g.lower() in TR_ROOT_LER:
        return False
    return bool(TR_PLURAL.search(g))


GOOD = [
    # единственное слово — единственная статья
    ("Partisan", "partizan, gerilla"),
    ("Hund", "köpek"),
    ("Buch", "kitap, defter"),
    # pluralia tantum: множественная статья законна
    ("Gezeiten", "gelgitler"),
    ("Seeleute", "gemiciler, denizciler"),
    ("Windpocken", "su çiçekleri"),
    # «-lar» не в первой статье примету не трогает: смотрим только первую
    ("Blume", "çiçek, çiçekler"),
    # «-ler» в корне, а не суффиксом
    ("Speisekammer", "kiler, erzak odası"),
]
BAD = [
    ("Partisan", "partizanlar, gerillalar"),
    ("Hund", "köpekler"),
    ("Tourist", "turistler, gezginler"),
    ("Arbeiter", "işçiler"),
]


def selfcheck() -> None:
    for w, t in GOOD:
        if hit(w, t):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {w} / {t!r}")
            sys.exit(1)
    for w, t in BAD:
        if not hit(w, t):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {w} / {t!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GOOD)} правильных и {len(BAD)} "
          f"испорченных статей разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, article, translation_tr, translation_ru "
            "FROM words WHERE pos = 'NOUN' AND translation_tr IS NOT NULL "
            "AND article IS NOT NULL AND btrim(article) <> '' ORDER BY id"
        )).all()

    found = [r for r in rows if hit(r[1], r[3])]
    print(f"прочитано существительных с артиклем: {len(rows)}")
    print(f"со множественной первой статьёй: {len(found)}\n")
    for i, w, art, tr, ru in found:
        print(f"  {i:>6}  {art} {w:<24} tr: {first_gloss(tr):<22} "
              f"ru: {first_gloss(ru)}")


if __name__ == "__main__":
    main()
