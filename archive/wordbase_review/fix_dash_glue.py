"""
Класс: словарная статья, приклеенная к примеру через тире.

Выглядит так: «To switch — I switch the channel», «Pelvis — Pelvis
iskeletin önemli bir parçasıdır». Перед тире стоит перевод заголовка,
после — сам пример. Карточка показывает это как одну фразу, и человек
учит тире посреди предложения.

Класс считался закрытым: сторож `scan_artifacts` даёт 44 попадания, и
они были разом записаны ложными. Это неверно. Ложных там 30 — обычное
тире вместо сказуемого («Моё имя — Анна Вебер», «Мой IBAN — DE75…») и
четыре ряда, где тире стоит и в немецком эталоне (8490, 9126, 9573,
18372). Настоящих — четырнадцать, по всем шести языкам.

Нашлось при вычитке блока 18: `schalten` (id 2792), английское
«To switch — I switch the channel». Дальше — сплошным поиском.

Попутно, раз ряды всё равно открыты, правятся дефекты в них же:
`Becken` английский мыл раковину вместо таза, `Action` рассказывал про
кинотеатр, `anstecken` в украинском зажигал свечу, `Stäbchen` в польском
ел суши, `abdrücken` в турецком содержал «natıştırman» — такого слова нет.

    python -m app.scripts.fix_dash_glue            # показать
    python -m app.scripts.fix_dash_glue --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- снять приклеенную словарную статью -----------------------------------
    (2792, "example_en", "To switch — I switch the channel",
     "I switch the channel", "«To switch» — заголовок, приклеенный к примеру"),
    (7391, "example_en", "To catch – We need to catch the animal",
     "We need to catch the animal", "то же"),
    (7400, "example_uk",
     "Натиснути — Ти повинен натиснути на спусковий гачок, щоб зробити фото",
     "Ти повинен натиснути на спусковий гачок, щоб зробити фото", "то же"),
    (7413, "example_en", "Solid – That's solid work", "That's solid work",
     "то же"),
    (7982, "example_tr", "Neden olmak – Bu sorunlara neden olacak",
     "Bu sorunlara neden olacak", "то же"),
    (9575, "example_en", "Latin – That's a Latin proverb",
     "That's a Latin proverb", "то же"),
    (11951, "example_tr",
     "Asyada büyüdüğü için çubukla yedi — Kültüründe olduğu gibi çubukla yedi",
     "Kültüründe olduğu gibi çubuklarla yedi",
     "два варианта через тире; оставлен тот, что переводит немецкий"),
    (12671, "example_tr", "Pelvis — Pelvis iskeletin önemli bir parçasıdır",
     "Leğen kemiği iskeletin önemli bir parçasıdır",
     "приклеен заголовок, и «pelvis» — латынь: по-турецки «leğen kemiği»"),
    (12671, "example_uk", "Таз — Таз — важлива частина скелета",
     "Таз — важлива частина скелета", "заголовок приклеен к примеру"),
    (12995, "example_en",
     "To spit out — He spat out the medicine because it tasted so bitter",
     "He spat out the medicine because it tasted so bitter", "то же"),
    (13007, "example_en",
     "Straitjacket — He had to be held in a straitjacket",
     "He had to be held in a straitjacket", "то же"),
    (14433, "example_en",
     "Action – The new action movie with lots of action is playing in the cinema",
     "This movie has a lot of action",
     "приклеен заголовок, и немецкий «Dieser Film hat viel Action»"),
    (18093, "example_en", "Ore — Ore is mined in the mine",
     "Ore is mined in the mine", "заголовок приклеен к примеру"),
    (18100, "example_en",
     "Boost — The economic boost helped the whole region",
     "After the reform the economy got a new boost",
     "приклеен заголовок, и немецкий «Nach der Reform bekam die Wirtschaft "
     "neuen Auftrieb»"),

    # --- дефекты в тех же рядах ------------------------------------------------
    (12671, "example_en", "Fill the basin with warm water",
     "The pelvis is an important part of the skeleton",
     "немецкий про таз в скелете, английский мыл раковину — спутаны омонимы"),
    (12671, "example_pl", "Umyj ręce w zlewie obok",
     "Miednica jest ważną częścią szkieletu", "то же"),
    (14433, "example_uk",
     "Новий бойовик з великою кількістю екшну йде в кінотеатрі",
     "У цьому фільмі багато екшену",
     "немецкий «Dieser Film hat viel Action», а не про кинотеатр"),
    (14433, "example_tr", "Bol aksiyonlu yeni aksiyon filmi sinemada oynuyor",
     "Bu filmde bol aksiyon var", "то же"),
    (18093, "example_tr", "Cevher maden çıkarılıyor",
     "Cevher madende çıkarılıyor", "пропущен местный падеж: «madende»"),
    (18100, "example_tr", "Ekonomik artış tüm bölgeye yardımcı oldu",
     "Reformdan sonra ekonomi yeni bir canlanma yaşadı",
     "в немецком «после реформы», а не «помогло всему региону»"),
    (11951, "example_pl", "Je sushi pałeczkami",
     "Jadła pałeczkami, jak było przyjęte w jej kulturze",
     "немецкий «Sie aß mit Stäbchen, wie es in ihrer Kultur üblich war»"),
    (12829, "example_uk", "Не запалюй свічку на столі",
     "Не заражай мене – я хворий",
     "взято другое значение: «anstecken» тут заражать, а не зажигать"),
    (12829, "example_tr", "Bana gribini bulaştırma",
     "Bana hastalığını bulaştırma – ben hastayım",
     "потеряна вторая половина фразы"),
    (12829, "example_pl", "Nie podchodź, bo mnie zarazisz",
     "Nie możesz mnie zarazić – jestem chory",
     "«не подходи» в немецком нет"),
    (18372, "example_uk", "Треба полагодити газонокосарку",
     "Газонокосарка зламалася – треба купити нову",
     "немецкий «Der Rasenmäher ist kaputt – ich muss einen neuen kaufen»"),
    (7400, "example_tr",
     "Fotoğraf çekmek için deklanşörü natıştırman gerekiyor",
     "Fotoğraf çekmek için deklanşöre basman gerekiyor",
     "«natıştırmak» — такого слова нет; на спуск «basmak»"),
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
