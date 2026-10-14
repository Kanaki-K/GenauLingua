"""
Ищет ЧУЖУЮ БУКВУ — литеру, которой в алфавите этого языка нет.

Зачем. Блок 63 дал одну ячейку:

    pl  piosenka, piosenečka

`č` в польском алфавите не существует. Это чешская буква, и попала она
в польскую ячейку, где должно стоять `piosneczka`. Такое не поймает ни
одна смысловая проверка: слово читается как польское, значение верное,
и ошибка только в одном знаке, которого в языке нет вовсе.

Чем эта примета отличается от всех предыдущих. До сих пор каждая
опиралась на язык — на падеж, на согласование, на выводимость формы, —
и потому не могла быть гейтом: язык всегда даёт исключения. Здесь
правило чисто орфографическое: набор букв у алфавита конечен и закрыт.
Поэтому примета ВОЗВРАЩАЕТ КОД 1 и годится в гейт.

Чего примета не умеет. Единственный род законных исключений — чужое
имя или заимствование внутри фразы. По базе их семь: пять в английских
ячейках (`Dear Ms. Müller`, `Mr Müller is here`, `döner kebab`,
`I'm eating a döner kebab`, `People used to call young women Fräulein`)
и две в польских, где та же фамилия Müller. Немецкая буква в
английском или польском предложении, когда это фамилия, — не дефект,
так и надо.

Они вынесены в белый список ПО id И СТОЛБЦУ, а не по букве. Это важно:
разрешить `ü` в английском вообще — значит выключить примету для
английского целиком, и настоящий случай она пропустит. Белый список
точечный, и в этом вся его ценность: он разрешает семь конкретных
ячеек, а не семь букв.

    python -m app.scripts.scan_alien_letter
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Буквы, которых в алфавите языка нет. Берём только диакритику: базовая
# латиница есть у всех, и по ней отличить ничего нельзя.
ALIEN = {
    "pl": set("ěščřžýďťňåæøđäöüß"),
    "de": set("ěščřžýåæøąćęłńśźżçğı"),
    "tr": set("ěščřžýåæøąćęłńśźżäß"),
    "en": set("ěščřžýåæøąćęłńśźżäöüßçğı"),
}

COLUMNS = {
    "pl": ("translation_pl", "example_pl"),
    "de": ("word_de", "example_de"),
    "tr": ("translation_tr", "example_tr"),
    "en": ("translation_en", "example_en"),
}

# Законные исключения: чужое имя или заимствование внутри фразы.
# Ключ — (id, столбец), а не буква: разрешать букву целиком нельзя.
LEGIT = {
    (315, "example_en"),     # Dear Ms. Müller
    (400, "example_en"),     # Mr Müller is here
    (2350, "translation_en"),  # döner kebab
    (2350, "example_en"),    # I'm eating a döner kebab
    (14936, "example_en"),   # young women Fräulein
    (315, "example_pl"),     # Szanowna Pani Müller
    (400, "example_pl"),     # Pan Müller jest tutaj
}


def alien(lang: str, value: str | None) -> list[str]:
    if not value:
        return []
    return sorted({c for c in value.lower() if c in ALIEN[lang]})


def selfcheck() -> None:
    cases = [
        ("pl", "piosenka, piosenečka", ["č"]),
        ("pl", "piosenka, piosneczka", []),
        ("pl", "Zażółć gęślą jaźń", []),
        ("de", "Die Straße ist schön", []),
        ("de", "Die Straße ist piękna", ["ę"]),
        ("tr", "Çağrı güzel şarkı söylüyor", []),
        ("tr", "Çağrı güzel Straße söylüyor", ["ß"]),
        ("en", "The street is beautiful", []),
        ("en", "The straße is beautiful", ["ß"]),
    ]
    for lang, value, want in cases:
        got = alien(lang, value)
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {lang} {value!r} дало {got}, "
                  f"а надо {want}")
            sys.exit(1)
    print(f"самопроверка: {len(cases)} строк на четырёх алфавитах "
          f"разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = sorted({c for pair in COLUMNS.values() for c in pair})
    with engine.connect() as conn:
        rows = conn.execute(text(
            f"SELECT id, word_de, {', '.join(cols)} FROM words "
            "ORDER BY id")).all()

    idx = {name: i + 2 for i, name in enumerate(cols)}
    print(f"прочитано рядов: {len(rows)}")

    found, skipped = [], 0
    for r in rows:
        wid, word = r[0], r[1]
        for lang, pair in COLUMNS.items():
            for col in pair:
                got = alien(lang, r[idx[col]])
                if not got:
                    continue
                if (wid, col) in LEGIT:
                    skipped += 1
                    continue
                found.append((wid, word, lang, col, got, r[idx[col]]))

    print(f"законных заимствований пропущено: {skipped}")
    print(f"ячеек с чужой буквой: {len(found)}\n")
    for wid, word, lang, col, got, val in found:
        print(f"  {wid:>6}  {word:<22} {col:<16} {got}")
        print(f"          {val}")

    if found:
        print("\nГЕЙТ НЕ ПРОЙДЕН: чужая буква в алфавите языка")
        sys.exit(1)
    print("гейт пройден")


if __name__ == "__main__":
    main()
