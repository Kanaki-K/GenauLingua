"""
Из класса «слова ряда нет в немецком примере» — то, что оказалось дефектом.

Сторож `scan_word_in_example` даёт 45 существительных. Сорок одно из них
**не дефект**: слово стоит внутри слитного составного — «Lichtstrahl» у
ряда `Strahl`, «Nachtschicht» у `Schicht`, «Kontoauszug» у `Auszug`.
Немецкий там естественный, слово видно, и для учащегося составное слово
скорее польза. Трогать их нельзя: это и есть немецкий язык.

Настоящих четыре, и каждое по своей причине:

* `Million` (9864) — «Die Stadt hat etwa 2 Mio. Einwohner». Слова нет
  вовсе, стоит сокращение. Озвучка прочитает «Mio.» как есть, и ученик
  не услышит самого слова. Русский и украинский туда же: «2 млн».
* `Langeweile` (10711) — «Die Langweile». Это опечатка в эталоне:
  правильно «Langeweile». Заодно английский, украинский и турецкий
  переводят совсем другую фразу — про уборку квартиры от скуки.
* `Umwelt` (1996) — «Umweltschutz ist wichtig». Слово спрятано в
  составном, и ряд целиком, со всеми пятью переводами, повторяет ряд
  2916 `Umweltschutz`. Две карточки учили одному и тому же.
* `Nummer` (1736) — «Was ist deine Telefonnummer?». То же: ряд дословно
  повторяет 921 `Telefonnummer`, и «Nummer» сама по себе не показана.

Для `Umwelt` и `Nummer` пример заменён целиком, во всех шести языках:
иначе дубликат останется. Новые примеры выбраны так, чтобы слово стояло
отдельно и фраза была простая.

    python -m app.scripts.fix_word_in_example            # показать
    python -m app.scripts.fix_word_in_example --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- Million: сокращение вместо слова -------------------------------------
    (9864, "example_de", "Die Stadt hat etwa 2 Mio. Einwohner",
     "Die Stadt hat etwa 2 Millionen Einwohner",
     "«Mio.» — сокращение; само слово в примере не стоит и не прозвучит"),
    (9864, "example_ru", "В городе примерно 2 млн жителей",
     "В городе примерно 2 миллиона жителей", "«млн» — сокращение"),
    (9864, "example_uk", "У місті приблизно 2 млн жителів",
     "У місті приблизно 2 мільйони жителів", "то же"),
    (9864, "example_pl", "To miasto ma około 2 mln mieszkańców",
     "To miasto ma około 2 miliony mieszkańców", "то же"),
    (9864, "example_tr", "Şehrin yaklaşık 2 milyon sakinı var",
     "Şehrin yaklaşık 2 milyon sakini var", "«sakinı» — опечатка"),
    (9864, "translation_ru", "млн, миллион", "миллион, млн",
     "сокращение стояло первым значением, его и показывала карточка"),

    # --- Langeweile: опечатка в эталоне и три перевода про другое -------------
    (10711, "example_de", "Die Langweile in der Vorlesung war unerträglich",
     "Die Langeweile in der Vorlesung war unerträglich",
     "«Langweile» — опечатка, слово пишется «Langeweile»"),
    (10711, "example_en", "I cleaned the whole flat out of boredom",
     "The boredom in the lecture was unbearable",
     "немецкий про скуку на лекции, а не про уборку"),
    (10711, "example_uk", "Мені нудно",
     "Нудьга на лекції була нестерпною", "то же"),
    (10711, "example_tr", "Can sıkıntısından bütün evi temizledim",
     "Derste can sıkıntısı dayanılmazdı", "то же"),

    # --- Umwelt: ряд дословно повторял 2916 Umweltschutz ----------------------
    (1996, "example_de", "Umweltschutz ist wichtig",
     "Plastik schadet der Umwelt",
     "слово было спрятано в «Umweltschutz», и ряд повторял 2916"),
    (1996, "example_ru", "Защита окружающей среды важна",
     "Пластик вредит окружающей среде", "вслед за эталоном"),
    (1996, "example_en", "Environmental protection is important",
     "Plastic harms the environment", "вслед за эталоном"),
    (1996, "example_uk", "Захист довкілля важливий",
     "Пластик шкодить довкіллю", "вслед за эталоном"),
    (1996, "example_tr", "Çevreyi korumak önemlidir",
     "Plastik çevreye zarar veriyor", "вслед за эталоном"),
    (1996, "example_pl", "Ochrona środowiska jest ważna",
     "Plastik szkodzi środowisku", "вслед за эталоном"),

    # --- Nummer: ряд дословно повторял 921 Telefonnummer ----------------------
    (1736, "example_de", "Was ist deine Telefonnummer?",
     "Welche Nummer hat dein Haus?",
     "«Nummer» сама по себе не показана, и ряд повторял 921"),
    (1736, "example_ru", "Какой у тебя номер телефона?",
     "Какой номер у твоего дома?", "вслед за эталоном"),
    (1736, "example_en", "What is your phone number?",
     "What number is your house?", "вслед за эталоном"),
    (1736, "example_uk", "Який твій номер телефону?",
     "Який номер у твого будинку?", "вслед за эталоном"),
    (1736, "example_tr", "Telefon numaran ne?", "Evinin numarası kaç?",
     "вслед за эталоном"),
    (1736, "example_pl", "Jaki jest twój numer telefonu?",
     "Jaki numer ma twój dom?", "вслед за эталоном"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
