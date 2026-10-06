"""
Ищет турецкое ИМЯ СОБСТВЕННОЕ без апострофа перед падежным суффиксом.

Зачем. По-турецки суффикс к имени собственному присоединяется через
апостроф: `Berlin'de`, `Mozart'ın`, `Roma'dan`, `Noel'de`. Это правило
орфографии, не стиля. По базе такое попадалось почти в каждом блоке
начиная с шестидесятого, и правилось по одному; пора собрать класс.

Как ищется. Слово с заглавной буквы, к которому без апострофа приклеен
один из падежных суффиксов, и его основа есть в списке имён. Список
именно нужен: по одному строению отличить имя от обычного слова нельзя.

Три рода ложных срабатываний, из-за которых список именно такой.

  1. НАЗВАНИЯ ЯЗЫКОВ апострофа НЕ берут: `Almancayı akıcı konuşuyor`,
     `Fransızcayı çok iyi konuşuyor` — так и надо. Поэтому `Almanca`,
     `Fransızca`, `Kantonca` и прочие в список не входят.

  2. ОБЫЧНОЕ СЛОВО, КОНЧАЮЩЕЕСЯ КАК ИМЯ. `Romanın girişi` это «начало
     романа»: `roman` плюс `ın`. Но если отрезать `nın`, остаётся
     `roma` — и примета принимает роман за Рим. Поэтому `Roma` из
     списка убран, хотя `Roma'dan` в базе есть и правится вручную.
     Цена честная: лучше потерять одно настоящее попадание, чем выдать
     три ложных.

  3. СЛОВО, КОТОРОЕ БЫВАЕТ И ИМЕНЕМ, И НЕТ. `dünya` — это и «мир», и
     планета Земля. `Dünyanın her yerinde` («по всему миру») апострофа
     не требует, а `Dünya'nın kutbu` («полюс Земли») требует. Отличить
     можно только по смыслу, поэтому `Dünya` тоже не в списке, а
     четыре таких ряда разобраны глазами.

Итого примета ловит имена мест и людей — то, где правило безоговорочно.

    python -m app.scripts.scan_tr_apostrophe
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

SUFFIXES = (
    "daki", "deki", "taki", "teki",
    "nın", "nin", "nun", "nün",
    "dan", "den", "tan", "ten",
    "yla", "yle",
    "da", "de", "ta", "te",
    "ya", "ye", "yı", "yi",
    "ın", "in", "un", "ün",
    "la", "le",
    "a", "e", "ı", "i", "u", "ü",
)

# Имена мест и людей. Названий языков тут нет — они апострофа не берут.
# `Roma` и `Dünya` тоже нет, и почему — написано в заголовке файла.
NAMES = {
    "berlin", "london", "londra", "mozart", "akdeniz", "frankfurt",
    "hollanda", "almanya", "türkiye", "avrupa", "venedik", "noel",
    "varşova", "hamburg", "münih", "paris", "viyana", "polonya",
    "amerika", "alpler", "sivas", "istanbul", "ankara", "italya",
    "ispanya", "fransa", "rusya", "ukrayna", "japonya", "mısır",
    "bavyera", "kanada", "avustralya", "afrika", "asya", "antarktika",
}

WORD = re.compile(r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\b")


def hit(example: str) -> list[str]:
    out = []
    for m in WORD.finditer(example or ""):
        tok = m.group(0)
        low = tok.lower()
        for s in SUFFIXES:
            if low.endswith(s) and low[: -len(s)] in NAMES:
                out.append(tok)
                break
    return out


def selfcheck() -> None:
    cases = [
        ("Güzel bir eski binada Berlinde oturuyor", ["Berlinde"]),
        ("Güzel bir eski binada Berlin'de oturuyor", []),
        ("Birçok göçmen Amerikaya gitti", ["Amerikaya"]),
        ("Her Noelde birlikte kutlamak gelenek", ["Noelde"]),
        # название языка апострофа не берёт
        ("Rus olmasına rağmen Almancayı akıcı konuşuyor", []),
        # обычное слово, кончающееся как имя
        ("Romanın girişi gerçekten heyecan vericiydi", []),
        # «мир», а не планета
        ("Dünyanın her yerinde birçok hayranı var", []),
        # имя без суффикса
        ("Berlin çok güzel bir şehir", []),
    ]
    for ex, want in cases:
        got = hit(ex)
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {ex!r} дало {got}, а надо {want}")
            sys.exit(1)
    print(f"самопроверка: {len(cases)} строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_tr FROM words "
            "WHERE example_tr IS NOT NULL ORDER BY id")).all()

    print(f"прочитано турецких примеров: {len(rows)}")
    found = [(i, w, e, h) for i, w, e in rows if (h := hit(e))]
    print(f"имя собственное без апострофа: {len(found)}\n")
    for wid, word, ex, h in found:
        print(f"  {wid:>6}  {word:<22} [{', '.join(h)}]")
        print(f"          {ex}")


if __name__ == "__main__":
    main()
