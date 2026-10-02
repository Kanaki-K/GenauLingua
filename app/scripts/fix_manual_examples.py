"""
Примеры, которые переводили другое предложение. Переведено руками.

ЗАЧЕМ. Карточка после ответа показывает немецкий пример и перевод стопкой,
друг под другом с флагами. Человек читает их как пару. Когда немецкое «Ich
trinke Wasser» стоит рядом с украинским «Хочеш випити чаю з нами?», пара
читается как плохой перевод и подрывает доверие ко всей базе.

Это самый массовый класс дефектов: на 300 вычитанных рядов таких около 80.
Здесь — те, что я перевёл сам, начиная с высокочастотных слов уровней A1–B2:
их видят чаще всего.

ПРАВИЛО ПЕРЕВОДА, которому я следовал: то же действующее лицо, тот же
предмет, то же время, то же число. Живой язык, но содержание немецкой фразы
менять нельзя. «Die Prüfung ist gut verlaufen» — это экзамен, а не концерт и
не встреча.

У каждой правки записано «было»: если база изменилась с момента вычитки,
правка пропускается, а не затирает чужое.

    python -m app.scripts.fix_manual_examples            # показать
    python -m app.scripts.fix_manual_examples --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, перевод немецкого примера, немецкий оригинал)
FIXES: list[tuple[int, str, str, str, str]] = [

    (398, "example_uk", "Осінь цього року тепла",
     "Восени стає прохолодно", "Im Herbst wird es kühl"),

    (880, "example_pl", "Samochód stoi przed domem",
     "Stoję tutaj", "Ich stehe hier"),

    (908, "example_uk", "Вона приймає таблетку",
     "Я щоранку приймаю таблетку", "Ich nehme jeden Morgen eine Tablette"),
    (908, "example_en", "She takes a tablet",
     "I take a tablet every morning", "Ich nehme jeden Morgen eine Tablette"),
    (908, "example_tr", "Hap alıyor",
     "Her sabah bir hap alıyorum", "Ich nehme jeden Morgen eine Tablette"),

    (942, "example_uk", "Хочеш випити чаю з нами?",
     "Я п'ю воду", "Ich trinke Wasser"),
    (942, "example_tr", "Günde bol bol su içmelisin",
     "Su içiyorum", "Ich trinke Wasser"),

    (1462, "example_uk", "Це протилежність",
     "Ці два брати — справжня протилежність",
     "Die beiden Brüder sind ein echter Gegensatz"),
    (1462, "example_en", "That is the opposite",
     "The two brothers are a real contrast",
     "Die beiden Brüder sind ein echter Gegensatz"),
    (1462, "example_tr", "Bu bir zıtlık",
     "İki kardeş gerçek bir zıtlık",
     "Die beiden Brüder sind ein echter Gegensatz"),

    (1718, "example_en", "There's a nice park in the vicinity",
     "There's a supermarket nearby", "In der Nähe ist ein Supermarkt"),

    (1876, "example_uk", "Хто піклується про твого собаку?",
     "Я хвилююся за тебе", "Ich sorge mich um dich"),

    (1976, "example_uk", "Я тренуюся тричі на тиждень",
     "Мені сьогодні ще треба повправлятися на піаніно",
     "Ich muss heute noch Klavier üben"),
    (1976, "example_en", "I practice every day",
     "I still have to practice the piano today",
     "Ich muss heute noch Klavier üben"),
    (1976, "example_tr", "Her gün pratik yapıyorum",
     "Bugün hâlâ piyano çalışmam gerekiyor",
     "Ich muss heute noch Klavier üben"),

    (10422, "example_uk", "Мене це дратує",
     "Тобі не треба так хвилюватися", "Du musst dich nicht so aufregen"),
    (10422, "example_en", "That annoys me",
     "You don't need to get so worked up", "Du musst dich nicht so aufregen"),
    (10422, "example_tr", "Bu beni sinirlendiriyor",
     "Bu kadar sinirlenmene gerek yok", "Du musst dich nicht so aufregen"),

    (14393, "example_en", "That's a beautiful work by Picasso",
     "That's a beautiful work of modern art",
     "Das ist ein schönes Werk der modernen Kunst"),
    (14393, "example_tr", "Bu Picassonun güzel bir eseri",
     "Bu, modern sanatın güzel bir eseri",
     "Das ist ein schönes Werk der modernen Kunst"),

    (2949, "example_uk", "Концерт проходить у парку",
     "Іспит пройшов добре", "Die Prüfung ist gut verlaufen"),
    (2949, "example_en", "The meeting went well",
     "The exam went well", "Die Prüfung ist gut verlaufen"),
    (2949, "example_tr", "Buluşma iyi geçti",
     "Sınav iyi geçti", "Die Prüfung ist gut verlaufen"),

    (2954, "example_uk", "Я пакую подарунок",
     "Можеш гарно запакувати подарунок?",
     "Kannst du das Geschenk schön verpacken?"),
    (2954, "example_en", "I pack the gift",
     "Can you wrap the gift nicely?",
     "Kannst du das Geschenk schön verpacken?"),
    (2954, "example_tr", "Hediyeyi paketliyorum",
     "Hediyeyi güzelce paketleyebilir misin?",
     "Kannst du das Geschenk schön verpacken?"),

    (1272, "example_uk", "Збережи квитанцію",
     "Ми повинні зберігати холодну голову",
     "Wir müssen einen kühlen Kopf bewahren"),
    (1272, "example_en", "Keep the receipt",
     "We have to keep a cool head",
     "Wir müssen einen kühlen Kopf bewahren"),
    (1272, "example_tr", "Faturayı saklayın",
     "Soğukkanlılığımızı korumalıyız",
     "Wir müssen einen kühlen Kopf bewahren"),

    (7151, "example_uk", "Приєднайся, ми якраз грали у футбол",
     "Приєднуйся, ми якраз граємо у футбол",
     "Komm hinzu, wir spielen gerade Fußball"),
    (7151, "example_en", "In addition, we need more time",
     "Come join us, we're playing football right now",
     "Komm hinzu, wir spielen gerade Fußball"),
    (7151, "example_tr", "Buna ek olarak başka bir sorunumuz var",
     "Sen de gel, şu anda futbol oynuyoruz",
     "Komm hinzu, wir spielen gerade Fußball"),
    (7151, "example_pl", "Dodatkowo doszły nowe koszty",
     "Dołącz do nas, właśnie gramy w piłkę",
     "Komm hinzu, wir spielen gerade Fußball"),

    (15592, "example_pl", "Delfin wyskoczył wysoko z wody",
     "Delfiny bawią się w wodzie", "Die Delfine spielen im Wasser"),

    (7640, "example_uk", "Вона допомогла мені в важкі часи",
     "Я завжди буду поруч із тобою", "Ich werde dir immer beistehen"),
    (7640, "example_en", "She supported me during difficult times",
     "I will always stand by you", "Ich werde dir immer beistehen"),
    (7640, "example_tr", "Zor zamanlarda bana yardım etti",
     "Her zaman senin yanında olacağım", "Ich werde dir immer beistehen"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, de in FIXES:
            current = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if current is None or current.strip() != was:
                skipped.append((wid, col, current))
            else:
                ok.append((wid, col, was, now, de))

    print(f"=== правок: {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, was, now, de in ok:
        print(f"  {wid} {col}")
        print(f"      de:    {de}")
        print(f"      было:  {was}")
        print(f"      стало: {now}")
    if skipped:
        print("\n--- пропущено, в базе другое ---")
        for wid, col, cur in skipped:
            print(f"  {wid} {col}: {cur!r}")

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
    print("Озвучка этих примеров устарела — клипы пересоберутся при показе")


if __name__ == "__main__":
    main()
