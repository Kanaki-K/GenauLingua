"""
Правки блока 57 (ряды 9701–9900, ранги 19675–20085).

Четыре сломанных эталона:
  · `Ich esse gerne eine Waffel mit Schoklade` — опечатка в немецком
    существительном: `Schoklade` вместо `Schokolade`;
  · `..., die den Film ab 16 Jahren freigegeben machten` — связка
    развалилась;
  · `Das ist eine reizvoll interessante Idee` — два определения без
    союза;
  · `Ich erdulde seine ständigen Kritik nicht länger` — `Kritik`
    женского рода и единственного числа.

Отдельная находка — числовая, а не языковая: немецкое `Billion` это
10¹², и русское «триллион», украинское «трильйон», турецкое `trilyon`
верны. А польское `trylion` это 10¹⁸: по-польски нужно `bilion`.
Ученику показывали число в миллион раз больше.

Прочие классы:
  · перевод другого предложения — больше пятидесяти рядов;
  · турецкие обрывки: `takı giyen adamlar` (украшения вместо костюма),
    `Bant` вместо `Grup`, `Maraton sonra`, `Münafaklıktan`, `tamponı`;
  · турецкое `Kargalar` (вороны) у ряда про гусей;
  · украинские сломанные формы: `піднути`, `гнилу м'ясо`, `Гуски`,
    `люстр`, `обличь`, `домашна`.

    python -m app.scripts.fix_block_0057            # показать
    python -m app.scripts.fix_block_0057 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 9701 gesetzlos
    (16731, "example_ru",
     "Беззаконные условия во время войны были катастрофальными",
     "Беззаконные условия во время войны были катастрофическими",
     "«катастрофальный» — нет такого слова"),
    (16731, "example_tr",
     "Savaş sırasındaki kanun dışı koşullar feci idi",
     "Savaş sırasındaki kanun dışı koşullar feciydi",
     "«idi» отдельно"),
    (16731, "example_pl",
     "Bezprawne stosunki w czasie wojny były katastrofalne",
     "Bezprawny stan w czasie wojny był katastrofalny",
     "«stosunki» это отношения, а «Zustände» — обстановка"),
    # 9702 Abschiedskuss
    (15265, "example_uk", "Вона дала йому прощальний поцілунок на вокзалі",
     "Вона дала йому останній прощальний поцілунок на вокзалі",
     "потеряно «letzten»"),
    (15265, "example_pl", "Dała mu pocałunek na pożegnanie na dworcu",
     "Dała mu ostatni pocałunek na pożegnanie na dworcu",
     "потеряно «letzten»"),
    # 9703 Insasse
    (16732, "example_ru", "Пассажир автомобиля был слегка ранен в аварии",
     "Пассажир автомобиля был слегка ранен при аварии",
     "«ранен в аварии» — не то управление"),
    # 9704 umsteigen
    (1995, "example_uk", "Тут вам потрібно пересідати",
     "Тут тобі потрібно пересісти",
     "эталон обращается на «ты»"),
    # 9706 Dossier
    (9192, "translation_tr", "dosya, künye dosyası",
     "dosya, kişisel dosya",
     "«künye dosyası» — не выражение"),
    # 9707 Laus
    (13009, "example_en", "I found a louse in her hair",
     "The child had lice at school and had to see a doctor",
     "перевод другого предложения"),
    (13009, "example_uk", "У дитини в волоссі завелася воша",
     "У дитини в школі завелися воші, і їй довелося йти до лікаря",
     "перевод другого предложения"),
    (13009, "example_tr", "Çocuğun saçında bit var",
     "Çocukta okulda bit çıktı ve doktora gitmesi gerekti",
     "перевод другого предложения"),
    (13009, "example_pl", "Dziecko przyniosło wszy ze szkoły",
     "Dziecko miało wszy w szkole i musiało iść do lekarza",
     "потеряно «musste zum Arzt»"),
    # 9709 Waffel — опечатка в эталоне
    (11940, "example_de",
     "Ich esse gerne eine Waffel mit Schoklade und Erdbeeren",
     "Ich esse gerne eine Waffel mit Schokolade und Erdbeeren",
     "«Schoklade» — опечатка, в базе есть «Schokolade»"),
    (11940, "example_tr",
     "Çikolata ve çilek ile bir gofret yemeyi seviyorum",
     "Çikolata ve çilekle bir waffle yemeyi seviyorum",
     "«ile» слитно, и перевод слова — «waffle»"),
    # 9710 Pfau
    (15773, "example_ru",
     "Павлин в зоопарке гордо развернул свои перья",
     "Павлин в зоопарке гордо распускает свои перья",
     "эталон в настоящем времени"),
    (15773, "example_uk",
     "Павич в зоопарку гордо розпростер своє пір'я",
     "Павич у зоопарку гордо розпускає своє пір'я",
     "эталон в настоящем времени"),
    (15773, "example_pl", "W zoo paw rozłożył ogon",
     "Paw w zoo dumnie rozkłada swoje pióra",
     "перевод другого предложения"),
    # 9711 Brauch
    (14726, "example_tr",
     "Almanyada birçok geleneksel gelenek ve kutlama vardır",
     "Almanya'da birçok geleneksel örf ve kutlama vardır",
     "потерян апостроф, и «geleneksel gelenek» — тавтология"),
    (14726, "example_pl", "W naszej rodzinie są świąteczne zwyczaje",
     "W Niemczech jest wiele tradycyjnych zwyczajów i uroczystości",
     "перевод другого предложения"),
    # 9712 Flugsteig
    (17333, "example_ru",
     "Самолёт отправляется с выхода на посадку 5, "
     "обратите внимание на объявление",
     "Рейс отправляется с выхода на посадку 5, "
     "обратите внимание на объявление",
     "в эталоне «Flug» — рейс, а не самолёт"),
    (17333, "example_uk",
     "Літак вилітає з виходу на посадку 5, "
     "будь ласка, зверніть увагу на оголошення",
     "Рейс відправляється з виходу на посадку 5, "
     "будь ласка, зверніть увагу на оголошення",
     "в эталоне «Flug» — рейс, а не самолёт"),
    # 9713 Peilung
    (17334, "example_en",
     "The ships bearing showed it was approaching the harbor",
     "According to the bearing, the ship was not far from the harbour",
     "потерян апостроф, и смысл другой"),
    (17334, "example_ru",
     "Пеленг корабля показал, что он приближается к порту",
     "По пеленгу судно было уже недалеко от порта",
     "перевод другого предложения"),
    (17334, "example_tr", "Kaptan kerteriz alarak yolumuzu buldu",
     "Kerterize göre gemi limandan artık uzak değildi",
     "перевод другого предложения"),
    # 9714 gebannt
    (11356, "example_tr",
     "İzleyiciler oyuncunun her hareketini takip eden "
     "büyülenmiş bir şekilde oturuyorlardı",
     "İzleyiciler büyülenmiş bir şekilde oturup "
     "oyuncunun her hareketini takip ediyordu",
     "причастие прицепилось не к тому слову"),
    (11356, "example_pl", "Dzieci siedziały zafascynowane przedstawieniem",
     "Widzowie siedzieli urzeczeni, śledząc każdy ruch aktora",
     "перевод другого предложения"),
    # 9715 anbelangen
    (8250, "example_uk", "Це питання стосується всіх нас",
     "Щодо оплати, ми ще не дійшли згоди",
     "перевод другого предложения"),
    (8250, "example_pl", "Ta zasada nie dotyczy małych dzieci",
     "Jeśli chodzi o zapłatę, nie osiągnęliśmy jeszcze porozumienia",
     "перевод другого предложения"),
    # 9716 Beraterin
    (9193, "example_uk",
     "Консультантка дала мені корисні поради щодо моєї професійної кар'єри",
     "Консультантка дала мені корисні поради "
     "щодо мого професійного майбутнього",
     "в эталоне «Zukunft» — будущее, а не карьера"),
    # 9717 durchnässt
    (15774, "example_uk",
     "Після дощу його сорочка була повністю мокра",
     "Після дощу його сорочка була повністю промокла",
     "перевод слова — «промоклий»"),
    (15774, "example_pl", "Wróciłem do domu całkiem przemoczony",
     "Po deszczu jego koszula była całkiem przemoczona",
     "перевод другого предложения"),
    # 9718 fatal
    (8251, "example_tr",
     "Ölümcül bir hata tüm projenin başarısızlığına yol açabilir",
     "Vahim bir hata tüm projenin başarısızlığına yol açabilir",
     "«ölümcül» это смертельный, а тут «вахим»"),
    (8251, "example_pl", "To był fatalny błąd",
     "Fatalny błąd mógłby doprowadzić do upadku całego projektu",
     "перевод другого предложения"),
    # 9720 unwirklich
    (11357, "example_uk",
     "Сценарій був настільки нереальним, що він ледь вірив, що це насправді",
     "Сценарій здавався настільки нереальним, "
     "що він ледве міг повірити, що це відбувається насправді",
     "«ледь вірив» — обрывок, и «wirkte» это здавався"),
    (11357, "example_tr",
     "Senaryo o kadar gerçek dışı görünüyordu ki "
     "bunun gerçek olduğuna iyice inanamıyordu",
     "Senaryo o kadar gerçek dışı görünüyordu ki "
     "bunun gerçek olduğuna bir türlü inanamıyordu",
     "«iyice inanamıyordu» — не то наречие"),
    (11357, "example_pl", "To wszystko wydawało się nierealne",
     "Scenariusz wydawał się tak nierealny, "
     "że z trudem mógł uwierzyć, że to się dzieje",
     "перевод другого предложения"),
    # 9721 Seelenverwandte
    (15267, "example_uk",
     "Вони спорідненні душі і розуміють один одного без слів",
     "Вони споріднені душі і розуміють одне одного без слів",
     "«спорідненні» с двойной «н»"),
    (15267, "example_tr",
     "Onlar ruh eşleri ve birbirlerini kelime olmadan anlarlar",
     "Onlar ruh eşi ve birbirlerini sözsüz anlıyorlar",
     "«kelime olmadan» — калька"),
    (15267, "example_pl", "Ona jest moją bratnią duszą",
     "Są bratnimi duszami i rozumieją się bez słów",
     "перевод другого предложения"),
    # 9722 fertigen
    (9194, "example_en", "The craftsman manufactures furniture from wood",
     "Here furniture is made by hand",
     "перевод другого предложения"),
    (9194, "example_uk", "Ремісник виготовляє меблі з дерева",
     "Тут меблі виготовляють вручну",
     "перевод другого предложения"),
    (9194, "example_tr", "Zanaatçı ahşaptan mobilya üretiyor",
     "Burada mobilyalar elde üretiliyor",
     "перевод другого предложения"),
    (9194, "example_pl", "Rzemieślnik wytwarza meble z drewna",
     "Tutaj meble wytwarzane są ręcznie",
     "перевод другого предложения"),
    # 9723 Wahrsagerin
    (14727, "example_tr", "Fal bakan tarot kartlarında geleceği okudu",
     "Falcı tarot kartlarında geleceği okudu",
     "«fal bakan» — обрывок причастия"),
    (14727, "example_pl", "Wróżka przewidziała mu długą podróż",
     "Wróżka czytała przyszłość z kart tarota",
     "перевод другого предложения"),
    # 9724 Parkett
    (18416, "example_ru", "В танцевальном зале блестящий паркетный пол",
     "В танцевальном зале был блестящий паркетный пол",
     "эталон в прошедшем времени"),
    (18416, "example_uk", "У залі була гарна паркетна підлога",
     "У бальному залі була блискуча паркетна підлога",
     "потерян бальный зал, и «glänzend» это блискуча"),
    # 9725 krumm
    (8252, "example_uk", "У нього крива носа, що дає йому характер",
     "У нього кривий ніс, який надає йому характерності",
     "«крива носа» — рассогласование рода"),
    (8252, "example_tr", "Onun karakterini veren eğri bir burnu vardır",
     "Ona karakter veren eğri bir burnu var",
     "«onun karakterini veren» переворачивает смысл"),
    (8252, "example_pl", "To drzewo ma całkiem krzywy pień",
     "Ma krzywy nos, który dodaje mu charakteru",
     "перевод другого предложения"),
    # 9726 Sehenswürdigkeit
    (17335, "example_tr", "Romadaki turist yerleri gerçekten harika",
     "Roma'daki turistik yerler gerçekten harika",
     "потерян апостроф, и «turist yerleri» — обрывок"),
    # 9727 erotisch — связка в эталоне развалилась
    (11323, "example_de",
     "Der Film hatte erotische Szenen, "
     "die den Film ab 16 Jahren freigegeben machten",
     "Der Film hatte erotische Szenen, "
     "weshalb er erst ab 16 Jahren freigegeben wurde",
     "«freigegeben machten» — не немецкая конструкция"),
    (11323, "example_tr",
     "Filmin erotik sahneleri vardı ve "
     "bu onu 16 yaşından itibaren derecelendirdi",
     "Filmde erotik sahneler vardı, bu yüzden 16 yaş sınırı kondu",
     "«derecelendirdi» это оценил по шкале"),
    # 9728 Rechtfertigung
    (16733, "example_tr", "Davranışı için bir haklılık aradı",
     "Davranışı için bir gerekçe aradı",
     "«haklılık» это правота, а не оправдание"),
    # 9729 brauen
    (11941, "example_uk", "Вона заварює чай із свіжими травами",
     "Вона заварює чай зі свіжими травами",
     "«із» перед свистящей"),
    (11941, "example_pl", "W tym pubie sami warzą piwo",
     "Parzy herbatę ze świeżymi ziołami",
     "перевод другого предложения"),
    # 9731 Delirium
    (13010, "example_pl", "Przy wysokiej gorączce wpadł w delirium",
     "Pacjent zapadł w delirium, gdy gorączka stała się zbyt wysoka",
     "перевод другого предложения"),
    # 9732 Stadtteil
    (18417, "example_tr", "Şehrin mahallesi çok kültürlü ve canlıdır",
     "Bu semt çok kültürlü ve canlı",
     "«şehrin mahallesi» — лишний изафет"),
    # 9733 tappen
    (8253, "example_uk", "Він намацував вимикач у темряві",
     "Він ходив навпомацки в темряві й намагався знайти вимикач",
     "потеряно «umher» и «versuchte»"),
    (8253, "example_tr",
     "Karanlıkta yürüyordu ve ışık anahtarını bulmaya çalışıyordu",
     "Karanlıkta el yordamıyla ilerliyor ve "
     "ışık düğmesini bulmaya çalışıyordu",
     "«yürüyordu» теряет ощупь"),
    (8253, "example_pl", "Po ciemku szedł po omacku do wyłącznika",
     "Szedł po omacku w ciemności i próbował znaleźć włącznik",
     "потеряно «versuchte zu finden»"),
    # 9734 Flaschengeist
    (14728, "translation_uk", "джин з бутилки, дух із пляшки",
     "джин з пляшки, дух із пляшки",
     "«бутилка» — русизм"),
    # 9735 anmutig
    (11358, "example_tr", "Dansçı sahnede zarifane hareket ediyordu",
     "Dansçı sahnede zarif bir şekilde hareket ediyordu",
     "«zarifane» — нет такого наречия"),
    (11358, "example_pl", "Tańczyła pełna gracji po scenie",
     "Tancerka poruszała się pełna gracji po scenie",
     "в эталоне «bewegte sich», и потеряна танцовщица"),
    # 9736 ahnungslos
    (11359, "translation_uk",
     "нічого не підозрюючий, необізнаний, несвідомий",
     "який нічого не підозрює, необізнаний, несвідомий",
     "«не підозрюючий» — калька активного дієприкметника"),
    (11359, "example_pl",
     "Wrócił do domu zupełnie nieświadomy niespodzianki",
     "Był całkowicie nieświadomy tego, co planowała jego żona",
     "перевод другого предложения"),
    # 9737 Duett
    (14729, "example_uk", "Два співаки співають чудовий дует",
     "Обидва співаки співають чудовий дует",
     "в эталоне «die beiden»"),
    (14729, "example_pl", "Zaśpiewali razem piękny duet",
     "Obaj śpiewacy śpiewają piękny duet",
     "эталон в настоящем времени"),
    # 9738 inszenieren
    (14730, "example_pl", "Reżyser chce inscenizować nową sztukę",
     "Reżyser chce wystawić sztukę",
     "«nową» в эталоне нет"),
    # 9739 plausibel
    (8254, "example_pl", "Jego tłumaczenie brzmi wiarygodnie",
     "Jego tłumaczenie brzmi wiarygodnie, ale w nie nie wierzę",
     "потеряна вторая половина"),
    # 9740 lahmen
    (8255, "example_en", "He's still limping after the injury",
     "The horse has been limping since the fall",
     "перевод другого предложения"),
    (8255, "example_uk", "Він досі кульгає після травми коліна",
     "Кінь кульгає після падіння",
     "перевод другого предложения"),
    (8255, "example_tr", "Dizi ağrıdığı için topallıyor",
     "At düşüşten beri topallıyor",
     "перевод другого предложения"),
    (8255, "example_pl", "Pies kuleje po skaleczeniu łapy",
     "Koń kuleje od upadku",
     "перевод другого предложения"),
    # 9741 zerkratzt
    (8256, "example_pl", "Ekran telefonu jest cały porysowany",
     "Porysowany telefon jednak jeszcze działa",
     "перевод другого предложения"),
    # 9743 Kilogramm
    (18054, "example_tr", "Bu un çuvalı bir kilogram ağırlanıyor",
     "Bu un çuvalı bir kilogram ağırlığında",
     "«ağırlanıyor» это принимают как гостя"),
    # 9744 Winterschlaf
    (15775, "example_ru", "Медведь впадает в зимнюю спячку",
     "Медведь находится в зимней спячке",
     "«hält Winterschlaf» — уже спит, а не впадает"),
    (15775, "example_uk", "Ведмідь входить в зимову сплячку",
     "Ведмідь перебуває в зимовій сплячці",
     "«hält Winterschlaf» — уже спить, а не входить"),
    (15775, "example_pl", "Niedźwiedź zapada w sen zimowy",
     "Niedźwiedź zapadł w sen zimowy",
     "«hält Winterschlaf» — уже спит"),
    # 9745 ausspionieren
    (16734, "example_uk", "Таємні агенти хочуть шпигунити за ворогом",
     "Таємні агенти хочуть шпигувати за ворогом",
     "«шпигунити» — нет такой формы"),
    (16734, "example_tr",
     "Gizli ajanlar düşman hakkında casus yapmak istiyorlar",
     "Gizli ajanlar düşmana casusluk yapmak istiyor",
     "«casus yapmak» — не выражение"),
    # 9746 flach
    (8257, "example_pl", "Ten dach jest zupełnie płaski",
     "Płytkie jezioro jest idealne do pływania",
     "перевод другого предложения"),
    # 9749 Hecht
    (15776, "example_ru", "Щука — это большая рыба в озере",
     "Щука — большая рыба в озере",
     "лишнее «это» при тире"),
    (15776, "example_tr", "Turna balığı göldeki büyük bir balık",
     "Turna balığı göldeki büyük bir balıktır",
     "фраза без связки"),
    (15776, "example_pl", "W jeziorze złowiliśmy dużego szczupaka",
     "Szczupak to duża ryba w jeziorze",
     "перевод другого предложения"),
    # 9750 Kettenreaktion
    (18055, "example_tr",
     "Küçük bir hata zincir reaksiyonuna neden oldu",
     "Küçük bir hata zincirleme reaksiyona neden oldu",
     "перевод слова — «zincirleme reaksiyon»"),
    # 9752 irrational
    (11360, "example_pl", "To był zupełnie irracjonalny strach",
     "Jego irracjonalny strach przed samolotami jest nieuzasadniony",
     "перевод другого предложения"),
    # 9753 mixen
    (11942, "example_uk", "Я мішаю смузі з фруктами та йогуртом",
     "Я змішую смузі з фруктів та йогурту",
     "«мішаю» разговорное, и не тот падеж"),
    (11942, "example_pl", "Zmiksuj banana z jogurtem",
     "Miksuję smoothie z owoców i jogurtu",
     "перевод другого предложения"),
    # 9754 paranormal
    (14731, "example_tr", "Paranormal olaylarla ilgileniyordu",
     "Paranormal olaylarla ilgileniyor",
     "эталон в настоящем времени"),
    # 9755 Pelzmantel
    (13757, "example_uk",
     "Вона носила елегантний хутровий плащ на вечірку",
     "Вона вдягнула на вечірку елегантну шубу",
     "«плащ» это не шуба, и «носила на вечірку» — калька"),
    (13757, "example_pl",
     "Włożyła na przyjęcie elegancki płaszcz z futra",
     "Włożyła na przyjęcie eleganckie futro",
     "перевод слова — «futro»"),
    # 9757 Gerichtsverfahren
    (16735, "example_uk", "Судовий процес тривало вже два роки",
     "Судовий процес триває вже два роки",
     "рассогласование рода, и время"),
    (16735, "example_tr", "Dava çoktan iki yıldır sürüyor",
     "Dava iki yıldır sürüyor",
     "«çoktan» с «-dır» противоречат друг другу"),
    # 9758 Anteilnahme
    (11361, "example_uk", "Його співчуття до мого болю було щирим",
     "Його співчуття до мого болю було справді щирим",
     "потеряно «echt»"),
    (11361, "example_tr",
     "Acımıma karşı duyduğu sempati çok samimiydi",
     "Acıma karşı duyduğu ilgi çok samimiydi",
     "«Acımıma» — двойное притяжание"),
    (11361, "example_pl", "Dziękuję za okazane współczucie",
     "Jego współczucie dla mojego bólu było naprawdę szczere",
     "перевод другого предложения"),
    # 9759 Passagierliste
    (17336, "example_en", "My name is on the airplanes passenger list",
     "My name is on the airplane's passenger list",
     "потерян апостроф"),
    (17336, "example_tr", "Benim adım uçağın yolcu listesinde var",
     "Adım uçağın yolcu listesinde var",
     "лишнее «benim» при притяжательной форме"),
    # 9761 Gesichtserkennung
    (17691, "translation_uk", "розпізнавання обличь",
     "розпізнавання облич",
     "«обличь» — нет такой формы"),
    (17691, "example_uk",
     "Розпізнавання обличь на смартфоні працює дуже добре",
     "Розпізнавання облич на смартфоні працює дуже добре",
     "«обличь» — нет такой формы"),
    # 9762 Eishockey
    (2396, "example_uk", "Я граю в хокей на льоду",
     "Я люблю грати в хокей на льоду",
     "потеряно «gern»"),
    # 9763 bekehren
    (14732, "example_tr", "Onu kendi dinine döndürmeye çalıştılar",
     "Arkadaşını dine döndürmeye çalıştı",
     "в эталоне один человек и его друг"),
    (14732, "example_pl", "Próbował nawrócić całą swoją rodzinę",
     "Próbował nawrócić swojego przyjaciela",
     "в эталоне друг, а не семья"),
    # 9764 vernaschen
    (11943, "example_uk",
     "Діти з'їли всі цукерки, що принесла бабуся",
     "Діти злопали всі солодощі, які принесла їхня бабуся",
     "перевод слова — «злопати», и «Süßigkeiten» это солодощі"),
    (11943, "example_tr",
     "Çocuklar, büyükannenin getirdiği tüm şekerleri yediler",
     "Çocuklar büyükannelerinin getirdiği tüm şekerleri silip süpürdü",
     "«yediler» теряет оттенок, и потеряно притяжание"),
    (11943, "example_pl", "Dzieci pochłonęły wszystkie ciastka od babci",
     "Dzieci pochłonęły wszystkie słodycze, które przyniosła ich babcia",
     "«ciastka» это печенье, а «Süßigkeiten» — сладости"),
    # 9765 dichtmachen
    (8258, "example_uk",
     "Ресторан повинен закритися, тому що мало клієнтів",
     "Ресторан має закритися, бо клієнтів занадто мало",
     "потеряно «zu wenig»"),
    (8258, "example_pl", "Sklep na rogu musiał zamknąć interes",
     "Restauracja musi zamknąć interes, bo jest za mało klientów",
     "перевод другого предложения"),
    # 9766 hinken
    (13011, "example_uk", "Він кульгає після травми коліна",
     "Після аварії він трохи кульгає, але стає краще",
     "перевод другого предложения"),
    (13011, "example_pl", "Po wypadku wciąż trochę kuleje",
     "Od wypadku trochę kuleje, ale jest coraz lepiej",
     "потеряна вторая половина"),
    # 9767 Billion — польский «trylion» это 10¹⁸
    (9913, "translation_pl", "trylion",
     "bilion",
     "немецкий Billion это 10¹², по-польски bilion, а trylion — 10¹⁸"),
    (9913, "example_pl", "Dług publiczny sięga kilku trylionów euro",
     "Dług publiczny sięga kilku bilionów euro",
     "число было завышено в миллион раз"),
    # 9768 Schlafsaal
    (18418, "example_ru",
     "В спальне интерната спит двенадцать мальчиков в одной комнате",
     "В спальне интерната спят двенадцать мальчиков в одной комнате",
     "«спит двенадцать» — рассогласование"),
    # 9770 Demenz
    (13012, "example_uk",
     "Його дідусь страждає деменцією й іноді не впізнає свою сім'ю",
     "Його дідусь страждає на деменцію й іноді не впізнає свою сім'ю",
     "«страждати» требует «на»"),
    (13012, "example_tr",
     "Büyükbabası demans hastalığına sahip ve ailesini bazen tanımıyor",
     "Büyükbabası demans hastası ve ailesini bazen tanımıyor",
     "«hastalığına sahip» — калька"),
    (13012, "example_pl", "Dziadek ma demencję i czasem nas nie poznaje",
     "Jego dziadek ma demencję i czasem nie poznaje swojej rodziny",
     "в эталоне он не узнаёт семью, а не нас"),
    # 9771 Pieps
    (14262, "example_pl", "Usłyszałem pisk czujnika dymu",
     "Pisk czujnika dymu ostrzega nas przed pożarem",
     "перевод другого предложения"),
    # 9772 Rückwärtsgang
    (17337, "example_tr", "Araba geri vitese alıyor ve garajdan çıkıyor",
     "Araba geri vitesi takıyor ve garajdan çıkıyor",
     "«vitese almak» без дополнения не держится"),
    # 9773 Boutique
    (9914, "example_tr",
     "Eski şehirdeki küçük butikten gerçek tasarımcı kıyafetler bulabilirsin",
     "Eski şehirdeki küçük butikte gerçek tasarımcı kıyafetler bulabilirsin",
     "«butikten bulmak» — не то управление"),
    (9914, "example_pl", "Kupiła tę sukienkę w małym butiku",
     "W małym butiku na starym mieście można znaleźć "
     "prawdziwe ubrania designerskie",
     "перевод другого предложения"),
    # 9774 unantastbar
    (8259, "example_pl", "Godność człowieka jest nietykalna",
     "Prawa człowieka są nietykalne i powinny być wszędzie respektowane",
     "перевод другого предложения"),
    # 9775 Tumult
    (8260, "example_uk",
     "На концерті сталася велика метушня і поліція мала втрутитися",
     "На концерті сталася велика метушня, і поліція мала втрутитися",
     "пропущена запятая"),
    (8260, "example_tr",
     "Konsertte büyük bir kargaşa oldu ve polis müdahale etmek zorunda kaldı",
     "Konserde büyük bir kargaşa oldu ve polis müdahale etmek zorunda kaldı",
     "«Konsertte» — лишняя согласная"),
    (8260, "example_pl", "Na koncercie zrobiło się wielkie zamieszanie",
     "Na koncercie zrobiło się wielkie zamieszanie "
     "i policja musiała interweniować",
     "потеряна полиция"),
    # 9776 Radioaktivität
    (18056, "example_uk",
     "Радіоактивність в зоні сильно зросла після аварії",
     "Радіоактивність у зоні сильно зросла після аварії",
     "«в» перед согласной"),
    # 9777 rechtlich
    (16469, "example_tr", "Bu dava da hukuki durum çok karmaşık",
     "Bu davada hukuki durum çok karmaşık",
     "«dava da» вместо «davada» меняет смысл"),
    # 9778 unfruchtbar
    (15777, "example_uk",
     "Безплідний грунт робить вирощування овочів неможливим",
     "Неродючий ґрунт робить вирощування овочів неможливим",
     "«безплідний» о живом, и «грунт» без ґ"),
    (15777, "example_pl", "Ta ziemia jest jałowa i nic tu nie rośnie",
     "Jałowa ziemia uniemożliwia uprawę warzyw",
     "перевод другого предложения"),
    # 9779 Gehege
    (15778, "example_tr",
     "Maymunlar hayvanat bahçesinin kafesinde oynuyorlar",
     "Maymunlar hayvanat bahçesinin bölmesinde oynuyor",
     "«kafes» это клетка, а «Gehege» — вольер"),
    (15778, "example_pl", "Małpy biegają po wybiegu w zoo",
     "Małpy bawią się na wybiegu w zoo",
     "«spielen» это играют, а не бегают"),
    # 9780 Kopierer
    (2625, "example_uk", "Копіювальний апарат зламаний",
     "Ксерокс зламаний",
     "перевод слова — «ксерокс»"),
    # 9781 Staatspolizei
    (16738, "example_ru",
     "Государственная полиция строго контролировала границы",
     "Государственная полиция очень строго контролировала границы",
     "потеряно «sehr»"),
    (16738, "example_uk",
     "Державна поліція суворо контролювала кордони",
     "Державна поліція дуже суворо контролювала кордони",
     "потеряно «sehr»"),
    # 9782 Brautpaar
    (15269, "example_tr",
     "Yeni evli çift düğünde ilk danslarını yaptılar",
     "Yeni evli çift düğünde ilk danslarını yaptı",
     "«çift» единственного числа"),
    (15269, "example_pl", "Para młoda tańczyła pierwszy taniec",
     "Para młoda tańczyła pierwszy taniec na weselu",
     "потеряно «auf der Hochzeit»"),
    # 9783 Bestimmung
    (16739, "example_tr", "Kontratın hükümleri çok karmaşık",
     "Sözleşmenin hükümleri çok karmaşık",
     "«kontrat» просторечие, термин — «sözleşme»"),
    # 9784 ratsam
    (8261, "example_pl", "Lepiej wziąć parasol, to wskazane",
     "Wskazane byłoby skonsultować się z prawnikiem",
     "перевод другого предложения"),
    # 9786 Geschwafel
    (14263, "example_uk",
     "Це була просто пустомеля, ніхто йому не вірив",
     "Це була просто балаканина, ніхто йому не вірив",
     "«пустомеля» это человек, а не болтовня"),
    (14263, "example_tr", "O sadece saçmamaydı, kimse ona inanmadı",
     "O sadece boş laftı, kimse ona inanmadı",
     "«saçmamaydı» — разорванное слово"),
    (14263, "example_pl", "Dość tej gadaniny, przejdźmy do rzeczy",
     "To była tylko gadanina, nikt mu nie wierzył",
     "перевод другого предложения"),
    # 9788 sogleich
    (18891, "example_en", "Come here at once!",
     "I'll come right away, wait a moment",
     "перевод другого предложения"),
    # 9789 klebrig
    (8262, "example_tr", "Şekerleme yapışkan ve çilek tadında",
     "Şekerler yapışkan ve çilek tadında",
     "эталон во множественном числе"),
    (8262, "example_pl", "Mam lepkie ręce od cukierków",
     "Cukierki są lepkie i smakują truskawką",
     "перевод другого предложения"),
    # 9790 klinisch
    (13013, "example_tr", "Klinik araştırması olumlu sonuçlar gösterdi",
     "Klinik araştırma olumlu sonuçlar gösterdi",
     "лишний изафет"),
    (13013, "example_pl", "Badania kliniczne dały dobre wyniki",
     "Badanie kliniczne pokazało pozytywne wyniki",
     "эталон в единственном числе"),
    # 9791 Wirtshaus
    (11944, "example_uk", "Ми йдемо в пивну пити пиво вечором",
     "Сьогодні ввечері ми йдемо в пивну випити пива",
     "порядок слов и потеряно «heute»"),
    (11944, "example_tr", "Bu gece meyhaneye gidip bira içiyoruz",
     "Bu akşam meyhaneye gidip bira içeceğiz",
     "«bu gece» это ночью, и время"),
    # 9792 Transportmittel
    (17338, "example_uk",
     "Автомобіль – важливий засіб транспорту в повсякденному житті",
     "Автомобіль – важливий транспортний засіб у повсякденному житті",
     "перевод слова — «транспортний засіб»"),
    (17338, "example_tr",
     "Araba günlük hayatta önemli bir ulaştırma aracıdır",
     "Araba günlük hayatta önemli bir ulaşım aracıdır",
     "перевод слова — «ulaşım aracı»"),
    # 9793 Laderaum
    (17339, "example_en", "The trucks cargo hold was packed with goods",
     "The truck's cargo hold was packed with goods",
     "потерян апостроф"),
    (17339, "example_uk",
     "Вантажне відділення вантажівки було запаковано товарами",
     "Вантажний відсік вантажівки був напханий товарами",
     "«було запаковано товарами» — не то управление"),
    # 9795 Raupe
    (15779, "example_pl", "Na liściu siedzi zielona gąsienica",
     "Zielona gąsienica pełznie po liściu",
     "«kriecht» это ползёт, а не сидит"),
    # 9796 Bistro
    (11945, "example_tr", "Köşedeki bistroda öğle yemeği yiyelim",
     "Sinemadan sonra bistroya kahve içmeye gidiyoruz",
     "перевод другого предложения"),
    # 9797 überbrücken
    (8264, "example_uk", "Ми маємо подолати різниці й працювати разом",
     "Ми маємо подолати розбіжності й працювати разом",
     "«різниці» это разницы в числах"),
    (8264, "example_tr", "Farklılıkları aşmalı ve birlikte çalışmalıyız",
     "Farklılıkları aşmalıyız ve birlikte çalışmalıyız",
     "у первого сказуемого потеряно лицо"),
    # 9799 Frettchen
    (15780, "example_ru", "Хорек – милое домашнее животное",
     "Хорёк – милое домашнее животное",
     "«е» вместо «ё»"),
    (15780, "example_uk", "Тхір – мила домашна тварина",
     "Тхір – мила домашня тварина",
     "«домашна» — нет такой формы"),
    (15780, "example_pl", "Moja fretka śpi całymi dniami",
     "Fretka to miłe zwierzę domowe",
     "перевод другого предложения"),
    # 9800 Kontonummer
    (9915, "example_tr", "Senin hesap numarası nedir?",
     "Senin hesap numaran nedir?",
     "потеряно притяжание"),
    # 9801 untertan
    (16740, "example_en",
     "The subject peoples rebelled against their oppressors",
     "He didn't want to be subject to anyone",
     "перевод другого предложения"),
    (16740, "example_ru",
     "Подчинённые народы восстали против своих угнетателей",
     "Он не хотел быть никому подвластным",
     "перевод другого предложения"),
    (16740, "example_uk",
     "Залежні народи повстали проти своїх гнетителів",
     "Він не хотів бути нікому підвладним",
     "перевод другого предложения"),
    (16740, "example_tr", "Tabi halklar baskıcılarına karşı isyan etti",
     "Kimseye tabi olmak istemiyordu",
     "перевод другого предложения"),
    # 9802 Buchhandlung
    (9916, "example_tr", "Yeni kitapları kitap dükkanından alıyorum",
     "Yeni kitapları kitapçıdan alıyorum",
     "перевод слова — «kitapçı»"),
    (9916, "example_pl", "Kupiłem tę książkę w księgarni",
     "Kupuję nowe książki w księgarni",
     "эталон в настоящем и о новых книгах"),
    # 9803 Haferbrei
    (11946, "example_uk", "Теплу вівсяну кашу особливо смачно взимку",
     "Тепла вівсяна каша особливо смачна взимку",
     "рассогласование падежа"),
    (11946, "example_pl", "Na śniadanie jem owsiankę z owocami",
     "Ciepła owsianka smakuje szczególnie dobrze w zimie",
     "перевод другого предложения"),
    # 9804 Brokkoli
    (11947, "example_pl", "Dzieci nie lubią brokułów",
     "Brokuł jest bardzo zdrowy i smaczny",
     "перевод другого предложения"),
    # 9805 siegreich
    (8265, "example_pl", "Zwycięska drużyna głośno świętowała",
     "Zwycięska drużyna głośno świętowała swoje zwycięstwo",
     "потеряно «seinen Sieg»"),
    # 9806 vorherbestimmt
    (8266, "example_uk", "Доля, здається, передбачена",
     "Доля, здається, передвизначена",
     "«передбачена» это предсказана, а не предопределена"),
    (8266, "example_pl",
     "Czuł, że to spotkanie było z góry przeznaczone",
     "Los zdaje się być z góry przeznaczony",
     "перевод другого предложения"),
    # 9807 Urwald
    (15781, "example_ru",
     "В первобытном лесу Бразилии ещё много неизученных территорий",
     "В девственном лесу Бразилии ещё много неизученных территорий",
     "перевод слова — «девственный лес»"),
    (15781, "example_uk",
     "У первісному лісі Бразилії ще багато невідомих територій",
     "У пралісі Бразилії ще багато недосліджених територій",
     "перевод слова — «праліс», и «unerforscht» это недосліджений"),
    (15781, "example_pl", "W dżungli jest bardzo gorąco i wilgotno",
     "W puszczy Brazylii jest jeszcze wiele niezbadanych terenów",
     "перевод другого предложения"),
    # 9808 vorankommen
    (8267, "example_en", "We're just not making progress on this project",
     "We finally want to make progress on this project",
     "эталон о желании, а не о неудаче"),
    (8267, "example_uk",
     "У цьому проекті ми просто не просуваємось вперед",
     "Ми хочемо нарешті просунутися в цьому проекті",
     "эталон о желании, а не о неудаче"),
    (8267, "example_tr", "Bu projede hiç ilerleme sağlayamıyoruz",
     "Bu projede nihayet ilerlemek istiyoruz",
     "эталон о желании, а не о неудаче"),
    (8267, "example_pl", "W pracy wreszcie zaczynam robić postępy",
     "Chcemy wreszcie zrobić postępy w tym projekcie",
     "перевод другого предложения"),
    # 9809 Börsenaufsicht
    (17869, "example_ru",
     "Надзор фондовой биржи устанавливает строгие правила "
     "для финансовых компаний",
     "Биржевой регулятор устанавливает строгие правила "
     "для финансовых компаний",
     "«надзор биржи» — калька"),
    (17869, "example_uk",
     "Наглядова служба біржі встановлює суворі правила "
     "для фінансових компаній",
     "Біржовий нагляд встановлює суворі правила для фінансових компаній",
     "«наглядова служба біржі» — калька"),
    (17869, "example_pl", "Nadzór giełdowy sprawdza te transakcje",
     "Nadzór giełdowy ma surowe zasady dla firm finansowych",
     "перевод другого предложения"),
    # 9810 Unkosten
    (9917, "example_uk", "Видатки на ремонт вище, ніж очікувалось",
     "Видатки на ремонт вищі, ніж очікувалося",
     "«вище» наречие вместо прилагательного"),
    (9917, "example_pl", "Koszty remontu okazały się wyższe",
     "Koszty remontu są wyższe niż oczekiwano",
     "потеряно «als erwartet»"),
    # 9811 gegenüberstehen
    (8268, "example_uk",
     "Ми стоїмо перед великим завданням, яке маємо вирішити разом",
     "Ми стоїмо перед великим викликом, який маємо здолати разом",
     "«Herausforderung» это виклик, а не завдання"),
    (8268, "example_pl", "Stoimy przed trudnym wyborem",
     "Stoimy przed wielkim wyzwaniem, które musimy pokonać razem",
     "перевод другого предложения"),
    # 9812 gebeugt
    (8269, "example_uk",
     "Старий чоловік пройшов вулицею зі зігнутою спиною",
     "Старий чоловік пройшов вулицею із зігнутою спиною",
     "«зі» перед согласной"),
    (8269, "example_pl", "Szedł ulicą z pochylonymi plecami",
     "Stary mężczyzna szedł ulicą z pochylonymi plecami",
     "потерян старик"),
    # 9813 Sonnencreme
    (13758, "example_uk", "Не забудь сонцезахисний крем на пляж",
     "Не забудь узяти сонцезахисний крем, коли поїдемо на море",
     "перевод другого предложения"),
    (13758, "example_tr",
     "Sahile gittiğimizde güneş kremi almayı unutma",
     "Denize gittiğimizde güneş kremi almayı unutma",
     "в эталоне море, а не пляж"),
    # 9815 zuordnen
    (8270, "example_uk", "Віднеси ці книжки до бібліотеки",
     "Я не можу віднести цей випадок до якоїсь чіткої категорії",
     "перевод другого предложения"),
    # 9816 verschonen
    (8271, "example_tr", "Askerler köydeki çocukları bağışladı",
     "Lütfen beni yorumlarından esirge",
     "перевод другого предложения"),
    # 9817 Knochenmark
    (13014, "example_uk",
     "Кістковий мозок виробляє червоні кров'яні клітини",
     "Кістковий мозок виробляє червоні кров'яні тільця",
     "перевод слова — «кров'яне тільце»"),
    # 9818 neurotisch
    (11362, "example_pl", "Jego neurotyczne zachowanie wszystkich męczy",
     "Jego neurotyczne zachowanie staje się coraz bardziej problematyczne",
     "перевод другого предложения"),
    # 9819 beständig
    (8272, "example_pl", "Mamy dziś stałą, ładną pogodę",
     "Pokazuje niezmienną postawę, niezależnie od tego, jak trudno się staje",
     "перевод другого предложения"),
    # 9820 blitzschnell
    (8273, "example_tr", "Tehlikeye şimşek hızında tepki verdi",
     "Tehlikeye yıldırım hızıyla tepki verdi",
     "перевод слова — «yıldırım hızıyla»"),
    # 9821 Raster
    (8274, "example_uk", "Повісь на вікно сітку від комарів",
     "Сітка цієї графіки занадто груба для наших цілей",
     "перевод другого предложения"),
    (8274, "example_pl", "Poukładaj ikonki według siatki",
     "Siatka tej grafiki jest zbyt gruba do naszych celów",
     "перевод другого предложения"),
    # 9822 abschrecken
    (8275, "example_pl", "Wysoka cena odstrasza wielu klientów",
     "Egzamin odstrasza wielu studentów",
     "перевод другого предложения"),
    # 9823 ausgehend
    (8276, "example_pl", "Połączenia wychodzące są dziś darmowe",
     "Wychodząc z tych faktów, musimy opracować nowe strategie",
     "перевод другого предложения"),
    # 9824 Doppelmord
    (16742, "example_tr", "Çift cinayet tüm şehri şok etti",
     "Çifte cinayet tüm şehri şok etti",
     "перевод слова — «çifte cinayet»"),
    # 9826 erklimmen
    (8277, "example_pl", "Powoli wspinamy się na szczyt góry",
     "Wspinamy się na górę powoli, ale pewnie",
     "потеряно «aber sicher»"),
    # 9827 reizvoll — в эталоне два определения без союза
    (8278, "example_de", "Das ist eine reizvoll interessante Idee",
     "Das ist eine reizvolle und interessante Idee",
     "«reizvoll interessante» — наречие на месте прилагательного"),
    (8278, "example_tr",
     "Bu, hakkında düşünmem gereken çekici bir fikirdir",
     "Bu, çekici ve ilginç bir fikir",
     "перевод другого предложения"),
    (8278, "example_pl", "To bardzo atrakcyjna propozycja dla nas",
     "To atrakcyjny i interesujący pomysł",
     "перевод другого предложения"),
    # 9828 Mordversuch
    (16743, "example_uk",
     "Замах на вбивство відомого співака потрясло місто",
     "Замах на вбивство відомого співака потряс місто",
     "рассогласование рода"),
    # 9829 erdulden — в эталоне «Kritik» во множественном
    (8279, "example_de", "Ich erdulde seine ständigen Kritik nicht länger",
     "Ich erdulde seine ständige Kritik nicht länger",
     "«Kritik» женского рода и единственного числа"),
    (8279, "example_pl", "Musiała znosić jego ciągłe narzekanie",
     "Nie będę dłużej znosić jego ciągłej krytyki",
     "перевод другого предложения"),
    # 9830 abkratzen
    (8280, "example_uk", "Я зішкрібаю наліпку зі скла",
     "Я зішкрібаю стару наліпку зі скляної банки",
     "потеряно «alte» и «Glas» как банка"),
    # 9831 Navigation
    (17340, "example_en",
     "The navigation on this website is very user-friendly",
     "The navigation in the car helps me find the right way",
     "перевод другого предложения"),
    (17340, "example_tr",
     "Bu web sitesinin navigasyonu çok kullanıcı dostudur",
     "Arabadaki navigasyon doğru yolu bulmama yardım ediyor",
     "перевод другого предложения"),
    # 9832 grenzenlos
    (8281, "example_pl", "Jego cierpliwość jest bezgraniczna",
     "Jego fantazja jest bezgraniczna",
     "в эталоне фантазия, а не терпение"),
    # 9833 unbegreiflich
    (8282, "example_uk",
     "Його поведінка була для мене зовсім незрозуміла",
     "Його поведінка була для мене зовсім незбагненна",
     "перевод слова — «незбагненний»"),
    (8282, "example_pl", "To dla mnie zupełnie niepojęte",
     "Jego zachowanie było dla mnie zupełnie niepojęte",
     "потеряно подлежащее"),
    # 9834 Bootsmann
    (9201, "example_uk", "Боцман наказав команді піднути вітрила",
     "Боцман наказав команді підняти вітрила",
     "«піднути» — опечатка"),
    # 9835 angewidert
    (11363, "example_uk", "Він був відштовхнутий лицемірством",
     "Він відчував огиду до лицемірства",
     "«був відштовхнутий» — калька страдательного"),
    (11363, "example_tr", "Münafaklıktan tiksinmişti",
     "İkiyüzlülükten tiksinmişti",
     "«münafaklık» — нет такого слова"),
    (11363, "example_pl",
     "Był zniesmaczony jej zachowaniem przy stole",
     "Był zniesmaczony hipokryzją",
     "перевод другого предложения"),
    # 9836 gebügelt
    (13759, "example_uk", "Сорочка випрасувана й висить у шафі",
     "Сорочка була ідеально випрасувана",
     "перевод другого предложения"),
    # 9837 unglaubwürdig
    (8283, "example_uk", "Його виправдання звучить непереконливо",
     "Його історія звучить неправдоподібно",
     "в эталоне «Geschichte», а не оправдание"),
    (8283, "example_tr", "Hikâyesi inanılmaz geliyor",
     "Hikâyesi inandırıcı gelmiyor",
     "«inanılmaz» это поразительный, а не неправдоподобный"),
    (8283, "example_pl", "Jego tłumaczenie brzmi niewiarygodnie",
     "Jego historia brzmi niewiarygodnie",
     "в эталоне «Geschichte», а не объяснение"),
    # 9838 Polizeibeamte
    (9202, "example_uk", "Поліцейський регулював дорожний рух",
     "Поліцейський регулював дорожній рух",
     "«дорожний» — нет такой формы"),
    (9202, "example_tr", "Polis trafiği kontrol ediyordu",
     "Polis memuru trafiği düzenliyordu",
     "перевод слова — «polis memuru»"),
    # 9839 Hochschule
    (9607, "example_tr", "Üniversitede okuyor",
     "Yüksekokulda okuyor",
     "перевод слова — «yüksekokul»"),
    # 9841 Ballsaal
    (14733, "example_tr", "Bütün gece balo salonunda dansettiler",
     "Bütün akşam balo salonunda dans ettiler",
     "«dansettiler» слитно, и «gece» это ночь"),
    (14733, "example_pl", "Tańczyli całą noc w sali balowej",
     "Tańczyli cały wieczór w sali balowej",
     "в эталоне вечер, а не ночь"),
    # 9842 barmherzig
    (11364, "example_tr", "Doktor çok merhamet ediciydi",
     "Doktor çok merhametliydi",
     "«merhamet edici» — не форма"),
    (11364, "example_pl", "Był miłosierny wobec biednych",
     "Lekarz był bardzo miłosierny",
     "перевод другого предложения"),
    # 9843 Abstieg
    (8284, "example_en", "The descent was difficult for the family",
     "The descent from the mountain was exhausting for the whole family",
     "потеряно «vom Berg» и «ganze»"),
    (8284, "example_uk", "Спуск був важким для сім'ї",
     "Спуск з гори був виснажливим для всієї сім'ї",
     "потеряно «vom Berg» и «ganze»"),
    (8284, "example_tr", "İniş aile için zordu",
     "Dağdan iniş bütün aile için yorucuydu",
     "потеряно «vom Berg» и «ganze»"),
    (8284, "example_pl", "Zejście z góry zajęło nam dwie godziny",
     "Zejście z góry było wyczerpujące dla całej rodziny",
     "перевод другого предложения"),
    # 9846 Frauenheld
    (15270, "example_uk", "Він відомий як жінколюб",
     "Він відомий як бабій",
     "перевод слова — «бабій»"),
    (15270, "example_tr", "Kadın düşkünü olarak bilinir",
     "Çapkın olarak bilinir",
     "перевод слова — «çapkın»"),
    (15270, "example_pl", "Twój brat to straszny kobieciarz",
     "Jest znany jako kobieciarz",
     "перевод другого предложения"),
    # 9847 Ebbe
    (15783, "example_uk", "При відливі ми можемо гуляти по пляжу",
     "При відпливі ми можемо гуляти по пляжу",
     "перевод слова — «відплив»"),
    (15783, "example_pl", "Podczas odpływu zbieramy muszle na plaży",
     "Podczas odpływu możemy spacerować po plaży",
     "перевод другого предложения"),
    # 9848 dehydriert
    (13016, "example_tr", "Maraton sonra tamamen susuzlaşmıştım",
     "Maratondan sonra tamamen susuz kalmıştım",
     "«Maraton sonra» без падежа, и «susuzlaşmak» — нет такого"),
    (13016, "example_pl", "Po biegu byłem całkiem odwodniony",
     "Po maratonie byłem całkiem odwodniony",
     "в эталоне марафон, а не просто бег"),
    # 9849 flöten
    (8285, "example_uk", "Вона тихо грала на флейті",
     "Вона тихо мугикала собі під ніс пісеньку",
     "перевод другого предложения"),
    (8285, "example_pl", "Moja siostra uczy się grać na flecie",
     "Cicho nuciła sobie piosenkę",
     "перевод другого предложения"),
    # 9851 bereitwillig
    (8286, "example_uk", "Він охоче мені допомагав",
     "Він охоче мені допоміг",
     "эталон в совершённом виде"),
    (8286, "example_pl", "Chętnie mi pomógł z zakupami",
     "Chętnie mi pomógł",
     "«z zakupami» в эталоне нет"),
    # 9853 Verbundenheit
    (11365, "example_uk", "Між нами міцний зв'язок",
     "Між ними глибокий зв'язок",
     "в эталоне «zwischen ihnen», и «tief» это глибокий"),
    (11365, "example_pl", "Czuję silną więź z rodzinnym miastem",
     "Jest między nimi głęboka więź",
     "перевод другого предложения"),
    # 9854 Watt
    (18057, "example_uk", "Лампочка споживає 60 ватів",
     "Лампочка споживає 60 ват",
     "«ватів» — не та форма родительного"),
    # 9855 eigensinnig
    (11366, "example_tr",
     "Çocuk çok inatçı ve yaptığı istediği yapıyor",
     "Çocuk çok inatçı ve istediğini yapıyor",
     "«yaptığı istediği yapıyor» — разваленная фраза"),
    (11366, "example_pl", "Ten mały jest strasznie uparty",
     "Chłopiec jest bardzo uparty i robi, co chce",
     "потеряна вторая половина"),
    # 9857 unverwundbar
    (8288, "example_tr", "Kendini yaralanmaz sanıyor",
     "Savaş kahramanı tankında neredeyse yaralanmazdı",
     "перевод другого предложения"),
    (8288, "example_pl", "Bohater filmu wydaje się niezniszczalny",
     "Bohater wojenny był prawie niezniszczalny w swoim czołgu",
     "перевод другого предложения"),
    # 9858 verduften
    (8289, "example_uk", "Хлопак просто втік і залишив нас самих",
     "Хлопець просто змився і залишив нас самих",
     "«хлопак» — не украинская форма"),
    (8289, "example_tr", "Adam kayboldu ve bizi yalnız bıraktı",
     "Adam sıvışıp gitti ve bizi yalnız bıraktı",
     "перевод слова — «sıvışmak»"),
    # 9859 gestärkt
    (8290, "example_uk",
     "Після відпустки я відчував себе зміцненим і відпочившим",
     "Після відпустки я почувався зміцнілим і відпочилим",
     "«відпочившим» — калька"),
    (8290, "example_pl", "Po urlopie czuję się wzmocniony i wypoczęty",
     "Po urlopie czułem się wzmocniony i wypoczęty",
     "эталон в прошедшем времени"),
    # 9860 salzig
    (11948, "example_pl", "Ta zupa jest za słona",
     "Zupa jest za słona, nie mogę jej jeść",
     "потеряна вторая половина"),
    # 9862 Weinberg
    (11949, "example_uk", "Виноградник лежить на гарному місці",
     "Виноградник розташований у прекрасній місцевості",
     "«лежить на місці» — калька"),
    (11949, "example_pl", "Za domem mają małą winnicę",
     "Winnica położona jest w pięknej okolicy",
     "перевод другого предложения"),
    # 9864 kaltmachen
    (8292, "example_tr", "Bu filmde çeteci, rakibini öldürmek istiyor",
     "Bu filmde gangster rakibini öldürmek istiyor",
     "«çeteci» это член шайки, а в эталоне гангстер"),
    # 9865 Tiefgarage
    (18419, "example_ru", "Машина стоит в подземной парковке",
     "Машина стоит в подземном гараже",
     "«в парковке» — не то управление"),
    (18419, "example_tr", "Araba kapalı otoparkta duruyor",
     "Araba yeraltı otoparkında duruyor",
     "перевод слова — «yeraltı otoparkı»"),
    # 9866 umfassend
    (8293, "example_uk", "Нам потрібен всебічний аналіз ситуації",
     "Всеосяжне дослідження показує всі важливі аспекти",
     "перевод другого предложения"),
    (8293, "example_pl", "Dostaliśmy obszerny raport z badań",
     "Wszechstronne badanie pokazuje wszystkie ważne aspekty",
     "перевод другого предложения"),
    # 9867 Fliese
    (18420, "example_ru",
     "Плитки в ванной комнате очень красивые и голубые",
     "Плитка в ванной комнате очень красивая и голубая",
     "«плитки» по-русски собирательно в единственном"),
    (18420, "example_uk",
     "Плитки у ванній кімнаті дуже гарні та сині",
     "Плитка у ванній кімнаті дуже гарна та синя",
     "«плитки» по-украински собирательно в единственном"),
    # 9868 Freispruch
    (16746, "example_ru",
     "Обвиняемый получил оправдание от всех обвинений",
     "Обвиняемый был оправдан по всем обвинениям",
     "«оправдание от обвинений» — не то управление"),
    (16746, "example_uk",
     "Обвинувачений отримав виправдувальний вирок від всіх звинувачень",
     "Обвинуваченого виправдали за всіма звинуваченнями",
     "«вирок від звинувачень» — не то управление"),
    # 9870 ehelichen
    (15271, "example_uk",
     "Він хоче одружитися на ній і створити сім'ю",
     "Він хоче одружитися з нею і створити сім'ю",
     "«одружитися на» — русизм"),
    # 9871 rausgeben
    (8294, "example_tr", "Elli euroyu bozabilir misiniz?",
     "Elli eurodan para üstü verebilir misiniz?",
     "перевод слова — «para üstü vermek»"),
    (8294, "example_pl",
     "Czy może pan wydać z pięćdziesięciu złotych?",
     "Czy może pan wydać z pięćdziesięciu euro?",
     "в эталоне евро, а не злотые"),
    # 9873 beschämen
    (11367, "example_uk", "Його поведінка ганьбила всю сім'ю",
     "Його поведінка зганьбила всю сім'ю",
     "эталон в совершённом виде"),
    (11367, "example_pl", "Nie chciałem cię zawstydzać przy wszystkich",
     "Jego zachowanie zawstydziło całą rodzinę",
     "перевод другого предложения"),
    # 9874 Stoßstange
    (2854, "example_en", "The bumper of my car is damaged",
     "The bumper of my car was damaged in the accident",
     "потеряно «beim Unfall»"),
    (2854, "example_uk", "Бампер моєї машини пошкоджений",
     "Бампер моєї машини пошкоджений в аварії",
     "потеряно «beim Unfall»"),
    (2854, "example_tr", "Arabamın tamponı hasar gördü",
     "Arabamın tamponu kazada hasar gördü",
     "«tamponı» нарушена гармония, и потеряна авария"),
    # 9875 kommentieren
    (14264, "example_tr", "Bu konuda yorum yapmak istemiyorum",
     "Gazeteci son siyasi olayları yorumladı",
     "перевод другого предложения"),
    (14264, "example_pl", "Nie chcę komentować tej sprawy",
     "Dziennikarz komentował najnowsze wydarzenia polityczne",
     "перевод другого предложения"),
    # 9876 Krabbe
    (11950, "example_pl", "Na obiad zamówiliśmy kraba",
     "Krab to pyszne danie z owoców morza",
     "перевод другого предложения"),
    # 9877 Reiseführer
    (17342, "example_tr", "Rehber bize Paristeki en iyi yerleri gösterdi",
     "Rehber bize Paris'teki en iyi turistik yerleri gösterdi",
     "потерян апостроф, и «Sehenswürdigkeiten»"),
    # 9878 Ausfall
    (8296, "example_uk", "Збій інтернету був дуже дратівним",
     "Збій інтернету був дуже неприємним",
     "«дратівний» о человеке, не о сбое"),
    (8296, "example_pl", "Awaria prądu popsuła nam wieczór",
     "Awaria internetu była bardzo irytująca",
     "перевод другого предложения"),
    # 9879 stinkreich
    (9918, "example_uk", "Багата сім'я живе в величезному замку",
     "Страшенно багата сім'я живе у величезному замку",
     "потеряно «stink-», и «в» перед гласной"),
    (9918, "example_pl", "Jego wujek jest obrzydliwie bogaty",
     "Obrzydliwie bogata rodzina mieszka w ogromnym zamku",
     "перевод другого предложения"),
    # 9880 einchecken
    (2376, "example_uk", "Зареєструйся на сайті, щоб увійти",
     "Я реєструюся в готелі",
     "перевод другого предложения"),
    # 9881 zerschmettern
    (8297, "example_uk", "У гніві він розбив стілець на щепки",
     "У гніві він розтрощив стілець на тріски",
     "«щепки» — русизм"),
    (8297, "example_tr", "Öfkesinde sandalyeyi parçaladı",
     "Öfkeyle sandalyeyi paramparça etti",
     "«öfkesinde» — не то управление"),
    (8297, "example_pl", "Ze złości roztrzaskał krzesło o ścianę",
     "Ze złości roztrzaskał krzesło na kawałki",
     "«o ścianę» в эталоне нет"),
    # 9882 Notlage
    (8298, "example_pl", "W trudnej sytuacji pomogli nam sąsiedzi",
     "W trudnej sytuacji możemy liczyć na pomoc państwa",
     "перевод другого предложения"),
    # 9884 Kronleuchter
    (18421, "example_uk",
     "Величавий хрустальний люстр висить у центрі залу",
     "Розкішна кришталева люстра висить у центрі бальної зали",
     "«люстр» мужского рода и «хрустальний» — русизмы"),
    # 9885 verhöhnen
    (11368, "example_en",
     "The mocked students complained about the teachers behavior",
     "The mocked students complained to the principal",
     "перевод другого предложения, да ещё без апострофа"),
    (11368, "example_uk", "Він почувався висміяним перед усім класом",
     "Висміяні учні поскаржилися директорові",
     "перевод другого предложения"),
    (11368, "example_tr",
     "Alay edilen öğrenciler öğretmenin davranışından şikayet ettiler",
     "Alay edilen öğrenciler müdüre şikayet etti",
     "в эталоне жалуются директору"),
    (11368, "example_pl", "Czuł się wyśmiany przez kolegów z klasy",
     "Wyśmiewani uczniowie skarżyli się dyrektorowi",
     "перевод другого предложения"),
    # 9887 Anzugträger
    (13760, "example_tr",
     "Bu takı giyen adamlar tüm gün ofiste oturur ve "
     "bilgisayarda çalışırlar",
     "Bu takım elbiseli adamlar tüm gün ofiste oturup "
     "bilgisayarda çalışır",
     "«takı» это украшения, костюм — «takım elbise»"),
    # 9888 injizieren
    (13019, "example_en", "The doctor will give me an injection now",
     "The nurse injects the medicine into him",
     "перевод другого предложения"),
    (13019, "example_uk", "Лікар мені зараз зробить ін'єкцію",
     "Медсестра вводить йому ліки",
     "перевод другого предложения"),
    (13019, "example_tr", "Doktor şimdi bana iğneyi enjekte edecek",
     "Hemşire ona ilacı enjekte ediyor",
     "перевод другого предложения"),
    # 9889 Odyssee
    (14734, "example_uk",
     "Його подорож по Африці була справжньою одисеєю з багатьма пригодами",
     "Його подорож по Африці була справжньою одіссеєю з багатьма пригодами",
     "перевод слова — «одіссея»"),
    (14734, "example_tr",
     "Afrikaya olan yolculuğu birçok macerası olan uzun bir yolculuk oldu",
     "Afrika'daki yolculuğu birçok maceralı, gerçek bir destansı serüvendi",
     "потерян апостроф, и «yolculuk ... yolculuk» — тавтология"),
    (14734, "example_pl", "Ta podróż do domu była prawdziwą odyseją",
     "Jego podróż przez Afrykę była prawdziwą odyseją z wieloma przygodami",
     "перевод другого предложения"),
    # 9890 Swing
    (14735, "example_tr",
     "Bant bütün akşam swing çaldı ve herkes dansetti",
     "Grup bütün akşam swing çaldı ve herkes dans etti",
     "«bant» это лента, музыкальная группа — «grup»"),
    # 9891 verwundert
    (11369, "example_pl", "Spojrzał na mnie zdziwiony",
     "Spojrzał na mnie zdziwiony, kiedy nagle się roześmiałam",
     "потеряна вторая половина"),
    # 9892 beklauen
    (16748, "example_ru", "Вора поймали, когда он крал у старика",
     "Вора поймали, когда он обворовывал старика",
     "«крал у» — не то управление для «beklauen»"),
    (16748, "example_uk", "Його обікрали в переповненому автобусі",
     "Злодія зловили, коли він обкрадав старого чоловіка",
     "перевод другого предложения"),
    # 9894 Abscheu
    (11370, "example_uk", "Він дивився на гнилу м'ясо з відразою",
     "Він дивився на гниле м'ясо з відразою",
     "рассогласование рода"),
    (11370, "example_tr", "Çürük ete iğrenç bir şekilde baktı",
     "Çürük ete iğrenerek baktı",
     "«iğrenç bir şekilde» значит, что взгляд был отвратителен"),
    # 9895 Korrespondenz
    (14265, "example_pl",
     "Cała korespondencja z klientem leży w tej teczce",
     "Korespondencja między dwoma politykami była bardzo poufna",
     "перевод другого предложения"),
    # 9896 schnattern
    (14266, "example_uk", "Гуски гучно гагакали в подвір'ї",
     "Гуси гучно ґелґотали на подвір'ї",
     "«гуски» — не форма, и «в подвір'ї»"),
    (14266, "example_tr", "Kargalar ağaçta durmadan gaklıyor",
     "Kazlar avluda yüksek sesle gakladı",
     "«kargalar» это вороны, а в эталоне гуси"),
    # 9897 Rächer
    (15272, "example_pl", "W tym filmie mściciel szuka sprawiedliwości",
     "Mściciel chciał sprawiedliwości dla swojego narodu",
     "перевод другого предложения"),
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
