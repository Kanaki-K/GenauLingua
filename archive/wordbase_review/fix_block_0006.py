"""
Сплошная вычитка, блок 6: ряды 501–600 по рангу частотности.

Находки:

* `genommen` — немецкое «den Bus nehmen» идиома, и четыре языка перевели её
  дословно: «Я взял автобус», «Wziąłem autobus», «Otobüsü aldım» — по-русски
  и по-польски так не говорят, а по-турецки это читается как «купил
  автобус». Немецкий пример заменён на «Ich hab das Buch genommen»: он
  переводится дословно во все пять языков, и форма «genommen» видна везде.
* `Laden` — в русском списке значений «заряжать». Это глагол «laden», а ряд
  про существительное «der Laden» — магазин.
* `sobald` — в турецком значении стоит многоточие-заглушка: «en kısa sürede
  ... -dığında». Сплошной поиск следов правки её не видел: он смотрит
  примеры, а не переводы.
* `Schreiben` — в английском примере слеш: «I received a letter/notice».
  Тот же поиск ищет слеш с пробелами и этот пропустил.
* `Mord` — в немецком «wegen Mord» без родительного падежа.
* `perfekt` — в украинском «безперечний» (бесспорный) вместо «бездоганний».
* `Gejammer` — в украинском «нитики», такого слова нет.

Отдельный класс, найденный сплошным поиском: **знак ударения U+0301**,
затесавшийся в семь украинских ячеек — «калі́ка», «кова́ль», «піра́та». На
экране он выглядит как лишняя чёрточка, а синтезатор спотыкается.

    python -m app.scripts.fix_block_0006            # показать
    python -m app.scripts.fix_block_0006 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

ACUTE = "́"

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- знак ударения U+0301 в украинских ячейках ----------------------------
    (12594, "translation_uk", f"калі{ACUTE}ка, інвалід", "каліка, інвалід",
     "знак ударения U+0301 в слове"),
    (8976, "translation_uk", f"кова{ACUTE}ль", "коваль",
     "знак ударения U+0301 в слове"),
    (11208, "translation_uk",
     f"нити{ACUTE}ки, нарікання, скиглення, бідкання, скарги",
     "нарікання, скиглення, бідкання, скарги",
     "«нитики» — такого слова нет; и знак ударения U+0301"),
    (10068, "translation_uk",
     f"неймовірний, непра{ACUTE}вдоподібний, дивовижний",
     "неймовірний, неправдоподібний, дивовижний",
     "знак ударения U+0301 в слове"),
    (15039, "translation_uk", f"нарече{ACUTE}ний, жених", "наречений, жених",
     "знак ударения U+0301 в слове"),
    (745, "translation_uk", f"курити, димити, копти{ACUTE}ти",
     "курити, димити, коптити", "знак ударения U+0301 в слове"),
    (13692, "example_uk", f"Його костюм піра{ACUTE}та був дійсно смішним",
     "Його костюм пірата був дійсно смішним",
     "знак ударения U+0301 в слове"),

    # --- следы правки в переводах ---------------------------------------------
    (13383, "translation_tr", "-ir imez, olur olmaz, en kısa sürede ... -dığında",
     "-ir -mez, olur olmaz",
     "многоточие-заглушка в значении, и «-ir imez» вместо «-ir -mez»"),
    (2802, "example_en", "I received a letter/notice",
     "I received an official letter",
     "слеш с двумя вариантами остался от правки"),

    # --- неверное значение в списке -------------------------------------------
    (1639, "translation_ru", "магазин, лавка, ставня, заряжать",
     "магазин, лавка, ставня",
     "«заряжать» — это глагол laden, а ряд про существительное"),
    (6322, "translation_uk", "ідеальний, досконалий, безперечний, чудовий",
     "ідеальний, досконалий, бездоганний, чудовий",
     "«безперечний» — бесспорный, а perfekt — безупречный"),

    # --- ошибка в немецком эталоне -------------------------------------------
    (15933, "example_de", "Die Polizei ermittelt wegen Mord",
     "Die Polizei ermittelt wegen Mordes",
     "«wegen» требует родительного падежа"),

    # --- идиома, переведённая дословно ----------------------------------------
    (6301, "example_de", "Ich hab den Bus genommen",
     "Ich hab das Buch genommen",
     "«den Bus nehmen» — идиома, и дословно она не переводится ни в один язык"),
    (6301, "example_en", "Sorry, this seat is taken", "I took the book",
     "вслед за немецким; прежний пример был вообще о другом"),
    (6301, "example_ru", "Я взял автобус", "Я взял книгу",
     "«взял автобус» по-русски не говорят"),
    (6301, "example_uk", "Я взяв автобус", "Я взяв книгу",
     "«взяв автобус» по-украински не говорят"),
    (6301, "example_tr", "Otobüsü aldım", "Kitabı aldım",
     "«otobüsü aldım» читается как «купил автобус»"),
    (6301, "example_pl", "Wziąłem autobus", "Wziąłem książkę",
     "«wziąłem autobus» по-польски не говорят"),

    # --- пример переводит другую фразу ----------------------------------------
    (2505, "example_uk", "У мене дивне почуття", "У мене погане почуття",
     "в немецком «плохое», а не «странное»"),
    (2505, "example_tr", "Kötü bir his var bende", "İçimde kötü bir his var",
     "порядок слов: по-турецки так не говорят"),
    (6298, "example_uk", "У мене мало часу", "У мене сьогодні мало часу",
     "потеряно «сегодня»"),
    (6298, "example_tr", "Bugün çok az uyudum", "Bugün çok az zamanım var",
     "пример про сон, а немецкий про время"),
    (1714, "example_uk", "Я отримала повідомлення",
     "Я отримав повідомлення",
     "женский род, а в остальных языках мужской"),
    (13382, "example_en", "That costs three million",
     "That costs three million euros", "потеряно «евро»"),
    (13382, "example_uk", "Це коштує три мільйони",
     "Це коштує три мільйони євро", "потеряно «євро»"),
    (13382, "example_tr", "Bu ev bir milyon lira", "Bu üç milyon euro",
     "в немецком три миллиона евро, а не дом за миллион лир"),
    (2636, "example_en", "I'll take care of it", "Take care of it",
     "в немецком повеление, а не обещание"),
    (2636, "example_uk", "Я піклуюся про свою бабусю", "Займися цим",
     "пример про бабушку, а немецкий — повеление"),
    (2636, "example_tr", "Onunla ilgileniyorum", "Bununla ilgilen",
     "в немецком повеление, а не рассказ"),
    (10060, "example_pl", "Cholera, zapomniałem kluczy",
     "Cholera, jestem spóźniony",
     "пример про ключи, а немецкий про опоздание"),
    (6306, "example_en", "We have to fight",
     "The boxers fight for the title",
     "в немецком боксёры и титул"),
    (6306, "example_tr", "Savaşmalıyız",
     "Boksörler şampiyonluk için dövüşüyor", "в немецком боксёры и титул"),
    (13383, "example_tr", "Eve varır varmaz beni ara",
     "Oraya varır varmaz seni arayacağım",
     "в немецком «как только я приду, я позвоню», а не приказ"),
    (937, "example_en", "She wears pants", "She wears blue trousers",
     "потеряно «синие»"),
    (937, "example_uk", "Вона носить штани", "Вона носить сині штани",
     "потеряно «синие»"),
    (937, "example_tr", "Bir pantolon giyiyor", "Mavi bir pantolon giyiyor",
     "потеряно «синие»"),
    (394, "example_uk", "Як називається ця вулиця?", "Як тебе звати?",
     "в немецком «как тебя зовут», а не про улицу"),
    (13384, "example_uk", "Він став лікарем минулого року",
     "Робота була зроблена", "в немецком «работа была сделана»"),
    (13384, "example_tr", "Her şey çok çabuk oldu", "İş yapıldı",
     "в немецком «работа была сделана»"),
    (1589, "example_en", "Our class has twenty students",
     "I'm in the fifth grade", "в немецком «я в пятом классе»"),
    (617, "example_tr", "Ağzım yandı, çorba çok sıcaktı", "Ağzını aç",
     "в немецком «открой рот», а не рассказ про суп"),
    (15930, "example_ru", "В конце фильма убили главного героя",
     "Эта учёба меня когда-нибудь убьёт",
     "в немецком про учёбу, а не про фильм"),
    (15930, "example_uk", "У фільмі вбили головного героя",
     "Це навчання мене колись уб'є",
     "в немецком про учёбу, а не про фильм"),
    (15930, "example_en", "This stress will kill me",
     "All this studying will kill me",
     "в немецком про учёбу, а не про стресс"),
    (15930, "example_tr", "Bu stres beni öldürecek",
     "Bu kadar çalışmak beni öldürecek",
     "в немецком про учёбу, а не про стресс"),
    (30, "example_uk", "Не забудь дзвонити мамі", "Я подзвоню тобі завтра",
     "в немецком «я позвоню тебе завтра»"),
    (1426, "example_tr", "Yarın sabah İzmir'e uçuyorum",
     "İspanya'ya uçuyoruz", "в немецком «мы летим в Испанию»"),
    (2492, "example_tr", "Müdür toplantıyı yürütüyor",
     "Konuşmayı ben yürütüyorum",
     "в немецком «я веду разговор», а не директор собрание"),
    (625, "example_en", "I like chocolate",
     "We don't like onions in the soup",
     "в немецком про лук в супе, и с отрицанием"),
    (625, "example_uk", "Мені подобається шоколад",
     "Ми не любимо цибулю в супі",
     "в немецком про лук в супе, и с отрицанием"),
    (625, "example_tr", "Çikolatayı severim",
     "Çorbada soğan sevmiyoruz",
     "в немецком про лук в супе, и с отрицанием"),
    (13387, "example_uk", "У нашій групі лише вісім людей",
     "Я встаю о восьмій", "в немецком «я встаю в восемь»"),
    (13387, "example_pl", "Mój syn ma osiem lat", "Wstaję o ósmej",
     "в немецком «я встаю в восемь»"),
    (562, "example_tr", "Dünkü parti çok eğlenceliydi", "Şaka komikti",
     "в немецком про шутку, а не про вечеринку"),
    (6320, "example_tr", "Savaş henüz bitmedi", "Mücadele henüz bitmedi",
     "«savaş» — война, а Kampf здесь борьба"),
    (6324, "example_uk", "Пішли назовні, тут душно", "Виходь звідти",
     "в немецком «выходи оттуда»"),
    (2204, "example_en", "She couldn't hide her anger",
     "I'm in big trouble",
     "в немецком «у меня большие неприятности»"),
    (2204, "example_uk", "Він не міг стримати злість",
     "У мене великі неприємності",
     "в немецком «у меня большие неприятности»"),

    # --- вежливая форма и лишнее против немецкого -----------------------------
    (657, "example_uk", "Скажіть це ще раз", "Скажи це ще раз",
     "в немецком «Sag» — ты, а не Вы"),
    (657, "example_tr", "Bunu tekrar söyleyin", "Bunu tekrar söyle",
     "в немецком «Sag» — ты, а не Вы"),
    (1433, "example_tr", "Lütfen beni takip edin", "Lütfen beni takip et",
     "в немецком «Folg» — ты, а не Вы"),
    (1433, "example_pl", "Proszę iść za mną", "Idź za mną, proszę",
     "в немецком повеление на «ты»"),
    (706, "example_pl", "Ile państwa jest osób?", "Ile państwa jest?",
     "порядок слов: по-польски так не спрашивают"),
    (10061, "example_pl", "Nie jestem na ciebie zły", "Nie jestem zły",
     "«на тебя» в немецком нет"),
    (10063, "example_pl", "Jestem z ciebie bardzo dumny",
     "Jestem z ciebie dumny", "«bardzo» в немецком нет"),
    (10064, "example_pl", "Bądź ostrożny na schodach", "Bądź ostrożny",
     "«на лестнице» в немецком нет"),
    (10068, "example_pl", "To jest wprost niewiarygodne",
     "To jest niewiarygodne", "«wprost» в немецком нет"),
    (10073, "example_pl", "Nie pamiętam jego imienia", "Nie pamiętam",
     "«его имени» в немецком нет"),
    (1129, "example_uk", "Ти можеш змінити час?",
     "Ти можеш змінити дату зустрічі?",
     "в немецком Termin — встреча, а не просто время"),
    (790, "example_uk", "Я надішлю тобі фото ввечері",
     "Я надсилаю тобі фото",
     "«ввечері» в немецком нет, и время настоящее"),

    # --- опечатки и грамматика -------------------------------------------------
    (10062, "example_pl", "Myślę że to prawda", "Myślę, że to prawda",
     "пропущена запятая перед «że»"),
    (13385, "example_en", "As long as you're here, everythings good",
     "As long as you're here, everything's good",
     "«everythings» без апострофа"),
    (18596, "example_tr", "Önce her şey farklıydı",
     "Önceden her şey farklıydı",
     "«önce» значит «сначала», а vorher — «прежде»"),
    (2258, "example_tr", "Kitabı tutuyorum", "Kitabı kendimde tutuyorum",
     "behalten — оставить себе, а «tutuyorum» просто «держу»"),
    (15933, "example_tr", "Polis cinayet soruşturuyor",
     "Polis cinayeti soruşturuyor", "пропущен винительный падеж"),
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
