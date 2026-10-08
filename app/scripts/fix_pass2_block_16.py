"""ВТОРОЙ ПРОХОД, блок 16 (ряды 3001–3200) + класс «потерянная просьба».

ТРЕТИЙ БЛОК ПОДРЯД С ПОДМЕНЁННЫМ ПРЕДЛОЖЕНИЕМ, и опять те же языки:

    gelten (6970)      de «Diese Regel muss für alle gelten»
        en, uk, tr добавили «учеников без исключения» и потеряли модальный
        глагол — все три одинаково. ru и pl верны.

    krachen (2628)     de «Das Holz krachte, als er darauf trat»
        en «The wood cracked loudly under the weight»
        tr «Ağaç ağırlık altında çatırdadı» — и «ağaç» это дерево
        растущее, а Holz — древесина

    feststellen (6969) uk «Поліція встановила причину пожежі»
    bedeckt (6975)     uk «Стіл був прикритий скатертиною»
    Streich (12166)    pl «Dzieci zrobiły nauczycielowi niewinny figiel»
    Seife (18701)      pl «Umyj ręce mydłem przed obiadem»
    Feierabend (260)   pl «Koniec pracy, idziemy do domu!»

И ряд, который нашёлся не глазами, а через отброшенный замер:

    schlank (1833)     de «Du bist sehr schlank»
        en «These jeans make you look slim»
        tr «Duvarlar çok ince, her şeyi duyuyoruz» — про СТЕНЫ
        Два языка подменены по-разному, то есть это не один источник, а
        два разных сбоя в одном ряду. Плюс род адресата расходился:
        ru и pl женский, uk мужской. Приведено к мужскому, как по базе.

ЗАМЕР, КОТОРЫЙ НЕ ДАЛ КЛАССА, И ПОЧЕМУ Я ЕГО ВСЁ РАВНО СДЕЛАЛ. В блоке
накопилось четыре «потерянных усиления» (en/uk «echt», en «Bitte») и
четыре «добавленных» (uk «просто», pl «bardzo» дважды, pl «już»).
Напрашивалась примета на усиление вообще: sehr/echt/wirklich/ganz/
total/einfach против соответствий в пяти языках.

**209 потерь и 461 добавка, и почти всё — дыры моего же списка.**
Польское «całkiem» ничем не хуже «ganz», «po-настоящему» — не хуже
«wirklich», а турецкое «çok» ставится свободнее немецкого «sehr».
Перечисление по шести языкам не работает, и это ровно тот урок, что в
журнале записан уже пять раз.

Но у ОДНОЙ части список замкнут: у «bitte» в каждом языке ровно одно
слово, и больше их не бывает. Написан `scan_bitte_dropped`: эталон
просит, перевод велит голым приказом. 106 эталонов с «bitte», 16
попаданий, настоящих 13 — все в этой правке. Ложные три и названы:
«bitte schön» (14035), где английское «there you go» и турецкое
«buyrun» — правильная передача идиомы.

ВТОРОЙ ЗАМЕР БЕЗ КЛАССА. Турецкое «dostça» (по-дружески) в роли
сказуемого попалось второй раз — первый был `Nachbarschaft` (1710) в
блоке 14. Проверено: немецкий предикатив плюс турецкое слово на
«-ça/-ce» даёт 168 попаданий, и это законное турецкое наречие
(«sadece», «oldukça», «açıkça»), а как сказуемое «aptalca» и «çılgınca»
тоже законны. Беда ровно у «dostça», и это не класс, а одно слово.
Правится один ряд (18187), примета не пишется.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение ═══════════════════════════
    (6970, "example_en",
     "This rule applies to all students without exception",
     "This rule must apply to everyone",
     "добавлены «ученики без исключения», потерян модальный; ru и pl верны"),
    (6970, "example_uk",
     "Це правило діє для всіх учнів без винятку",
     "Це правило повинно діяти для всіх",
     "то же"),
    (6970, "example_tr",
     "Bu kural istisna olmaksızın tüm öğrenciler için geçerlidir",
     "Bu kural herkes için geçerli olmalı",
     "то же"),
    (2628, "example_en",
     "The wood cracked loudly under the weight",
     "The wood cracked when he stepped on it",
     "подмена: эталон «als er darauf trat»"),
    (2628, "example_tr",
     "Ağaç ağırlık altında çatırdadı",
     "Odun, üzerine bastığında çatırdadı",
     "подмена; и «ağaç» это дерево растущее, а Holz — древесина"),
    (6969, "example_uk",
     "Поліція встановила причину пожежі",
     "Я з'ясував, що він не прийде",
     "подмена: эталон «Ich habe festgestellt, dass er nicht kommt»"),
    (6975, "example_uk",
     "Стіл був прикритий скатертиною",
     "Небо весь день було сірим і захмареним",
     "подмена: эталон про небо, а не про стол"),
    (12166, "example_pl",
     "Dzieci zrobiły nauczycielowi niewinny figiel",
     "Figiel był zabawny i wszyscy się śmiali",
     "подмена: эталон «Der Streich war witzig und alle haben gelacht»"),
    (18701, "example_pl",
     "Umyj ręce mydłem przed obiadem",
     "Myję ręce mydłem",
     "подмена: эталон не велит, а рассказывает"),
    (260, "example_pl",
     "Koniec pracy, idziemy do domu!",
     "Koniec pracy! Chodźmy",
     "подмена второй половины: эталон «Lass uns gehen»"),
    (1833, "example_en",
     "These jeans make you look slim",
     "You are very slim",
     "подмена: эталон «Du bist sehr schlank»"),
    (1833, "example_tr",
     "Duvarlar çok ince, her şeyi duyuyoruz",
     "Çok incesin",
     "подмена: перевод про СТЕНЫ, а эталон про человека"),
    (1833, "example_ru",
     "Ты очень стройная",
     "Ты очень стройный",
     "род адресата расходился внутри ряда: ru и pl женский, uk мужской"),
    (1833, "example_pl",
     "Jesteś bardzo szczupła",
     "Jesteś bardzo szczupły",
     "то же"),

    # ══ КЛАСС по примете: потерянная просьба «bitte» ══════════════
    (1111, "example_pl",
     "Zamknij drzwi na klucz",
     "Zamknij proszę drzwi na klucz",
     "эталон просит: «Schließ bitte die Tür ab»"),
    (1138, "example_pl",
     "Kliknij na ten link",
     "Kliknij proszę na ten link",
     "эталон просит: «Klick bitte den Link an»"),
    (1150, "example_en",
     "Follow the instructions",
     "Please follow the instructions",
     "эталон просит: «Bitte folge den Anweisungen»"),
    (1224, "example_ru",
     "Обрати внимание на указания",
     "Обрати, пожалуйста, внимание на указания",
     "эталон просит: «Beachte bitte die Hinweise»"),
    (1628, "example_en",
     "Cool the drink",
     "Please cool the drink",
     "эталон просит: «Kühl bitte das Getränk»"),
    (1628, "example_tr",
     "İçkiyi soğut",
     "Lütfen içkiyi soğut",
     "то же"),
    (8088, "example_pl",
     "Rozluźnij trochę pasek",
     "Rozluźnij proszę pasek",
     "эталон просит, и «trochę» в нём нет"),
    (8142, "example_pl",
     "Nie szarpaj klamką, drzwi są zamknięte",
     "Proszę nie szarpać klamką, drzwi są zamknięte",
     "эталон просит: «Bitte nicht an der Tür rütteln»"),
    (8271, "example_pl",
     "Oszczędź mi swoich komentarzy",
     "Proszę, oszczędź mi swoich komentarzy",
     "эталон просит: «Bitte verschon mich von deinen Kommentaren»"),
    (14003, "example_pl",
     "Nie przesadzaj, to była tylko drobna sprawa",
     "Proszę, nie przesadzaj, to była tylko drobna sprawa",
     "эталон просит: «Bitte übertreibe nicht»"),
    (14164, "example_pl",
     "Postaw tutaj swój podpis",
     "Proszę postaw tutaj swój podpis",
     "эталон просит: «Bitte unterschreib hier»"),
    (17333, "example_ru",
     "Рейс отправляется с выхода на посадку 5, обратите внимание на объявление",
     "Рейс отправляется с выхода на посадку 5, обратите, пожалуйста, внимание на объявление",
     "эталон просит: «bitte beachten Sie die Durchsage»"),
    (17605, "example_uk",
     "Закрути кришку",
     "Закрути, будь ласка, кришку",
     "эталон просит: «Schraub bitte den Deckel zu»"),

    # ══ эталон: грамматика ═══════════════════════════════════════
    (6772, "example_de",
     "Das Wetter ist mir heute zu miese, ich bleibe lieber drinnen",
     "Das Wetter ist mir heute zu mies, ich bleibe lieber drinnen",
     "предикативное прилагательное окончания не получает"),

    # ══ форма, которой в языке нет ═══════════════════════════════
    (6974, "example_tr",
     "Araba çok kiri, onu yıkamalıyım",
     "Araba çok kirli, onu yıkamalıyım",
     "«kiri» не форма: нужно «kirli»"),
    (16109, "example_tr",
     "Senat kanun hakkında oy kullandı",
     "Senato kanun hakkında oy kullandı",
     "по-турецки «Senato», и так в списке переводов"),
    (18187, "example_tr",
     "Evin sakinleri çok dostça",
     "Evin sakinleri çok cana yakın",
     "«dostça» наречие, сказуемым быть не может; второй раз после 1710"),
    (10400, "example_tr",
     "Çocuk annesine oldukça arsızca davrandı",
     "Çocuk annesine gerçekten arsızdı",
     "то же: наречие вместо прилагательного, и «echt» это не «oldukça»"),
    (15014, "example_tr",
     "Bugün bizim evlilik yıldönümümüz",
     "Bugün bizim evlilik yıldönümümüz",
     "уже исправлено в блоке 15 — строка оставлена для сверки"),
    (10408, "example_tr",
     "Onun argümanı çok ikna edici değildi",
     "Onun argümanı pek ikna edici değildi",
     "«çok ... değildi» значит «совсем не», а эталон говорит «не очень»"),
    (6966, "example_tr",
     "Sıcaklık yükseltildi ve çok sıcak",
     "Sıcaklıklar yüksek ve rahatsız edici derecede sıcak",
     "«yükseltildi» значит «подняли»; и потеряно «unangenehm»"),
    (10405, "example_tr",
     "Çok konsantre oldu ve görevine odaklandı",
     "Çok konsantreydi ve görevine odaklandı",
     "«oldu» значит «стал», а эталон «war»"),
    (10417, "example_tr",
     "Babam benim büyük modelim",
     "Babam benim büyük rol modelim",
     "«model» по-турецки это манекенщик; в списке «rol model»"),
    (1923, "example_tr",
     "Çocuklar şekerlemeyi sever",
     "Çocuklar şekerlemeleri sever",
     "эталон во множественном: «Kinder lieben Süßigkeiten»"),

    # ══ русизм в украинском ══════════════════════════════════════
    (15482, "example_uk",
     "Мрак ночі мене лякає",
     "Морок ночі мене лякає",
     "«мрак» русское; в списке «темрява, морок»"),

    # ══ подмена и выдумка в одном языке ══════════════════════════
    (6954, "example_en",
     "Can you retrieve my bag from upstairs?",
     "Can you retrieve my things?",
     "«сумку сверху» в эталоне нет: «Kannst du meine Sachen zurückholen?»"),
    (10399, "example_en",
     "That's a cool idea",
     "That's a really wild idea",
     "«cool» нет в списке, и потеряно «ja»"),
    (16105, "example_en",
     "The meeting takes place tomorrow at 6 p.m",
     "The meeting takes place tomorrow at 6 o'clock",
     "«p.m» без второй точки — обрубок, озвучка прочитает неверно"),
    (16105, "example_uk",
     "Зібрання відбудеться завтра о 18:00",
     "Зібрання відбудеться завтра о 18 годині",
     "двоеточие в часах озвучка не читает; в ru «в 18 часов»"),
    (18186, "example_ru",
     "Я храню свои носки в ящике шкафа",
     "Я храню свои носки в ящике",
     "«шкафа» в эталоне нет: «in der Schublade»"),
    (18186, "example_uk",
     "Я тримаю свої шкарпетки в ящику шафи",
     "Я тримаю свої шкарпетки в шухляді",
     "то же; и «шухляда» стоит первой в списке"),
    (18186, "example_tr",
     "Çoraplarımı dolabın çekmecesinde tutuyorum",
     "Çoraplarımı çekmecede tutuyorum",
     "то же"),
    (9772, "example_uk",
     "Хочу накопити грошей на відпустку",
     "Я намагаюся щомісяця накопити грошей на відпустку",
     "потеряно «versuche» и «jeden Monat»"),
    (6976, "example_tr",
     "Merdiven çatıya çıkıyor",
     "Merdivenler yukarı, çatıya çıkıyor",
     "слова ряда в примере не было: «hinauf» это «yukarı»"),
    (15020, "example_ru",
     "Мой зять — врач",
     "Мой шурин — врач",
     "«зять» это муж дочери, а Schwager — брат супруга"),
    (2607, "example_ru",
     "На выходных я лажу по горам",
     "На выходных я занимаюсь скалолазанием в горах",
     "«лажу» читается двояко по ударению; вариант есть в списке"),
    (2607, "example_uk",
     "На вихідних я лажу по горах",
     "На вихідних я займаюся скелелазінням у горах",
     "то же"),
    (2967, "example_ru",
     "Я страхую машину",
     "Я страхую свою машину",
     "потеряно «mein»; в uk, en, tr и pl оно есть"),

    # ══ время и вид глагола ══════════════════════════════════════
    (2285, "example_ru",
     "Я пожалуюсь менеджеру",
     "Я жалуюсь менеджеру",
     "будущее против «Ich beschwere mich»; в остальных четырёх настоящее"),

    # ══ потерянное и добавленное усиление ════════════════════════
    (2831, "example_en",
     "The movie is exciting",
     "The movie is really exciting",
     "потеряно «echt»: в ru, tr и pl усиление есть"),
    (2831, "example_uk",
     "Фільм захопливий",
     "Фільм реально захопливий",
     "то же"),
    (1150, "example_pl",
     "Postępuj, proszę, zgodnie ze wskazówkami",
     "Postępuj, proszę, zgodnie ze wskazówkami",
     "вежливость на месте — строка для сверки"),
    (10415, "example_uk",
     "Погода просто жалюгідна",
     "Погода жалюгідна",
     "«просто» в эталоне «Das Wetter ist erbärmlich» нет"),
    (15485, "example_pl",
     "Tego roku plony były bardzo słabe",
     "Tego roku plony były słabe",
     "«bardzo» в эталоне нет"),
    (13984, "example_pl",
     "To był z jego strony bardzo miły gest",
     "To był z jego strony miły gest",
     "то же"),
    (18700, "example_pl",
     "Ręce mam już umyte",
     "Moje ręce są umyte",
     "«już» в эталоне нет, и порядок слов уводил от «Meine Hände»"),
    (6929, "example_tr",
     "Burada olanlar gerçekten inanılmaz",
     "Burada olanlar gerçekten inanılmaz",
     "уже исправлено в блоке 15 — строка для сверки"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    same: list[tuple[int, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if was == now:
                # строка для сверки: правки нет, проверяем только что текст тот
                if (cur or "").strip() != was:
                    skipped.append((wid, col, cur))
                else:
                    same.append((wid, col))
                continue
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(ok)}, сверок {len(same)}, пропущено {len(skipped)} ===\n")
    for wid, col in same:
        print(f"сверка OK id={wid} {col}")
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
