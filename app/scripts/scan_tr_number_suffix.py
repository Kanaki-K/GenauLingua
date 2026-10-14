"""Турецкое число, к которому падеж приклеен без апострофа.

ТРЕТИЙ ГЕЙТ обзора. Как и два предыдущих (scan_alien_letter,
scan_number_mismatch), это правило орфографическое, а не смысловое:
в турецком любой аффикс после цифры отделяется апострофом —
«saat 8'de», «1960'larda», «2'si», «5'inci». Без апострофа выходит
не вариант написания, а ошибка. Поэтому у приметы нет белого списка
по смыслу, и она имеет право падать с кодом 1.

Нашлось в блоке 68: «Sabah ibadeti saat 8de başlıyor» (id 14845).

Чего примета НЕ видит и видеть не должна:
  • цифра с единицей измерения через пробел («20 euro», «3 kg») —
    там нет аффикса;
  • латинские буквы сразу за цифрой в кодах и марках («A4», «MP3») —
    это не турецкий аффикс, а часть имени; отсев идёт по тому,
    что за цифрой стоит именно начало турецкого аффикса;
  • отсутствие апострофа у имён собственных — это другой класс
    и другая примета (scan_tr_apostrophe), там правило зависит
    от того, имя ли это вообще, и белый список нужен.

Самопроверка на GOOD/BAD обязательна: примета — гейт, и молчаливая
поломка регулярки означала бы ложное «чисто».
"""

from __future__ import annotations

import re
import sys

from sqlalchemy import create_engine, text

from app.config import settings

# Турецкие аффиксы начинаются с ограниченного набора букв. Берём именно
# их, а не «любая буква»: так из выдачи сами выпадают коды и марки,
# где за цифрой стоит латинская заглавная (A4, MP3, B2).
SUFFIX_START = "abcdeghiklmnprstuvyzçğıöşü"

# Цифра, сразу за ней буква начала аффикса, и дальше ещё хотя бы одна
# строчная буква: один символ может оказаться обозначением («5m»),
# а аффикс короче двух букв в турецком не бывает.
GLUED = re.compile(rf"\d[{SUFFIX_START}][a-zçğıiöşü]")

COLUMNS = ("translation_tr", "example_tr")

GOOD = (
    "Sabah ibadeti saat 8'de başlıyor",
    "Bu araba 1960'larda üretildi",
    "Park ücreti iki euro",
    "Fiyat 20 euro",
    "Kağıt boyutu A4",
    "MP3 çalar bozuldu",
    "Toplantı 15.30'da",
)
BAD = (
    "Sabah ibadeti saat 8de başlıyor",
    "Bu araba 1960larda üretildi",
    "Toplantı 15.30da",
    "Sınıfın 2si geldi",
)


def selfcheck() -> None:
    bad_good = [s for s in GOOD if GLUED.search(s)]
    good_bad = [s for s in BAD if not GLUED.search(s)]
    if bad_good or good_bad:
        print("САМОПРОВЕРКА НЕ ПРОШЛА")
        for s in bad_good:
            print(f"  ложное срабатывание: {s!r}")
        for s in good_bad:
            print(f"  не поймано: {s!r}")
        sys.exit(1)
    print(f"самопроверка: {len(GOOD)} чистых, {len(BAD)} грязных — ок\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(COLUMNS)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT id, word_de, {cols} FROM words ORDER BY id")
        ).all()

    hits: list[tuple[int, str, str, str]] = []
    for row in rows:
        wid, word = row[0], row[1]
        for col, val in zip(COLUMNS, row[2:]):
            if not val:
                continue
            m = GLUED.search(val)
            if m:
                hits.append((wid, word, col, val))

    for wid, word, col, val in hits:
        print(f"id={wid} {word} · {col}")
        print(f"  {val}")

    print(f"\nвсего: {len(hits)}")
    if hits:
        sys.exit(1)


if __name__ == "__main__":
    main()
