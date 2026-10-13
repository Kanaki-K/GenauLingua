"""
Сплошная вычитка, блок 26: ряды 3501–3700 по рангу частотности
(id первого 7073, id последнего 8872).

Находки:

* `ängstlich` — немецкий про ребёнка, который боится собак, а украинский
  и польский про пугливого пса. Два языка из пяти переставили местами
  того, кто боится.
* `eindringen` — немецкий «Diebe konnten ins Haus eindringen», а
  английский, украинский и турецкий про воду, которая просочилась в дом.
* `drängen` — немецкий про учителя и учеников, турецкий «не торопи
  меня», польский «не давите на меня».
* `zeichnen` — в немецком «я рисую», в трёх языках «она рисует».
* `Gefecht`, `quälen`, `manipulieren`, `unheimlich`, `Mumm`,
  `aufhängen`, `Anfänger`, `Casino`, `befürchten`, `allmählich`,
  `vergeuden`, `backen`, `speziell`, `Autogramm`, `Prügel`,
  `Garderobe` — то же: перевод переводит другую фразу.
* `drunter` — английское «maybe its there», `läuten` — «at 8 oclock»:
  тот же класс пропущенного апострофа, что и в блоках 22 и 25.
* `überdenken` — украинское «перш ніж сказу так», `benommen` — польское
  «po jazdzie», `Glückspilz` — турецкое «Piyangoyı»,
  `Durchsuchungsbefehl` — «Polisinin». Опечатки.
* `Knöchel` — «вывихнута лодыжка» при немецком «verstaucht». Вывих и
  растяжение — разные травмы.
* Турецкие падежи: `erpressen` («beni şantaj yapmaya»), `quälen` («onu
  işkence ediyor»), `formen` («kili şekil veriyor»), `zerbrochen`,
  `Bräutigam`.

    python -m app.scripts.fix_block_0026            # показать
    python -m app.scripts.fix_block_0026 --apply    # применить
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
    (10460, "example_uk", "Наш пес дуже полохливий",
     "Дитина боязка і боїться собак",
     "немецкий «Das Kind ist ängstlich und fürchtet sich vor Hunden»"),
    (10460, "example_pl", "Ten pies jest bardzo lękliwy",
     "Dziecko jest lękliwe i boi się psów",
     "то же: в немецком ребёнок, а не пёс"),
    (10460, "example_en", "The child is fearful of dogs",
     "The child is fearful and afraid of dogs",
     "потеряно «ängstlich und»"),
    (10460, "example_tr", "Çocuk köpeklerden korkar",
     "Çocuk ürkek ve köpeklerden korkuyor", "то же"),
    (7088, "example_en", "Water penetrated the house",
     "Thieves managed to break into the house",
     "немецкий «Diebe konnten ins Haus eindringen» — воры, не вода"),
    (7088, "example_uk", "Вода проникла в будинок",
     "Злодії змогли проникнути в будинок", "то же"),
    (7088, "example_tr", "Su eve sızdı", "Hırsızlar eve zorla girdi",
     "то же"),
    (10472, "example_tr", "Beni acele ettirme, lütfen",
     "Öğretmen öğrencileri ödevlerini yapmaya zorluyor",
     "немецкий «Der Lehrer drängt die Schüler, ihre Hausaufgaben zu machen»"),
    (10472, "example_pl", "Nie naciskaj na mnie, muszę to przemyśleć",
     "Nauczyciel naciska na uczniów, żeby robili zadania domowe", "то же"),
    (1069, "example_en", "She draws a picture", "I draw a picture",
     "немецкий «Ich zeichne ein Bild» — я, а не она"),
    (1069, "example_uk", "Вона малює картину", "Я малюю картину", "то же"),
    (1069, "example_tr", "O bir resim çiziyor", "Bir resim çiziyorum",
     "то же"),
    (16142, "example_ru", "Бой длился до самого утра",
     "В бою было много раненых",
     "немецкий «In dem Gefecht gab es viele Verletzte»"),
    (16142, "example_uk", "Бій тривав усю ніч",
     "У бою було багато поранених", "то же"),
    (10465, "example_pl", "Nie dręcz kota, on tego nie lubi",
     "Myśli dręczą go codziennie",
     "немецкий «Die Gedanken quälen ihn jeden Tag»"),
    (10466, "example_pl", "On ciągle próbuje mną manipulować",
     "Ciągle próbujesz mną manipulować, ale to już nie działa",
     "в немецком «ты», а не «он»"),
    (10467, "example_pl", "Ten stary dom jest trochę przerażający",
     "To była przerażająca noc w starym zamku",
     "немецкий «Das war eine unheimliche Nacht im alten Schloss»"),
    (10469, "example_pl", "Nie miał odwagi, żeby jej to powiedzieć",
     "Ma odwagę mówić przed klasą",
     "немецкий «Er hat den Mumm, vor der Klasse zu sprechen»"),
    (7084, "example_tr", "Çamaşırları balkona asmak lazım",
     "Resmi duvara asıyorum",
     "немецкий про картину на стене, а не про бельё на балконе"),
    (9480, "example_tr", "Bu kitap yeni başlayanlara göre",
     "Yeni başlayan olarak yavaş antrenman yapmalısın",
     "немецкий «Als Anfänger solltest du langsam trainieren»"),
    (12179, "example_pl", "Wygrał trochę pieniędzy w kasynie",
     "Idziemy do kasyna pograć",
     "немецкий «Wir gehen ins Casino und spielen»"),
    (10463, "example_pl", "Obawiam się, że spóźnimy się na pociąg",
     "Obawiam się, że on nie przyjdzie",
     "немецкий «Ich befürchte, er kommt nicht»"),
    (18717, "example_pl", "Stopniowo przyzwyczaiłem się do nowej pracy",
     "Słońce stopniowo zachodziło i niebo ciemniało",
     "немецкий «Die Sonne ging allmählich unter»"),
    (18714, "example_pl", "Nie marnuj tyle jedzenia",
     "Nie powinieneś marnować swoich pieniędzy",
     "в немецком деньги, а не еда"),
    (67, "example_uk", "Мама пече пиріг із яблуками",
     "Моя бабуся пече чудові пироги",
     "немецкий «Meine Oma backt wunderbare Kuchen»"),
    (1886, "example_uk", "У неї особливий голос", "Це спеціально для тебе",
     "немецкий «Das ist speziell für dich»"),
    (14463, "example_tr", "Oyuncudan bir otograf aldım",
     "Futbolcu bana imzasını verdi",
     "немецкий «Der Fußballspieler hat mir sein Autogramm gegeben»"),
    (10461, "example_pl", "Dostał lanie od starszych chłopaków",
     "Dostał lanie od innych dzieci",
     "в немецком другие дети, а не старшие мальчики"),
    (13662, "example_pl", "Płaszcz powieś w garderobie",
     "Moja garderoba potrzebuje nowych ciuchów",
     "немецкий «Meine Garderobe braucht neue Klamotten»"),
    (12586, "example_en", "The mosquito keeps stinging me",
     "The mosquitoes are stinging everywhere today",
     "немецкий «Die Mücken stechen heute überall»"),
    (12586, "example_uk", "Комар постійно мене кусає",
     "Комари сьогодні кусають усюди", "то же"),
    (12586, "example_tr", "Sivrisinek beni sürekli sokuyor",
     "Sivrisinekler bugün her yerde sokuyor", "то же"),
    (13514, "example_uk", "Подивись внизу, можливо, це там",
     "Подивись під ним, можливо, воно там",
     "немецкий «Schau mal drunter» — под ним, а не внизу"),
    (10471, "example_pl", "Dzieci piszczały z radości",
     "Dziewczyny piszczą z radości",
     "в немецком девушки, а не дети"),

    # --- пропущенный апостроф (тот же класс, что в блоках 22 и 25) ------------
    (13514, "example_en", "Look under it, maybe its there",
     "Look under it, maybe it's there", "«its» вместо «it's»"),
    (14001, "example_en", "The bell rings at 8 oclock",
     "The bell rings at 8 o'clock", "«oclock» без апострофа"),

    # --- потеряно или добавлено ------------------------------------------------
    (14461, "example_en", "The director is in charge of the direction",
     "The director is in charge of the direction of this film",
     "потеряно «bei diesem Film»"),
    (10464, "example_tr", "Evet demeden önce tekrar düşünmem gerekiyor",
     "Evet demeden önce teklifini tekrar düşünmem gerekiyor",
     "потеряно «твоё предложение»"),
    (13515, "example_tr", "Bugün bunun üçüncüsü", "Bu bugün üçüncü kahve",
     "потеряно «кофе»"),
    (12594, "example_en", "He became a cripple after the accident",
     "After the accident he was a cripple and could no longer walk",
     "потеряно «konnte nicht mehr laufen»"),
    (12594, "example_uk", "Він став інвалідом після аварії",
     "Після аварії він став калікою і більше не міг ходити", "то же"),
    (12594, "example_tr", "Kazadan sonra bacağı sakat kaldı",
     "Kazadan sonra sakat kaldı ve artık yürüyemedi", "то же"),
    (2824, "example_uk", "Сьогодні багато сонячного світла",
     "Сьогоднішнє сонячне світло чудове",
     "немецкий «Der Sonnenschein heute ist wunderbar»"),
    (10470, "example_pl", "On ma naprawdę wielkie ego",
     "Jego wielkie ego to problem",
     "немецкий «Sein großes Ego ist ein Problem»"),
    (10473, "example_tr", "Piyangoyı kazandığın için şanslısın",
     "Piyangoyu kazandığın için gerçekten şanslısın",
     "«Piyangoyı» — опечатка, и потеряно «wirklich»"),
    (542, "example_tr", "Gıda alıyor", "Market alışverişi yapıyor",
     "«Gıda alıyor» — не говорят о покупке продуктов"),

    # --- немецкий эталон -------------------------------------------------------
    (7084, "example_de", "Ich häng das Bild an die Wand auf",
     "Ich hänge das Bild an die Wand auf",
     "«häng» — разговорное усечение"),

    # --- опечатки --------------------------------------------------------------
    (10464, "example_uk",
     "Я повинен ще раз переосмислити твою пропозицію, перш ніж сказу так",
     "Я повинен ще раз переосмислити твою пропозицію, перш ніж скажу так",
     "«сказу» — опечатка"),
    (12587, "example_pl", "Po jazdzie czułem się oszołomiony",
     "Po jeździe czułem się oszołomiony", "«jazdzie» — опечатка"),
    (16144, "example_tr", "Polisinin arama emri vardı ve eve geldiler",
     "Polisin arama emri vardı ve eve geldiler",
     "«Polisinin» — чьей-то полиции"),
    (14008, "translation_uk", "почерк, шрифт, письмо, надпис",
     "почерк, шрифт, письмо, напис", "«надпис» — русизм"),

    # --- грамматика целевого языка --------------------------------------------
    (16141, "example_tr", "Birisi beni şantaj yapmaya çalışıyor",
     "Birisi bana şantaj yapmaya çalışıyor",
     "«şantaj yapmak» требует дательного"),
    (10465, "example_tr", "Düşünceler onu her gün işkence ediyor",
     "Düşünceler ona her gün işkence ediyor", "то же для «işkence etmek»"),
    (7077, "example_tr", "Sanatçı elleriyle kili şekil veriyor",
     "Sanatçı elleriyle kile şekil veriyor",
     "«şekil vermek» требует дательного"),
    (7089, "example_tr", "Kırık pencere onarılması gerekiyor",
     "Kırık pencerenin onarılması gerekiyor", "пропущен родительный падеж"),
    (15039, "example_tr", "Damat gelin için bekliyordu",
     "Damat gelini bekliyordu", "«gelin için» — для невесты"),
    (16140, "example_tr", "Mektupta mühür önemlidir",
     "Mektuptaki mühür önemli", "неверный падеж и «-dir»"),
    (11712, "example_uk", "Добре перемішуй соус", "Добре перемішай соус!",
     "вид глагола, и в немецком восклицание"),
    (14001, "example_uk", "Дзвін лунає в 8 годин",
     "Дзвін лунає о 8 годині", "«в 8 годин» — не та форма"),
    (14002, "example_uk", "Прес-конференція починається о 14 годин",
     "Прес-конференція починається о 14 годині", "то же"),
    (14002, "example_tr", "Basın toplantısı saat 14te başlıyor",
     "Basın toplantısı saat 14.00'te başlıyor",
     "в турецком число берёт апостроф"),
    (2904, "example_tr", "Yayın saat 20:00de başlıyor",
     "Yayın saat 20.00'de başlıyor", "то же"),
    (1268, "example_en", "Your order is on the way",
     "My order is on the way", "в немецком «meine Bestellung»"),
    (1268, "example_tr", "Siparişiniz yolda", "Siparişim yolda", "то же"),

    # --- подменённое значение -------------------------------------------------
    (1598, "example_ru", "У меня вывихнута лодыжка",
     "У меня подвёрнута лодыжка",
     "«verstaucht» — подвёрнута; вывих это другая травма"),
    (16142, "example_tr", "Savaşta çok yaralı vardı",
     "Çarpışmada çok yaralı vardı",
     "«savaş» — война; в значениях «çarpışma»"),
    (12587, "example_tr", "Gezintiden sonra başım döndü",
     "Yolculuktan sonra sersemlemiş hissettim",
     "«gezinti» — прогулка; в немецком поездка"),
    (10461, "example_uk", "Він отримав побиття від інших дітей",
     "Він отримав прочухана від інших дітей",
     "в значениях стоит «прочухан»"),
    (10471, "example_uk", "Дівчата пищать від радості",
     "Дівчата верещать від радості", "в значениях стоит «верещати»"),
    (10462, "example_pl", "Uczciwość jest ważna w przyjaźni",
     "Uczciwość jest ważna w związku",
     "в немецком отношения, а не дружба"),
    (10472, "example_uk", "Учитель тисне учнів робити домашнє завдання",
     "Учитель підганяє учнів робити домашнє завдання",
     "«тисне учнів» — так не говорят"),

    # --- говорить по-людски ---------------------------------------------------
    (14461, "example_tr", "Yönetmen yönetmenliği üstleniyor",
     "Bu filmin yönetmenliğini o yapıyor",
     "«yönetmen yönetmenliği» — одно и то же дважды"),
    (10470, "example_tr", "Onun büyük egosu bir sorundur",
     "Onun büyük egosu bir sorun", "«-dur» — канцелярит"),
    (10468, "example_pl", "Na szczęście nic mi się nie stało",
     "Na szczęście nie zostałem ranny",
     "немецкий «bin ich nicht verletzt worden»"),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
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
