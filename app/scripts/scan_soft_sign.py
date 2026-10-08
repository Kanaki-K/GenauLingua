"""
ГЕЙТ: мягкий или твёрдый знак там, где его в орфографии не бывает.

ЗАЧЕМ. В ряду `entgehen` (7021) украинский список переводов был
«уникнути, ускользнути, пройти мимо **увагиь**». Три дефекта в одной
ячейке: русское слово, русская фраза и слово, которого нет ни в одном
языке. Глазами это видно сразу, а ни одна примета не видела.

ПОЧЕМУ НЕ УВИДЕЛА `scan_ru_in_uk`. Она сравнивает корпуса: слово частое
в русских ячейках и однократное в украинских. «ускользнути» — это
русская основа с украинским окончанием, то есть гибрид, которого нет НИ
В ОДНОМ корпусе. А «увагиь» нет и в природе. Примета, которая ищет
слово по частоте, гибрид не найдёт никогда: у него частота ноль с двух
сторон.

ПРИЗНАК ОРФОГРАФИЧЕСКИЙ, А НЕ СЛОВАРНЫЙ. Поэтому он и годится в гейты:
проверяется не «есть ли такое слово», а «возможна ли такая буква после
такой». Правила разные по языкам, и первая версия приметы на этом
упала:

  • «ь»/«ъ» ПОСЛЕ ГЛАСНОЙ не бывает ни в русском, ни в украинском.
  • «ь» после г/к/х/ж/ч/ш/щ не бывает В УКРАИНСКОМ.
  • А В РУССКОМ после ж/ч/ш/щ он нормален и очень част: «ночь»,
    «помощь», «хочешь», «печь». Первая версия применила украинское
    правило к русскому и дала **658 попаданий**, из них настоящих ноль.
    Это записано здесь, потому что ошибка выглядела как находка.
  • Двух знаков подряд не бывает нигде.

Турецкий, польский, английский и немецкий не смотрим: там этих букв
нет вовсе.

По базе после правки ряда 7021: ноль. Гейт падает на любом новом.

    python -m app.scripts.scan_soft_sign
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Ни в русском, ни в украинском знак не стоит после гласной.
AFTER_VOWEL = re.compile(r"[аеєиіїоуюяыэё][ьъ]", re.IGNORECASE)
# В украинском — ещё и после твёрдых и шипящих. В русском это норма.
UK_AFTER_HARD = re.compile(r"[гкхжчшщ]ь", re.IGNORECASE)
# Двух знаков подряд не бывает нигде.
DOUBLED = re.compile(r"[ьъ]{2}", re.IGNORECASE)

RULES: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "ru": [("знак после гласной", AFTER_VOWEL), ("два знака подряд", DOUBLED)],
    "uk": [("знак после гласной", AFTER_VOWEL),
           ("ь после г/к/х/ж/ч/ш/щ", UK_AFTER_HARD),
           ("два знака подряд", DOUBLED)],
}
COLUMNS = [f"{kind}_{lang}" for lang in RULES for kind in ("example", "translation")]


def hits(lang: str, s: str | None) -> list[tuple[str, str]]:
    out = []
    for name, pat in RULES[lang]:
        m = pat.search(s or "")
        if m:
            out.append((name, m.group(0)))
    return out


def selfcheck() -> None:
    errs = []
    # Русский: шипящая плюс «ь» — норма, трогать нельзя.
    for s in ("Как ты хочешь заплатить?", "Мне нужна помощь", "Ночью мы спим",
              "печь, запекать, испечь", "дочь", "вещь"):
        if hits("ru", s):
            errs.append(f"ru: законное слово объявлено дефектом: {s!r}")
    # Украинский: законные слова с «ь» после согласной.
    for s in ("На підлозі", "сьогодні", "мільйон", "батько", "стань тут"):
        if hits("uk", s):
            errs.append(f"uk: законное слово объявлено дефектом: {s!r}")
    # А вот это невозможно.
    if not hits("uk", "пройти мимо увагиь"):
        errs.append("uk: «увагиь» — знак после гласной — не найден")
    if not hits("ru", "по дорогиь"):
        errs.append("ru: знак после гласной не найден")
    if not hits("uk", "хочь"):
        errs.append("uk: «ь» после «ч» не найден")
    if not hits("ru", "statьь"):
        errs.append("ru: два знака подряд не найдены")
    # И главное: украинское правило НЕ применяется к русскому.
    if hits("ru", "хочь") or hits("ru", "ночь"):
        errs.append("украинское правило применено к русскому — 658 ложных")
    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print("самопроверка: русская шипящая с «ь» законна, украинская — нет")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(COLUMNS)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT id, word_de, {cols} FROM words ORDER BY id")
        ).mappings().all()

    found: list[tuple[int, str, str, str, str, str]] = []
    for r in rows:
        for lang in RULES:
            for kind in ("example", "translation"):
                col = f"{kind}_{lang}"
                for name, frag in hits(lang, r[col]):
                    found.append((r["id"], r["word_de"], col, name, frag, r[col]))

    print(f"\nпрочитано рядов: {len(rows)}")
    print(f"невозможный знак: {len(found)}")
    for wid, word, col, name, frag, val in found:
        print(f"  {wid:>6}  {word:<18} {col:<15} [{name}: {frag}]")
        print(f"          {val}")

    if found:
        print("\nГЕЙТ НЕ ПРОЙДЕН")
        sys.exit(1)
    print("гейт пройден")


if __name__ == "__main__":
    main()
