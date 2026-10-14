"""
Перепроверка собственных правок по правилу «говорить по-людски».

Владелец сформулировал требование, которого в прежних критериях не было:
перевод делается по-человечески, без заумных и канцелярских слов, так, чтобы
понял и ребёнок. Это записано в REVIEW_CRITERIA.md первым пунктом, и по
нему перечитаны все 1289 правок, сделанных мной до этого.

ЧТО НАШЛОСЬ. Два настоящих огреха — слово не той формы:

* `kriegen` — турецкое «Karnım acılıyor»: такого слова нет, нужно
  «acıkıyor». Это я и написал неверно.
* `verbinden` — «Seni patronla bağlıyorum»: нужен дательный, «patrona».

И около тридцати мест, где я сам написал книжно там, где немецкий сказал
просто. Самые показательные:

    Вирушання було заплановане на сім ранку   →  Вихід запланували на сім ранку
    Там була велика кількість людей            →  Там було багато людей
    Кафе розташоване навпроти мене             →  Кафе навпроти мене
    Я повідомляю, що захворів                  →  Я кажу, що захворів
    Можеш пояснити мені своє обґрунтування
      цього рішення?                           →  Можеш пояснити, чому ти так вирішив?
    I'm reporting in sick                      →  I'm calling in sick
    She is a kind creature                     →  She is a kind soul
    The timing is really badly chosen          →  The timing is really bad
    Şöminedeki külün dışarı çıkarılması gerek  →  Şöminedeki külü dışarı çıkarmak gerek
    После этого положение улучшилось           →  После этого стало лучше

Правило, по которому я их отбирал: сказал бы я так вслух другому человеку?
Если нет — заменяю, даже когда фраза грамматически безупречна.

    python -m app.scripts.fix_plain_language            # показать
    python -m app.scripts.fix_plain_language --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- мои собственные ошибки в слове ---------------------------------------
    (6261, "example_tr", "Karnım acılıyor", "Karnım acıkıyor",
     "«acılıyor» — нет такого слова; голод это «acıkmak»"),
    (973, "example_tr", "Seni patronla bağlıyorum",
     "Seni patrona bağlıyorum", "«bağlamak» требует дательного падежа"),

    # --- книжно вместо человеческого: украинский -------------------------------
    (16382, "example_uk", "Вирушання було заплановане на сім ранку",
     "Вихід запланували на сім ранку",
     "«вирушання» — книжное слово, живьём так не говорят"),
    (1685, "example_uk", "Там була велика кількість людей",
     "Там було багато людей", "«велика кількість» — канцелярит"),
    (2206, "example_uk", "Це цікавий спосіб це зробити",
     "Цікавий спосіб це зробити", "«це… це» — спотыкается на слух"),
    (6753, "example_uk", "Чи все вийшло із зустріччю?",
     "Зі зустріччю все вийшло?", "порядок слов: так не спрашивают"),
    (6785, "example_uk", "Вибач, чи можу я тебе ненадовго перервати?",
     "Вибач, можна тебе на хвилинку?",
     "по-людски просят именно так, а не «чи можу я перервати»"),
    (1684, "example_uk", "Я повідомляю, що захворів",
     "Я кажу, що захворів", "«повідомляю» — канцелярит"),
    (14171, "example_uk",
     "Можеш пояснити мені своє обґрунтування цього рішення?",
     "Можеш пояснити, чому ти так вирішив?",
     "«своє обґрунтування цього рішення» — канцелярит"),
    (8593, "example_uk", "Дай я швидко приблизно підрахую витрати",
     "Дай я швидко прикину витрати",
     "«швидко приблизно підрахую» — три слова вместо одного"),
    (2948, "example_uk", "Я покидаю місто", "Я їду з міста",
     "«покидаю» — книжное, в живой речи «їду з»"),
    (2573, "example_uk", "Я допомагаю тим, що беру участь у роботі",
     "Я допомагаю тим, що працюю разом",
     "«беру участь у роботі» — канцелярит"),
    (318, "example_uk", "Кафе розташоване навпроти мене",
     "Кафе навпроти мене", "«розташоване» здесь лишнее"),
    (14565, "example_uk",
     "Можеш мені продемонструвати свої нові танцювальні рухи?",
     "Можеш показати свої нові танцювальні рухи?",
     "«продемонструвати» — книжное вместо «показати»"),

    # --- книжно вместо человеческого: турецкий ---------------------------------
    (18348, "example_tr",
     "Bu otelde paran karşılığında gerçekten çok konfor alıyorsun",
     "Bu otelde paranın hakkını alıyorsun",
     "фраза громоздкая; по-турецки говорят короче"),
    (16749, "example_tr",
     "Burada park etmek yasaktır ve senin için pahalı olur",
     "Burada park etmek yasak, sana pahalıya gelir",
     "«yasaktır» — канцелярская форма"),
    (859, "example_tr", "Bu, evin spesiyalitesi", "Bu evin spesiyalitesi",
     "запятая делает фразу книжной"),
    (17069, "example_tr", "Otobüs kilisenin orada duruyor",
     "Otobüs kilisenin önünde duruyor", "«kilisenin orada» — так не говорят"),
    (6694, "example_tr", "Şöminedeki külün dışarı çıkarılması gerek",
     "Şöminedeki külü dışarı çıkarmak gerek",
     "страдательный оборот вместо простого"),
    (10638, "example_tr",
     "Zaferden sonraki zafer sevinci tarif edilemezdi",
     "Kazandıktan sonraki sevinç anlatılamazdı",
     "«zafer» дважды, и «tarif edilemezdi» книжно"),
    (8081, "example_tr",
     "Bu kadar muğlak değil de bana somut bir örnek verebilir misin?",
     "Bana somut bir örnek verebilir misin, bu kadar belirsiz olmasın?",
     "порядок слов делал фразу спотыкающейся"),
    (101, "example_tr", "Sana acil şifalar diliyorum",
     "Sana acil şifalar dilerim", "по-турецки желают в форме «dilerim»"),

    # --- книжно вместо человеческого: английский -------------------------------
    (1685, "example_en", "A large crowd of people was there",
     "There was a big crowd of people", "порядок слов: так естественнее"),
    (3039, "example_en", "The timing is really badly chosen",
     "The timing is really bad", "«badly chosen» — калька с немецкого"),
    (1684, "example_en", "I'm reporting in sick", "I'm calling in sick",
     "по-английски говорят «call in sick»"),
    (6481, "example_en", "She is a kind creature", "She is a kind soul",
     "«creature» о человеке по-английски звучит странно"),
    (8132, "example_en", "I squashed my finger", "I jammed my finger",
     "палец «jam», а не «squash»"),
    (8683, "example_en", "He straightened the fallen tree again",
     "He stood the fallen tree back up", "так говорят живьём"),
    (17432, "example_en", "There are many travel options to Berlin",
     "There are many ways to travel to Berlin",
     "«travel options» — язык брошюры"),
    (2565, "example_en", "The flood has flooded the city",
     "The flood swamped the city", "«flood flooded» — спотыкается"),

    # --- книжно вместо человеческого: польский и русский ----------------------
    (7857, "example_pl", "Czy potrafisz właściwie ocenić sytuację?",
     "Umiesz dobrze ocenić sytuację?", "«potrafisz właściwie» — книжно"),
    (706, "example_pl", "Ile państwa jest?", "Ile osób?",
     "в кафе спрашивают именно так"),
    (13145, "example_pl",
     "Grupa wsparcia spotykała się w każdy wtorek, by rozmawiać o problemach",
     "Grupa wsparcia spotykała się w każdy wtorek, żeby rozmawiać o swoich problemach",
     "«by» — книжный союз, в речи «żeby»"),
    (18939, "example_ru", "После этого положение улучшилось",
     "После этого стало лучше", "«положение улучшилось» — канцелярит"),
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
