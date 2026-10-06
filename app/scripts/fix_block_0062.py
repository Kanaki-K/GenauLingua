"""
Правки блока 62 (ряды 10701–10900, ранги 22021–22465).

Главная находка блока — украинское слово в РУССКОЙ ячейке:

    de  Die Polizei musste einschreiten, um den Streit zu beenden
    ru  Полиция должна была вмешаться, чтобы остановить сварку

«Сварка» по-русски это сварка металла. По-украински «сварка» — ссора,
и именно ссора имелась в виду: немецкое `Streit`. То есть украинское
слово заехало в русскую ячейку и там обрело совсем другой смысл,
оставшись при этом грамматически безупречным.

Обратное направление — русское слово в украинской ячейке — в этом
блоке попалось пять раз (`на полу`, `дома`, `босс`, `Знаружи`,
`овсянка`), и оно стало отдельной сквозной приметой. А вот этот,
единственный, случай примета найти не может, и почему — написано в
её скрипте: направление «украинское в русском» даёт только ложные
срабатывания. Найден глазами, и иначе найден быть не мог.

Семь дефектов в самих немецких примерах:

    geniesst → genießt                  (уже правлено в блоке 61)
    brilliant → brillant                (английское написание)
    wiedertroffen → wiedergetroffen     (потеряно ge-)
    wisch → wische                      (потеряно личное окончание)
    Am Basar → Auf dem Basar            (не тот предлог)
    Seine Versprechungen … trauen       (`trauen` требует датива)
    forderte Einhalt gegen              (идиома `Einhalt gebieten`)

`brilliant` стоит отметить: это английское слово, написанное в
немецком примере, причём заголовок ряда написан правильно —
`brillant`. То есть ошибка не в знании слова, а в том, что рука
набрала английское.

Ещё раз встретился расклад блока 61: эталон `vorsehen` (8495) в
настоящем о паузе, а английский, украинский и турецкий переводят
совсем другую фразу про план и понедельник — и сходятся между собой.
Эталон заменили после перевода, обновили русский и польский.

    python -m app.scripts.fix_block_0062            # показать
    python -m app.scripts.fix_block_0062 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 10701 Dampfbad
    (13080, "translation_uk", "парова баня, хамам, парня",
     "парова баня, хамам, парильня",
     "«парня» — ни украинское, ни по делу"),
    (13080, "example_uk", "Після спорту я приймаю парну баню",
     "Після спорту я приймаю парову баню",
     "в статье «парова баня»"),
    (13080, "example_pl", "Po treningu poszliśmy do łaźni parowej",
     "Po sporcie chodzę do łaźni parowej",
     "эталон в настоящем и от первого лица"),
    # 10702 Grundriss
    (18457, "example_ru",
     "Посмотри на план новой квартиры, она хорошо спланирована",
     "Посмотри на план новой квартиры, у неё хорошая планировка",
     "«gute Aufteilung» это планировка, а не «хорошо спланирована»"),
    (18457, "example_uk",
     "Подивись на план нової квартири, вона добре спланована",
     "Подивись на план нової квартири, у неї добре планування",
     "«gute Aufteilung» это планировка"),
    # 10703 Feuerwache
    (16843, "example_ru",
     "Мой брат работает на пожарной станции рядом с нашим домом",
     "Мой брат работает в пожарной части рядом с нашим домом",
     "перевод слова — «пожарная часть»"),
    (16843, "example_uk",
     "Мій брат працює на пожежній станції біля нашого дому",
     "Мій брат працює в пожежній частині поруч із нашим домом",
     "перевод слова — «пожежна частина»"),
    # 10704 ergeben
    (11449, "example_tr",
     "Klübün sadık bir hayranıydı ve her maçı izledi",
     "Kulübün sadık bir hayranıydı ve her maçı izliyordu",
     "«klüb» — нет такого написания"),
    (11449, "example_pl", "Jest oddanym fanem tej drużyny",
     "Był oddanym fanem klubu i chodził na każdy mecz",
     "перевод другого предложения"),
    # 10706 unkompliziert
    (11450, "example_pl", "To jest proste, zrobimy tak jak mówisz",
     "To naprawdę proste, możemy zrobić tak, jak mówisz",
     "потеряно «echt» и «können», и нет запятой"),
    # 10709 Röntgenbild
    (13081, "example_uk",
     "Рентгенівський знімок показує, що кість переломана",
     "Рентгенівський знімок показує, що кість зламана",
     "«переломана» — не украинская форма"),
    (13081, "example_pl", "Zdjęcie rentgenowskie pokazało złamanie",
     "Zdjęcie rentgenowskie pokazuje, że kość jest złamana",
     "эталон в настоящем, и в нём целое придаточное"),
    # 10710 neunzehn
    (13600, "example_uk",
     "Мій син наступного тижня виповнюється дев'ятнадцять років",
     "Моєму сину наступного тижня виповнюється дев'ятнадцять років",
     "«виповнюється» требует датива"),
    # 10711 hinziehen
    (8468, "example_tr", "Toplantı akşama kadar uzayıp gitti",
     "Süreç yıllardır uzayıp gidiyor, bu çok uzun",
     "перевод другого предложения"),
    # 10712 familiär
    (15300, "example_pl", "W tej firmie jest rodzinna atmosfera",
     "Panuje między nimi ciepła, rodzinna atmosfera",
     "перевод другого предложения"),
    # 10713 Zensur
    (16846, "example_ru", "Цензура была очень строгой во время войны",
     "Цензура со стороны правительства была очень строгой во время войны",
     "потеряно «durch die Regierung»"),
    # 10714 innig
    (11451, "example_pl", "Łączy ich serdeczna przyjaźń od dziecka",
     "Łączy ich serdeczna przyjaźń, która trwa od dzieciństwa",
     "потеряно «die seit ihrer Kindheit besteht»"),
    # 10715 Familientradition
    (15301, "example_pl", "To u nas tradycja rodzinna",
     "To rodzinna tradycja, że każde Boże Narodzenie świętujemy razem",
     "перевод другого предложения"),
    # 10716 vollgestopft
    (8469, "example_uk", "Валіза набита, я ледве її закриваю",
     "Валіза повністю напхана, я ледве її закриваю",
     "потеряно «völlig»"),
    (8469, "example_tr", "Bavul tamamen dolu, onu zar zor kapatabiliyorum",
     "Bavul tıka basa dolu, onu zar zor kapatabiliyorum",
     "«dolu» теряет силу слова `vollgestopft`"),
    # 10717 bedürftig
    (11452, "example_pl",
     "Paczki z jedzeniem trafiają do potrzebujących rodzin",
     "Organizacja pomocowa wspiera potrzebujące rodziny żywnością",
     "перевод другого предложения"),
    # 10719 Paddel
    (12378, "example_en",
     "I take the paddle and paddle the canoe down the river",
     "I take the paddle and cross the river by canoe",
     "«paddle the paddle» — повтор, и в эталоне «über den Fluss»"),
    (12378, "example_uk", "Я беру весло і плаву на каное по річці",
     "Я беру весло і пливу на каное через річку",
     "«плаву» — не та форма, и в эталоне «über den Fluss»"),
    (12378, "example_tr", "Küreği alıp nehir üzerinde kano ile gidiyorum",
     "Küreği alıp kanoyla nehri geçiyorum",
     "«nehir üzerinde» — калька"),
    # 10720 Standesamt
    (16847, "example_tr",
     "Evlenmeleri için evlendirme dairesine gidiyorlar",
     "Evlenmek için evlendirme dairesine gidiyorlar",
     "«evlenmeleri için» — лишний притяжательный"),
    # 10721 rapide
    (8470, "example_uk",
     "Ціни швидко зростають, ми повинні щось з цим зробити",
     "Ціни стрімко зростають, ми повинні щось з цим зробити",
     "перевод слова — «стрімко»"),
    (8470, "example_tr",
     "Fiyatlar hızla yükseliyor, bunu durdurmamız gerekiyor",
     "Fiyatlar hızla yükseliyor, buna karşı bir şey yapmalıyız",
     "в эталоне «etwas dagegen tun», а не «остановить»"),
    # 10722 zuvorkommen
    (11453, "example_tr",
     "Sorunları önceden tahmin etmek ve her şeyi önceden planlamak "
     "istiyorum",
     "Sorunların önüne geçmek ve her şeyi önceden planlamak istiyorum",
     "«tahmin etmek» это предсказать, а `zuvorkommen` — опередить"),
    (11453, "example_pl", "Chciałem zapłacić ale on mnie uprzedził",
     "Chcę zapobiec problemom i wszystko zaplanować z wyprzedzeniem",
     "перевод другого предложения"),
    # 10723 unterdessen
    (18914, "example_uk",
     "Я готував їжу, тим часом моя дружина готувала стіл",
     "Я готував їжу, тим часом моя дружина накривала стіл",
     "«готувати стіл» — калька"),
    # 10724 Geisteszustand
    (13082, "example_tr",
     "Hastanın zihinsel durumu son haftalar içinde kötüleşti",
     "Hastanın zihinsel durumu son haftalarda kötüleşti",
     "«son haftalar içinde» — калька"),
    (13082, "example_pl", "Lekarz ocenił jego stan psychiczny",
     "Stan psychiczny pacjenta pogorszył się w ostatnich tygodniach",
     "перевод другого предложения"),
    # 10725 Diagramm
    (2343, "example_tr", "Diyagram gelişimi gösteriyor",
     "Diyagram satış rakamlarının gelişimini açıkça gösteriyor",
     "потеряны «Verkaufszahlen» и «deutlich»"),
    # 10726 Gönner
    (11454, "example_tr",
     "Zengin himayecisi sanat projesini finansal olarak destekledi",
     "Zengin hamisi sanat projesini maddi olarak destekledi",
     "«himayeci» — не слово, в статье «hami»"),
    (11454, "example_pl", "Bogaty mecenas wsparł młodego artystę",
     "Jego bogaty mecenas wsparł finansowo projekt artystyczny",
     "перевод другого предложения"),
    # 10728 Geisteskrankheit
    (13083, "example_en",
     "His mental illness was finally diagnosed after years of struggle",
     "His mental illness was finally diagnosed",
     "«after years of struggle» в эталоне нет"),
    (13083, "example_tr",
     "Onun ruh hastalığı yıllar sonra nihayet teşhis edildi",
     "Onun ruh hastalığı nihayet teşhis edildi",
     "«yıllar sonra» в эталоне нет"),
    # 10729 zunutze
    (8471, "example_tr",
     "Durumu kendi lehine kullanarak daha fazla para kazanmaya çalışıyor",
     "Daha fazla para kazanmak için durumu kendi lehine kullanıyor",
     "«çalışıyor» в эталоне нет"),
    # 10731 Schlüsselloch
    (18458, "example_ru",
     "Он подглядывал через замочную скважину, чтобы увидеть, что "
     "происходит",
     "Он посмотрел через замочную скважину, чтобы увидеть, что "
     "происходит внутри",
     "«schaute» это посмотрел, и потеряно «drinnen»"),
    (18458, "example_uk",
     "Він підглядав крізь замкову скважину, щоб бачити, що відбувалося",
     "Він подивився крізь замкову щілину, щоб побачити, що "
     "відбувається всередині",
     "«скважина» — русское слово, в статье «замкова щілина»"),
    # 10732 Börsenmakler
    (17883, "example_pl", "Mój kuzyn pracuje jako makler giełdowy",
     "Makler giełdowy dobrze zarabia na handlu akcjami",
     "перевод другого предложения"),
    # 10734 Rentier
    (15825, "example_ru", "Олень быстро бежит по снегу",
     "Северный олень быстро бежит по снежному краю",
     "потеряно «северный» и «Schneelandschaft»"),
    (15825, "example_uk",
     "Північний олень швидко біжить крізь снігову ландшафт",
     "Північний олень швидко біжить засніженим краєвидом",
     "«снігову ландшафт» — рассогласование рода"),
    # 10735 Zähler
    (2114, "example_uk", "Лічильник потрібно прочитати",
     "Потрібно зняти показання лічильника",
     "«прочитати лічильник» — калька"),
    # 10736 traurigerweise
    (11455, "example_pl", "Niestety nie udało się go uratować",
     "Niestety zmarł przed swoim wielkim sukcesem",
     "перевод другого предложения"),
    # 10738 Wiederbelebung
    (13084, "example_en",
     "Resuscitation of the patient was successful after cardiac massage",
     "Resuscitation was successful after cardiac massage",
     "«of the patient» в эталоне нет"),
    (13084, "example_tr",
     "Kalp masajından sonra hastanın diriltilmesi başarılı oldu",
     "Kalp masajından sonra canlandırma başarılı oldu",
     "«diriltilme» это воскрешение из мёртвых"),
    (13084, "example_pl", "Reanimacja udała się po kilku minutach",
     "Reanimacja była udana po masażu serca",
     "перевод другого предложения"),
    # 10739 schwinden
    (8474, "example_uk", "Моя надія зникає, чим довше я чекаю",
     "Чим довше я чекаю, тим більше тане моя надія",
     "«чим» без «тим» разваливает сравнение"),
    (8474, "example_tr",
     "Umutum ne kadar uzun beklersem, o kadar yok oluyor",
     "Ne kadar uzun beklersem umudum o kadar azalıyor",
     "«umutum» — не та форма, и порядок слов сломан"),
    # 10740 Empörung
    (11456, "example_uk",
     "Обурення новою політикою дуже велике в населенні",
     "Обурення новою політикою дуже велике серед населення",
     "«в населенні» — калька"),
    (11456, "example_pl", "Jego słowa wywołały wielkie oburzenie",
     "Oburzenie nową polityką jest bardzo duże wśród ludności",
     "перевод другого предложения"),
    # 10743 Fahrwerk
    (17369, "example_en",
     "The aircrafts landing gear was inspected after landing",
     "The aircraft's landing gear was inspected after landing",
     "потерян апостроф"),
    # 10744 aufgeblasen
    (11457, "example_uk", "Його надуте його було просто нестерпним",
     "Його надуте его було просто нестерпним",
     "«Ego» переведено как «його» — слово столкнулось с местоимением"),
    (11457, "example_tr", "Onun şişmiş egosı gerçekten dayanılmazdı",
     "Onun şişmiş egosu gerçekten dayanılmazdı",
     "«egosı» — не та гласная в суффиксе"),
    (11457, "example_pl", "Ten nadęty facet ciągle się przechwala",
     "Jego nadęte ego było naprawdę nieznośne",
     "перевод другого предложения"),
    # 10746 Verruf
    (11458, "example_uk", "Його ім'я набуло дурної слави",
     "Його ім'я набуло лихої слави",
     "перевод слова — «лиха слава»"),
    (11458, "example_tr", "Adı kötü bir şöhrete maruz kaldı",
     "Adı kötü bir şöhrete düştü",
     "«maruz kalmak» это подвергнуться, а не впасть"),
    (11458, "example_pl", "Ta firma popadła w złą sławę",
     "Jego imię popadło w złą sławę",
     "в эталоне имя, а не фирма"),
    # 10747 Unmögliches
    (8475, "example_tr", "Gerçekten benden imkansızı istiyorsun",
     "Gerçekten benden imkânsızı istiyorsun",
     "в статье «imkânsız», с циркумфлексом"),
    # 10748 ziellos
    (11459, "example_uk", "Він безцільно ходить містом",
     "Він зовсім безцільно блукає містом",
     "потеряно «völlig», и «wandern» это блукати"),
    (11459, "example_tr", "Şehir içinde amaçsızca dolaşıyor",
     "Şehirde tamamen amaçsızca dolaşıyor",
     "потеряно «völlig», и «şehir içinde» — калька"),
    (11459, "example_pl", "Chodził po mieście bez celu",
     "Błąka się całkiem bez celu po mieście",
     "эталон в настоящем, и потеряно «völlig»"),
    # 10749 ausgeschlafen
    (18916, "example_ru",
     "После отпуска я наконец чувствую себя выспавшейся",
     "После отпуска я наконец чувствую себя выспавшимся",
     "в эталоне рода нет, а перевод выбрал женский"),
    (18916, "example_uk",
     "Після відпустки я нарешті почуваюсь виспаною",
     "Після відпустки я нарешті почуваюся виспаним",
     "в эталоне рода нет, а перевод выбрал женский"),
    # 10750 Fahrerin
    (17370, "example_ru", "Водительница была очень вежлива и уверена",
     "Водительница была очень вежлива и ехала уверенно",
     "«sicher» о водителе это уверенно вести, а не «быть уверенной»"),
    (17370, "example_uk", "Водійка була дуже ввічлива і впевнена",
     "Водійка була дуже ввічлива і впевнено керувала",
     "«sicher» о водителе это уверенно вести"),
    (17370, "example_tr", "Kadın sürücü çok kibar ve güvenliydi",
     "Kadın sürücü çok kibar ve güvenli sürüyordu",
     "«güvenli» о человеке не говорят"),
    # 10751 Bildhauer
    (14778, "example_ru", "Скульптор создавал чудесные скульптуры",
     "Скульптор создал чудесные скульптуры",
     "«schuf» это однократно"),
    (14778, "example_pl", "Rzeźbiarz tworzył wspaniałe rzeźby",
     "Rzeźbiarz stworzył wspaniałe rzeźby",
     "«schuf» это однократно"),
    # 10752 kostspielig
    (9934, "example_en",
     "The project turned out expensive and time-consuming",
     "The project was expensive and time-consuming",
     "«turned out» в эталоне нет"),
    (9934, "example_uk", "Проект виявився дорогим і затратним",
     "Проект був дорогим і забирав багато часу",
     "«zeitaufwändig» это про время, а не про затраты"),
    (9934, "example_tr", "Proje pahalı ve zaman alıcı oldu",
     "Proje pahalı ve zaman alıcıydı",
     "«oldu» в эталоне нет"),
    # 10756 sorglos
    (11460, "example_tr", "Çocuklar parkta endişesizce oynadılar",
     "Çocuklar parkta kaygısızca oynadılar",
     "перевод слова — «kaygısız»"),
    (11460, "example_pl", "Dzieci beztrosko biegały po podwórku",
     "Dzieci beztrosko grały w parku",
     "перевод другого предложения"),
    # 10757 Sperrstunde
    (18917, "example_ru", "Бар закрывается в два часа",
     "Время закрытия заведения — два часа",
     "потеряно слово ряда"),
    (18917, "example_uk", "Бар закривається о другій годині",
     "Час закриття закладу — друга година",
     "потеряно слово ряда"),
    # 10758 bemerkbar
    (8478, "example_tr", "Fark açıkça belirgindir",
     "Fark açıkça belirgindi",
     "эталон в прошедшем времени"),
    # 10759 vergiftet
    (13085, "example_pl", "Pies zjadł zatrute mięso",
     "Zatruta woda nie była bezpieczna dla nikogo",
     "перевод другого предложения"),
    # 10760 Perversion
    (11461, "example_pl", "Jego zachowanie to czysta perwersja",
     "To perwersja prawdy",
     "перевод другого предложения"),
    # 10762 Turteltaube
    (15827, "example_uk", "Горлиці гуркотять у нашому саду",
     "Горлиці туркочуть у нашому саду",
     "«гуркотіти» это грохотать"),
    (15827, "example_tr", "Kumrular bahçemizde guguldüyorlar",
     "Kumrular bahçemizde ötüyor",
     "«guguldümek» — нет такого слова"),
    # 10763 Evangelium
    (14779, "example_pl", "W kościele czytali dziś Ewangelię",
     "Ewangelię czyta się w kościele",
     "перевод другого предложения"),
    # 10764 Kerosin
    (17372, "example_tr",
     "Uçak kalkıştan önce keroseniyle dolduruluyor",
     "Uçak kalkıştan önce jet yakıtı alıyor",
     "«kerosen» — не турецкое слово, в статье «jet yakıtı»"),
    # 10765 Blumenladen
    (9935, "example_uk",
     "Моя мати завжди купує троянди в квіткарні на кутку",
     "Моя мати завжди купує троянди в квітковому магазині на розі",
     "«на кутку» — не по-украински"),
    (9935, "example_tr",
     "Annem her zaman köşedeki çiçekçi dükkanından gül alır",
     "Annem her zaman köşedeki çiçekçi dükkânından gül alır",
     "в статье «dükkân», с циркумфлексом"),
    # 10766 Pferdeschwanz
    (13767, "example_ru",
     "Она носит свои длинные волосы в конском хвосте",
     "Она носит свои длинные волосы, собранные в хвост",
     "«в конском хвосте» — калька, причёска называется «хвост»"),
    (13767, "example_uk",
     "Вона носить своє довге волосся в конському хвісті",
     "Вона носить своє довге волосся, зібране у хвіст",
     "«в хвісті» — не та форма, и калька"),
    # 10768 ausspannen
    (12379, "example_en", "After work I relax and have a coffee",
     "After work we relax and have a coffee",
     "в эталоне «wir», а не «я»"),
    (12379, "example_uk", "Після роботи я розслабляюся й п'ю каву",
     "Після роботи ми відпочиваємо й п'ємо каву",
     "в эталоне «wir», а не «я»"),
    (12379, "example_tr", "İşten sonra rahatlıyorum ve kahve içiyorum",
     "İşten sonra dinleniyoruz ve kahve içiyoruz",
     "в эталоне «wir», а не «я»"),
    # 10769 Bestattung
    (15302, "example_uk", "Похорони відбудуться в понеділок у каплиці",
     "Похорон відбудеться наступного понеділка в каплиці",
     "потеряно «nächsten», и в статье единственное число"),
    (15302, "example_tr",
     "Cenaze törenı gelecek pazartesi şapelde yapılacak",
     "Cenaze töreni gelecek pazartesi şapelde yapılacak",
     "«törenı» — не та гласная в суффиксе"),
    # 10770 Interferenz
    (18078, "example_ru", "Интерференции в сигнале влияют на качество радио",
     "Помехи в сигнале влияют на качество радио",
     "перевод слова первым значением — «помехи»"),
    (18078, "example_uk",
     "Інтерференції в сигналі впливають на якість радіо",
     "Перешкоди в сигналі впливають на якість радіо",
     "перевод слова первым значением — «перешкоди»"),
    # 10772 orientieren
    (8479, "example_uk", "Я вмію орієнтуватися за картою",
     "Я орієнтуюся за зорями, коли я в лісі",
     "перевод другого предложения"),
    # 10773 mühelos
    (8480, "example_tr", "Zor görevini zahmetsizce beş dakikada çözdü",
     "Zor görevi zahmetsizce beş dakikada çözdü",
     "лишний притяжательный"),
    # 10776 Plädoyer
    (16850, "example_tr",
     "Avukat müvekkilinin savunması için ikna edici bir konuşma yaptı",
     "Avukat müvekkili için etkileyici bir savunma konuşması yaptı",
     "«müvekkilinin savunması için» — двойной изафет на пустом месте"),
    # 10778 fade
    (11977, "example_en", "The food was bland and unappetizing",
     "The food was bland and tasted of nothing",
     "в эталоне «schmeckte nach nichts»"),
    (11977, "example_uk", "Їжа була прісною та неапетитною",
     "Їжа була прісною й не мала жодного смаку",
     "в эталоне «schmeckte nach nichts»"),
    (11977, "example_pl", "Ta zupa jest mdła i bez smaku",
     "Jedzenie było mdłe i nie miało żadnego smaku",
     "перевод другого предложения"),
    # 10779 Landsmann
    (15303, "example_tr", "Onunla hemşehriyiz, ikimiz de Sivaslıyız",
     "Hemşehrim de Bavyera'dan geliyor",
     "перевод другого предложения"),
    # 10780 verlogen — падеж в эталоне
    (11462, "example_de",
     "Seine verlogenen Versprechungen konnte niemand trauen",
     "Seinen verlogenen Versprechungen konnte niemand trauen",
     "«trauen» требует датива"),
    (11462, "example_uk",
     "Його брехливі обіцянки ніхто не міг брати на віру",
     "Його брехливим обіцянкам ніхто не міг вірити",
     "в украинском тот же падеж не на месте"),
    # 10781 Gicht
    (13086, "example_pl", "Dziadek ma podagrę i boli go stopa",
     "Mój dziadek cierpi na podagrę i nie może dobrze chodzić",
     "перевод другого предложения"),
    # 10783 Akademiker
    (9616, "example_uk", "Академік опублікував кілька наукових праць",
     "Випускник вишу опублікував кілька наукових праць",
     "«академік» это член академії, совсем другое звание"),
    # 10784 Müllmann
    (9242, "example_uk",
     "Сміттєзбиральник приходить кожного понеділка вранці",
     "Смітяр приходить щопонеділка вранці",
     "перевод слова первым значением — «смітяр»"),
    # 10786 verschieden
    (8483, "example_uk", "У тачці лежить різне: молоко, хліб і сир",
     "У візку лежать різні речі: молоко, хліб і сир",
     "«тачка» это садова тачка, а не візок"),
    # 10787 Streichmusik
    (14780, "example_tr",
     "Yaylı müzik konser salonunda harika ses çıkardı",
     "Yaylı çalgı müziği konser salonunda harika geliyordu",
     "«ses çıkardı» это издала звук"),
    (14780, "example_pl", "Na weselu grała muzyka smyczkowa",
     "Muzyka smyczkowa brzmiała wspaniale w sali koncertowej",
     "перевод другого предложения"),
    # 10788 Schmeichelei
    (14302, "translation_uk", "лестощі, підлабузництво, комплименти",
     "лестощі, підлабузництво, компліменти",
     "«комплименти» — русское написание"),
    (14302, "example_uk", "Його лестощі мене зовсім не зворушують",
     "Її лестощі були наскрізь видні й нещирі",
     "перевод другого предложения, и в эталоне «ihre»"),
    (14302, "example_tr", "Bu iltifat için teşekkür ederim",
     "Onun iltifatları açıkça görülüyordu ve samimiyetsizdi",
     "перевод другого предложения"),
    (14302, "example_pl", "Nie wierz w jego pochlebstwa",
     "Jej pochlebstwa były przejrzyste i nieszczere",
     "перевод другого предложения"),
    # 10789 Album
    (14781, "example_tr", "Favori grubumin albümü efsanevi",
     "Favori grubumun albümü efsanevi",
     "«grubumin» — не та гласная"),
    (14781, "example_pl", "Oglądamy album ze zdjęciami z wakacji",
     "Album mojego ulubionego zespołu jest legendarny",
     "перевод другого предложения"),
    # 10792 Verschwiegenheit
    (11463, "example_uk",
     "Його мовчання про таємницю було гідним захоплення",
     "Його вміння тримати таємницю було гідним захоплення",
     "перевод слова первым значением"),
    (11463, "example_tr", "Sır hakkında onun sessizliği takdire değerdi",
     "Onun sır konusundaki ağzı sıkılığı takdire değerdi",
     "порядок слов сломан, и «sessizlik» это тишина"),
    # 10794 herfallen
    (8485, "example_en", "The predators pounced on the prey",
     "The children wanted to pounce on the cake",
     "перевод другого предложения"),
    (8485, "example_uk", "Не накидайся на мене одразу",
     "Діти хотіли накинутися на торт",
     "перевод другого предложения"),
    (8485, "example_tr", "Yırtıcılar avının üzerine saldırdı",
     "Çocuklar pastanın üzerine çullanmak istediler",
     "перевод другого предложения"),
    # 10795 Katzenfutter
    (11978, "example_uk", "Корм для кішок коштує п'ять євро за банку",
     "Корм для котів коштує п'ять євро за банку",
     "в статье «корм для котів»"),
    (11978, "example_pl", "Kupiłem karmę dla kota w sklepie",
     "Karma dla kota kosztuje pięć euro za puszkę",
     "перевод другого предложения"),
    # 10796 Waschanlage
    (17375, "example_ru", "Я регулярно вожу мою машину на автомойку",
     "Я регулярно вожу свою машину на автомойку",
     "«мою машину» вместо «свою»"),
    (17375, "example_uk", "Я регулярно возю мою машину на автомийню",
     "Я регулярно вожу свою машину на автомийку",
     "«возю» и «автомийня» — нет таких форм"),
    (17375, "example_tr",
     "Araçımı düzenli olarak araba yıkama istasyonuna götürüyorum",
     "Aracımı düzenli olarak oto yıkamaya götürüyorum",
     "«araçımı» — не та согласная"),
    (17375, "example_pl", "Zawiozłem auto do myjni",
     "Regularnie zawożę auto do myjni",
     "эталон в настоящем, и потеряно «regelmäßig»"),
    # 10797 verfüttern
    (15828, "example_uk", "Ми даємо рештки їжі як корм курам",
     "Ми згодовуємо рештки їжі курам",
     "перевод слова первым значением — «згодовувати»"),
    (15828, "example_tr",
     "Kalan yemeği tavuklara yemek olarak veriyoruz",
     "Kalan yemekleri tavuklara yem olarak veriyoruz",
     "«yemek olarak» вместо «yem olarak» — еда вместо корма"),
    (15828, "example_pl",
     "Pozostałe resztki jedzenia skarmiamy kurom",
     "Resztki jedzenia dajemy kurom",
     "«skarmiać» — диалектное"),
    # 10800 wälzen
    (8486, "example_uk",
     "Він всю ніч ворушився в ліжку й не міг заснути",
     "Він усю ніч вертівся в ліжку й не міг заснути",
     "«ворушився» это слегка двигался"),
    (8486, "example_tr", "Bütün gece yatakta döne döne uyuyamadı",
     "Bütün gece yatakta dönüp durdu ve uyuyamadı",
     "«döne döne uyuyamadı» слепляет два сказуемых в одно"),
    # 10801 Ganove
    (16852, "example_uk",
     "Бандита нарешті заарештували після місяців грабежів магазинів",
     "Бандита нарешті заарештували після місяців грабування магазинів",
     "«грабежів» — русская форма"),
    (16852, "example_tr",
     "Hırsız aylarca mağazaları soymaktan sonra nihayet tutuklandı",
     "Hırsız, aylarca mağazaları soyduktan sonra nihayet tutuklandı",
     "«soymaktan sonra» — не та форма"),
    # 10802 ekelhaft
    (11464, "example_uk",
     "Це огидна примітка – як ти можеш так говорити?",
     "Це огидне зауваження – як ти можеш таке говорити?",
     "«примітка» это сноска, а `Bemerkung` — замечание"),
    # 10805 Dirigent
    (14782, "example_pl",
     "Dyrygent uniósł batutę i orkiestra zaczęła grać",
     "Dyrygent prowadził orkiestrę z wielką elegancją i precyzją",
     "перевод другого предложения"),
    # 10806 abhaken
    (18921, "example_en",
     "I check off the items on my list as I complete them",
     "I check off the items when I finish them",
     "«on my list» в эталоне нет"),
    (18921, "example_ru",
     "Я отмечаю галочками пункты в списке по мере их выполнения",
     "Я отмечаю галочками пункты, когда их заканчиваю",
     "«в списке» в эталоне нет"),
    (18921, "example_uk",
     "Я позначаю галочками пункти у списку по мірі їх виконання",
     "Я позначаю галочками пункти, коли їх завершую",
     "«у списку» в эталоне нет, и «по мірі» — калька"),
    (18921, "example_tr",
     "Yaptığım işleri listemdeki maddelerle işaretliyorum",
     "Maddeleri bitirdiğimde işaretliyorum",
     "фраза собрана наоборот: отмечает список делами"),
    # 10807 Sättigung
    (11979, "example_en", "I felt a pleasant fullness after dinner",
     "After the meal I quickly felt full and couldn't eat anything more",
     "перевод другого предложения"),
    (11979, "example_uk",
     "Після їжі я швидко відчув ситість й більше нічого не міг їсти",
     "Після їжі я швидко відчув ситість і більше нічого не міг їсти",
     "«й» перед согласной"),
    (11979, "example_pl", "Po obiedzie czuję przyjemną sytość",
     "Po posiłku szybko poczułem sytość i nie mogłem nic więcej zjeść",
     "перевод другого предложения"),
    # 10809 Schatzmeister
    (9244, "example_tr", "Derneğin saymanı yıllık bütçeyi sundu",
     "Derneğin saymanı yıllık bütçeyi genel kurula sundu",
     "потеряно «vor der Versammlung»"),
    # 10810 Löwin
    (15830, "example_uk",
     "Львиця захищала своїх дітей з великою силою від нападника",
     "Левиця з великою силою захищала своїх дитинчат від нападника",
     "в статье «левиця», и «діти» у звірів — дитинчата"),
    (15830, "example_tr",
     "Aslan dişi yavrularını saldırgan kişiden büyük güçle savundu",
     "Dişi aslan yavrularını saldırgana karşı büyük bir güçle savundu",
     "«aslan dişi» значит «зуб льва»"),
    # 10811 herumschnüffeln
    (8487, "example_uk", "Ти мусиш ритися в моїх речах?",
     "Ти мусиш пхати носа в мої речі?",
     "перевод слова первым значением"),
    # 10812 Schulleiter
    (9617, "example_uk",
     "Директор школи виголосив промову при відкритті навчального року",
     "Директор школи виголосив промову на відкритті нового навчального "
     "року",
     "«при відкритті» — калька, и потеряно «neuen»"),
    # 10813 Arrestzelle
    (16853, "example_uk", "Його кинули в карцер, й він провів там ніч",
     "Його кинули в карцер, і він мусив провести там ніч",
     "«й» перед согласной, и потеряно «musste»"),
    (16853, "example_tr",
     "Onu tutukluluk hücresine attılar ve gece orada geçirmek zorunda "
     "kaldı",
     "Onu nezaret hücresine attılar ve geceyi orada geçirmek zorunda "
     "kaldı",
     "«gece» без аккузатива, и в статье «nezaret hücresi»"),
    # 10815 spreizen
    (8489, "example_en",
     "He spread his legs and did the splits – it was impressive",
     "He spread his legs – impressive",
     "«did the splits» в эталоне нет"),
    (8489, "example_tr",
     "Bacaklarını açtı ve şpagat yaptı – harika bir şeydi",
     "Bacaklarını yana açtı – etkileyici",
     "«şpagat» в эталоне нет и написано не так"),
    # 10817 Prohibition
    (16854, "example_uk",
     "Сухий закон в Америці привів до підземних барів і гангстеризму",
     "Сухий закон в Америці призвів до підпільних барів і гангстерської "
     "злочинності",
     "«підземні» вместо «підпільні», и «привів до» — калька"),
    (16854, "example_tr",
     "Amerikada alkol yasağı yasadışı barlar ve gangster suçlarına "
     "neden oldu",
     "Amerika'da alkol yasağı yasadışı barlara ve gangster suçlarına "
     "neden oldu",
     "потерян апостроф и падеж первого дополнения"),
    # 10818 Gulden
    (9936, "example_tr", "Hollanda'da eskiden gulden kullanılırdı",
     "Orta Çağ'da gulden en değerli paralardan biriydi",
     "перевод другого предложения"),
    # 10819 Überläufer
    (16855, "example_uk", "Перебіжник видав своїх товаришів ворогу",
     "Перебіжчик видав своїх товаришів ворогу",
     "«перебіжник» — нет такой формы"),
    (16855, "example_tr", "Kaçak arkadaşlarını düşmana ihbar etti",
     "Saf değiştiren, silah arkadaşlarını düşmana ihanet etti",
     "«ihbar etmek» это донести, а `verraten` — предать"),
    # 10820 Einhalt — идиома в эталоне
    (8491, "example_de",
     "Der Richter forderte Einhalt gegen die zunehmende Gewalt in der "
     "Stadt",
     "Der Richter wollte der zunehmenden Gewalt in der Stadt Einhalt "
     "gebieten",
     "«Einhalt» живёт только в «Einhalt gebieten»"),
    (8491, "example_tr",
     "Hakim şehirdeki artan şiddete karşı durdurma çağrısında bulundu",
     "Hakim şehirdeki artan şiddete dur demek istedi",
     "вслед за исправленным эталоном"),
    # 10821 Schatzkarte
    (12380, "example_uk",
     "Пірати намалювали карту скарбів, щоб пізніше знайти острів",
     "Пірати намалювали карту скарбів, щоб пізніше знову знайти острів",
     "потеряно «wieder»"),
    # 10822 Kollateralschaden
    (16856, "example_uk",
     "Війна залишила багато невинних жертв як побічні втрати",
     "Війна залишила багато невинних жертв як побічну шкоду",
     "в статье первое значение — «побічна шкода»"),
    # 10823 losschicken
    (8492, "example_en",
     "The boss sent the employees off to visit the new clients",
     "The boss sends the employees off to visit the new clients",
     "эталон в настоящем времени"),
    (8492, "example_uk",
     "Начальник відправив працівників відвідати нових клієнтів",
     "Начальник відправляє працівників відвідати нових клієнтів",
     "эталон в настоящем времени"),
    (8492, "example_tr",
     "Patron yeni müşterileri ziyaret etmek için çalışanları gönderdi",
     "Patron yeni müşterileri ziyaret etmek için çalışanları gönderiyor",
     "эталон в настоящем времени"),
    # 10824 Tänzchen
    (12381, "example_uk",
     "Вони танцювали невеликий танець разом, щоб святкувати",
     "Вони вдвох танцювали невеликий танець, щоб відсвяткувати",
     "«щоб святкувати» — не та форма"),
    (12381, "example_pl",
     "Oboje zatańczyli razem krótkiego taneczka, żeby to uczcić",
     "Oboje zatańczyli razem krótki taneczek, żeby to uczcić",
     "не тот падеж"),
    # 10825 Bäuerin
    (9245, "example_tr",
     "Çiftçi kadını hayvanlarla ve bahçeyle ilgilendi",
     "Çiftçi kadın hayvanlara ve bahçeye baktı",
     "лишний притяжательный у подлежащего"),
    # 10826 durchfahren — пять переводов против эталона
    (17376, "example_de", "Wir fahren die ganze Nacht durch, ohne anzuhalten",
     "Wir fuhren die ganze Nacht durch, ohne anzuhalten",
     "все пять переводов в прошедшем, эталон один в настоящем"),
    (17376, "example_tr", "Biz bütün gece durmadan geçtik",
     "Bütün gece durmadan yol aldık",
     "«geçtik» это прошли мимо, а не проехали"),
    # 10827 Einleitung — чисто
    # 10829 Mittagsschlaf
    (18922, "example_tr", "Öğleden sonra bir uyku lazımdı ona",
     "Öğle yemeğinden sonra öğle uykusuna ihtiyacı vardı",
     "потеряно «Mittagessen», и порядок слов сломан"),
    # 10830 Optimist
    (11468, "example_uk",
     "Він був справжнім оптимістом, незалежно від того, наскільки "
     "погано обстояли справи",
     "Він був справжнім оптимістом, незалежно від того, наскільки "
     "погано йшли справи",
     "«обстояли» — русская форма"),
    # 10831 Strafregister
    (16857, "example_ru", "Его имя было в уголовном реестре",
     "Его имя было в реестре судимостей",
     "перевод слова — «реестр судимостей»"),
    (16857, "example_uk", "Його ім'я було в кримінальному реєстрі",
     "Його ім'я було в реєстрі судимостей",
     "перевод слова — «реєстр судимостей»"),
    # 10832 bizarre
    (8493, "example_tr", "Kimsenin beklemediği tuhaf bir durum vardı",
     "Bu, kimsenin beklemediği tuhaf bir durumdu",
     "фраза пересобрана и потеряла подлежащее эталона"),
    # 10833 Moskito
    (15831, "example_uk", "Комарі були особливо погані цього літа",
     "Комарі були особливо дошкульні цього літа",
     "«погані» о комарах ничего не говорит"),
    # 10834 Einöde
    (15832, "example_ru",
     "Он странствовал дни напролёт через дикую местность без людей",
     "Он днями брёл по безлюдной глуши, никого не встречая",
     "«без людей» — калька от «ohne jemanden zu sehen»"),
    (15832, "example_uk",
     "Він днями мандрував через дику місцевість без людей",
     "Він днями мандрував глухоманню, не бачачи нікого",
     "«без людей» — калька от «ohne jemanden zu sehen»"),
    # 10835 Saatgut
    (15833, "example_tr", "Tohumlar kıştan önce ekilmesi gerekiyordu",
     "Tohumların kıştan önce ekilmesi gerekiyordu",
     "потерян родительный при отглагольном"),
    # 10837 Ballade
    (14783, "example_tr",
     "Balad kaybolmuş bir âşığın trajik hikayesini anlattı",
     "Balad, yitik bir âşığın trajik hikâyesini anlattı",
     "«kaybolmuş» это заблудившийся, и в статье «hikâye»"),
    (14783, "example_pl", "Zaśpiewał smutną balladę przy gitarze",
     "Ballada opowiadała tragiczną historię utraconego kochanka",
     "перевод другого предложения"),
    # 10839 Rückspiegel
    (17377, "example_en",
     "In the rear mirror I could see the car that was following me",
     "In the rearview mirror I could see the car that was following me",
     "по-английски это «rearview mirror»"),
    (17377, "example_tr", "Dikiz aynasından arkadaki arabayı gördüm",
     "Dikiz aynasından beni takip eden arabayı görebiliyordum",
     "потеряно «das mir folgte»"),
    (17377, "example_pl", "Spójrz w lusterko wsteczne przed skrętem",
     "W lusterku wstecznym widziałem samochód, który za mną jechał",
     "перевод другого предложения"),
    # 10840 Aufschrift
    (14303, "example_uk", "Напис на вивісці був ледве читаємим",
     "Напис на табличці був ледве читабельним",
     "«читаємий» — нет такой формы, и `Schild` это табличка"),
    (14303, "example_tr", "Tablodaki yazı zor okunuyordu",
     "Levhadaki yazı zor okunuyordu",
     "«tablo» это картина"),
    (14303, "example_pl", "Napis na tabliczce był ledwo widoczny",
     "Napis na tabliczce był ledwo czytelny",
     "«widoczny» это видимый, а `lesbar` — читаемый"),
    # 10841 Erzfeind
    (11469, "example_uk",
     "Він зустрів свого заклятого ворога на вулиці й одразу розгнівався",
     "Він побачив свого старого заклятого ворога на вулиці й одразу "
     "розгнівався",
     "потеряно «alten», и «sah» это побачив"),
    (11469, "example_tr", "Eski düşmanını sokakta görüp hemen öfkelendi",
     "Eski baş düşmanını sokakta görünce hemen öfkelendi",
     "потеряно «Erz-»"),
    # 10843 Gravitation
    (18079, "example_tr", "Yerçekimi her şeyi Dünyaya çekiyor",
     "Yerçekimi her şeyi Dünya'ya çekiyor",
     "потерян апостроф в имени"),
    # 10844 Magengeschwür
    (13088, "example_uk", "Стрес спричинив йому виразку шлунка",
     "Через стрес у нього виникла виразка шлунка",
     "«спричинити комусь» — не то управление"),
    (13088, "example_tr", "Stres ona mide ülseri verdi",
     "Stres onda mide ülserine neden oldu",
     "«vermek» о болезни не говорят"),
    (13088, "example_pl", "Od stresu dostał wrzodów żołądka",
     "Od stresu dostał wrzodu żołądka",
     "в эталоне одна язва"),
    # 10845 fremdgehen
    (15304, "example_uk", "Він зраджував їй роками",
     "Він зрадив дружину, і тепер вони розлучені",
     "перевод другого предложения"),
    (15304, "example_tr", "Karısını aldattı ve şimdi boşanmışlar",
     "Karısını aldattı ve şimdi boşandılar",
     "«boşanmışlar» — пересказ с чужих слов"),
    # 10846 nebenher
    (18923, "example_tr", "Yanında İngilizce de öğreniyor",
     "Bir yandan da İngilizce öğreniyor",
     "«yanında» это рядом с ним"),
    # 10847 Hohn
    (11470, "example_tr", "Sözleri alay ve hor görmeden doluydu",
     "Sözleri alay ve küçümsemeyle doluydu",
     "«hor görmeden» — не та форма"),
    # 10848 vorsehen — эталон заменили после перевода
    (8495, "example_en",
     "The plan stipulates that we start next Monday",
     "We have to allow for a short break",
     "перевод остался от прежнего эталона"),
    (8495, "example_uk",
     "План передбачає, що ми починаємо наступного понеділка",
     "Ми повинні передбачити коротку перерву",
     "перевод остался от прежнего эталона"),
    (8495, "example_tr", "Plan, gelecek pazartesi başlamamızı öngörüyor",
     "Kısa bir mola öngörmemiz gerekiyor",
     "перевод остался от прежнего эталона"),
    # 10849 Basar — предлог в эталоне
    (9937, "example_de", "Am Basar konnte man alles kaufen",
     "Auf dem Basar konnte man alles kaufen",
     "на базаре — «auf dem», а не «am»"),
    (9937, "example_tr", "Pazarda her şey alınabilirdi",
     "Çarşıda her şeyi satın alabilirdiniz",
     "в статье «çarşı», и пассив тут не нужен"),
    # 10851 zurückspulen
    (17721, "example_tr", "Videoyu biraz geri sar lütfen",
     "Sahneyi tekrar görmek için videoyu geri sarmak zorunda kaldım",
     "перевод другого предложения"),
    # 10853 Verfolgungswahn
    (13089, "example_uk",
     "Його манія переслідування ставала все гіршою, і він нікому не "
     "довіряв",
     "Його манія переслідування ставала все гіршою, і він більше нікому "
     "не довіряв",
     "потеряно «mehr»"),
    (13089, "example_pl", "Ma manię prześladowczą i nikomu nie ufa",
     "Jego mania prześladowcza stawała się coraz gorsza i nikomu już "
     "nie ufał",
     "перевод другого предложения"),
    # 10854 Verweis
    (9620, "example_en", "He got a reprimand for showing up late",
     "The pupil got a reprimand from the school management for being late",
     "потеряно «der Schüler» и «von der Schulleitung»"),
    # 10855 Hörensagen
    (14304, "example_uk", "Я це знаю тільки зі чуток, я там не був",
     "Я це знаю тільки з чуток, я там не був",
     "«зі» перед согласной"),
    # 10856 Schimpanse
    (15835, "example_tr",
     "Hayvananat bahçesindeki şempanze çok oyuncu ve zekiydi",
     "Hayvanat bahçesindeki şempanze çok oyuncu ve zekiydi",
     "«hayvananat» — лишний слог"),
    # 10857 Lebenserwartung
    (13090, "example_pl", "Średnia długość życia w Polsce rośnie",
     "Średnia długość życia w tym kraju wzrosła w ostatnich latach",
     "перевод другого предложения"),
    # 10860 Sterblichkeit
    (13092, "example_pl", "Śmiertelność przy tej chorobie jest wysoka",
     "Śmiertelność przy tej chorobie była przerażająco wysoka",
     "эталон в прошедшем, и потеряно «erschreckend»"),
    # 10861 erbarmungslos
    (11472, "example_uk", "Сонце палило безпощадно на нас",
     "Сонце нещадно палило на нас",
     "«безпощадно» — русизм, в статье «нещадний»"),
    (11472, "example_tr", "Güneş bize acımasızca yakıyordu",
     "Güneş acımasızca üzerimize vuruyordu",
     "«yakmak» требует прямого дополнения"),
    # 10862 kurieren
    (13093, "example_uk",
     "З хорошим відпочинком та ліками ми змогли вилікувати хворобу",
     "Завдяки гарному відпочинку та лікам ми змогли вилікувати хворобу",
     "«з відпочинком» — калька"),
    (13093, "example_pl", "Kurowałem przeziębienie przez cały tydzień",
     "Dzięki dobremu odpoczynkowi i lekom udało się nam wyleczyć chorobę",
     "перевод другого предложения"),
    # 10864 Mopp — личное окончание в эталоне
    (18459, "example_de", "Ich hole den Mopp und wisch schnell den Boden",
     "Ich hole den Mopp und wische schnell den Boden",
     "«wisch» это повелительное, а фраза от первого лица"),
    (18459, "example_en", "I grabbed the mop and quickly wiped the floor",
     "I grab the mop and quickly wipe the floor",
     "эталон в настоящем времени"),
    (18459, "example_ru", "Я взял швабру и быстро вымыл пол",
     "Я беру швабру и быстро вытираю пол",
     "эталон в настоящем времени"),
    (18459, "example_uk", "Я взяв мопу і швидко витер підлогу",
     "Я беру швабру і швидко витираю підлогу",
     "«мопа» — нет такого слова, и эталон в настоящем"),
    (18459, "example_tr", "Paspası aldım ve hızla zemini sildum",
     "Paspası alıp hızla zemini siliyorum",
     "«sildum» — не та гласная, и эталон в настоящем"),
    # 10865 Zwischenstopp
    (17378, "example_uk",
     "Ми зробили коротку зупинку в Берліні в дорозі до Варшави",
     "Ми зробили коротку зупинку в Берліні по дорозі до Варшави",
     "«в дорозі» — не то управление"),
    (17378, "example_tr",
     "Varşovaya gitmek için Berlinde kısa bir ara durak yaptık",
     "Varşova'ya giderken Berlin'de kısa bir mola verdik",
     "потеряны апострофы, и «ara durak yapmak» — не выражение"),
    (17378, "example_pl", "Zrobiliśmy krótki przystanek w Berlinie",
     "Zrobiliśmy krótki przystanek w Berlinie w drodze do Warszawy",
     "потеряно «auf dem Weg nach Warschau»"),
    # 10866 brillant — английское написание в эталоне
    (8496, "example_de",
     "Seine Lösung war absolut brilliant und sparte viel Zeit",
     "Seine Lösung war absolut brillant und sparte viel Zeit",
     "«brilliant» — английское написание, заголовок ряда правильный"),
    # 10867 Gefährt
    (17379, "translation_uk",
     "транспортний засіб, візок, засіб передвиження",
     "транспортний засіб, візок, засіб пересування",
     "«передвиження» — русское слово"),
    (17379, "example_ru", "Его старую машину давно уже не гонял",
     "Его старое транспортное средство давно уже не ездило",
     "фраза без подлежащего и не в том падеже"),
    (17379, "example_uk",
     "Його старе засіб передвиження давно вже не їздив",
     "Його старий транспортний засіб давно вже не їздив",
     "«старе засіб» — рассогласование рода"),
    # 10869 Nacktheit
    (15305, "example_uk",
     "Нагота на цій картині була артистичною, а не непристойною",
     "Нагота на цій картині була мистецькою, а не непристойною",
     "«артистичний» это об актёре, а `künstlerisch` — мистецький"),
    (15305, "example_tr",
     "Bu tablodan çıplaklık sanatsal ve müstehcen değildi",
     "Bu tablodaki çıplaklık sanatsaldı, müstehcen değildi",
     "«tablodan» — не тот падеж, и сказуемое повисло"),
    # 10870 lichten
    (15836, "example_tr", "Sis yavaş açıldı ve güneş çıktı",
     "Sis yavaşça dağıldı ve güneş çıktı",
     "«yavaş» это прилагательное, и «açıldı» о тумане не говорят"),
    # 10871 dementsprechend
    (8497, "example_uk",
     "Погода була поганою і відповідно багато людей залишилися дома",
     "Погода була поганою, і відповідно багато людей залишилися вдома",
     "«дома» — русское слово, и нет запятой"),
    # 10873 Besserwisser
    (11473, "example_tr",
     "Bu bilgiç herkesin en iyisini bildiğini düşünüyor",
     "Bu bilgiç, her şeyi herkesten iyi bildiğini sanıyor",
     "фраза собрана наоборот: знает лучшее у каждого"),
    # 10874 festmachen
    (8498, "example_uk", "Давай призначимо дату для зустрічі",
     "Давай призначимо дату нашої зустрічі",
     "потеряно «unser»"),
    # 10875 abschicken
    (2146, "example_en", "I send the letter",
     "I'll send the letter right away",
     "потеряно «gleich»"),
    (2146, "example_uk", "Я відправляю лист",
     "Я одразу відправляю лист",
     "потеряно «gleich»"),
    (2146, "example_tr", "Mektubu gönderiyorum",
     "Mektubu hemen gönderiyorum",
     "потеряно «gleich»"),
    # 10876 Abschlussprüfung
    (9621, "example_uk",
     "Випускний екзамен на наступному тижні і я нервую",
     "Випускний іспит наступного тижня, і я нервую",
     "в статье «іспит», и нет запятой"),
    # 10878 Sprechstunde
    (868, "example_uk", "Прийом у лікаря по понеділках",
     "Прийом у мого лікаря завжди щопонеділка",
     "потеряно «meinem» и «immer», и «по понеділках» — калька"),
    (868, "example_tr", "Muayene saati haftada pazartesi günüdür",
     "Doktorumun muayene saati her zaman pazartesi günüdür",
     "«haftada» лишнее, и потеряно «bei meinem Arzt»"),
    # 10879 Landeanflug
    (17380, "example_tr",
     "Uçak inişe yaklaşmaya başladı ve 15 dakikada ineceğiz",
     "Uçak iniş yaklaşmasına başlıyor ve 15 dakika sonra ineceğiz",
     "время рассогласовано, и «15 dakikada» это за 15 минут"),
    (17380, "example_pl", "Samolot zaczyna podejście do lądowania",
     "Samolot zaczyna podejście do lądowania i wylądujemy za 15 minut",
     "потеряна вторая половина"),
    # 10880 Turteltäubchen
    (15306, "example_uk", "Ці голубочки знову цілуються в парку",
     "Голубки сиділи разом у парку й тримались за руки",
     "перевод другого предложения"),
    (15306, "example_tr", "Şu aşık çifte bak, el ele yürüyorlar",
     "Aşık çift parkta birlikte oturup el ele tutuşuyordu",
     "перевод другого предложения"),
    # 10881 Qualifikation
    (2737, "example_en", "My qualifications are good",
     "My qualifications are very good",
     "потеряно «sehr»"),
    (2737, "example_uk", "Моя кваліфікація хороша",
     "Моя кваліфікація дуже хороша",
     "потеряно «sehr»"),
    (2737, "example_tr", "Niteliklerim iyi",
     "Niteliklerim çok iyi",
     "потеряно «sehr»"),
    # 10883 zermalmen
    (8499, "example_tr",
     "Makine kahve çekirdeklerini ince toza dönüştürdü",
     "Makine kahve çekirdeklerini ezerek ince toz haline getirdi",
     "«dönüştürmek» это превратить, а `zermalmen` — размолоть"),
    # 10884 da sein
    (18924, "example_uk", "Я хочу бути присутнім на зустрічі",
     "Я весь час був там і дивився",
     "перевод другого предложения"),
    (18924, "example_tr", "Bütün zaman oradaydım ve seyrettim",
     "Hep oradaydım ve seyrettim",
     "«bütün zaman» — калька"),
    # 10885 einschreiten — украинское слово в русской ячейке
    (16859, "example_ru",
     "Полиция должна была вмешаться, чтобы остановить сварку",
     "Полиция должна была вмешаться, чтобы прекратить ссору",
     "«сварка» по-русски это сварка металла; имелась в виду "
     "украинская «сварка» — ссора"),
    # 10886 erzürnt
    (11475, "example_uk", "Розлючений босс одразу покинув засідання",
     "Розлючений бос одразу покинув засідання",
     "«босс» — русское написание"),
    # 10887 verschmutzt
    (15837, "example_uk", "Його сорочка була дуже брудною після роботи",
     "Його сорочка була зовсім брудною після роботи",
     "«völlig» это зовсім, а не дуже"),
    # 10888 temperamentvoll
    (11476, "example_tr", "O, yüksek sesle gülen hareketli bir kadın",
     "O, yüksek sesle gülen ateşli bir kadın",
     "«hareketli» это подвижный, а не темпераментный"),
    # 10889 Reform
    (16860, "example_tr",
     "Hükümet okul sisteminin önemli bir reformunu yaptı",
     "Hükümet okul sisteminde önemli bir reform gerçekleştirdi",
     "двойной изафет и «reform yapmak» вместо «gerçekleştirmek»"),
    # 10890 vorzeigen
    (8500, "example_uk", "Можеш ти мені показати свої нові туфлі?",
     "Можеш показати мені свої нові туфлі?",
     "порядок слов сломан"),
    # 10891 Fügung — потеряно ge- в эталоне
    (8501, "example_de",
     "Es war eine glückliche Fügung, dass wir uns wiedertroffen haben",
     "Es war eine glückliche Fügung, dass wir uns wiedergetroffen haben",
     "«wiedertroffen» — потеряно ge-"),
    (8501, "example_tr", "Yeniden karşılaşmamız mutlu bir tesadüfdü",
     "Yeniden karşılaşmamız mutlu bir tesadüftü",
     "«tesadüfdü» — не та согласная в суффиксе"),
    # 10893 Scheidungspapier
    (16861, "example_tr",
     "Avukatı ile boşanma kağıtlarını imzalamak zorunda kaldı",
     "Avukatının yanında boşanma evraklarını imzalamak zorunda kaldı",
     "«avukatı ile» значит «вместе с адвокатом», и в статье «evrak»"),
    # 10894 diszipliniert
    (11477, "example_uk",
     "Він дуже дисциплінований спортсмен і тренується кожен день",
     "Він дуже дисциплінований спортсмен і тренується щодня",
     "«кожен день» — калька"),
    # 10895 Haferflocken
    (11981, "translation_uk", "вівсяні пластівці, овсянка",
     "вівсяні пластівці, вівсянка",
     "«овсянка» — русское написание"),
    (11981, "example_tr", "Kahvaltıda yulaf ezmesini sütle yerim",
     "Kahvaltıda her zaman sütlü yulaf ezmesi yerim",
     "лишний аккузатив, и потеряно «immer»"),
    # 10896 kastrieren
    (13095, "example_pl", "Weterynarz wykastrował naszego kota",
     "Weterynarz musi wykastrować psa, żeby zapobiec przeludnieniu",
     "перевод другого предложения"),
    # 10897 dämmern
    (18925, "example_ru", "Снаружи смеркается, скоро совсем темно",
     "Снаружи смеркается, скоро будет совсем темно",
     "вторая половина без сказуемого"),
    (18925, "example_uk", "Знаружи смеркається, скоро буде зовсім темно",
     "Надворі смеркається, скоро буде зовсім темно",
     "«знаружи» — русское слово"),
    # 10899 hellsehen
    (14784, "example_en", "Some claim they can predict the future",
     "Some people claim they can be clairvoyant and predict the future",
     "потеряны «Leute» и «hellsehen»"),
    (14784, "example_uk",
     "Деякі стверджують, що можуть передбачати майбутнє",
     "Деякі люди стверджують, що мають дар ясновидіння й можуть "
     "передбачати майбутнє",
     "потеряны «Leute» и «hellsehen»"),
    (14784, "example_tr",
     "Bazıları gelecek görebildiklerini iddia ediyorlar",
     "Bazı insanlar geleceği görebildiklerini iddia ediyor",
     "«gelecek» без аккузатива"),
    (14784, "example_pl", "Twierdzi że potrafi przewidywać przyszłość",
     "Niektórzy twierdzą, że potrafią przewidywać przyszłość",
     "нет запятой, и в эталоне «manche Leute»"),
    # 10900 hinknien
    (8502, "example_uk", "Він став на коліна й просив прощення",
     "Він став на коліна й попросив прощення",
     "«просив» это многократно"),
    (8502, "example_tr",
     "Dizlerinin üzerine oturdu ve affedilmesini istedi",
     "Diz çöktü ve affedilmesini istedi",
     "«oturdu» это сел, а не опустился на колени"),
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
