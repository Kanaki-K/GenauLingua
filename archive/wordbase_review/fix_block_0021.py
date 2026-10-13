"""
Сплошная вычитка, блок 21: ряды 2501–2700 по рангу частотности
(id первого 17512, id последнего 16062).

Блок оказался чище предыдущих: 55 правок против 84 и 80. Зато дал два
класса, которые нашлись в нём и закрыты по всей базе.

**Апостроф U+02BC в украинских значениях** — 26 ячеек, вынесены в
отдельный скрипт `fix_uk_apostrophe`. Нашлось здесь: у `vorfahren` в
значениях «підʼїхати» с буквой-модификатором, а в примере «підїхати»
вообще без апострофа.

**Турецкие месяцы со строчной буквы** — 4 ячейки на всю базу: `April`
(«nisan»), `Februar` («şubat»), `Oktober` («ekim, ekim ayı») и `geplant`
(«haziran ayına»). В турецком названия месяцев пишутся с заглавной.
Поиск осторожный: «ocak» это ещё и очаг, «aralık» — промежуток, «ekim» —
сев, и такие ячейки (`Herd`, `Lücke`, `Saat`, `Spektrum`, `Brenner`)
верны, их трогать нельзя.

Прочие находки:

* `Stirn` — немецкий «я ударился лбом», а английский, украинский и
  турецкий сообщают, что лоб прохладный.
* `Praxis` — «Ich gehe in die Praxis zum Zahnarzt»: английский и турецкий
  отправили туда кого-то третьего, украинский записался на приём.
* `vielmals` — английский «I've told you that many times» при немецком
  «Danke vielmals für deine Hilfe».
* `kotzen`, `gespannt`, `begegnen`, `Flieger`, `nebenbei`,
  `Zwischenzeit` — то же: перевод переводит другую фразу.
* `Ofen` — в украинских значениях «печиво-грубка». «Печиво» это печенье.
* `Moral` — в русских значениях «боевой духа».
* `eigenartig` — турецкое «tuhaflı», `Verhältnis` — «Birbrinizle»,
  `spritzen` — украинское «брискати». Таких слов нет.
* `erleichtert` — польское «Jestem bardzo ulżony»: прилагательного
  «ulżony» в польском нет, по-польски «odczuwam ulgę».
* `Dankeschön` — украинское «Щире дякую»: «дякую» это глагол, с
  прилагательным не склеивается.
* `Rasse` — «твоя собака»: в украинском «собака» мужского рода.

    python -m app.scripts.fix_block_0021            # показать
    python -m app.scripts.fix_block_0021 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- пример переводит другую фразу ---------------------------------------
    (883, "example_en", "My forehead is cool", "I bumped my forehead",
     "немецкий «Ich hab mir die Stirn gestoßen» — ударился лбом"),
    (883, "example_uk", "Лоб прохолодний", "Я вдарився лобом", "то же"),
    (883, "example_tr", "Alın serin", "Alnımı çarptım", "то же"),
    (12550, "example_en", "She goes to the practice",
     "I'm going to the dentist's office",
     "немецкий «Ich gehe in die Praxis zum Zahnarzt» — я и к зубному"),
    (12550, "example_tr", "Muayenehaneye gidiyor",
     "Dişçi muayenehanesine gidiyorum", "то же"),
    (12550, "example_uk", "Я записався на прийом у кабінет лікаря",
     "Я йду в кабінет до стоматолога", "то же"),
    (6844, "example_en", "I've told you that many times",
     "Thank you very much for your help",
     "немецкий «Danke vielmals für deine Hilfe»"),
    (12546, "example_en", "I feel sick, I'm going to throw up",
     "That really makes me want to puke",
     "немецкий «Das macht mich echt kotzen»"),
    (12546, "example_tr", "Çocuk bütün gece kustu",
     "Bu gerçekten midemi bulandırıyor", "то же: турецкий про ребёнка"),
    (10337, "example_uk", "Мені цікавий результат",
     "Мені цікаво, яким буде концерт",
     "немецкий «Ich bin gespannt, wie das Konzert wird»"),
    (10337, "example_tr", "Sonucu merak ediyorum",
     "Konserin nasıl olacağını merak ediyorum", "то же"),
    (6854, "example_en", "That was a strange encounter",
     "I ran into him by chance on the street",
     "немецкий «Ich bin ihm zufällig auf der Straße begegnet»"),
    (17105, "example_uk", "Наш літак відлітає о восьмій годині",
     "Літак до Берліна відлітає о восьмій годині", "потеряно «в Берлин»"),
    (17105, "example_tr", "Uçağımız saat sekizde kalkıyor",
     "Berlin uçağı saat sekizde kalkıyor", "то же"),
    (2683, "example_en", "I work on the side on weekends",
     "I work on the side", "«по выходным» в немецком нет"),
    (2683, "example_uk", "Я працюю побічно по вихідних",
     "Я працюю попутно",
     "то же, и «побічно» нет в значениях"),
    (18683, "example_pl", "W tym czasie ja już ugotuję obiad",
     "W tym czasie już zacznę gotować",
     "«ja» лишнее, и обеда в немецком нет"),
    (3077, "example_tr", "Katılıyorum", "Sana tamamen katılıyorum",
     "потеряно «тебе» и «полностью»"),
    (3066, "example_tr", "Birlikte çalışıyoruz",
     "Birlikte çalışmak istiyoruz", "в немецком «хотим работать вместе»"),
    (2261, "example_en", "She has mastered three languages",
     "I have mastered three languages", "в немецком «я»"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (6860, "example_tr", "Davranışı çok tuhaflı", "Davranışı çok tuhaftı",
     "«tuhaflı» — такого слова нет"),
    (15006, "example_tr", "Birbrinizle ilişkiniz nasıl?",
     "Birbirinizle ilişkiniz nasıl?", "«Birbrinizle» — опечатка"),
    (11725, "translation_uk", "брискати, поливати, робити ін'єкцію, колоти",
     "бризкати, поливати, робити ін'єкцію, колоти",
     "«брискати» — опечатка"),
    (10340, "translation_ru",
     "мораль, нравственность, боевой духа, настрой",
     "мораль, нравственность, боевой дух, настрой",
     "«боевой духа» — опечатка"),
    (1741, "translation_uk", "духовка, піч, печиво-грубка",
     "духовка, піч, грубка", "«печиво» — це печиво, а не печка"),
    (10343, "translation_pl", "ulżony, odczuwający ulgę",
     "odczuwający ulgę, z ulgą",
     "прилагательного «ulżony» в польском нет"),
    (10343, "example_pl", "Jestem bardzo ulżony",
     "Odczuwam wielką ulgę", "то же"),
    (13946, "example_uk", "Щире дякую за твою допомогу",
     "Щира подяка за твою допомогу",
     "«дякую» — глагол, с прилагательным не склеивается"),
    (17106, "example_uk", "Чи можеш підїхати?", "Чи можеш під'їхати?",
     "пропущен апостроф"),

    # --- турецкие месяцы со строчной (сплошной поиск по базе) -----------------
    (40, "translation_tr", "nisan", "Nisan",
     "в турецком название месяца с заглавной"),
    (258, "translation_tr", "şubat", "Şubat", "то же"),
    (673, "translation_tr", "ekim, ekim ayı", "Ekim, Ekim ayı", "то же"),
    (6454, "example_tr", "Gezi haziran ayına planlandı",
     "Gezi Haziran ayına planlandı", "то же"),

    # --- русизмы в украинской колонке ----------------------------------------
    (6852, "translation_uk", "кудись, куда-небудь", "кудись, куди-небудь",
     "«куда-небудь» — русизм"),
    (16051, "translation_uk", "невинність, невиновність, наївність",
     "невинність, невинуватість, наївність", "«невиновність» — русизм"),
    (17105, "translation_uk", "літак, літун", "літак, авіатор",
     "«літун» — не то слово"),

    # --- грамматика целевого языка --------------------------------------------
    (14998, "example_uk", "Якої породи твоя собака?",
     "Якої породи твій собака?", "«собака» в украинском мужского рода"),
    (6852, "example_tr", "Sessiz olan bir yerlere gitmem gerek",
     "Sessiz bir yere gitmem gerek",
     "«bir yerlere» — единственное число с множественным"),
    (6838, "example_tr", "Bu hafta zaten sekizinci pizza bu",
     "Bu hafta zaten sekizinci pizza", "«bu» сказано дважды"),
    (17106, "example_tr", "Arabayla önüne çekebilir misin?",
     "Arabayla öne çekebilir misin?", "«önüne» — перед чем?"),
    (6844, "example_uk", "Дякую дуже за твою допомогу",
     "Дуже дякую за твою допомогу", "порядок слов"),

    # --- подменённое значение -------------------------------------------------
    (69, "example_tr", "Çocuklar gölde banyo yapıyorlar",
     "Çocuklar gölde yüzüyor",
     "«banyo yapmak» — мыться в ванне, а дети в озере"),
    (122, "example_tr", "Bana bir sayfa kağıt ver",
     "Bana bir yaprak kağıt ver", "«sayfa» — страница; лист это «yaprak»"),
    (17514, "example_tr", "Hoparlörler çok gürültülü",
     "Hoparlörlerin sesi çok yüksek",
     "«gürültülü» — шумные; в немецком слишком громкие"),
    (13947, "example_uk", "У ресторані був великий гуркіт голосів",
     "У ресторані був великий гомін голосів",
     "«гуркіт» — грохот; в значениях стоит «гомін»"),
    (13947, "example_tr", "Restoranda büyük bir ses karmaşası vardı",
     "Restoranda büyük bir ses uğultusu vardı",
     "в значениях стоит «ses uğultusu»"),
    (2261, "example_tr", "Üç dili biliyorum", "Üç dile hakimim",
     "в значениях «hakim olmak», и немецкий про владение языком"),
    (10335, "example_tr", "Yemek iğrenç tadı var", "Yemeğin tadı iğrenç",
     "фраза не складывается"),

    # --- говорить по-людски ---------------------------------------------------
    (10332, "example_ru", "Друзья подарили ему утешение",
     "Друзья были для него утешением", "«подарили утешение» — калька"),
    (10332, "example_uk", "Його друзі дали йому втіху",
     "Його друзі були для нього втіхою", "то же"),
    (493, "example_uk", "Дверний дзвоник дзвонить", "У двері дзвонять",
     "«дзвоник дзвонить» — тавтология"),
    (13496, "example_uk", "Не цей фільм, а той там",
     "Не цей фільм, а он той", "«той там» — калька"),
    (16051, "example_ru", "Он утверждает свою невиновность",
     "Он настаивает на своей невиновности",
     "«утверждать невиновность» — так не говорят"),
    (16051, "example_uk", "Він стверджує свою невинність",
     "Він наполягає на своїй невинності", "то же"),
    (17781, "example_tr", "Bu restoranda servis çok iyidir",
     "Bu restoranda servis çok iyi", "«-dir» — канцелярит"),
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
