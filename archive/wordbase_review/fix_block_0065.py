"""
Правки блока 65 (ряды 11301–11500, ранги 23348–23740).

Главное в блоке — не отдельная находка, а ПЛОТНОСТЬ одного класса.
«Эталон заменили после перевода», описанный в блоке 61, встретился здесь
шестнадцать раз на 200 рядов: `Hafer`, `vorübergehen`, `rumrennen`,
`wohnhaft`, `Schlafplatz`, `nervig`, `zerstreuen`, `Schnauzer`, `Kraut`,
`Hammel`, `unser`, `wohingegen`, `Folie`, `Sonnenstrahl`, `aufleben`,
`seinesgleichen`. Расклад везде один: немецкий говорит одно, два-три
перевода говорят то же, а остальные плотно сходятся между собой на
совсем другой фразе.

За пять блоков класс прошёл путь от находки до самого частого дефекта
базы. Приметой он не ловится — обе ячейки грамматически безупречны, — но
читается с одного взгляда, если смотреть не «расходится ли перевод с
немецким», а «согласны ли переводы между собой».

Два немецких дефекта, которые стоит записать отдельно.

    Sie hecken einen Plan gegen mich aus

Ряд называется `hecken`, а в примере `aushecken` — другой глагол.
`hecken` значит «плодиться» о животных, `aushecken` — «замышлять». Все
пять переводов перевели второе. То же строение, что `Skalp`/`Skalpell`
в блоке 64, но приставкой вперёд, а не хвостом, и потому примета
`scan_de_headword_swap` его не берёт: она смотрит только слова,
начинающиеся с заголовка. Заголовок отдан владельцу.

    Ihr teurer Nerz-Mantel war die Rede der ganzen Stadt

`war die Rede` — не идиома; по-немецки `war Stadtgespräch`. Плюс лишний
дефис в составном слове.

    python -m app.scripts.fix_block_0065            # показать
    python -m app.scripts.fix_block_0065 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 11301 absorbieren
    (8591, "example_tr", "Bebek biberonu emmeye başladı",
     "Süngerler suyu hızla emer",
     "перевод совсем другого предложения"),
    # 11302 Hirnschaden
    (13129, "example_pl", "Po wypadku doszło do uszkodzenia mózgu",
     "Uszkodzenie mózgu było poważne",
     "перевод другого предложения"),
    # 11304 Röntgenaufnahme
    (13130, "example_pl",
     "Lekarz pokazał mi zdjęcie rentgenowskie nogi",
     "Zdjęcia rentgenowskie pokazują złamanie",
     "перевод другого предложения"),
    # 11305 Tablet
    (17730, "example_ru",
     "Мой планшет очень практичный, беру его с собой",
     "Мой планшет очень практичный в дороге",
     "«für unterwegs» это в дороге, а не «беру с собой»"),
    # 11306 Schlitzohr
    (11527, "example_uk", "Це хитрунок, йому не можна довіряти",
     "Це хитрун, йому не можна довіряти",
     "в статье «хитрун», без уменьшительного"),
    (11527, "example_tr", "Bu bir hileci, ona güvenemezsiniz",
     "Bu bir kurnaz, ona güvenemezsiniz",
     "«hileci» это обманщик, а в статье «kurnaz»"),
    (11527, "example_pl", "Ten cwaniak zawsze coś kombinuje",
     "To cwaniak, nie można mu ufać",
     "перевод другого предложения"),
    # 11307 maskiert
    (8592, "example_tr", "Maskalı kişi dükkanına girdi",
     "Maskeli kişi dükkâna girdi",
     "«maskalı» — не та гласная, и лишний притяжательный"),
    (8592, "example_pl", "Zamaskowany mężczyzna wbiegł do sklepu",
     "Zamaskowana osoba weszła do sklepu",
     "в эталоне `Person`, а не мужчина, и «kam», а не «вбежал»"),
    # 11309 Hafer — эталон заменили после перевода
    (12005, "example_en", "For breakfast I like to eat oats with milk",
     "The horses like to eat oats",
     "перевод остался от прежнего эталона"),
    (12005, "example_uk", "Ми посіяли овес на полі",
     "Коні охоче їдять овес",
     "перевод остался от прежнего эталона"),
    (12005, "example_tr", "Kahvaltıda yulafı sütle yemeyi severim",
     "Atlar yulaf yemeyi sever",
     "перевод остался от прежнего эталона"),
    (12005, "example_pl", "Konie jedzą owies",
     "Konie chętnie jedzą owies",
     "потеряно «gern»"),
    # 11310 überschlagen
    (8593, "example_pl", "Oszacuj szybko, ile to będzie kosztować",
     "Pozwól mi szybko oszacować koszty",
     "эталон не в повелительном"),
    # 11311 Kongressabgeordnete
    (16907, "example_tr", "Milletvekili yasaya karşı oy kullandı",
     "Kongre üyesi yasaya karşı oy kullandı",
     "«milletvekili» это депутат парламента, в статье «kongre üyesi»"),
    # 11313 erblühen
    (15854, "example_tr", "Güller baharında açılır",
     "Güller baharda açar",
     "«baharında» — лишний притяжательный"),
    # 11315 vorübergehen — эталон заменили после перевода
    (8594, "example_en", "The man passed by me without greeting",
     "Let the thunderstorm pass first",
     "перевод остался от прежнего эталона"),
    (8594, "example_uk", "Чоловік пройшов повз мене, не привітавшись",
     "Нехай гроза спочатку пройде",
     "перевод остался от прежнего эталона"),
    (8594, "example_tr", "Zaman çabuk geçiyor",
     "Fırtınanın önce geçmesine izin ver",
     "перевод остался от прежнего эталона"),
    # 11316 rumrennen — эталон заменили после перевода
    (8595, "example_en",
     "The kids are running around everywhere in the yard",
     "The children want to run around outside",
     "перевод остался от прежнего эталона"),
    (8595, "example_uk", "Діти бігають скрізь по подвір'ю",
     "Діти хочуть побігати на вулиці",
     "перевод остался от прежнего эталона"),
    (8595, "example_tr", "Çocuklar avluda her yerde koşuşturuyorlar",
     "Çocuklar dışarıda koşuşturmak istiyor",
     "перевод остался от прежнего эталона"),
    (8595, "example_pl", "Dzieci biegają po podwórku",
     "Dzieci chcą pobiegać na zewnątrz",
     "перевод остался от прежнего эталона"),
    # 11317 Beatmungsgerät
    (13131, "example_uk", "Пацієнту потрібен апарат ШВЛ",
     "Пацієнту потрібен апарат штучної вентиляції легенів",
     "сокращение вместо слова статьи"),
    (13131, "example_pl", "Pacjent leży pod respiratorem",
     "Pacjent potrzebuje respiratora",
     "перевод другого предложения"),
    # 11318 vorknöpfen
    (8596, "example_uk", "Начальник викликає працівника для розмови",
     "Начальник викликає працівника на килим",
     "перевод слова третьим значением, а не описанием"),
    # 11320 naschen
    (2677, "translation_uk", "ласувати, їсти солодощі, підїдати цукерки",
     "ласувати, їсти солодощі, під'їдати цукерки",
     "потерян апостроф"),
    (2677, "example_uk", "Я люблю ласувати солодке",
     "Я люблю ласувати солодким",
     "«ласувати» требует орудного"),
    (2677, "example_tr", "Tatlı atıştırmalıkları seviyorum",
     "Tatlı atıştırmayı severim",
     "«atıştırmalık» это закуска, а нужно действие"),
    # 11324 Schmerzensschrei
    (13132, "example_pl", "Z pokoju słychać było krzyk bólu",
     "Krzyki bólu rannego były słyszalne",
     "перевод другого предложения"),
    # 11325 geschmackvoll
    (8598, "example_uk", "Квартира дуже зі смаком обставлена",
     "Квартира обставлена дуже зі смаком",
     "порядок слов сломан"),
    # 11326 unerfreulich
    (11531, "example_pl", "To była dla nas nieprzyjemna wiadomość",
     "To nieprzyjemna wiadomość",
     "«dla nas» в эталоне нет, и время не то"),
    # 11327 Immobilie
    (8599, "example_tr", "Bir gayrimenkulü alıyorlar",
     "Bir gayrimenkul alıyorlar",
     "лишний аккузатив при неопределённом артикле"),
    (8599, "example_pl", "Kupili nieruchomość pod miastem",
     "Kupują nieruchomość",
     "эталон в настоящем, и «pod miastem» в нём нет"),
    # 11328 Testperson
    (18086, "example_tr", "Test öznesi tüm görevleri çözdü",
     "Denek tüm görevleri çözdü",
     "«özne» это подлежащее в грамматике, а в статье «denek»"),
    # 11329 gezähmt
    (15855, "translation_uk", "приручений, укрощений, приборканий",
     "приручений, упокорений, приборканий",
     "«укрощений» — русское слово"),
    # 11331 Vollstrecker
    (16908, "example_ru",
     "Исполнитель должен привести завещание в исполнение",
     "Исполнитель должен исполнить завещание",
     "«привести в исполнение» о завещании не говорят"),
    (16908, "example_uk",
     "Виконавець повинен привести заповіт у виконання",
     "Виконавець повинен виконати заповіт",
     "«привести у виконання» — калька"),
    (16908, "example_pl", "Wykonawca testamentu zajął się majątkiem",
     "Wykonawca musi wykonać testament",
     "перевод другого предложения"),
    # 11333 Weihrauch
    (14807, "example_tr", "Odada tütsü yaktım, mis gibi kokuyor",
     "Buhurun kokusu kiliseyi doldurdu",
     "перевод другого предложения"),
    (14807, "example_pl", "W kościele pachniało kadzidłem",
     "Zapach kadzidła wypełnił kościół",
     "перевод другого предложения"),
    # 11334 Schlafplatz — четыре перевода против эталона
    (18473, "example_en",
     "The dog made its sleeping place under the table",
     "The dog has its sleeping place under the table",
     "в эталоне «hat», а не «устроила»"),
    (18473, "example_ru",
     "Собака устроила своё спальное место под столом",
     "У собаки своё спальное место под столом",
     "в эталоне «hat», а не «устроила»"),
    (18473, "example_uk",
     "Собака облаштувала своє місце для сну під столом",
     "У собаки своє місце для сну під столом",
     "в эталоне «hat», а не «облаштувала»"),
    (18473, "example_tr",
     "Köpek masanın altında uyku yerini hazırladı",
     "Köpeğin yatacak yeri masanın altında",
     "в эталоне «hat», а не «приготовила»"),
    # 11335 Mammut
    (15856, "example_uk", "У музеї ми бачили скам'янілості мамута",
     "У музеї ми бачили скам'янілості мамонта",
     "в статье «мамонт»"),
    (15856, "example_tr", "Müzede bir mamutin fossillerini gördük",
     "Müzede bir mamutun fosillerini gördük",
     "«mamutin» и «fossil» — не те формы"),
    # 11336 Rune
    (14808, "example_uk",
     "Археологи аналізували руни на древньому камені",
     "Археологи аналізували руни на давньому камені",
     "«древній» — русизм"),
    (14808, "example_tr", "Taşın üstünde eski rünler var",
     "Arkeologlar eski taştaki rünleri analiz etti",
     "перевод другого предложения"),
    (14808, "example_pl", "Na starym kamieniu wyryto runy",
     "Archeolodzy analizowali runy na starym kamieniu",
     "перевод другого предложения"),
    # 11337 absprechen
    (2149, "example_uk", "Ми домовилися про зустріч",
     "Ми узгоджуємо зустріч",
     "эталон в настоящем времени"),
    # 11338 flussabwärts
    (15857, "example_tr",
     "Nehrin akış yönünde bir sonraki köye kaydık",
     "Nehrin akış yönünde bir sonraki köye kürek çektik",
     "«kaymak» это скользить, а `paddeln` — гребти"),
    # 11339 Salve
    (16910, "example_ru", "Залп пушки раздался по всему полю боя",
     "Залп пушки раскатился по полю боя",
     "«раздался по» — не то управление"),
    (16910, "example_uk",
     "Залп гармати розійшовся по всьому полю бою",
     "Залп гармати розкотився по полю бою",
     "«розійшовся по» — не то управление"),
    (16910, "example_pl", "Salwa armat zagrzmiała nad polem",
     "Salwa armaty zagrzmiała nad polem bitwy",
     "потеряно «Schlachtfeld», и пушка в эталоне одна"),
    # 11340 Startbahn
    (17391, "example_tr", "Uçak pistine yöneldi",
     "Uçak piste çıktı",
     "лишний притяжательный, и «yöneldi» это направился"),
    # 11341 Statist
    (14809, "example_uk", "Статисти стояли на фоні фільму",
     "Статисти стояли на задньому плані фільму",
     "«на фоні» — калька"),
    (14809, "example_tr", "Figuranlar filmin arka planında duruyorlardı",
     "Figüranlar filmin arka planında duruyorlardı",
     "«figuran» — не та гласная"),
    # 11342 wohnhaft — эталон заменили после перевода
    (18474, "example_en", "The family is resident in Berlin",
     "He is resident in Hamburg",
     "перевод остался от прежнего эталона"),
    (18474, "example_ru", "Семья проживает в Берлине",
     "Он проживает в Гамбурге",
     "перевод остался от прежнего эталона"),
    (18474, "example_uk", "Сім'я мешкає у Берліні",
     "Він мешкає в Гамбурзі",
     "перевод остался от прежнего эталона"),
    (18474, "example_tr", "Aile Berlinde ikamet etmektedir",
     "Hamburg'da ikamet etmektedir",
     "перевод остался от прежнего эталона"),
    # 11344 Epilepsie
    (13133, "example_ru",
     "Эпилепсия является неврологическим расстройством",
     "Эпилепсия — неврологическое расстройство",
     "«является» — канцелярит"),
    (13133, "example_pl", "Mój kuzyn choruje na padaczkę",
     "Padaczka to zaburzenie neurologiczne",
     "перевод другого предложения"),
    # 11347 Rechtschaffenheit
    (11532, "example_pl", "Wszyscy cenią go za uczciwość",
     "Jego uczciwość była niepodważalna",
     "перевод другого предложения"),
    # 11348 Pechsträhne
    (11533, "example_uk", "У нього була довга смуга невдачі у грі",
     "У нього була довга смуга невдач у грі",
     "в статье «смуга невдач», во множественном"),
    (11533, "example_tr", "Oyunda uzun bir talihsizlik şeridi vardı",
     "Oyunda uzun bir şanssızlık dönemi vardı",
     "«şerit» это полоса как предмет"),
    (11533, "example_pl", "Mam ostatnio pasmo niepowodzeń",
     "Miał długie pasmo niepowodzeń w grze",
     "перевод другого предложения"),
    # 11349 Verwahrung
    (16911, "example_pl",
     "Przechowywanie dokumentów w sejfie jest bezpieczne",
     "Przechowywanie dokumentów odbywa się w bezpiecznym sejfie",
     "фраза пересобрана и сказуемое потерялось"),
    # 11350 Fußfessel
    (16912, "example_uk",
     "Засуджений носив електронний браслет на ногу",
     "Засуджений носив електронний браслет на нозі",
     "не тот падеж"),
    # 11351 mörderisch
    (16913, "example_tr", "Bu sıcaklık öldürücü, dışarı çıkamıyorum",
     "Sıcaklık öldürücüydü, zar zor çalışabiliyorduk",
     "перевод другого предложения"),
    (16913, "example_pl", "Upał był dzisiaj morderczy",
     "Upał był morderczy i ledwo mogliśmy pracować",
     "потеряна вторая половина"),
    # 11352 Naturwissenschaft
    (18087, "example_ru",
     "Естественные науки, как биология и химия, важны",
     "Естественные науки, такие как биология и химия, важны",
     "«как» без «такие» разваливает перечисление"),
    (18087, "example_uk",
     "Природничі науки, як біологія й хімія, важливі",
     "Природничі науки, такі як біологія й хімія, важливі",
     "«як» без «такі» разваливает перечисление"),
    # 11353 Sensibilität
    (11534, "example_pl", "Ma dużą wrażliwość na krytykę",
     "Wrażliwość na różnice kulturowe jest ważna",
     "перевод другого предложения"),
    # 11354 untypisch
    (8602, "example_en", "That's really atypical for him",
     "His behaviour was atypical for him",
     "в эталоне подлежащее «его поведение»"),
    (8602, "example_tr", "Bu onun için atipik bir davranış",
     "Davranışı onun için alışılmadıktı",
     "в эталоне подлежащее «его поведение», и время прошедшее"),
    # 11355 nervig — эталон заменили после перевода
    (11535, "example_de", "Das ist mir echt nervig",
     "Das ist echt nervig",
     "«nervig» с дативом не употребляется"),
    (11535, "example_en",
     "That's an annoying situation I'd rather avoid",
     "That's really annoying",
     "перевод остался от прежнего эталона"),
    (11535, "example_uk",
     "Це дратівна ситуація, яку я б краще уникнув",
     "Це справді дратує",
     "перевод остался от прежнего эталона, и «дратівна» — не форма"),
    (11535, "example_tr", "Bu beni sinir bozucu",
     "Bu gerçekten sinir bozucu",
     "«beni sinir bozucu» — разваленная конструкция"),
    (11535, "example_pl", "Ten hałas jest naprawdę irytujący",
     "To jest naprawdę irytujące",
     "перевод другого предложения"),
    # 11356 Bürgerin
    (16914, "example_pl", "Ona jest obywatelką Niemiec",
     "Jest obywatelką Niemiec i pracuje tu jako nauczycielka",
     "потеряна вторая половина"),
    # 11357 Würze
    (12007, "example_uk",
     "Трошки прянощів робить їжу набагато цікавішою",
     "Трохи приправи робить їжу набагато цікавішою",
     "«трошки» разговорное, и в статье «приправа»"),
    (12007, "example_pl", "Tej zupie brakuje przyprawy",
     "Trochę przyprawy czyni jedzenie znacznie ciekawszym",
     "перевод другого предложения"),
    # 11361 Bandenkrieg
    (16915, "example_uk", "Війна банд у місті тривала вже роки",
     "Війна банд у місті триває вже роки",
     "эталон в настоящем времени"),
    # 11363 Tischler
    (9265, "example_uk", "Столяр збудував для нас гарну шафу",
     "Столяр зробив для нас гарну шафу",
     "«збудувати» о шкафе не говорят"),
    (9265, "example_pl", "Stolarz zrobił nam nową szafę",
     "Stolarz zrobił nam piękną szafę",
     "в эталоне «schön», а не «новый»"),
    # 11364 ehrenamtlich
    (9266, "example_tr", "Çorbacıda gönüllü olarak çalışıyor",
     "Aşevinde gönüllü olarak çalışıyor",
     "«çorbacı» это суповая закусочная, а `Suppenküche` — аşevi"),
    (9266, "example_pl", "To praca wolontariacka, bez wynagrodzenia",
     "Pracuje jako wolontariuszka w jadłodajni dla bezdomnych",
     "перевод другого предложения"),
    # 11366 Archäologie
    (18088, "example_tr",
     "Arkeoloji beni oldukça ilgilendirir, özellikle antik çağlar",
     "Arkeoloji beni çok ilgilendiriyor, özellikle antik çağlar",
     "«ilgilendirir» о постоянном увлечении не говорят"),
    # 11367 primär
    (8604, "example_en",
     "The primary cause of the problem lies in poor communication",
     "The primary reason is the poor communication",
     "«of the problem» и «lies in» в эталоне нет"),
    (8604, "example_uk",
     "Первинна причина проблеми полягає в поганій комунікації",
     "Основна причина — погана комунікація",
     "«проблеми» и «полягає» в эталоне нет"),
    (8604, "example_tr",
     "Sorunun birincil sebebi kötü iletişimde yatıyor",
     "Birincil sebep kötü iletişim",
     "«sorunun» и «yatıyor» в эталоне нет"),
    # 11368 Arbeitskollege
    (9267, "example_uk",
     "Мої колеги по роботі дуже люб'язні і чуйні",
     "Мої колеги по роботі дуже милі й готові допомогти",
     "«nett» это милі, и `hilfsbereit` — готові допомогти"),
    (9267, "example_pl", "Moi koledzy z pracy są bardzo mili",
     "Moi koledzy z pracy są naprawdę mili i pomocni",
     "потеряно «hilfsbereit»"),
    # 11369 unser — стянутая форма в эталоне
    (13604, "example_de",
     "Ich vertraue auf die Unterstützung unsrer Familie",
     "Ich vertraue auf die Unterstützung unserer Familie",
     "«unsrer» — поэтическое стяжение, в прозе «unserer»"),
    (13604, "example_tr", "Bu ev bizim",
     "Ailemizin desteğine güveniyorum",
     "перевод другого предложения"),
    # 11370 zuvorkommend
    (11537, "example_tr", "Garson çok misafirperver ve dikkatliydi",
     "Garson çok nazik ve dikkatliydi",
     "«misafirperver» это гостеприимный"),
    (11537, "example_pl", "Kelner był bardzo uprzejmy",
     "Kelner był bardzo uprzejmy i uważny",
     "потеряно «aufmerksam»"),
    # 11371 Fratze
    (15317, "example_tr", "Adam bana gülünç bir yüz yaptı ve kaçtı",
     "Adam bana çirkin bir surat yaptı ve kaçtı",
     "«gülünç» это смешной, а `Fratze` — уродливая рожа"),
    # 11372 loyale
    (11538, "example_tr",
     "O, her zaman güvenebileceğin sadık bir arkadaş oldu",
     "O sadık bir arkadaştı",
     "«her zaman güvenebileceğin» в эталоне нет"),
    (11538, "example_pl", "Zawsze był lojalnym przyjacielem",
     "Był lojalnym przyjacielem",
     "«zawsze» в эталоне нет"),
    # 11373 verleiten
    (11539, "example_uk",
     "Його друзі постійно спокушають його до поганих рішень",
     "Його друзі постійно підбивають його на погані рішення",
     "«спокушати до» — не то управление"),
    (11539, "example_pl", "Koledzy namawiają go do głupot",
     "Jego koledzy ciągle namawiają go do złych decyzji",
     "потеряно «ständig», и «głupoty» вместо «schlechte Entscheidungen»"),
    # 11377 beweglich
    (8606, "example_uk",
     "Добрий танцюрист повинен бути рухомим і гнучким",
     "Добрий танцюрист повинен бути рухливим і гнучким",
     "«рухомий» о предметах, о человеке — «рухливий»"),
    (8606, "example_pl",
     "Dobry tancerz powinien być ruchliwy i elastyczny",
     "Dobry tancerz powinien być zwinny i elastyczny",
     "«ruchliwy» значит суетливый"),
    # 11378 Familienvater
    (15318, "example_uk",
     "Як батько сім'ї, мають нести велику відповідальність",
     "Як батько сім'ї, треба нести велику відповідальність",
     "«мають» без подлежащего"),
    # 11379 Korkenzieher
    (12009, "example_tr", "Tırabzanın var mı? Şişeyi açmam lazım",
     "Şişe açacağın var mı? Şişeyi açmam lazım",
     "«tırabzan» значит перила"),
    (12009, "example_pl", "Masz korkociąg? Muszę otworzyć wino",
     "Masz korkociąg? Muszę otworzyć butelkę",
     "в эталоне бутылка, а не вино"),
    # 11380 Folie — эталон заменили после перевода
    (8607, "example_tr", "Artan yemeği folyoya sardım",
     "Yemeği folyoya sar, kurumasın",
     "перевод остался от прежнего эталона"),
    # 11381 weltlich
    (14810, "example_en",
     "He's interested only in worldly pleasures, not spiritual ones",
     "He's interested only in worldly pleasures",
     "«not spiritual ones» в эталоне нет"),
    (14810, "example_uk",
     "Його цікавлять лише світські утіхи, а не духовні",
     "Його цікавлять лише світські утіхи",
     "«а не духовні» в эталоне нет"),
    (14810, "example_tr",
     "Sadece dünyevi zevkleri ilgilendiriyor, ruhani değil",
     "Sadece dünyevi zevklerle ilgileniyor",
     "«ilgilendiriyor» — обратное направление, и хвост придуман"),
    # 11382 einmarschieren
    (16916, "example_pl", "Wojsko wkroczyło do miasta nad ranem",
     "Wojsko wkroczyło do miasta",
     "«nad ranem» в эталоне нет"),
    # 11383 wohingegen
    (13605, "example_tr", "Ben çalıştım, oysa o uyudu",
     "Kardeşim futbolu sever, oysa ben satranç oynamayı tercih ederim",
     "перевод другого предложения"),
    # 11384 Krücke
    (13134, "example_pl", "Po złamaniu nogi chodzi o kulach",
     "Po wypadku potrzebował kuli do chodzenia",
     "перевод другого предложения"),
    # 11385 obliegen
    (8608, "example_en",
     "It is the teachers duty to motivate the students",
     "It is the teacher's duty to motivate the students",
     "потерян апостроф"),
    (8608, "example_uk",
     "На учителю лежить обов'язок мотивувати учнів",
     "На учителеві лежить обов'язок мотивувати учнів",
     "не тот падеж"),
    # 11386 jahrhundertelang
    (18938, "example_uk", "Цей замок стояв столітнями незмінним",
     "Цей замок століттями стояв незмінним",
     "«столітнями» — нет такой формы"),
    # 11388 ausbaden
    (11540, "example_uk",
     "Тепер вона розплачується за власну недбалість",
     "Ти влаштував цей хаос, тепер тобі й розхльобувати",
     "перевод другого предложения"),
    # 11391 Atheist
    (8609, "example_tr",
     "O, ikna edici bir ateist ve hiçbir dine inanmıyor",
     "O, koyu bir ateist ve hiçbir dine inanmıyor",
     "«ikna edici» это убедительный, а `überzeugt` — убеждённый"),
    # 11392 Nerz — не идиома в эталоне
    (15860, "example_de",
     "Ihr teurer Nerz-Mantel war die Rede der ganzen Stadt",
     "Ihr teurer Nerzmantel war Stadtgespräch",
     "«war die Rede» — не идиома, и дефис в составном лишний"),
    (15860, "example_ru",
     "Её дорогое норковое пальто было разговором всего города",
     "Её дорогое норковое пальто обсуждал весь город",
     "«было разговором» — калька"),
    (15860, "example_uk",
     "Її дорогий норковий пальто було предметом розмов всього міста",
     "Її дороге норкове пальто було предметом розмов усього міста",
     "рассогласование рода"),
    (15860, "example_tr",
     "Pahalı vizonyonu paltosu tüm kentin konuşu oldu",
     "Pahalı vizon paltosu tüm kentin konusu oldu",
     "«vizonyonu» и «konuşu» — не те формы"),
    # 11393 Sonnenstrahl
    (15861, "example_en", "A warm sunbeam fell on my face",
     "A warm sunbeam came through the window",
     "перевод остался от прежнего эталона"),
    # 11394 ausmalen
    (14811, "example_uk",
     "Діти розфарбовують картини яскравими фарбами",
     "Діти розфарбовують картинки яскравими фарбами",
     "`Bilder` здесь картинки, а не картины"),
    (14811, "example_pl", "Dzieci kolorują obrazki kredkami",
     "Dzieci kolorują obrazki na kolorowo",
     "«kredkami» в эталоне нет, зато потеряно «bunt»"),
    # 11395 Hammel
    (15862, "example_en", "We had mutton stew for dinner",
     "The wether grazed peacefully in the meadow",
     "перевод остался от прежнего эталона"),
    # 11396 Kraut — эталон заменили после перевода
    (12010, "example_en", "She seasoned the dish with fresh herbs",
     "I season the dish with fresh herbs",
     "перевод остался от прежнего эталона"),
    (12010, "example_uk", "Вона приправила страву свіжими травами",
     "Я приправляю страву свіжими травами",
     "перевод остался от прежнего эталона"),
    (12010, "example_tr", "Yemeği taze otlarla baharat verdi",
     "Yemeği taze otlarla baharatlıyorum",
     "перевод остался от прежнего эталона, и «baharat verdi» — не "
     "выражение"),
    (12010, "example_pl", "Posyp zupę świeżymi ziołami",
     "Przyprawiam danie świeżymi ziołami",
     "перевод другого предложения"),
    # 11397 selbstgefällig
    (11541, "example_uk",
     "Його самозадоволена посмішка мене дратувала",
     "Його самовдоволена посмішка мене дратує",
     "в статье «самовдоволений», и эталон в настоящем"),
    (11541, "example_tr",
     "Onun kendini beğenmiş gülüşü beni sinir etti",
     "Onun kendini beğenmiş gülüşü beni sinir ediyor",
     "эталон в настоящем времени"),
    # 11398 zerstreuen — эталон заменили после перевода
    (8610, "example_en", "Music helps me distract myself",
     "The police dispersed the crowd",
     "перевод остался от прежнего эталона"),
    (8610, "example_uk", "Музика допомагає мені розвіяти мої думки",
     "Поліція розсіяла натовп",
     "перевод остался от прежнего эталона"),
    (8610, "example_tr",
     "Müzik benim düşüncelerimi dağıtmaya yardımcı oluyor",
     "Polis kalabalığı dağıttı",
     "перевод остался от прежнего эталона"),
    # 11399 Gutachter
    (9268, "example_tr", "Bilirkişi hasarlı arabayı dikkatle inceledi",
     "Bilirkişi arabayı dikkatle inceledi",
     "«hasarlı» в эталоне нет"),
    # 11401 Volleyball
    (2064, "example_en", "I play volleyball",
     "I like to play volleyball with friends",
     "потеряно «gerne» и «mit Freunden»"),
    (2064, "example_uk", "Я граю у волейбол зі своїми друзями",
     "Я люблю грати у волейбол з друзями",
     "потеряно «gerne»"),
    (2064, "example_tr", "Voleybol oynuyorum",
     "Arkadaşlarımla voleybol oynamayı seviyorum",
     "потеряно «gerne» и «mit Freunden»"),
    # 11403 Schnauzer — эталон заменили после перевода
    (15863, "example_en", "The schnauzer is a loyal companion",
     "Our schnauzer is really loyal and always with us",
     "перевод остался от прежнего эталона"),
    (15863, "example_uk",
     "Шнауцер — вірний супутник і добрий охоронець",
     "Наш шнауцер справді вірний і завжди з нами",
     "перевод остался от прежнего эталона"),
    (15863, "example_tr", "Şnauzer sadık bir arkadaştır",
     "Bizim şnavzerimiz gerçekten sadık ve her zaman yanımızda",
     "перевод остался от прежнего эталона, и в статье «şnavzer»"),
    # 11404 übersinnlich
    (14812, "example_pl", "Wierzy w zjawiska nadprzyrodzone",
     "Zajmuje się zjawiskami nadprzyrodzonymi",
     "«wierzy» вместо «beschäftigt sich»"),
    # 11406 Schokoladenkuchen
    (12011, "example_uk", "Шоколадний торт із ганашем був чудовий",
     "Домашній шоколадний торт із ганашем був чудовий",
     "потеряно «selbstgebacken»"),
    (12011, "example_tr", "Çikolatalı pasta harika",
     "Ev yapımı ganajlı çikolatalı pasta harikaydı",
     "потеряны «selbstgebacken», «mit Ganache» и прошедшее время"),
    (12011, "example_pl", "Upiekłam ciasto czekoladowe na urodziny",
     "Domowe ciasto czekoladowe z ganaszem było wyśmienite",
     "перевод другого предложения"),
    # 11407 Gymnastik
    (1510, "example_en", "I do gymnastics every day",
     "I do gymnastics every morning",
     "в эталоне «jeden Morgen», а не каждый день"),
    (1510, "example_uk", "Діти займаються гімнастикою у спортзалі",
     "Я роблю гімнастику щоранку",
     "перевод другого предложения"),
    # 11408 texten
    (14317, "example_uk", "Він мені пише повідомлення весь час",
     "Він весь час пише мені повідомлення",
     "порядок слов сломан"),
    # 11409 Gefrierschrank
    (18475, "example_en", "I put the groceries in the freezer",
     "I store the food in the freezer",
     "«lagere» это храню, а не кладу"),
    # 11410 einstehen
    (11542, "example_tr", "Arkadaşlarım için ayakta duruyorum",
     "Arkadaşlarımın arkasında duruyorum",
     "«ayakta durmak» значит стоять на ногах"),
    (11542, "example_pl", "Zawsze wstawiam się za swoimi kolegami",
     "Wstawiam się za swoimi przyjaciółmi",
     "«zawsze» в эталоне нет"),
    # 11411 Meeresboden
    (15864, "example_en", "The sea bottom is very uneven",
     "The seabed is very uneven",
     "по-английски это «seabed»"),
    (15864, "example_tr", "Deniz tabanı çok düzensiz",
     "Deniz tabanı çok engebeli",
     "«düzensiz» значит беспорядочный"),
    # 11412 navigieren
    (17393, "example_ru", "Мы навигируем по GPS",
     "Мы ориентируемся по GPS",
     "«навигировать» — не русское слово"),
    (17393, "example_uk", "Ми навігуємо за GPS",
     "Ми орієнтуємося за GPS",
     "«навігувати» — не украинское слово"),
    (17393, "example_tr", "Ormanda pusulayla yön bulduk",
     "GPS ile yön buluyoruz",
     "перевод другого предложения"),
    # 11413 Überbringer
    (14318, "example_uk", "Посланник новин був нервовим",
     "Гонець, що приніс звістку, нервував",
     "«посланник новин» — не выражение"),
    (14318, "example_tr", "Haberi getiren kişi gergin oldu",
     "Haberi getiren kişi gergindi",
     "«gergin oldu» значит «стал напряжённым»"),
    # 11414 Polizeipräsidium
    (16918, "example_tr", "Polis başkanlığı çok meşguldü",
     "Emniyet müdürlüğü bu davayla çok meşguldü",
     "в статье «emniyet müdürlüğü», и потеряно «mit dem Fall»"),
    # 11416 Wiederherstellung
    (17732, "example_uk", "Відновлення вебсайту займало кілька годин",
     "Відновлення вебсайту зайняло кілька годин",
     "«займало» это многократно"),
    # 11417 allmächtig
    (14814, "example_pl", "Wierzy, że Bóg jest wszechmocny",
     "Bóg jest wszechmocny",
     "«wierzy, że» в эталоне нет"),
    # 11418 hiernach
    (18939, "example_ru", "После этого стало лучше",
     "После этого ситуация улучшилась",
     "потеряно «die Situation»"),
    # 11419 empörend
    (11543, "translation_uk", "обурливий, волаючий",
     "обурливий, кричущий",
     "«волаючий» — калька активного дієприкметника"),
    (11543, "example_tr", "Bu tamamen öfkelendirici",
     "Bu tamamen rezalet",
     "в статье «rezalet»"),
    # 11420 Debüt
    (14815, "example_tr", "Sahnedeki debütü çok başarılı geçti",
     "Onun ilk çıkışı harikaydı",
     "перевод другого предложения"),
    (14815, "example_pl", "Jej debiut na scenie był udany",
     "Jego debiut był fantastyczny",
     "перевод другого предложения, да ещё и про неё"),
    # 11421 Gondel
    (17394, "example_tr", "Venedikte gondolle gezdik",
     "Venedik'te gondolla gezdik",
     "потерян апостроф, и «gondolle» — не та форма"),
    (17394, "example_pl",
     "Popłynęliśmy gondolą po kanałach Wenecji",
     "Popłynęliśmy gondolą przez Wenecję",
     "«po kanałach» в эталоне нет"),
    # 11423 Neptun
    (18090, "example_tr",
     "Neptün bizim güneş sisteminin sekizinci gezegenidir",
     "Neptün güneş sistemimizin sekizinci gezegenidir",
     "«bizim güneş sisteminin» — двойное притяжание"),
    # 11424 postieren
    (16919, "example_ru", "Полиция расставила офицеров у всех входов",
     "Полиция расставила сотрудников у всех входов",
     "`Beamte` это сотрудники, а не офицеры"),
    (16919, "example_uk",
     "Поліція розставила офіцерів біля всіх входів",
     "Поліція розставила співробітників біля всіх входів",
     "`Beamte` это співробітники, а не офіцери"),
    # 11425 Bestreben
    (11544, "example_uk",
     "Його прагнення було стати хорошим учителем",
     "Його прагненням було стати хорошим учителем",
     "не тот падеж в связке"),
    (11544, "example_pl", "Jego dążenie do sukcesu było widoczne",
     "Jego dążeniem było zostać dobrym nauczycielem",
     "перевод другого предложения"),
    # 11426 zerfleischen
    (16920, "example_tr", "Mermi kapıyı yırtıp geçti",
     "Eleştirmenler filmi sert sözlerle parçaladı",
     "перевод совсем другого предложения"),
    # 11427 entbinden — валентность в эталоне
    (13136, "example_de", "Der Arzt half der Frau, das Baby zu entbinden",
     "Der Arzt entband die Frau im Krankenhaus",
     "`entbinden` делает врач, а не роженица"),
    (13136, "example_en", "The doctor helped the woman deliver the baby",
     "The doctor delivered the woman's baby at the hospital",
     "вслед за исправленным эталоном"),
    (13136, "example_ru", "Врач помог женщине родить ребёнка",
     "Врач принял роды у женщины в больнице",
     "вслед за исправленным эталоном"),
    (13136, "example_uk", "Вона народжувала в лікарні всю ніч",
     "Лікар прийняв пологи в жінки в лікарні",
     "перевод другого предложения"),
    (13136, "example_tr", "Doktor kadına bebek doğurmasına yardımcı oldu",
     "Doktor kadını hastanede doğurttu",
     "двойной датив разваливает фразу"),
    (13136, "example_pl", "Rodziła w szpitalu przez całą noc",
     "Lekarz odebrał poród w szpitalu",
     "перевод другого предложения"),
    # 11428 Schienbein
    (15319, "example_uk", "Він поранив гомілку під час футболу",
     "Він забив гомілку, граючи у футбол",
     "`geprellt` это забив, а не поранив"),
    (15319, "example_tr", "Futbol oynarken kaval kemiğini çarptı",
     "Futbol oynarken kaval kemiğini bereledi",
     "«çarpmak» требует другого управления"),
    # 11431 aufleben — эталон заменили после перевода
    (11545, "example_en", "After vacation, he revived",
     "With music she can really come alive",
     "перевод остался от прежнего эталона"),
    (11545, "example_uk", "Після відпустки він ожив",
     "Від музики вона справді оживає",
     "перевод остался от прежнего эталона"),
    (11545, "example_tr", "Tatilden sonra canlandı",
     "Müzikle gerçekten canlanıyor",
     "перевод остался от прежнего эталона"),
    # 11436 Revue — не та приставка в эталоне
    (14816, "example_de", "Im Theater spielten sie eine bunte Revue auf",
     "Im Theater führten sie eine bunte Revue auf",
     "«aufspielen» значит играть музыку, а ставят — «aufführen»"),
    # 11439 Maskenball
    (14817, "example_uk", "Ти йдеш з нами на маскарад?",
     "Ти йдеш зі мною на маскарад?",
     "в эталоне «mit», то есть со мной"),
    # 11440 beschwipst
    (12013, "example_en", "After two glasses of wine she was tipsy",
     "After two glasses of wine he was already tipsy",
     "в эталоне «er», и потеряно «schon»"),
    (12013, "example_uk",
     "Після двох кубків вина він був уже трохи п'яний",
     "Після двох келихів вина він був уже трохи п'яний",
     "«кубок» это спортивный приз"),
    # 11441 ihretwillen
    (13606, "example_uk", "Я роблю це для неї",
     "Я роблю це заради неї",
     "перевод слова первым значением"),
    # 11442 glätten
    (8615, "example_uk", "Вона розгладжує складки в папері",
     "Вона розгладжує складки на папері",
     "не то управление"),
    # 11443 schnaufen
    (8616, "example_uk", "Після бігу він дихає важко",
     "Після бігу він важко дихає",
     "порядок слов сломан"),
    (8616, "example_tr", "Koştudan sonra hızlı nefes alıyor",
     "Koştuktan sonra hızlı nefes alıyor",
     "«koştudan» — нет такой формы"),
    # 11445 Retterin
    (15320, "example_uk", "Вона була його спасителькою від біди",
     "Вона була його рятівницею від біди",
     "перевод слова первым значением"),
    (15320, "example_tr", "O onun sıkıntısından kurtarıcı kadındı",
     "O, onun sıkıntıdan kurtarıcısıydı",
     "разваленная цепочка притяжательных"),
    # 11446 seinesgleichen
    (8617, "example_en", "As a cook, he never met his equal",
     "He only meets with his own kind",
     "перевод остался от прежнего эталона"),
    (8617, "example_uk", "Йому подібних я ще не зустрічав",
     "Він спілкується лише з собі подібними",
     "перевод остался от прежнего эталона"),
    (8617, "example_tr", "Böyle bir manzaranın eşi yok",
     "Sadece kendi gibilerle görüşüyor",
     "перевод остался от прежнего эталона"),
    (8617, "example_pl", "Była piękna jak nikt jemu podobny",
     "Spotyka się tylko z sobie podobnymi",
     "перевод остался от прежнего эталона"),
    # 11447 Zuwendung
    (11547, "example_uk", "Опіка матері була безумовною",
     "Турбота матері була безумовною",
     "перевод слова первым значением"),
    (11547, "example_pl", "Dzieci potrzebują troski i uwagi",
     "Troska matki była bezwarunkowa",
     "перевод другого предложения"),
    # 11448 hecken
    (8618, "example_en", "They are plotting against him",
     "They are hatching a plan against me",
     "в эталоне «gegen mich», и потерян «Plan»"),
    (8618, "example_uk", "Вони затіюють план проти нього",
     "Вони затівають план проти мене",
     "в эталоне «gegen mich», и «затіюють» — не та форма"),
    (8618, "example_tr", "Bana karşı bir komplotu hazırlıyorlar",
     "Bana karşı bir komplo hazırlıyorlar",
     "лишний аккузатив при неопределённом артикле"),
    # 11451 regenerieren
    (13137, "example_en",
     "After a week of vacation, my body regenerated",
     "After a week of vacation my body regenerates again",
     "эталон в настоящем, и потеряно «wieder»"),
    (13137, "example_uk", "Печінка здатна регенеруватися сама",
     "Після тижня відпустки моє тіло знову відновлюється",
     "перевод другого предложения"),
    (13137, "example_tr", "Bir hafta tatilden sonra vücudum yenilendi",
     "Bir hafta tatilden sonra vücudum yeniden yenileniyor",
     "эталон в настоящем, и потеряно «wieder»"),
    (13137, "example_pl", "Po urlopie organizm szybko się regeneruje",
     "Po tygodniu urlopu mój organizm znów się regeneruje",
     "«szybko» в эталоне нет, зато потеряны «eine Woche» и «wieder»"),
    # 11452 Projektion
    (17733, "example_tr", "Filmin duvara projeksiyonu çok netliydi",
     "Filmin duvara projeksiyonu çok netti",
     "«netliydi» — не та форма"),
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
