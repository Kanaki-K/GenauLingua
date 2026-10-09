"""ВТОРОЙ ПРОХОД, блок 31 (ряды 6001–6200): 50 правок.

ДЫРА В ПРИМЕТЕ НА РОД РАССКАЗЧИКА, И КАК ОНА ЗАКРЫТА:

    verwöhnen (10831)  de «Ich möchte mich mal richtig verwöhnen»
        ru «Я хочу себя побаловать»  — рода нет
        uk «Я хочу себе побалувати»  — рода нет
        pl «CHCIAŁABYM się porządnie rozpieścić» — ЖЕНСКИЙ

Польская половина `scan_speaker_gender` смотрела на «-łam», а условное
кончается на «-łabym». Добавлена четвёртая половина. Замер: 1 женская
форма против 20 мужских («Chciałbym zarezerwować stolik», «Chciałbym
wypłacić sto euro») — мужской род здесь такое же умолчание базы, как во
всех прочих половинах.

Признак оказался ЧИЩЕ, чем «-łam»: фильтр по инфинитивам ему не нужен,
потому что ни одно польское настоящее первого лица на «-łabym» не
кончается. У «-łam» эта неоднозначность есть и неустранима без словаря:
«kupiłam» женское прошедшее, а «wysyłam» нейтральное настоящее.

ПРОВЕРКА, КОТОРАЯ ОСТАНОВИЛА ТРИ ЛОЖНЫЕ ПРАВКИ. Грубый поиск по «-łam»
дал ещё три ряда с женскими формами: `rosa` (6634, «Kupiłam sobie
różową sukienkę»), `Strumpfhose` (13761), `Nagellack` (13749). Прежде
чем править, я посмотрел русский и украинский — и там женский род
СОГЛАСОВАН во всех трёх языках: «Я купила себе розовое платье», «Я
надела чёрные колготки». Это решение базы про платье, колготки и лак,
записанное ещё в `fix_pass2_block_08`, а не расхождение. Примета молчит
о них правильно, и трогать их нельзя.

ЧЕТЫРЕ ПОДМЕНЫ:

    verpackt       (9846)  uk «ТВІЙ ЧЕМОДАН уже упакований»
                           tr «HEDİYELERİ ZATEN PAKETLEDİM»
    Hochzeitsnacht (15134) pl «Noc poślubną SPĘDZILI W MAŁYM HOTELU»
    reservieren     (1805) uk «СТОЛИК ТРЕБА резервувати заздалегідь»
    Schwan         (15600) pl «NA STAWIE pływa biały łabędź»

В `verpackt` подменили два языка, и по-разному: украинский взял чужой
предмет, турецкий перевёл существительное глаголом в первом лице.

ПЯТАЯ ПАРА РЯДОВ НА ОДИН ЗАГОЛОВОК. `massiv` стоит в базе дважды: 7538
(C1, «Der massive Tisch war aus echtem Holz gefertigt») и 8084 (B1,
«Das neue Gebäude war aus massivem Stein gebaut»). Значение одно и то
же — цельный материал, — различаются только пример и уровень. Записано
в HANDOVER к пункту 1g.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ род рассказчика: новая половина приметы ═════════════════
    (10831, "example_pl",
     "Chciałabym się porządnie rozpieścić i pójść do spa",
     "Chciałbym się porządnie rozpieścić i pójść do spa",
     "женский род при нейтральных эталоне, ru и uk; в базе 20 мужских «Chciałbym»"),

    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (9846, "example_uk",
     "Твій чемодан уже упакований",
     "Запаковані подарунки лежать під ялинкою",
     "подмена: эталон «Die verpackten Geschenke stehen unter dem Baum»"),
    (9846, "example_tr",
     "Hediyeleri zaten paketledim",
     "Paketlenmiş hediyeler ağacın altında duruyor",
     "то же, и существительное стало глаголом в первом лице"),
    (15134, "example_pl",
     "Noc poślubną spędzili w małym hotelu",
     "Noc poślubna była niezapomniana dla tej pary",
     "подмена: эталон «Die Hochzeitsnacht war unvergesslich für das Paar»"),
    (1805, "example_uk",
     "Столик треба резервувати заздалегідь",
     "Я хочу зарезервувати столик",
     "подмена: эталон «Ich möchte einen Tisch reservieren»"),
    (15600, "example_pl",
     "Na stawie pływa biały łabędź",
     "Biały łabędź elegancko płynie po jeziorze",
     "пруд вместо озера, и потеряно «elegant»"),

    # ══ два языка разошлись вместе ══════════════════════════════
    (7564, "example_en",
     "The rumbling of the train woke me at night",
     "The rumbling of the train was loud at night",
     "«разбудил меня» вместо «war laut»; ru, uk и pl говорят «громкий»"),
    (7564, "example_tr",
     "Trenin gürültüsü beni gece uyandırdı",
     "Trenin gürültüsü geceleri yüksekti",
     "то же"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (7567, "example_uk",
     "Йому відібрана ліцензія",
     "У нього відібрали ліцензію",
     "«йому відібрана» не оборот украинского языка"),
    (18296, "example_uk",
     "Дзвінок у вхідних дверей, хтось хоче увійти",
     "Дзвонять у вхідні двері, хтось хоче увійти",
     "«дзвінок у вхідних дверей» не согласовано"),
    (10833, "example_uk",
     "Квартира виглядала жалюгідно з кількома меблями",
     "Квартира виглядала жалюгідно, меблів у ній було мало",
     "«з кількома меблями» не оборот; эталон «mit wenigen Möbeln»"),
    (10833, "example_pl",
     "Mieszkanie wyglądało nędznie, z paroma meblami",
     "Mieszkanie wyglądało nędznie, miało niewiele mebli",
     "то же"),
    (17821, "example_tr",
     "Kara pazarında her şey satın alabilirsin",
     "Karaborsada her şeyi satın alabilirsin",
     "«kara pazarı» не слово — есть «karaborsa»; и нужен винительный"),
    (3025, "example_tr",
     "Bebeğin beze ihtiyacı var",
     "Bebeğin bebek bezine ihtiyacı var",
     "«beze» не та форма: нужно «bezine»"),
    (10832, "example_tr",
     "O bir yalnızcı ve büyük grupları sevmez",
     "O içine kapanık bir kişi ve büyük grupları sevmez",
     "«yalnızcı» не слово; в списке «içine kapanık kişi»"),

    # ══ немецкое написание ══════════════════════════════════════
    (17980, "example_de",
     "Die Römische Legion war sehr diszipliniert",
     "Die römische Legion war sehr diszipliniert",
     "прилагательное от названия страны пишется со строчной"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (14120, "example_uk",
     "Він говорив відкрито про проблеми компанії",
     "Він говорив відкритим текстом про проблеми компанії",
     "ни одного слова списка; «відкритий текст» есть"),
    (14120, "example_en",
     "He spoke plainly about the company's problems",
     "He talked straight about the company's problems",
     "то же; «straight talk» есть в списке"),
    (14121, "translation_tr",
     "anlaşılmaz, net olmayan, bulanık",
     "anlaşılmaz, net değil, bulanık",
     "по-турецки это сказуемое «net değil», а не причастие"),
    (14121, "example_tr",
     "Konuşması belirsiz ve anlaşılması zor",
     "Konuşması net değil ve anlaşılması zor",
     "«belirsiz» это неопределённый, а не невнятный"),
    (10830, "example_tr",
     "Bunu söylediğimde kırılmış görünüyordu",
     "Bunu söylediğimde kırgın görünüyordu",
     "«kırılmış» о предмете; об обиде говорят «kırgın», и оно первое"),
    (18297, "example_tr",
     "Evin temeli güçlü ve istikrarlı",
     "Evin temeli güçlü ve sağlam",
     "«istikrarlı» о положении дел, а не о фундаменте"),
    (15613, "example_tr",
     "Şehir savaş tarafından tahrip edildi",
     "Şehir savaşta tahrip edildi",
     "«savaş tarafından» калька пассива"),
    (15131, "example_tr",
     "Bekar hâlâ küçük bir dairede yalnız yaşıyor",
     "Bekar erkek hâlâ küçük bir dairede yalnız yaşıyor",
     "в списке «bekar erkek», а пример давал половину"),
    (10825, "example_tr",
     "Kibar davranış iyi bir insanın önemli özelliğidir",
     "Nezaket iyi bir insanın önemli özelliğidir",
     "`Freundlichkeit` это приветливость, а не вежливое поведение"),
    (17217, "example_tr",
     "Tatil anısı olarak bir hatıra satın aldım",
     "Tatilin anısına bir hediyelik eşya satın aldım",
     "«anı» и «hatıra» один корень дважды в одной фразе"),
    (7542, "example_tr",
     "Kederini alkole boğmak istedi",
     "Kederini alkolde boğmak istedi",
     "нужен местный падеж: топят В чём-то"),
    (10834, "example_ru",
     "Только не рассказывай мне, пожалуйста, концовку",
     "Не раскрывай мне, пожалуйста, концовку",
     "ни одного слова списка; «раскрыть» есть, и в uk оно"),
    (10834, "example_tr",
     "Lütfen bana sonu söyleme",
     "Lütfen bana sonu ifşa etme",
     "то же; «ifşa etmek» стоит в списке первым"),
    (13557, "example_en",
     "Consequently, he was the culprit we were looking for",
     "Therefore, he was the culprit we were looking for",
     "«consequently» нет в списке, а «therefore» стоит первым"),
    (7548, "example_pl",
     "Możemy przeskoczyć ten rozdział?",
     "Możemy pominąć ten rozdział?",
     "«przeskoczyć» это перепрыгнуть; главу «pomija się»"),
    (1888, "example_en",
     "The players run across the field",
     "The players run across the playing field",
     "ни одного слова списка целиком; `Spielfeld` это «playing field»"),
    (2908, "example_ru",
     "Дерево опрокидывается во время бури",
     "Дерево падает во время бури",
     "дерево не «опрокидывается»; в uk и pl «падає»"),
    (15608, "example_ru",
     "Крестьяне хранят солому в сарае",
     "Фермеры хранят солому в сарае",
     "`Bauern` здесь фермеры; в en, uk, tr и pl фермеры"),
    (17218, "example_uk",
     "Моя тітка живе в заморських краях",
     "Моя тітка живе в заморських країнах",
     "в списке «заморські країни», а не «краї»"),

    # ══ существительное подменено глаголом ══════════════════════
    (18795, "example_ru",
     "Из-за погоды планы изменились в последний момент",
     "Из-за погоды произошло изменение планов в последний момент",
     "ряд о существительном, а пример давал глагол"),
    (18795, "example_uk",
     "Через погоду плани змінилися в останній момент",
     "Через погоду сталася зміна планів в останній момент",
     "то же"),
    (17216, "example_tr",
     "Almanya'dan geçerken birçok şehri ziyaret ettik",
     "Almanya'dan transit geçişimiz sırasında birçok şehri ziyaret ettik",
     "то же: слова ряда в примере не было"),

    # ══ управление и сочетаемость ═══════════════════════════════
    (17215, "example_tr",
     "Otoyolun sonraki çıkışını alıyoruz",
     "Otoyoldan sonraki çıkıştan çıkıyoruz",
     "«çıkışı almak» калька с «take the exit»"),
    (10833, "example_tr",
     "Daire az mobilyayla zavallı görünüyordu",
     "Daire az mobilyayla sefil görünüyordu",
     "«zavallı» о человеке; о жилье говорят «sefil»"),
    (12, "example_uk",
     "Ходити на роботу щодня — це його повсякденне життя",
     "Щодня він ходить на роботу — це його повсякденне життя",
     "эталон «Jeden Tag geht er zur Arbeit» — с подлежащим"),
    (18798, "example_ru",
     "Можешь мне пепельницу передать?",
     "Можешь передать мне пепельницу?",
     "порядок слов разрушал фразу"),
    (10836, "example_uk",
     "Він був їй невірний і це її дуже образило",
     "Він був їй невірний, і це її дуже вразило",
     "`verletzen` это ранить, а не обидеть; в ru, tr и pl ранило"),

    # ══ время глагола ═══════════════════════════════════════════
    (7559, "example_uk",
     "Я мав здати домашнє завдання до п'ятниці",
     "Я маю здати домашнє завдання до п'ятниці",
     "прошедшее против «Ich muss»"),
    (15611, "example_pl",
     "Ziemia drżała podczas trzęsienia",
     "Ziemia drży podczas trzęsienia ziemi",
     "прошедшее против «bebt», и потеряно «ziemi»"),
    (14124, "example_en",
     "We want to interview the candidate tomorrow",
     "We interview the candidate tomorrow",
     "«want to» в эталоне «Wir interviewen» нет"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (15602, "example_ru",
     "Мой дедушка долгие годы разводит голубей в саду",
     "Мой дедушка долгие годы разводит голубей в своём саду",
     "потеряно «seinem»: в en, uk, tr и pl оно есть"),
    (15609, "example_pl",
     "Rolnik pracuje na polu od świtu do nocy",
     "Rolnik pracuje na swoim polu od świtu do nocy",
     "потеряно «seinem»"),
    (17216, "example_ru",
     "Во время проезда через Германию мы посетили разные города",
     "Во время проезда через Германию мы посетили много городов",
     "«viele» это много, а не «разные»"),
    (13708, "example_pl",
     "Kupił nowe majtki na wyjazd",
     "Kupił nowe majtki",
     "«na wyjazd» в эталоне нет"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
