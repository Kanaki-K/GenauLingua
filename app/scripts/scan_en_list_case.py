"""ПРИМЕТА: в английском списке вариант с БОЛЬШОЙ буквы, а в примере то
же слово — с маленькой.

ОТКУДА ВЗЯЛАСЬ. Блок 8 третьего прохода, ряд `Krebs` (12498):

    en  Cancer, crab
        · My grandpa unfortunately got cancer

Английский различает регистром два РАЗНЫХ слова: «cancer» — болезнь,
«Cancer» — созвездие и знак зодиака. Список показывает первое значение
большой буквой, пример — маленькой, и карточка выдаёт ученику «Cancer»
там, где фраза учит болезни. Остальные языки этого различения не знают
(«рак», «rak» одинаковы во всех значениях), поэтому класс — ЧИСТО
АНГЛИЙСКИЙ, и ни один из девяти гейтов его не берёт: `scan_lowercase_start`
смотрит на начало примера, `scan_de_lowercase_noun` — на немецкий.

КАК УСТРОЕНО ПРАВИЛО. Для каждого варианта списка берётся его ПЕРВОЕ
слово. Если оно с большой буквы, а в английском примере то же слово
встречается с маленькой (поиск регистрозависимый, по границам слова) —
попадание. Правило структурное: списка имён собственных нет и не нужно,
потому что эталоном служит сам пример.

ПОЧЕМУ НЕ «ЛЮБАЯ БОЛЬШАЯ БУКВА В СПИСКЕ». Замер без примера-эталона даёт
сотни законных попаданий: «Monday», «German», «Christmas» — имена
собственные, и большая буква у них обязательна. Эталон отсекает их
сразу: в примере они тоже с большой.

ПОЧЕМУ НЕ ЛОВИТ НАЧАЛО ФРАЗЫ. Если пример начинается этим же словом,
большая буква в нём обязательна, строчного вхождения нет — попадания не
будет. Ложной тревоги на первом слове фразы быть не может.

ЗАМЕР ПО ВСЕЙ БАЗЕ: 5 попаданий, из них 3 дефекта и 2 законных.

ТРИ ДЕФЕКТА (исправлены `fix_pass3_block_08.py`):

    Krebs        (12498)  список  «Cancer, crab» → «cancer, crab»
        Правит СПИСОК: пример учит болезни, и пять языков из шести
        тоже дают болезнь первой.
    Republikaner (16342)  список  «Republican» → «republican, supporter
        of a republic, member of the Republican Party»
        Правит СПИСОК, но наоборот — не регистром, а полнотой. В ru/uk
        по три значения, в pl два, в en было одно и сразу партийное.
        Пример «defended his beliefs» — про общее значение, и оно
        по-английски строчное. Формулировку третьего варианта выбрала
        эта же примета: «Republican Party member» давала новое
        попадание (большая буква в начале варианта), «member of the
        Republican Party» — нет, при том же значении.
    Pilates      (12412)  ПРИМЕР  «I do pilates» → «I do Pilates»
        Правит ПРИМЕР, а не список: «Pilates» — фамилия Йозефа
        Пилатеса, по-английски всегда с большой. Русский, польский и
        турецкий пишут строчным правильно, и их не трогаем.

Один класс — и правка в нём трижды легла в РАЗНЫЕ места: дважды в
список, причём по разным причинам, и один раз в пример. Примета говорит
«эти две ячейки не согласны», а какая из них неправа — решается чтением.

ДВА ЗАКОННЫХ ОСТАТКА. Оба — настоящие имена собственные, стоящие в
списке рядом со строчным значением:

    Weltmeisterschaft (3012)   «world championship, World Cup»
        пример про «world championship»; «World Cup» — название турнира
    Heiligkeit        (14456)  «holiness, sanctity, Holiness as a title»
        пример про «holiness»; третий вариант сам себя и объясняет —
        «Seine Heiligkeit», обращение, и оно с большой буквы

Примета ждёт РОВНО ДВА остатка и падает, если число изменилось.

ПРЕДЕЛ ПРИМЕТЫ. Обратного случая — в списке строчное, а в примере с
большой — она не ловит: там большая буква может стоять просто в начале
фразы, и правило дало бы ложную тревогу на каждом втором ряду.
"""

from __future__ import annotations

import re
import sys

from sqlalchemy import create_engine, text

from app.config import settings

EXPECTED = 2  # Weltmeisterschaft (3012) и Heiligkeit (14456), см. docstring


def bad_variants(translation_en: str, example_en: str) -> list[str]:
    """Варианты списка, чья большая буква спорит с примером."""
    out: list[str] = []
    for part in (translation_en or "").split(","):
        part = part.strip()
        if not part or not part[:1].isupper():
            continue
        head = part.split()[0]
        if re.search(rf"\b{re.escape(head.lower())}\b", example_en or ""):
            out.append(part)
    return out


def selfcheck() -> None:
    cases = [
        # ХОРОШО: пример подтверждает регистр списка
        ("snake, queue, line", "The venomous snake hides in the grass", []),
        ("Monday", "I have no time on Monday", []),
        ("German, German language", "He is learning German", []),
        ("cancer, crab", "My grandpa unfortunately got cancer", []),
        # начало фразы — большая буква обязательна, это не спор
        ("Cancer", "Cancer is a serious disease", []),
        # слова вообще нет в примере — сравнивать нечего
        ("Republican", "He voted for the party", []),
        # ПЛОХО: список с большой, пример с маленькой
        ("Cancer, crab", "My grandpa unfortunately got cancer", ["Cancer"]),
        ("Pilates", "I do pilates twice a week", ["Pilates"]),
        (
            "Republican",
            "The republican passionately defended his beliefs",
            ["Republican"],
        ),
        # законный остаток: имя собственное рядом со строчным значением
        (
            "world championship, World Cup",
            "The world championship is taking place in Germany",
            ["World Cup"],
        ),
        (
            "holiness, sanctity, Holiness as a title",
            "The holiness of the place was respected by everyone",
            ["Holiness as a title"],
        ),
    ]
    bad = 0
    for translation, example, want in cases:
        got = bad_variants(translation, example)
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {translation!r} / {example!r}")
            print(f"    -> {got}, ждали {want}")
    if bad:
        sys.exit(1)
    print(f"самопроверка правила: {len(cases)} из {len(cases)}")


def main() -> int:
    if "--selfcheck" in sys.argv:
        selfcheck()
        return 0

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, translation_en, example_en FROM words "
            "WHERE translation_en IS NOT NULL AND example_en IS NOT NULL"
        )).mappings().all()

    hits = []
    for row in rows:
        bad = bad_variants(row["translation_en"], row["example_en"])
        if bad:
            hits.append((row, bad))

    for row, bad in hits:
        print(f"{row['word_de']} ({row['id']})  спорный вариант: {bad}")
        print(f"    en  {row['translation_en']}")
        print(f"      · {row['example_en']}")

    print(f"\nпросмотрено рядов: {len(rows)}")
    print(f"всего попаданий: {len(hits)}")
    print(f"ожидаемый остаток: {EXPECTED} — имена собственные, см. docstring")
    if len(hits) != EXPECTED:
        print("ВНИМАНИЕ: остаток изменился — разбери и обнови docstring")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
