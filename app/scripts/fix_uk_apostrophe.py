"""
Пропущенный украинский апостроф: «мясо» вместо «м'ясо».

Апостроф там не украшение. Он показывает, что согласный твёрдый, а «я/ю/є/ї»
читаются как [ja], [ju], [je], [ji]: «мясо» и «м'ясо» — разное чтение, и
синтезатор произносит их по-разному. Нашлось через проверку распознаванием:
в примере стояло «вязниці», и распознаватель услышал «в'язнайте».

Правилом по буквам это не берётся. Апостроф зависит от твёрдости согласного,
а не от написания: «бюджет», «купюра», «буряк», «ряд», «бязь», «морквяний»
пишутся БЕЗ апострофа, хотя буквы те же. Поэтому правка идёт по перечню
корней, каждый из которых проверен глазами.

«бю» в перечень не входит намеренно: 32 совпадения по нему — «бюджет» и
«бюрократія», и все верны.

    python -m app.scripts.fix_uk_apostrophe
    python -m app.scripts.fix_uk_apostrophe --apply
"""

import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings

# Корень без апострофа → с апострофом. Регистр сохраняется отдельно.
ROOTS = [
    ("вязн", "в'язн"),        # в'язні, ув'язнених, в'язниця
    ("вязк", "в'язк"),        # в'язка
    ("вязан", "в'язан"),
    ("повязк", "пов'язк"),
    ("запяст", "зап'яст"),
    ("розвяз", "розв'яз"),
    ("звяз", "зв'яз"),
    ("мяс", "м'яс"),          # м'ясо, м'ясник
    ("мяк", "м'як"),          # м'яко, м'якої
    ("мяч", "м'яч"),
    ("пят", "п'ят"),          # п'ять, п'ятірка
    ("пють", "п'ють"),
    ("пє", "п'є"),
    ("імя", "ім'я"),
    ("імям", "ім'ям"),
    ("сімя", "сім'я"),
    ("сімям", "сім'ям"),
    ("сімями", "сім'ями"),
    ("здоровя", "здоров'я"),
    ("подвіря", "подвір'я"),
    ("компютер", "комп'ютер"),
    ("інтервю", "інтерв'ю"),
    ("кровю", "кров'ю"),
    ("любовю", "любов'ю"),
    ("матірю", "матір'ю"),
    ("карєр", "кар'єр"),
    ("обєдн", "об'єдн"),
    ("обєкт", "об'єкт"),
    ("обєм", "об'єм"),
    ("девять", "дев'ять"),
    ("девяно", "дев'яно"),
    ("зїв", "з'їв"),
    ("зїст", "з'їст"),
    ("вїзд", "в'їзд"),
    ("вїхав", "в'їхав"),
    ("підїзд", "під'їзд"),
    ("полумя", "полум'я"),
    ("премєр", "прем'єр"),
    ("пєс", "п'єс"),
]

# Слова, внутри которых корень встречается законно и апостроф не нужен
KEEP = ("купюр", "бюджет", "бюрократ", "бюро", "пюре", "пюпітр")

apply_changes = "--apply" in sys.argv


def fix(value: str) -> str:
    if not value:
        return value
    result = value
    for bad, good in ROOTS:
        if bad not in result.lower():
            continue
        # Идём по вхождениям, сохраняя регистр первой буквы
        out = []
        index = 0
        low = result.lower()
        while True:
            found = low.find(bad, index)
            if found < 0:
                out.append(result[index:])
                break
            # Слово целиком — чтобы проверить исключения
            start = found
            while start > 0 and result[start - 1].isalpha():
                start -= 1
            end = found + len(bad)
            while end < len(result) and result[end].isalpha():
                end += 1
            word = result[start:end].lower()
            if any(k in word for k in KEEP):
                out.append(result[index:found + len(bad)])
                index = found + len(bad)
                continue
            replacement = good
            if result[found].isupper():
                replacement = good[0].upper() + good[1:]
            out.append(result[index:found])
            out.append(replacement)
            index = found + len(bad)
        result = "".join(out)
        low = result.lower()
    return result


engine = create_engine(settings.DATABASE_URL_SYNC)
with engine.connect() as conn:
    rows = conn.execute(text(
        "SELECT id, word_de, translation_uk, example_uk FROM words"
    )).mappings().all()

updates_word: list[dict] = []
updates_example: list[dict] = []
samples: list[str] = []

for row in rows:
    for column, store in (("translation_uk", updates_word),
                          ("example_uk", updates_example)):
        value = (row[column] or "").strip()
        if not value:
            continue
        fixed = fix(value)
        if fixed != value:
            store.append({"id": row["id"], "v": fixed})
            if len(samples) < 14:
                samples.append(f"    {row['word_de']!r:<18} {value[:52]!r}\n"
                               f"    {'':<18} → {fixed[:52]!r}")

total = len(updates_word) + len(updates_example)
print(f"значений с пропущенным апострофом: {total} "
      f"(переводов {len(updates_word)}, примеров {len(updates_example)})")
print()
print("\n".join(samples))

if not apply_changes:
    print()
    print("  (пробный прогон, для применения --apply)")
    sys.exit(0)

with engine.begin() as conn:
    if updates_word:
        conn.execute(text("UPDATE words SET translation_uk = :v WHERE id = :id"),
                     updates_word)
    if updates_example:
        conn.execute(text("UPDATE words SET example_uk = :v WHERE id = :id"),
                     updates_example)
print()
print(f"применено: {total}")
print("Украинский текст изменился — нужен пересинтез: "
      "python -m app.scripts.tts_synthesize --lang uk")
