"""
Правки блока 56 (ряды 9501–9700, ранги 19198–19674).

Пять сломанных эталонов — больше, чем в любом блоке до этого:
  · `Der Zug eintraf pünktlich am Bahnhof` — приставка не отделена,
    нужно `traf ... ein`;
  · `Ich muss mich meinen Ängsten gegenübertreten` — лишнее `mich`;
  · `Hör auf, mich runterziehen` — потеряно `zu`;
  · `Die Situation erfordert drastische Massnahmen` — `ss` вместо `ß`;
  · `Das Gefangenenlager war unter miserablen Bedingungen` — лагерь
    не «под условиями»; польский перевод был единственным верным
    и подсказал, как читать эталон.

Прочие классы:
  · перевод другого предложения — больше сорока рядов;
  · турецкие обрывки: `Boyn atardamarları`, `O gerçek bencil biri`,
    `Bu bana karşı`, `Falcı gelecek değişeceğini söyledi`;
  · украинские несуществующие формы: `Спасальна`, `Враги`, `Пійдемо`,
    `смирювальна`, `плідний міхур`, `мучимим`;
  · украинское «мешкати» в значении «медлить» — это «жить».

    python -m app.scripts.fix_block_0056            # показать
    python -m app.scripts.fix_block_0056 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 9501 Sternschnuppe
    (15764, "translation_uk", "падаюча зірка, метеор",
     "зірка, що падає, метеор",
     "«падаюча» — калька активного дієприкметника"),
    (15764, "example_uk", "Ми бачили падаючу зірку й загадали бажання",
     "Ми бачили зірку, що падала, й загадали бажання",
     "«падаючу» — калька активного дієприкметника"),
    (15764, "example_pl",
     "Widziałem spadającą gwiazdę i pomyślałem życzenie",
     "Widzieliśmy spadającą gwiazdę i pomyśleliśmy życzenie",
     "эталон о «мы»"),
    # 9503 Sorgfalt
    (11334, "example_tr", "Usta büyük dikkat ile çalışıyor",
     "Usta büyük bir özenle çalışıyor",
     "«ile» пишется слитно, и перевод слова — «özen»"),
    # 9504 Kulisse
    (14718, "example_tr", "Tiyatro sahne tasarımı harika görünüyordu",
     "Tiyatro dekoru harika görünüyordu",
     "потерян изафет, и «sahne tasarımı» это оформление сцены"),
    (14718, "example_pl", "Dekoracje w tym teatrze są piękne",
     "Dekoracja teatralna wyglądała wspaniale",
     "перевод другого предложения"),
    # 9505 Männerstimme
    (15254, "example_uk", "Глибокий чоловічий голос назвав моє ім'я",
     "Низький чоловічий голос назвав моє ім'я",
     "«глибокий голос» — калька, по-украински низький"),
    (15254, "example_tr", "Derin bir erkek sesi adımı çağırdı",
     "Kalın bir erkek sesi adımı seslendi",
     "«derin ses» — калька, и «adımı çağırdı» не по-турецки"),
    (15254, "example_pl", "Z korytarza usłyszałam niski męski głos",
     "Niski męski głos zawołał moje imię",
     "перевод другого предложения"),
    # 9506 Wendepunkt
    (18884, "example_ru",
     "Эта встреча стала поворотным моментом в его жизни",
     "Диагноз стал поворотным моментом в его жизни",
     "в эталоне диагноз, а не встреча"),
    # 9508 voraussagen
    (8213, "example_uk", "Прогноз погоди не завжди точний",
     "Прогноз погоди не завжди може передбачити погоду",
     "перевод другого предложения"),
    (8213, "example_pl", "Nikt nie przewidział takiego wyniku",
     "Prognoza pogody nie zawsze potrafi przewidzieć pogodę",
     "перевод другого предложения"),
    # 9509 Ballistik
    (18047, "example_tr", "Balistik uzmanları mermiye analiz etti",
     "Balistik uzmanları mermiyi analiz etti",
     "«analiz etmek» требует аккузатива"),
    # 9510 Vorschule
    (9598, "example_tr", "Oğlum şimdi okul öncesine gidiyor",
     "Oğlum şimdi ana sınıfına gidiyor",
     "перевод слова — «ana sınıfı»"),
    # 9511 Geldwäsche
    (17866, "example_pl", "Bank oskarżono o pranie pieniędzy",
     "Pranie pieniędzy to forma przestępczości finansowej",
     "перевод другого предложения"),
    # 9512 Jüngling
    (15255, "example_tr", "Genç sadece yirmi yaşındaydı",
     "Delikanlı sadece yirmi yaşındaydı",
     "«genç» это прилагательное, нужно «delikanlı»"),
    # 9513 Rettungsaktion
    (12992, "example_uk",
     "Спасальна операція пропалих альпіністів була успішною",
     "Рятувальна операція для зниклих альпіністів була успішною",
     "«спасальна» и «пропалих» — нет таких форм"),
    # 9514 weiterkämpfen
    (12346, "example_uk",
     "Команда хотіла продовжувати боротьбу, хоч вона відставала",
     "Команда хотіла продовжувати боротьбу, хоч і програвала",
     "«відставала» это отставала, а не проигрывала"),
    # 9515 Blindheit
    (12993, "example_pl", "Jego ślepota nie przeszkodziła mu w pracy",
     "Jego ślepota nie przeszkodziła mu prowadzić udanego życia",
     "перевод другого предложения"),
    # 9516 Tendenz
    (8214, "example_tr",
     "Gençlerin daha fazla çevrimiçi çalışması eğilimi var",
     "Gençlerin daha çok çevrimiçi çalışması yönünde bir eğilim var",
     "фраза без связки не держится"),
    (8214, "example_pl", "Widać tendencję do pracy w domu",
     "Istnieje tendencja, że młodzi ludzie pracują więcej online",
     "перевод другого предложения"),
    # 9517 Lebensretter
    (12994, "example_pl", "Ten lekarz był moim wybawcą",
     "Ten lekarz był jego wybawcą",
     "в эталоне «sein», а не «мой»"),
    # 9518 Direktion
    (9185, "example_uk", "Керівництво затвердило нову політику",
     "Дирекція ухвалила нову директиву",
     "перевод слова — «дирекція», и «Richtlinie» это директива"),
    (9185, "example_tr", "Yönetim yeni bir politikaya karar verdi",
     "Yönetim yeni bir yönerge kararlaştırdı",
     "«Richtlinie» это yönerge, а не политика"),
    # 9519 beiwohnen
    (8215, "example_uk", "Я буду присутній на зборах",
     "Я буду присутній на конференції",
     "в эталоне конференция"),
    (8215, "example_pl", "Chciałbym uczestniczyć w tym spotkaniu",
     "Będę uczestniczył w konferencji",
     "перевод другого предложения"),
    # 9520 trauern
    (11335, "example_uk", "Я сумую про мого покійного друга",
     "Я сумую за моїм покійним другом",
     "«сумувати про» — не то управление"),
    # 9521 reinhauen
    (8216, "example_uk", "Давайте налягати і закінчимо це завдання",
     "Давай наляжемо й закінчимо це завдання",
     "смешаны две формы повелительного"),
    # 9522 Schlagsahne
    (11934, "example_uk", "На торті зверху збита сметана",
     "На торті зверху збиті вершки",
     "«сметана» это не вершки"),
    (11934, "example_tr", "Pasta üstüne çırpılmış krema var",
     "Pastanın üstünde krem şanti var",
     "потерян изафет"),
    # 9523 Puppenspieler
    (14719, "example_uk", "Лялькар показав чудесний виступ",
     "Лялькар показав чудовий виступ",
     "«чудесний» — русизм"),
    (14719, "example_tr", "Kukla oyuncusu harika bir gösteri sundu",
     "Kuklacı harika bir gösteri sundu",
     "перевод слова — «kuklacı»"),
    (14719, "example_pl", "Lalkarz zrobił dzieciom świetne przedstawienie",
     "Lalkarz dał wspaniałe przedstawienie",
     "«dzieciom» в эталоне нет"),
    # 9524 infiltrieren
    (16714, "example_en", "The agents infiltrate the organization",
     "The agents infiltrated the criminal organization",
     "эталон в прошедшем, и организация преступная"),
    (16714, "example_uk", "Агенти проникли в організацію",
     "Агенти проникли в злочинну організацію",
     "потеряно «kriminelle»"),
    (16714, "example_tr", "Ajanlar örgüte sızıyor",
     "Ajanlar suç örgütüne sızdı",
     "эталон в прошедшем, и организация преступная"),
    # 9526 Zeiger
    (17684, "example_tr", "Saatin akrebi 12ye işaret ediyor",
     "Saatin akrebi 12'ye işaret ediyor",
     "потерян апостроф"),
    # 9528 drastisch — эталон с «ss» вместо «ß»
    (8217, "example_de", "Die Situation erfordert drastische Massnahmen",
     "Die Situation erfordert drastische Maßnahmen",
     "«Massnahmen» это швейцарское написание, в базе немецкое"),
    (8217, "example_pl", "Potrzebne są drastyczne środki",
     "Sytuacja wymaga drastycznych środków",
     "потеряна ситуация"),
    # 9531 Edelmann
    (15256, "example_tr", "Asil büyük toprakları işletiyordu",
     "Asilzade büyük topraklara sahipti",
     "«işletmek» это управлять хозяйством, а «besitzen» — владеть"),
    # 9532 formieren
    (8218, "example_uk", "Військо вишиковується для виступу",
     "Війська вишиковуються для виступу",
     "эталон во множественном числе"),
    (8218, "example_tr", "Askerler ayrılmak için sıralanıyor",
     "Askerler yürüyüşe geçmek için sıralanıyor",
     "«ayrılmak» это расставаться, а «Abmarsch» — выступление"),
    # 9534 Chrom
    (18048, "example_ru", "На автомобиле сверкают хромированные детали",
     "У автомобиля блестящие хромированные детали",
     "эталон не о том, что они сверкают, а что они есть"),
    (18048, "example_uk", "На авто сяють хромовані деталі",
     "Автомобіль має блискучі хромовані деталі",
     "эталон не о том, что они сяють, а что они є"),
    # 9535 umtauschen
    (9908, "example_pl", "Chcę wymienić tę koszulę na większą",
     "Chcę to wymienić",
     "перевод другого предложения"),
    # 9536 ausspucken — эталон в настоящем, переводы в прошедшем
    (12995, "example_en",
     "He spat out the medicine because it tasted so bitter",
     "He spits out the medicine because it tastes so bitter",
     "эталон в настоящем времени"),
    (12995, "example_ru",
     "Он выплюнул лекарство, потому что оно очень горькое",
     "Он выплёвывает лекарство, потому что оно очень горькое",
     "эталон в настоящем времени"),
    (12995, "example_uk",
     "Він виплював ліки, тому що вони мали гіркий смак",
     "Він випльовує ліки, бо вони дуже гіркі",
     "«виплював» — нет такой формы, и время"),
    (12995, "example_tr", "İlaçı tükürdü, çünkü tadı çok acıydı",
     "İlacı tükürüyor, çünkü tadı çok acı",
     "«İlaçı» нарушена согласная, и время"),
    (12995, "example_pl", "Dziecko wypluło lekarstwo, bo było gorzkie",
     "Wypluwa lekarstwo, bo jest bardzo gorzkie",
     "в эталоне не ребёнок, и время"),
    # 9537 ängstigen
    (11337, "translation_uk", "пугати, налякати, боятися",
     "лякати, налякати, боятися",
     "«пугати» — русизм"),
    (11337, "example_uk", "Голосні звуки налякують дитину",
     "Голосні звуки лякають дитину",
     "«налякують» — смешаны виды"),
    # 9538 Möwe
    (15767, "example_pl", "Mewy krążyły nad plażą i szukały jedzenia",
     "Mewa krążyła nad plażą i szukała jedzenia",
     "эталон в единственном числе"),
    # 9539 Anbeginn
    (18885, "example_uk",
     "З самого початку було ясно, що цей проект не вдалась",
     "З самого початку було ясно, що цей проект не вдасться",
     "«не вдалась» — сломанная форма"),
    # 9540 Bootshaus
    (18409, "example_uk",
     "Човневий сарай біля річки старий та покинутий",
     "Човнярня біля річки стара й напівзруйнована",
     "перевод слова — «човнярня», и «baufällig» это не покинутый"),
    (18409, "example_tr",
     "Nehir kenarındaki tekne evi eski ve çökmüş",
     "Nehir kenarındaki kayıkhane eski ve harap olmuş",
     "перевод слова — «kayıkhane»"),
    # 9541 Geldgeber
    (17867, "example_pl", "Film powstał dzięki prywatnemu inwestorowi",
     "Inwestor sfinansował cały projekt z własnej kieszeni",
     "перевод другого предложения"),
    # 9543 hiesig
    (8219, "example_pl", "Tutejsi ludzie są bardzo życzliwi",
     "Tutejsza ludność jest bardzo gościnna",
     "«gastfreundlich» — гостеприимная, а не доброжелательная"),
    # 9544 gnädig
    (15258, "example_tr",
     "Nazik hanım yemeğin hemen sunulmasını talep ediyor",
     "Hanımefendi yemeğin hemen servis edilmesini talep ediyor",
     "перевод слова — «hanımefendi»"),
    (15258, "example_pl", "Jaśnie pani życzy sobie kawy",
     "Jaśnie pani żąda, żeby jedzenie podano natychmiast",
     "перевод другого предложения"),
    # 9546 Pein
    (11339, "example_ru", "Мучение разлуки было трудно выносить",
     "Муку разлуки было трудно выносить",
     "«мучение было трудно выносить» — рассогласование"),
    (11339, "example_uk", "Мука розлуки була важко витримати",
     "Муку розлуки було важко витерпіти",
     "рассогласование падежа"),
    (11339, "example_tr", "Ayrılığın acısı katlanması zor oldu",
     "Ayrılığın acısına katlanmak zordu",
     "«acısı katlanması» — сломанная связка"),
    # 9547 Ampulle
    (12996, "example_pl", "Pielęgniarka otworzyła ampułkę z lekiem",
     "Lekarz otworzył ampułkę z lekiem",
     "в эталоне врач, а не медсестра"),
    # 9548 Regent
    (16715, "example_ru", "Регент правил страной с твёрдой рукой",
     "Регент правил страной твёрдой рукой",
     "«с твёрдой рукой» — калька"),
    (16715, "example_uk", "Регент керував країною з міцною рукою",
     "Регент правив країною твердою рукою",
     "«з міцною рукою» — калька"),
    (16715, "example_tr", "Kral vekili ülkeyi sert bir el ile yönetti",
     "Naip ülkeyi sert bir elle yönetti",
     "«el ile» слитно, и перевод слова — «naip»"),
    # 9549 Safari
    (17327, "example_ru",
     "Сафари через Африку было приключением всей моей жизни",
     "Сафари по Африке было приключением всей моей жизни",
     "«через Африку» — не то управление"),
    (17327, "example_uk",
     "Сафарі через Африку було пригодою усього мого життя",
     "Сафарі по Африці було пригодою всього мого життя",
     "«через Африку» — не то управление"),
    (17327, "example_tr", "Afrikadaki safari hayatımın macerasıydı",
     "Afrika'daki safari hayatımın macerasıydı",
     "потерян апостроф"),
    # 9550 kombinieren
    (8220, "example_pl", "Możesz łączyć te dwa kolory",
     "Możesz dobrze łączyć te kolory",
     "«dwa» в эталоне нет, потеряно «gut»"),
    # 9551 Pfote
    (15768, "example_tr", "Köpek pençesini kaldırıp bana el sallıyor",
     "Köpek pençesini kaldırıp bana pati veriyor",
     "«el sallamak» это махать рукой"),
    (15768, "example_pl", "Pies podał mi łapę",
     "Pies podnosi łapę i podaje mi ją",
     "потеряно «hebt», и время"),
    # 9552 Gottheit
    (14720, "example_tr",
     "İlah birçok insan tarafından saygıyla karşılandı",
     "İlaha birçok insan tapıyordu",
     "«saygıyla karşılanmak» это быть принятым с уважением"),
    (14720, "example_pl", "W tej świątyni czczono dawne bóstwo",
     "Bóstwo było czczone przez wielu ludzi",
     "перевод другого предложения"),
    # 9553 Lunte
    (8221, "example_uk", "Ґніт свічки вже майже згорів",
     "Ґніт горить, і феєрверк зараз почнеться",
     "перевод другого предложения"),
    (8221, "example_tr",
     "Fitil yanıyor ve havai fişekler hemen patlamaya hazır",
     "Fitil yanıyor, havai fişekler şimdi başlayacak",
     "«patlamaya hazır» это готов взорваться, а не взорвётся"),
    (8221, "example_pl", "Zapal lont i szybko się odsuń",
     "Lont się pali i fajerwerki zaraz wystrzelą",
     "перевод другого предложения"),
    # 9554 geplagt
    (11340, "example_uk",
     "Чоловік виглядав мучимим, ніби він страждав під великим тиском",
     "Чоловік виглядав змученим, ніби страждав під великим тиском",
     "«мучимим» — русская форма"),
    (11340, "example_tr",
     "Adam işkence görmüş gibi görünüyordu, "
     "sanki büyük baskı altında acı çekiyordu",
     "Adam bunalmış görünüyordu, "
     "sanki büyük bir baskı altında acı çekiyordu",
     "«işkence görmüş» это подвергнутый пыткам"),
    # 9555 Zwanziger
    (9909, "example_tr", "Cebimde sadece yirmi var",
     "Cebimde sadece bir yirmilik var",
     "потеряно слово ряда: «yirmi» это просто число"),
    # 9556 Menschenfleisch
    (11935, "example_tr", "Romanda insan etinin fikri ele alındı",
     "Romanda insan eti fikri ele alındı",
     "двойной изафет ломает фразу"),
    # 9557 Sprengkopf
    (16716, "example_ru",
     "Боевая головка была опасна и должна была быть обезврежена",
     "Боеголовка была опасна, и её нужно было обезвредить",
     "перевод слова — «боеголовка», и канцелярит"),
    (16716, "example_uk",
     "Бойова частина була небезпечна і повинна була бути знешкоджена",
     "Боєголовка була небезпечна, і її потрібно було знешкодити",
     "«бойова частина» это другое, и канцелярит"),
    # 9558 Wegweiser
    (17328, "example_tr",
     "Yön göstericisi bize istasyona giden doğru yolu gösterdi",
     "Yön tabelası bize istasyona giden doğru yolu gösterdi",
     "перевод слова — «yön tabelası»"),
    # 9559 Polizeiwagen
    (16717, "example_tr",
     "Bir polis arabası sokağın aşağısına doğru hızla gitti",
     "Bir polis arabası caddede hızla ilerledi",
     "«sokağın aşağısına doğru» — калька"),
    (16717, "example_pl", "Radiowóz szybko jechał ulicą w dół",
     "Radiowóz szybko przejechał ulicą",
     "«w dół» — калька"),
    # 9560 nachlassen
    (8222, "example_en", "The rain finally let up this afternoon",
     "His concentration has decreased",
     "перевод другого предложения"),
    (8222, "example_pl", "Deszcz wreszcie zaczął słabnąć",
     "Jego koncentracja osłabła",
     "перевод другого предложения"),
    # 9561 Zielort
    (17329, "example_en", "The destination of our trip is Berlin",
     "Our destination is Berlin",
     "«поездки» в эталоне нет"),
    (17329, "example_ru", "Пункт назначения нашей поездки — Берлин",
     "Наш пункт назначения — Берлин",
     "«поездки» в эталоне нет"),
    (17329, "example_uk", "Пункт призначення нашої подорожі — Берлін",
     "Наш пункт призначення — Берлін",
     "«подорожі» в эталоне нет"),
    (17329, "example_tr", "Seyahatimizin varış noktası Berlindir",
     "Varış noktamız Berlin'dir",
     "потерян апостроф, и «поездки» в эталоне нет"),
    # 9562 Rupie
    (9910, "example_pl", "Zostało mi jeszcze sto rupii",
     "Mam w kieszeni sto rupii",
     "перевод другого предложения"),
    # 9563 Trinkspruch
    (11936, "example_uk", "Він вимовив красивий тост за наречену",
     "Він виголосив гарний тост за наречену",
     "тост виголошують, а не вимовляють"),
    (11936, "example_tr", "Geline güzel bir içki tostu yaptı",
     "Gelin için güzel bir kadeh konuşması yaptı",
     "«içki tostu» — нет такого выражения"),
    # 9564 Namensschild
    (14256, "example_uk", "Мій бейдж сломався",
     "Мій бейдж зламався",
     "«сломався» — русизм"),
    # 9565 Flipper
    (12347, "translation_uk", "пінбол, ігровий автомат із шариком",
     "пінбол, ігровий автомат із кулькою",
     "«шарик» — русизм"),
    (12347, "example_en",
     "There was an old pinball machine in the game room",
     "There is an old pinball machine in the game room",
     "эталон в настоящем времени"),
    (12347, "example_uk", "У ігровій кімнаті стояв старий пінбол",
     "В ігровій кімнаті стоїть старий пінбол",
     "«у» перед гласной, и время"),
    (12347, "example_tr",
     "Oyun odasında eski bir pinball makinesi vardı",
     "Oyun odasında eski bir pinball makinesi var",
     "эталон в настоящем времени"),
    # 9566 Sicherheitskamera
    (17685, "example_ru", "Камеры безопасности в магазине всё снимают",
     "Камеры наблюдения в магазине всё снимают",
     "перевод слова — «камера наблюдения»"),
    (17685, "example_uk", "Камери безпеки в магазині все записують",
     "Камери спостереження в магазині все записують",
     "перевод слова — «камера спостереження»"),
    # 9567 Untersuchungshaft
    (16718, "example_uk",
     "Підозрюваний знаходиться у попередньому ув'язненні",
     "Підозрюваний перебуває у попередньому ув'язненні",
     "«знаходиться» о предметах, о человеке — «перебуває»"),
    (16718, "example_tr", "Şüpheli gözaltıda tutulmuş",
     "Şüpheli tutuklu yargılanıyor",
     "«gözaltı» это задержание в полиции, не следственный арест"),
    # 9568 Scharade
    (12348, "example_en", "We played a charade yesterday",
     "We played charades yesterday",
     "игра называется во множественном"),
    (12348, "example_uk", "Вчора ми грали в шараду",
     "Вчора ми грали в шаради",
     "игра называется во множественном"),
    (12348, "example_tr", "Dün bir şarada oynadık",
     "Dün sessiz sinema oynadık",
     "«şarada» — нет такого слова в турецком"),
    # 9570 Gefangenenlager — эталон сломан, польский был верным
    (16719, "example_de",
     "Das Gefangenenlager war unter miserablen Bedingungen",
     "Im Gefangenenlager herrschten miserable Bedingungen",
     "лагерь не может быть «под условиями»"),
    (16719, "example_en", "The POW camp was in miserable conditions",
     "Conditions in the POW camp were miserable",
     "вслед за эталоном"),
    (16719, "example_ru", "Лагерь военнопленных был в ужасных условиях",
     "В лагере военнопленных были ужасные условия",
     "вслед за эталоном"),
    (16719, "example_uk",
     "Табір для військовополонених був в жахливих умовах",
     "У таборі для військовополонених були жахливі умови",
     "вслед за эталоном"),
    (16719, "example_tr", "Esir kampı korkunç koşullardaydı",
     "Esir kampında koşullar berbattı",
     "вслед за эталоном"),
    # 9572 absaugen
    (12998, "example_tr",
     "Halıyı elektrik süpürgesi ile temizlemem gerekiyor",
     "Halıyı elektrikli süpürgeyle temizlemem gerekiyor",
     "«ile» слитно, и «elektrikli süpürge»"),
    # 9573 hinterhältig
    (11341, "example_tr", "Kurnaz niyetleri vardı",
     "Sinsi niyetleri vardı",
     "«kurnaz» это хитрый, а «hinterhältig» — коварный"),
    (11341, "example_pl",
     "To był podstępny plan, nikt się nie domyślił",
     "Miał podstępne zamiary",
     "перевод другого предложения"),
    # 9574 verbunden
    (8223, "example_pl", "Te dwie firmy są ze sobą związane",
     "Sprzymierzone kraje współpracują",
     "перевод другого предложения"),
    # 9575 Münztelefon
    (14257, "example_en",
     "There's still an old pay phone on the corner",
     "There's still a pay phone at the station",
     "в эталоне вокзал, а не угол"),
    (14257, "example_uk", "На розі ще є старий телефон-автомат",
     "На вокзалі ще стоїть телефон-автомат",
     "в эталоне вокзал, а не угол"),
    # 9577 Autopsiebericht
    (12999, "example_pl",
     "Raport z autopsji wyjaśnił przyczynę śmierci",
     "Raport z autopsji pokazał prawdziwą przyczynę",
     "потеряно «wahre», и «показал» вместо «выяснил»"),
    # 9578 Verbandszeug
    (13000, "example_uk",
     "У аптечці першої допомоги є перев'язувальний матеріал",
     "В аптечці першої допомоги є перев'язувальний матеріал",
     "«у» перед гласной"),
    (13000, "example_pl", "W apteczce mamy opatrunki i plastry",
     "W apteczce pierwszej pomocy są opatrunki",
     "«plastry» в эталоне нет"),
    # 9580 Pulsader
    (13001, "example_tr", "Boyn atardamarları açıkça görülüyor",
     "Boyundaki atardamarlar açıkça görülüyor",
     "«Boyn» — обрубленное слово"),
    # 9582 Chemikalie
    (2328, "example_uk", "Хімічні речовини треба зберігати безпечно",
     "Ця хімічна речовина отруйна",
     "перевод другого предложения"),
    # 9583 Keim
    (13002, "example_pl", "Mydło zabija zarazki na rękach",
     "Zarazek spowodował chorobę",
     "перевод другого предложения"),
    # 9584 Medizinstudium
    (9600, "example_uk",
     "Навчання в медичному закладі займає шість років",
     "Навчання на медичному триває шість років",
     "«займає» — калька, по-украински триває"),
    # 9585 umzingeln
    (16720, "example_uk", "Враги оточили місто",
     "Вороги оточили місто",
     "«враги» — русское слово"),
    # 9586 höllisch
    (10748, "example_tr",
     "Yazın cehennemsel sıcak bana çok ıstırap veriyor",
     "Yazın cehennem gibi sıcak bana çok zor geliyor",
     "«cehennemsel» — нет такого слова"),
    # 9587 sensibler
    (11343, "example_uk",
     "Він чутливий чоловік і приймає багато близько до серця",
     "Він чутлива людина і багато що бере близько до серця",
     "«чоловік» это муж, и «приймає багато» — калька"),
    (11343, "example_tr",
     "O hassas bir insan ve birçok şeyi ciddiye alıyor",
     "O hassas bir insan ve birçok şeyi kalbine takıyor",
     "«ciddiye almak» это принимать серьёзно, а не близко к сердцу"),
    (11343, "example_pl", "Jest bardzo wrażliwy na krytykę",
     "Jest wrażliwym człowiekiem i wiele bierze sobie do serca",
     "перевод другого предложения"),
    # 9588 Nutzung
    (8224, "example_pl",
     "Korzystanie z telefonu na lekcji jest zabronione",
     "Dziś nie sposób wyobrazić sobie życia bez korzystania z internetu",
     "перевод другого предложения"),
    # 9589 Fruchtblase
    (13003, "example_uk",
     "Лікар перевіряє плідний міхур при обстеженні",
     "Лікар перевіряє плодовий міхур при обстеженні",
     "«плідний» это плодородный"),
    (13003, "example_pl",
     "Lekarz sprawdził pęcherz płodowy na badaniu",
     "Lekarz sprawdza pęcherz płodowy podczas badania",
     "эталон в настоящем, и «na badaniu» — калька"),
    # 9591 Berichterstattung
    (14258, "example_en",
     "The media's coverage of the event was very detailed",
     "The coverage of the event was very detailed",
     "«media's» в эталоне нет"),
    (14258, "example_uk",
     "Висвітлення подій у ЗМІ було дуже детальним",
     "Висвітлення події у ЗМІ було дуже детальним",
     "эталон в единственном числе"),
    (14258, "example_tr",
     "Medyanın olayı haberleştirilmesi çok ayrıntılıydı",
     "Olayın basında yer alması çok ayrıntılıydı",
     "«olayı haberleştirilmesi» — сломанная связка"),
    # 9592 Doktorarbeit
    (9601, "example_tr",
     "Doktora tezi üzerinde çalışmaya üç yıldır devam ediyor",
     "Üç yıldır doktora tezi üzerinde çalışıyor",
     "«çalışmaya devam ediyor» — двойное сказуемое"),
    # 9593 sägen
    (9186, "example_en", "My father is sawing wood for the new shelf",
     "We need to saw the branch",
     "перевод другого предложения"),
    (9186, "example_uk", "Мій батько пиляє дерево для нової полиці",
     "Нам потрібно відпилити цю гілку",
     "перевод другого предложения"),
    (9186, "example_tr",
     "Babam yeni raf için ahşabı testereden kesiyor",
     "Dalı testereyle kesmemiz gerekiyor",
     "перевод другого предложения"),
    # 9594 Überlegenheit
    (11344, "example_uk", "Перевага нашої команди була явно видна",
     "Перевагу нашої команди було явно видно",
     "«видна» — не форма в этой конструкции"),
    # 9595 beschmutzen
    (8225, "example_uk", "Не бруди сорочку соусом!",
     "Твоя дитина забруднила стіну фарбою",
     "перевод другого предложения"),
    (8225, "example_tr", "Çocuğun duvarı boya ile kirletti",
     "Çocuğun duvarı boyayla kirletti",
     "«ile» слитно"),
    (8225, "example_pl", "Nie brudź podłogi butami",
     "Twoje dziecko pobrudziło ścianę farbą",
     "перевод другого предложения"),
    # 9596 Nachkomme
    (15259, "example_pl", "Jest potomkiem starego rodu",
     "Potomek tej rodziny mieszka dziś jeszcze w Niemczech",
     "перевод другого предложения"),
    # 9597 entzwei
    (8226, "example_ru", "Стакан разбился вдребезги",
     "Стакан разбился надвое",
     "«entzwei» это надвое, не вдребезги"),
    (8226, "example_uk", "Розріж яблуко навпіл",
     "Склянка розбилася надвоє",
     "перевод другого предложения"),
    (8226, "example_pl", "Patyk złamał się na dwoje",
     "Szklanka pękła na dwoje",
     "перевод другого предложения"),
    # 9601 schlürfen
    (11938, "example_uk", "Він гучно ковтає суп",
     "Він гучно сьорбає суп",
     "«ковтає» это глотает"),
    (11938, "example_tr", "Çorbasını gürültülü bir şekilde içiyor",
     "Çorbasını höpürdeterek içiyor",
     "перевод слова — «höpürdetmek»"),
    # 9602 Übeltäter
    (16721, "example_ru", "Полиция поймала преступника",
     "Полиция поймала злоумышленника",
     "перевод слова — «злоумышленник»"),
    # 9603 Gestein
    (15769, "example_pl", "Skała w tych górach jest bardzo twarda",
     "Skała na górze jest bardzo twarda",
     "в эталоне «am Berg», а не «в этих горах»"),
    # 9604 unvermeidbar
    (8228, "example_pl", "Taki koniec był nieunikniony",
     "Kolaps był nieunikniony",
     "перевод другого предложения"),
    # 9605 leiblich
    (15260, "example_tr", "Biyolojik babam Berlinde yaşıyor",
     "Öz babam Berlin'de yaşıyor",
     "потерян апостроф, и перевод слова — «öz»"),
    # 9606 Erforschung
    (18051, "example_uk", "Дослідження космосу дороговартісне",
     "Дослідження космосу дороге",
     "«дороговартісне» — канцелярит"),
    # 9607 Kiosk
    (9911, "example_en", "I buy a newspaper at the kiosk",
     "I always buy a newspaper at the kiosk",
     "потеряно «immer»"),
    (9911, "example_uk", "В кіоське я купую газету",
     "У кіоску я завжди беру собі газету",
     "«кіоське» — русская форма, и потеряно «immer»"),
    (9911, "example_tr", "Kioskta gazete alıyorum",
     "Büfeden her zaman gazete alıyorum",
     "«Kiosk» не турецкое слово, и потеряно «immer»"),
    (9911, "example_pl", "Kupiłem gazetę w kiosku na rogu",
     "W kiosku zawsze kupuję sobie gazetę",
     "перевод другого предложения"),
    # 9608 herumführen
    (17330, "example_en", "The guide leads tourists around the city",
     "I can show you around the house",
     "перевод другого предложения"),
    (17330, "example_ru", "Гид водит туристов вокруг города",
     "Я могу провести тебя по дому",
     "перевод другого предложения"),
    (17330, "example_uk", "Гід водить туристів навколо міста",
     "Я можу провести тебе по будинку",
     "перевод другого предложения"),
    (17330, "example_tr", "Rehber turistleri şehirde gezdirdi",
     "Seni evde gezdirebilirim",
     "перевод другого предложения"),
    # 9609 Schulabschluss
    (9602, "example_uk", "Я закінчив школу два роки тому",
     "Моє закінчення школи було два роки тому",
     "перевод другого предложения"),
    # 9610 Kunststück
    (14721, "example_uk", "Цей трюк мене справді здивував",
     "Це був справжній трюк — зуміти таке зробити",
     "перевод другого предложения"),
    (14721, "example_tr", "Bunu başarmak gerçekten bir başarıydı",
     "Bunu başarmak gerçek bir hünerdi",
     "«başarmak … başarı» — тавтология"),
    (14721, "example_pl", "Pokazał nam nową sztuczkę z kartami",
     "To był prawdziwy wyczyn, żeby tego dokonać",
     "перевод другого предложения"),
    # 9611 Uhrwerk
    (17686, "example_uk",
     "Годинниковий механізм цих старих годинників вражає",
     "Годинниковий механізм цього старого годинника вражає",
     "эталон в единственном числе"),
    # 9612 konservativ
    (16722, "example_tr", "Dedemin çok muhafazakâr görüşleri var",
     "Dedemin muhafazakâr görüşleri var",
     "«çok» в эталоне нет"),
    # 9616 Verführung
    (11345, "example_uk", "Спокуса солодощами велика для дітей",
     "Спокуса солодощами в дітей велика",
     "порядок слов ломает смысл"),
    (11345, "example_tr",
     "Çocuklar için tatlıların ayartması büyüktür",
     "Çocuklar için tatlıların cazibesi büyüktür",
     "«ayartma» о соблазнении человека"),
    (11345, "example_pl", "Ciastka to dla mnie wielka pokusa",
     "Pokusa słodyczy jest u dzieci duża",
     "перевод другого предложения"),
    # 9617 Blutzucker
    (13006, "example_uk",
     "Цукор крові в діабетиків часто занадто високий",
     "Цукор у крові в діабетиків часто занадто високий",
     "потерян предлог"),
    (13006, "example_pl", "Muszę codziennie mierzyć cukier we krwi",
     "Cukier we krwi u diabetyków jest często za wysoki",
     "перевод другого предложения"),
    # 9618 Pflegefamilie
    (15261, "example_tr", "Çocuk bir koruma ailesine yerleştirildi",
     "Çocuk bir koruyucu aileye yerleştirildi",
     "«koruma ailesi» — не термин"),
    # 9620 Tagung
    (9187, "example_tr",
     "Uluslararası konferans gelecek hafta Berlinde yapılacak",
     "Uluslararası konferans gelecek hafta Berlin'de yapılacak",
     "потерян апостроф"),
    # 9621 würdevoll
    (11346, "example_pl",
     "Zachował się bardzo godnie w tej sytuacji",
     "Wyszedł z sali w sposób pełen godności, nie narzekając",
     "перевод другого предложения"),
    # 9623 Arsen
    (18052, "example_tr",
     "Arsenik zehirli bir elementdir ve daha önce pestisitlerde "
     "kullanılıyordu",
     "Arsenik zehirli bir elementtir ve daha önce pestisitlerde "
     "kullanılıyordu",
     "«elementdir» — нарушена гармония согласных"),
    # 9624 Körperteil
    (529, "example_tr", "Diz bir vücut parçasıdır",
     "Diz bir vücut bölümüdür",
     "перевод слова — «vücut bölümü»"),
    # 9625 Inferno
    (8230, "example_pl", "Ten pożar to było prawdziwe piekło",
     "Bitwa była prawdziwym piekłem z tysiącami rannych",
     "перевод другого предложения"),
    # 9626 halbe-halbe
    (8231, "example_uk",
     "Ми витрати ділимо навпіл, кожен платить половину",
     "Ми ділимо витрати навпіл, кожен платить половину",
     "порядок слов"),
    (8231, "example_pl", "Zapłacimy za to po połowie",
     "Dzielimy koszty po połowie, każdy płaci połowę",
     "перевод другого предложения"),
    # 9627 Bürokrat
    (16723, "example_tr",
     "Belediye dairelerindeki bürokratlar bazen yavaş işlem görüyor",
     "Belediyedeki bürokratlar bazen işlemleri yavaş yapıyor",
     "«işlem görmek» это проходить обработку, а не обрабатывать"),
    # 9628 dekorieren
    (18412, "example_tr",
     "Partisi için odayı balonlar ve çelenklerle süslüyoruz",
     "Parti için odayı balonlarla ve çelenklerle süslüyoruz",
     "«Partisi» — лишнее притяжание"),
    # 9629 schlaff
    (8232, "example_uk",
     "Його поза була млявою, як ніби у нього більше нема енергії",
     "Його поза була млявою, наче в нього вже не було сил",
     "«як ніби» и «нема» — разговорные обрывки"),
    (8232, "example_pl", "Od braku ruchu ma zwiotczałe mięśnie",
     "Jego postawa była wiotka, jakby nie miał już siły",
     "перевод другого предложения"),
    # 9630 exotisch
    (2444, "example_tr",
     "Restoranda egzotik yemek, mutfakta bir sürprizdi",
     "Restorandaki egzotik yemek gerçek bir damak sürpriziydi",
     "«mutfakta sürpriz» это сюрприз на кухне"),
    # 9631 knirschen
    (8234, "example_uk",
     "Він скреготить зубами вночі, коли він у стресі",
     "Він скрегоче зубами вночі, коли нервує",
     "«скреготить» — не форма, и «він» дважды"),
    (8234, "example_pl", "Śnieg chrzęści pod butami",
     "Zgrzyta zębami w nocy, kiedy jest zestresowany",
     "перевод другого предложения"),
    # 9632 tätowieren
    (8235, "example_en", "He wanted to get a dragon tattoo",
     "I want to get a dragon tattoo",
     "эталон о «я» и в настоящем"),
    (8235, "example_uk", "Він хотів собі набити татуювання дракона",
     "Я хочу набити собі татуювання дракона",
     "эталон о «я» и в настоящем"),
    (8235, "example_tr", "Kendine ejderha dövme yaptırmak istedi",
     "Kendime ejderha dövmesi yaptırmak istiyorum",
     "эталон о «я», и потерян изафет"),
    (8235, "example_pl", "Chcę sobie wytatuować smoka na ramieniu",
     "Chcę sobie wytatuować smoka",
     "«na ramieniu» в эталоне нет"),
    # 9634 Alge
    (15770, "example_uk",
     "В озері ростуть водорості, які забарвлюють воду в зелене",
     "В озері ростуть водорості, які забарвлюють воду в зелений колір",
     "«в зелене» — обрывок"),
    # 9635 Wortspiel
    (14259, "example_uk", "Гра слів була дотепною, все сміялися",
     "Гра слів була дотепною, всі сміялися",
     "«все» вместо «всі»"),
    (14259, "example_tr", "Sözcük oyunu komik oldu, herkes güldü",
     "Sözcük oyunu komikti, herkes güldü",
     "«komik oldu» это стало смешным"),
    # 9637 Gaskammer
    (16724, "example_en",
     "The gas chamber remains a haunting symbol of historical atrocity",
     "The gas chamber was one of the darkest chapters of human history",
     "перевод другого предложения"),
    (16724, "example_ru",
     "Газовая камера была одной из самых страшных машин геноцида",
     "Газовая камера была одной из самых тёмных глав истории человечества",
     "перевод другого предложения"),
    (16724, "example_uk",
     "Газова камера залишилась символом жахіття Голокосту",
     "Газова камера була однією з найтемніших сторінок історії людства",
     "перевод другого предложения"),
    (16724, "example_tr",
     "Gaz odası tarihin en karanlık bölümlerinden biriydi",
     "Gaz odası insanlık tarihinin en karanlık bölümlerinden biriydi",
     "потеряно «Menschheits-»"),
    # 9639 Nahkampf
    (12350, "example_uk", "Боєць був досвідчений у рукопашному бою",
     "Солдат був досвідчений у рукопашному бою",
     "в эталоне «Soldat»"),
    (12350, "example_tr", "Asker yakın dövüşte deneyimli idi",
     "Asker yakın dövüşte deneyimliydi",
     "«idi» отдельно"),
    # 9644 bedrängen
    (11347, "example_uk", "Школярі постійно його докучають",
     "Школярі постійно йому докучають",
     "«докучати» требует датива"),
    (11347, "example_pl", "Dzieciaki ciągle go nękają na podwórku",
     "Dzieciaki ciągle go nękają",
     "«na podwórku» в эталоне нет"),
    # 9645 Erlass
    (16726, "example_uk", "Указ мера змінив правила парковки",
     "Указ мера змінив правило",
     "«правила парковки» в эталоне нет"),
    (16726, "example_tr", "Başkanın fermanı kuralı değiştirdi",
     "Belediye başkanının kararnamesi kuralı değiştirdi",
     "«Başkan» это президент, а в эталоне мэр"),
    # 9646 heizen
    (18414, "example_ru", "Мы отапливаем дом газом",
     "Мы отапливаем газом",
     "«дом» в эталоне нет"),
    (18414, "example_tr", "Gazla ısınıyoruz",
     "Gazla ısıtıyoruz",
     "«ısınmak» это самому согреваться"),
    # 9647 verdammen
    (11348, "example_uk", "Усі засуджують його вчинок",
     "Суд його засудить",
     "перевод другого предложения"),
    (11348, "example_pl", "Wszyscy potępiają takie zachowanie",
     "Sąd go skaże",
     "перевод другого предложения"),
    # 9648 Kinderheim
    (15263, "example_en", "The child is growing up in a childrens home",
     "The child is growing up in a children's home",
     "потерян апостроф"),
    (15263, "example_pl", "Wychował się w domu dziecka",
     "Dziecko wychowuje się w domu dziecka",
     "эталон в настоящем, и подлежащее — ребёнок"),
    # 9649 Gründung
    (17868, "example_ru", "Основание компании произошло в 1995 году",
     "Компания была основана в 1995 году",
     "«основание произошло» — канцелярит"),
    (17868, "example_uk", "Заснування компанії було в 1995 році",
     "Компанію заснували в 1995 році",
     "«заснування було» — канцелярит"),
    (17868, "example_tr", "Şirketin kurulması 1995 yılında oldu",
     "Şirket 1995 yılında kuruldu",
     "«kurulması oldu» — двойная пассивность"),
    (17868, "example_pl", "Od założenia firmy minęło dziesięć lat",
     "Firma została założona w 1995 roku",
     "перевод другого предложения"),
    # 9650 Zauberkraft
    (14722, "example_uk",
     "Магічна сила старого чарівника була легендарною",
     "Магічна сила чарівника була легендарною",
     "«старого» в эталоне нет"),
    (14722, "example_tr", "Yaşlı büyücünün sihirli gücü efsanevi idi",
     "Büyücünün sihirli gücü efsaneviydi",
     "«Yaşlı» в эталоне нет, и «idi» отдельно"),
    (14722, "example_pl", "Ten pierścień ma podobno magiczną moc",
     "Magiczna moc czarodzieja była legendarna",
     "перевод другого предложения"),
    # 9651 runterziehen — в эталоне потеряно «zu»
    (8237, "example_de", "Hör auf, mich runterziehen",
     "Hör auf, mich runterzuziehen",
     "после «aufhören» нужен инфинитив с «zu»"),
    (8237, "example_pl", "Ściągnij rolety w dół, słońce razi",
     "Przestań mnie przygnębiać",
     "перевод другого предложения"),
    # 9652 abspringen
    (12351, "example_uk", "Він зістрибнув з поїзда на ходу",
     "Парашутист зістрибує з літака",
     "перевод другого предложения"),
    # 9653 Codewort
    (14260, "example_pl", "Podaj hasło, bo cię nie wpuszczą",
     "Hasło jest zmieniane codziennie",
     "перевод другого предложения"),
    # 9655 unterbesetzt
    (9190, "translation_ru",
     "без хватки людей, недоукомплектованный, с нехваткой персонала",
     "недоукомплектованный, с нехваткой персонала",
     "«без хватки людей» — обрывок фразы"),
    (9190, "example_uk",
     "Офіс працює з недокомплектованим персоналом",
     "Офіс недоукомплектований",
     "«недокомплектований персонал» — канцелярит"),
    (9190, "example_tr", "Ofis yetersiz kadro ile çalışıyor",
     "Ofis yetersiz kadroyla çalışıyor",
     "«ile» слитно"),
    # 9656 Nebenzimmer
    (18415, "example_uk", "Пійдемо в сусідню кімнату",
     "Підемо в сусідню кімнату",
     "«Пійдемо» — опечатка"),
    # 9657 Dienstaufsicht
    (9191, "example_en", "The service supervision takes control",
     "The official supervision takes control",
     "«service supervision» — калька"),
    # 9659 Väterchen
    (15264, "example_uk", "Татусю, почитай мені казку!",
     "Його батечко раніше працював на фабриці",
     "перевод другого предложения"),
    (15264, "example_tr",
     "Onun babası eskiden fabrikada çalışmıştı",
     "Onun babacığı eskiden fabrikada çalışmıştı",
     "потерян уменьшительный оттенок слова ряда"),
    (15264, "example_pl", "Mój tatuś pracował kiedyś w fabryce",
     "Jego ojczulek pracował kiedyś w fabryce",
     "в эталоне «sein», а не «мой»"),
    # 9660 Erzengel
    (14723, "example_pl", "Na obrazie widać archanioła Michała",
     "Archanioł Michał jest ważną postacią w wielu religiach",
     "перевод другого предложения"),
    # 9661 Garnele
    (11939, "example_tr", "Karidesleri bugün özellikle leziz",
     "Karidesler bugün özellikle lezzetli",
     "лишний аккузатив при именном сказуемом"),
    # 9662 weiterkommen
    (8238, "example_uk", "Робота просувається дуже повільно",
     "Якщо ти не будеш учитися, ти не просунешся в житті",
     "перевод другого предложения"),
    (8238, "example_pl",
     "Bez znajomości języka nie posuniesz się dalej",
     "Jeśli nie będziesz się uczył, nie posuniesz się w życiu dalej",
     "перевод другого предложения"),
    # 9663 Spirale
    (8239, "example_uk", "Спіраль ДНК вражаюча",
     "Спіраль ДНК вражає",
     "«вражаюча» — калька активного дієприкметника"),
    (8239, "example_tr", "DNAnın sarmalı etkileyici",
     "DNA'nın sarmalı etkileyici",
     "потерян апостроф"),
    (8239, "example_pl", "Schody kręcą się w spiralę",
     "Spirala DNA jest imponująca",
     "перевод другого предложения"),
    # 9664 Inventar
    (9912, "example_uk", "Інвентар ресторану згорів при пожежі",
     "Інвентар ресторану був знищений після пожежі",
     "в эталоне «nach dem Brand zerstört»"),
    (9912, "example_pl", "Cały inwentarz sklepu spłonął w pożarze",
     "Inwentarz restauracji został zniszczony po pożarze",
     "в эталоне ресторан, а не магазин"),
    # 9665 rau
    (8240, "example_uk", "У нього хриплий голос після простуди",
     "Мені не сподобався хрипкий голос старого чоловіка",
     "перевод другого предложения"),
    (8240, "example_tr", "Yaşlı adamın kaba sesinden hoşlanmadım",
     "Yaşlı adamın boğuk sesinden hoşlanmadım",
     "«kaba ses» это грубый тон, а не хриплый голос"),
    (8240, "example_pl", "Jego dłonie są szorstkie od pracy",
     "Nie podobał mi się szorstki głos starego mężczyzny",
     "перевод другого предложения"),
    # 9666 Zwangsjacke
    (13007, "translation_uk", "гамівна сорочка, смиряльна сорочка",
     "гамівна сорочка, сорочка для буйних",
     "«смиряльна» — нет такого слова"),
    (13007, "example_uk",
     "Його довелося утримувати в смирювальній сорочці",
     "Його довелося утримувати в гамівній сорочці",
     "«смирювальна» — нет такого слова"),
    (13007, "translation_tr", "deli gömleği, zorlama gömleği",
     "deli gömleği, tımarhane gömleği",
     "«zorlama gömleği» — нет такого выражения"),
    (13007, "example_tr", "Onu dar bir cekette tutmak zorunda kalındı",
     "Onu deli gömleğiyle tutmak zorunda kaldılar",
     "«dar ceket» это узкий пиджак"),
    # 9669 Magistrat
    (16728, "example_tr",
     "Belediye yönetimi şehir için yeni kurallar kararlaştırdı",
     "Belediye yönetimi şehir için yeni kuralları kararlaştırdı",
     "потерян аккузатив"),
    # 9670 Entzündung
    (13008, "example_uk", "Запалення нарешті зажило",
     "Запалення нарешті минуло",
     "«зажило» о ране, не о воспалении"),
    (13008, "example_tr", "İltihaplanma sonunda iyileşti",
     "İltihap sonunda iyileşti",
     "перевод слова — «iltihap»"),
    (13008, "example_pl", "Lekarz stwierdził zapalenie gardła",
     "Zapalenie w końcu się wygoiło",
     "перевод другого предложения"),
    # 9671 Seher
    (14724, "example_tr", "Falcı gelecek değişeceğini söyledi",
     "Kâhin geleceğin değişeceğini söyledi",
     "потерян родительный, и перевод слова — «kâhin»"),
    (14724, "example_pl", "Jasnowidz przepowiedział jej przyszłość",
     "Jasnowidz powiedział, że przyszłość się zmieni",
     "перевод другого предложения"),
    # 9672 Egoist
    (11350, "example_tr", "O gerçek bencil biri",
     "O gerçek bir egoist",
     "фраза без артикля не держится"),
    (11350, "example_pl", "Nie bądź takim egoistą",
     "Jest prawdziwym egoistą",
     "перевод другого предложения"),
    # 9673 gegenübertreten — в эталоне лишнее «mich»
    (8241, "example_de", "Ich muss mich meinen Ängsten gegenübertreten",
     "Ich muss meinen Ängsten gegenübertreten",
     "«gegenübertreten» не возвратный"),
    (8241, "example_tr", "Bu teklife karşı koyamadım",
     "Korkularımla yüzleşmem gerekiyor",
     "перевод другого предложения"),
    # 9676 trödeln
    (18888, "example_uk", "Припини мешкати, нам потрібно йти",
     "Припини баритися, нам потрібно йти",
     "«мешкати» по-украински значит жить"),
    # 9677 kampflos
    (12352, "example_tr", "Savaş olmadan teslim oldu",
     "Savaşmadan teslim oldu",
     "«savaş olmadan» это без войны, а не без боя"),
    # 9678 Korps
    (16729, "example_tr", "Kolordu beş bin askerden oluşuyor",
     "Kolordu yaklaşık beş bin askerden oluşuyordu",
     "потеряно «etwa», и время"),
    # 9679 anlocken
    (8242, "example_uk", "Запах має привертати покупців до магазину",
     "Запах має заманювати покупців до магазину",
     "«привертати» требует «увагу»"),
    (8242, "example_pl",
     "Zapach ciasta przywabił wszystkich do kuchni",
     "Zapach ma przywabić klientów do sklepu",
     "перевод другого предложения"),
    # 9680 wegschmeißen
    (3005, "example_tr", "Bunu çöpe atıyorum",
     "Eski gazeteyi çöpe atıyorum",
     "потеряна газета"),
    # 9681 gründlich
    (6842, "example_pl",
     "Zrobił dokładne rozeznanie do swojego projektu",
     "Przeprowadził dokładne badania do swojego projektu",
     "«rozeznanie» не о исследовании"),
    # 9682 Schott
    (17331, "translation_uk", "перебірка, водонепроникна перегородка",
     "переборка, водонепроникна перегородка",
     "корабельный термин — «переборка»"),
    (17331, "example_tr", "Geminin su geçirmez bölmesi kapatıldı",
     "Gemiyi korumak için bölmenin kapatılması gerekiyor",
     "потеряна цель, и время"),
    # 9683 Zusammensetzung
    (18053, "example_tr", "Takımın bileşimi çok dengeli idi",
     "Takımın bileşimi çok dengeliydi",
     "«idi» отдельно"),
    # 9684 mähen
    (18890, "example_ru", "Сосед косит траву каждую субботу",
     "По субботам я кошу свой газон",
     "перевод другого предложения"),
    (18890, "example_uk", "Сусід косить траву перед домом",
     "По суботах я кошу свій газон",
     "перевод другого предложения"),
    # 9685 Aal
    (15772, "example_tr", "Yılan balığı ilginç bir balık",
     "Yılan balığı ilginç bir balıktır",
     "фраза без связки"),
    (15772, "example_pl", "Na targu kupiłem wędzonego węgorza",
     "Węgorz to ciekawa ryba",
     "перевод другого предложения"),
    # 9686 Leim
    (8244, "example_en", "I glued the broken glass together",
     "I glued the broken glass back together with glue",
     "слова ряда в примере не было"),
    (8244, "example_tr", "Kırık camı tutkal ile yapıştırdım",
     "Kırık camı tutkalla yapıştırdım",
     "«ile» слитно"),
    (8244, "example_pl", "Przyklej to mocnym klejem",
     "Przykleiłem rozbitą szybę klejem",
     "перевод другого предложения"),
    # 9687 unbeliebt
    (11352, "example_tr", "Bu önlem çok popüler değil",
     "Bu önlem hiç sevilmiyor",
     "перевод слова — «sevilmeyen»"),
    (11352, "example_pl", "Ta decyzja jest bardzo niepopularna",
     "To działanie jest bardzo niepopularne",
     "«Maßnahme» это мера, а не решение"),
    # 9688 zuwider
    (11353, "example_uk", "Цей запах просто огидний",
     "Це мені огидно",
     "перевод другого предложения"),
    (11353, "example_tr", "Bu bana karşı",
     "Bu bana iğrenç geliyor",
     "«bana karşı» это против меня"),
    # 9689 Dickschädel
    (11354, "example_uk",
     "Він справжній впертун, не слухає нікого",
     "Він справжній впертюх, який нікого не слухає",
     "перевод слова — «впертюх»"),
    (11354, "example_tr", "O, dinlemeyen gerçek bir inatçı",
     "O, hiç dinlemeyen gerçek bir inatçı",
     "потеряно «nicht»"),
    # 9691 Entsetzen
    (11355, "example_uk",
     "Його жах був великий, коли він почув новину",
     "Його охопив жах, коли він почув цю новину",
     "«жах був великий» — калька"),
    (11355, "example_pl", "Z przerażeniem patrzyła na wypadek",
     "Jego przerażenie było wielkie, gdy usłyszał tę wiadomość",
     "перевод другого предложения"),
    # 9692 straff
    (8245, "example_uk", "Мотузка натягнута",
     "Мотузка туго натягнута",
     "потеряно «straff»"),
    (8245, "example_tr", "İp gergindir",
     "İp gergin bir şekilde gerilmiş",
     "потеряно «gespannt»"),
    # 9693 mild
    (8246, "example_ru", "Сегодня погода мягкая и тёплая",
     "Сегодня погода мягкая",
     "«и тёплая» в эталоне нет"),
    (8246, "example_uk", "Сьогодні тепла погода",
     "Сьогодні погода м'яка",
     "«mild» это м'яка, а не тепла"),
    (8246, "example_pl", "Ta zima była bardzo łagodna",
     "Pogoda jest dziś łagodna",
     "перевод другого предложения"),
    # 9694 eintreffen — приставка в эталоне не отделена
    (8247, "example_de", "Der Zug eintraf pünktlich am Bahnhof",
     "Der Zug traf pünktlich am Bahnhof ein",
     "у отделяемой приставки личная форма рвётся: «traf … ein»"),
    # 9695 mitsamt
    (8248, "example_uk", "Разом з його сім'єю він уїхав",
     "Разом зі своєю сім'єю він виїхав",
     "«уїхав» — русизм, и «його» вместо «своєю»"),
    # 9696 Betonung
    (14261, "example_en", "The emphasis is on the first syllable",
     "The emphasis is on the first word",
     "в эталоне «Wort», а не слог"),
    (14261, "example_uk", "Наголос падає на перший склад",
     "Наголос падає на перше слово",
     "в эталоне «Wort», а не склад"),
    (14261, "example_tr", "Vurgu ilk heceye düşüyor",
     "Vurgu ilk kelimeye düşüyor",
     "в эталоне «Wort», а не слог"),
    (14261, "example_pl",
     "W tym słowie akcent pada na drugą sylabę",
     "Akcent pada na pierwsze słowo",
     "перевод другого предложения"),
    # 9697 freihalten
    (8249, "example_uk",
     "Можеш звільнити для мене наступну п'ятницю?",
     "Можеш залишити для мене вільною наступну п'ятницю?",
     "«звільнити» это освободить от чего-то"),
    (8249, "example_tr",
     "Gelecek haftanın cuma günü benim için boş bırakabilir misin?",
     "Gelecek hafta cuma gününü benim için boş bırakabilir misin?",
     "потерян аккузатив, фраза рассыпается"),
    # 9698 Handgranate
    (16730, "example_ru", "Боец бросил ручную гранату в бункер",
     "Солдат бросил ручную гранату в бункер",
     "в эталоне «Soldat»"),
    # 9699 Trojaner
    (17689, "example_ru",
     "Троянский конь заразил мой компьютер и украл все мои данные",
     "Троян заразил мой компьютер и украл все мои данные",
     "перевод слова — «троян»"),
    # 9700 jonglieren
    (12353, "example_uk", "Клоун жонглює трьома м'ячами",
     "Цирковий артист жонглює п'ятьма м'ячами",
     "перевод другого предложения"),
    (12353, "example_tr",
     "Sirk sanatçısı beş topu hokkabazlık yapıyor",
     "Sirk sanatçısı beş topla hokkabazlık yapıyor",
     "«topu» вместо «topla» ломает фразу"),
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
