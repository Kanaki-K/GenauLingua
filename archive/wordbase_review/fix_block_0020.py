"""
Сплошная вычитка, блок 20: ряды 2301–2500 по рангу частотности
(id первого 14421, id последнего 17103).

Находки:

* `Daumen` — немецкий «Ich drücke dir die Daumen» это пожелание удачи, а
  английский жаловался на больной палец, украинский порезал палец ножом,
  турецкий нажал пальцем на звонок. Три разных рассказа про палец вместо
  одного пожелания. Идиома с большим пальцем есть только в польском
  («trzymam kciuki»), поэтому остальные переведены своими выражениями —
  как с `Appetit` в блоке 18.
* `Fahrzeug` — русский требовал зарегистрировать машину, украинский ездил
  на работу общественным транспортом, а немецкий сказал «машина стоит
  перед дверью».
* `bilden`, `Aktion`, `Geisel`, `Vernunft`, `vollständig`, `Front`,
  `vorhaben`, `Generation`, `Bahn`, `Dschungel`, `verderben`, `nutzlos`,
  `Kostüm`, `Profi`, `rausgehen`, `hinlegen` — то же: перевод переводит
  другую фразу.
* `befragen` — турецкое «sorgulyoruz». Такого слова нет.
* `vor` и `daraus` — в немецком стоят стяжения «vorm Kino» и «draus», и
  само слово ряда в примере не видно. Для карточки это дорого: учится
  «vorm», а заголовок «vor». Эталон поправлен.
* `vor` — в польских значениях «przed, przed kinem»: второе это кусок
  примера, а не значение.
* `versagen` — в турецких значениях «beceremem», спряжённая форма среди
  инфинитивов.
* `ausschalten` — немецкое «Ich schalt» вместо «Ich schalte», а английский
  и турецкий сделали из утверждения приказ.
* `Juni` и `Hauptquartier` — «haziranda» и «Münihte»: в турецком название
  месяца пишется с заглавной, а имя собственное берёт апостроф.
* `Einbruch` — украинское «злам» это перелом; взлом «злом», как и в
  значениях.
* `Marine` — в русских значениях «морская пехота США». Это Marines,
  другое слово.

    python -m app.scripts.fix_block_0020            # показать
    python -m app.scripts.fix_block_0020 --apply    # применить
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
    (115, "example_uk", "Діти утворили велике коло",
     "Вона підвищує свою кваліфікацію",
     "немецкий «Sie bildet sich weiter», а украинский про дітей і коло"),
    (115, "example_tr", "Birlikte yeni bir ekip kurduk",
     "Kendini geliştirmeye devam ediyor", "то же: турецкий собрал команду"),
    (14992, "example_tr", "Bizim nesil teknolojiyi farklı düşünüyor",
     "Genç nesil teknolojiyi çok kullanıyor",
     "немецкий про молодое поколение и про то, что оно пользуется"),
    (6775, "example_uk", "Там був гучний гук", "Почувся гучний гуркіт",
     "«гук» — не то слово, и «там був» калька"),
    (6783, "example_tr", "Bugün ne planlıyorsun",
     "Büyük bir şey planlıyor olmalı",
     "немецкий «Er muss etwas Großes vorhaben»"),
    (1323, "example_en", "My thumb still hurts a bit",
     "I'm keeping my fingers crossed for you",
     "немецкий «Ich drücke dir die Daumen» — пожелание удачи"),
    (1323, "example_ru", "Держу за тебя большие пальцы",
     "Скрещиваю за тебя пальцы",
     "«держу большие пальцы» — дословная калька с немецкого"),
    (1323, "example_uk", "Я порізав великий палець ножем",
     "Тримаю за тебе кулачки",
     "то же: пожелание удачи, а не порезанный палец"),
    (1323, "example_tr", "Başparmağımla zile bastım",
     "Senin için şans diliyorum", "то же: турецкий нажал на звонок"),
    (14425, "example_tr", "Onun şarkısı çok güzeldi",
     "Onun şarkı söylemesi çok güzeldi",
     "«şarkısı» — её песня; «Gesang» это пение"),
    (17099, "example_ru", "Это транспортное средство надо зарегистрировать",
     "Автомобиль стоит перед дверью",
     "немецкий «Das Fahrzeug steht vor der Tür»"),
    (17099, "example_uk", "Я їжджу на роботу громадським транспортом",
     "Автомобіль стоїть перед дверима", "то же"),
    (6798, "example_uk", "У магазині акція на каву",
     "Це була спонтанна акція",
     "немецкий «Das war eine spontane Aktion»"),
    (15448, "example_tr", "Ormanda çok hayvan yaşıyor",
     "Yağmur ormanlarında çok hayvan yaşıyor",
     "«orman» — просто лес; «Dschungel» это «yağmur ormanı»"),
    (16041, "example_tr", "Kaçırma haberlerdeydi",
     "Adam kaçırma olayı haberlerdeydi",
     "«Kaçırma» одним словом не читается"),
    (6804, "example_uk", "Я хочу лягти й поспати",
     "Мені треба трохи прилягти",
     "немецкий «Ich muss mich kurz hinlegen»"),
    (6809, "example_tr", "Arabayı evin önüne park ettim",
     "Grubun önünde duruyor",
     "немецкий «Er steht an der Front der Gruppe», турецкий — про парковку"),
    (6810, "example_uk", "М'ясо швидко псується на спеці",
     "Їжа скоро зіпсується",
     "немецкий «Das Essen wird bald verderben»"),
    (6814, "example_tr", "Hava güzel, biraz dışarı çıkalım",
     "Biraz dışarı çıkıyoruz", "немецкий «Wir gehen kurz raus»"),
    (16043, "example_uk", "Злочинці відпустили всіх заручників",
     "Поліція веде переговори із захоплювачами заручників",
     "немецкий «Die Polizei verhandelt mit den Geiselnehmern»"),
    (10324, "example_tr", "Hasta babası yüzünden çok keder duyuyor",
     "Babasını kaybettiği için çok keder duyuyor",
     "в немецком отец умер, а не болен"),
    (13651, "example_pl", "Na bal przebierańców kupiłam kostium wiedźmy",
     "Na Halloween kupiłem sobie kostium wampira",
     "немецкий про Хэллоуин и костюм вампира"),
    (2066, "example_tr", "Tam zamanında geldin",
     "Lütfen formu eksiksiz doldur",
     "немецкий «Bitte füll das Formular vollständig aus»"),
    (72, "example_en", "We live near the railway station",
     "I take the train to work",
     "немецкий «Ich fahre mit der Bahn zur Arbeit»"),
    (10330, "example_tr", "Biraz akıl kullan lütfen",
     "Sağduyunu dinle ve o arabayı alma",
     "немецкий «Hör auf die Vernunft und kauf das Auto nicht»"),
    (6831, "example_uk", "Старий телефон уже непридатний",
     "Старий комп'ютер став зовсім непридатним", "в немецком компьютер"),
    (12535, "example_pl", "Osunęła się nieprzytomna na ziemię",
     "Straciła przytomność i upadła",
     "немецкий «wurde ohnmächtig und fiel um»"),
    (8807, "example_en", "She's a real professional at work",
     "He's a real professional",
     "в немецком «он», и «на работе» там нет"),

    # --- потеряно или добавлено ------------------------------------------------
    (18680, "example_pl", "Początek filmu był strasznie nudny",
     "Początek filmu był nudny", "«strasznie» в немецком нет"),
    (16032, "example_ru", "Поставьте подпись",
     "Пожалуйста, поставьте подпись", "потеряно «bitte»"),
    (2586, "example_pl", "Ktoś mi chyba pomoże?", "Ktoś mi pomoże?",
     "«chyba» в немецком нет"),
    (6785, "example_uk", "Вибач, можна тебе на хвилинку?",
     "Вибач, можна тебе на хвилинку перервати?", "потерян глагол"),
    (2682, "example_en", "It's foggy today",
     "The fog is very dense today", "потеряно «sehr dicht»"),
    (2682, "example_uk", "Сьогодні туманно",
     "Сьогодні туман дуже густий", "то же"),
    (2682, "example_tr", "Bugün sisli", "Bugün sis çok yoğun", "то же"),
    (6812, "example_uk", "Я можу тебе замінити",
     "Я можу тебе сьогодні замінити", "потеряно «heute»"),
    (6814, "example_uk", "Ми ненадовго виходимо",
     "Ми ненадовго виходимо надвір", "потеряно «на улицу»"),
    (6805, "example_uk", "Можеш надіти ланцюжок?",
     "Можеш надіти мені ланцюжок?", "потеряно «mir»"),
    (13494, "example_tr", "Şu kadın benim teyzem",
     "Şuradaki kadın benim teyzem", "потеряно «dort»"),
    (72, "example_tr", "Trenle gidiyorum", "İşe trenle gidiyorum",
     "потеряно «на работу»"),
    (10324, "example_uk", "Вона відчувала велике горе через смерть батька",
     "Горе через втрату батька велике",
     "в немецком настоящее время, и подлежащее — само горе"),

    # --- немецкий эталон -------------------------------------------------------
    (6780, "example_de", "Wir treffen uns vorm Kino",
     "Wir treffen uns vor dem Kino",
     "«vorm» — стяжение, и слово ряда «vor» в примере не видно"),
    (6824, "example_de", "Was soll ich draus machen?",
     "Was soll ich daraus machen?",
     "«draus» — стяжение, и слово ряда «daraus» в примере не видно"),
    (2232, "example_de", "Ich schalt das Licht aus",
     "Ich schalte das Licht aus", "«schalt» — разговорное усечение"),

    # --- значения ---------------------------------------------------------------
    (6780, "translation_pl", "przed, przed kinem", "przed",
     "«przed kinem» — кусок примера, а не значение"),
    (8806, "translation_ru",
     "военно-морской флот, флот, морская пехота США",
     "военно-морской флот, флот",
     "«морская пехота США» — это Marines, другое слово"),
    (6808, "translation_tr", "başarısız olmak, beceremem, bozulmak",
     "başarısız olmak, becerememek, bozulmak",
     "«beceremem» — спряжённая форма среди инфинитивов"),
    (6798, "translation_uk", "акція, дія, заход, знижка в магазині",
     "акція, дія, захід, знижка в магазині", "«заход» — русизм"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (2253, "example_tr", "Katılımcılara sorgulyoruz",
     "Katılımcılara anket yapıyoruz",
     "«sorgulyoruz» — такого слова нет; и «befragen» это опрашивать"),
    (6826, "example_tr", "Bu benim için kolay bir alıştırmadı",
     "Bu benim için kolay bir alıştırmaydı",
     "«alıştırmadı» читается как «не приучил»"),
    (455, "example_tr", "Kurs haziranda başlıyor",
     "Kurs Haziran'da başlıyor",
     "название месяца с заглавной и с апострофом"),
    (8809, "example_tr", "Şirketin genel merkezi Münihte",
     "Şirketin genel merkezi Münih'te",
     "пропущен апостроф в имени собственном"),
    (13937, "example_tr", "Bu arada, Annayı gördün mü?",
     "Bu arada, Anna'yı gördün mü?", "то же"),

    # --- грамматика целевого языка ---------------------------------------------
    (13936, "example_tr", "Bu sadece aptal laflar",
     "Bunlar sadece aptal laflar", "«bu» с множественным «laflar»"),
    (6780, "example_tr", "Sinema önünde buluşacağız",
     "Sinemanın önünde buluşacağız", "пропущен родительный падеж"),
    (17100, "example_tr", "Tank şehirde geçti", "Tank şehirden geçti",
     "нужен исходный падеж: «şehirden»"),
    (738, "example_tr", "Mutfak temizliyorum", "Mutfağı temizliyorum",
     "пропущен винительный падеж"),
    (16034, "example_uk", "У нього є залізна алібі на вечір",
     "У нього є залізне алібі на вечір", "«алібі» середнього роду"),
    (14428, "example_uk", "Мене цікавить інша культура",
     "Мене цікавлять інші культури", "в немецком множественное число"),
    (14992, "example_uk",
     "Молоде покоління багато користується технологією",
     "Молоде покоління багато користується технологіями",
     "по-людски во множественном, как и в остальных языках"),
    (2375, "example_uk", "Стався злам", "Стався злом",
     "«злам» — перелом; взлом это «злом», как и в значениях"),
    (13494, "example_ru", "Та женщина там моя тётя",
     "Та женщина там — моя тётя", "без тире фраза не читается"),
    (13494, "example_uk", "Та жінка там моя тітка",
     "Та жінка там — моя тітка", "то же"),
    (2217, "example_uk", "Будь уважною на уроці", "Будь уважним на уроці",
     "в остальных языках обращение к мужчине, немецкий без рода"),
    (2066, "example_uk", "Будь ласка, заповніть форму повністю",
     "Будь ласка, заповни форму повністю",
     "в немецком обращение на «ты», как и в русском"),
    (2232, "example_en", "Switch off the light", "I switch off the light",
     "в немецком утверждение, а не приказ"),
    (2232, "example_tr", "Işığı kapat", "Işığı kapatıyorum", "то же"),

    # --- подменённое значение ---------------------------------------------------
    (6785, "example_tr", "Pardon, seni kısaca kesebilir miyim?",
     "Pardon, sözünü kısaca kesebilir miyim?",
     "«seni kesmek» — разрезать человека; прерывают «sözünü»"),
    (13492, "example_tr", "Ekmek ve süte ihtiyacımız var",
     "Ekmeğe ve ayrıca süte ihtiyacımız var",
     "«sowie» — «а также», в значениях стоит «ve ayrıca»"),
    (13493, "example_tr", "Sorun hakkında hiçbir şey söyleyemem",
     "Sorduğun soru hakkında hiçbir şey söyleyemem",
     "«sorun» читается как «проблема»; в немецком «твой вопрос»"),
    (6812, "example_tr", "Seni bugün temsil edebilirim",
     "Bugün senin yerine bakabilirim",
     "«temsil etmek» — представлять; подменить это «yerine bakmak»"),
    (6819, "example_tr", "Asansörde sıkıştık",
     "Asansörde mahsur kaldık",
     "«sıkışmak» — зажало; заперты это «mahsur kalmak»"),
    (15451, "example_tr", "Balık yeme ısırmıyor", "Balık oltaya gelmiyor",
     "по-турецки рыба «не идёт на удочку»"),
    (12143, "example_uk", "Ніхто не любить поганого невдаху",
     "Ніхто не любить того, хто не вміє програвати",
     "«невдаха» — неудачник вообще; немецкий про того, кто плохо проигрывает"),
    (8806, "example_uk", "Мій брат служить у військовому флоті",
     "Мій брат служить у військово-морському флоті",
     "в значениях стоит «військово-морський флот»"),
    (762, "example_uk", "Я дотримуюся рецепта", "Я готую за рецептом",
     "немецкий «Ich koche nach dem Rezept» — готовлю по рецепту"),
    (762, "example_tr", "Tarife uyuyorum", "Tarife göre yemek yapıyorum",
     "то же"),
    (14995, "example_tr", "Baba işten eve hemen geliyor",
     "Babacığım işten az sonra eve geliyor",
     "«Papi» — папочка, и «hemen» это сейчас же, а не «скоро»"),

    # --- говорить по-людски -----------------------------------------------------
    (116, "example_ru", "Куртка была очень дёшева",
     "Куртка была очень дешёвой", "краткая форма «дёшева» — так не говорят"),
    (6780, "example_pl", "Spotkajmy się przed kinem",
     "Spotykamy się przed kinem",
     "в немецком утверждение, а не предложение встретиться"),
    (6817, "example_uk", "Коли повинна починатися вечірка?",
     "Коли ж починається вечірка?", "«повинна починатися» — калька"),
    (10330, "example_uk", "Послухай розум і не купуй цю машину",
     "Прислухайся до розуму і не купуй цю машину",
     "«послухай розум» — так не говорят"),
    (11676, "example_uk", "Він випив своє пиво залпом",
     "Він випив своє пиво одним духом", "«залпом» — русизм"),
    (2066, "example_pl", "Proszę wypełnić formularz kompletnie",
     "Proszę wypełnić formularz w całości",
     "«kompletnie» о заполнении так не говорят"),
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
