"""
Сплошная вычитка, блок 35: ряды 5301–5500 по рангу частотности
(id первого 7413, id последнего 10755).

Главное за блок:

* `Aufklärung` — турецкий пример про слабое освещение в комнате
  (`Odanın aydınlatması çok zayıf`). Слово действительно значит и
  «освещение», но в немецком примере оно про разъяснение темы.
* `zärtlich` — турецкий пример про тонкую ткань свитера, к нежности
  отношения не имеющий.
* `Korridor`, `Bann`, `Schweinerei`, `trocknen`, `Einfahrt`, `Mehl` —
  то же: половина языков переводит чужую фразу.
* `Meine Pyjama sind sehr bequem` — в немецком эталоне `Pyjama`
  мужского рода и единственного числа: `Mein Pyjama ist`.
* `leg of a angle` в английских значениях к `Schenkel` — «a» перед
  гласной.
* Украинские русизмы: `Жужжання`, `Петух`, `неслиханно`, `поступаю`,
  `трусцою`.
* Турецкие небывальщины: `Portyer`, `Kasapçıya`, `sonsuzydu`,
  `stoğumuz`, `kurde`, `kararsız` на месте `dengesiz`.

    python -m app.scripts.fix_block_0035            # показать
    python -m app.scripts.fix_block_0035 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- немецкий эталон -----------------------------------------------------
    (13691, "example_de", "Meine Pyjama sind sehr bequem zum Schlafen",
     "Mein Pyjama ist sehr bequem zum Schlafen",
     "«Pyjama» мужского рода и единственного числа"),
    (7426, "example_de", "Sieh oben auf Seite 5 für mehr Details",
     "Siehe oben auf Seite 5 für mehr Details",
     "слово ряда «siehe», а в примере «Sieh»"),

    # --- английские значения -------------------------------------------------
    (12706, "translation_en", "thigh, leg of a angle, side",
     "thigh, leg of an angle, side", "«a» перед гласной"),

    # --- Aufklärung, zärtlich: перевод про совсем другое ---------------------
    (9514, "example_en", "I need some clarification on this point",
     "We need more clarification on this topic",
     "немецкий «Wir brauchen mehr Aufklärung über dieses Thema»"),
    (9514, "example_uk", "Нам бракує інформування про зміни",
     "Нам потрібно більше роз'яснень щодо цієї теми", "то же"),
    (9514, "example_tr", "Odanın aydınlatması çok zayıf",
     "Bu konuda daha fazla bilgilendirmeye ihtiyacımız var",
     "«aydınlatma» тут про освещение комнаты"),
    (10733, "example_tr", "Bu kazağın kumaşı çok ince",
     "Onu şefkatle sardı ve kulağına fısıldadı",
     "немецкий «Sie umarmte ihn zärtlich»"),

    # --- Korridor, Bann, Schweinerei, trocknen, Einfahrt ---------------------
    (18262, "example_en", "The corridor leads to the classroom",
     "The corridor is long and dark",
     "немецкий «Der Korridor ist lang und dunkel»"),
    (18262, "example_uk", "Коридор веде до класу",
     "Коридор довгий і темний", "то же"),
    (18262, "example_tr", "Koridor sınıfa gidiyor",
     "Koridor uzun ve karanlık", "то же"),
    (14542, "example_en", "The book was banned",
     "The book is on the index, it was put under a ban",
     "немецкий «Das Buch steht auf dem Index, es wurde in den Bann getan»"),
    (14542, "example_uk", "Книгу поставили під заборону",
     "Книга в індексі, на неї наклали заборону", "то же"),
    (14542, "example_tr", "Kitabı yasaklamak",
     "Kitap yasaklılar listesinde, aforoz edildi",
     "то же, и инфинитив вместо фразы"),
    (10744, "example_en", "The room is a complete mess", "What a mess!",
     "немецкий «Was für eine Schweinerei!»"),
    (10744, "example_uk", "Кімната — повне свинство", "Ну й свинство!",
     "то же"),
    (10744, "example_tr", "Oda tamamen dağınık", "Ne pislik!", "то же"),
    (18263, "example_en", "My throat feels really dry",
     "The laundry dries in the sun",
     "немецкий «Die Wäsche trocknet in der Sonne»"),
    (18263, "example_uk", "Я сушу волосся феном",
     "Білизна сохне на сонці", "то же"),
    (1353, "example_en", "His car is in the driveway",
     "Entry is forbidden", "немецкий «Die Einfahrt ist verboten»"),

    # --- украинские русизмы и опечатки ---------------------------------------
    (7435, "example_uk", "Жужжання двигуна було гучним",
     "Дзижчання двигуна було гучним", "«Жужжання» — русское слово"),
    (15576, "example_uk", "Петух кричить щоранку",
     "Півень кукурікає щоранку", "«Петух» — русское слово"),
    (10730, "example_uk", "Це неслиханно, говорити таке",
     "Це просто нечувано — говорити таке", "«неслиханно» — русизм"),
    (13543, "example_uk", "Я поступаю всупереч власній волі",
     "Я дію всупереч власній волі", "«поступаю» — русизм"),
    (12216, "example_uk",
     "Я бігаю трусцою кожного ранку половину години",
     "Я бігаю підтюпцем кожного ранку півгодини",
     "«трусцою» — русизм, и «половину години»"),
    (14546, "example_uk", "Виставу в театрі була дійсно вражаючою",
     "Вистава в театрі була дійсно вражаючою", "падеж подлежащего"),
    (12706, "example_uk",
     "Стегно — це частина тіла між стегном і коліном",
     "Стегно — це частина тіла між кульшовим суглобом і коліном",
     "«між стегном» — слово объясняется через себя"),
    (10721, "example_uk", "Вона була жахнута від новини",
     "Вона була нажахана цією новиною", "«жахнута» — не форма"),
    (7416, "example_uk",
     "Спека була неможливою, я чуть не впав у непритомність",
     "Спека була немислимою, я майже знепритомнів",
     "«неможливою» не то, и «чуть» — русизм"),
    (12702, "example_uk", "Він відчуває себе депресивним",
     "Він почувається пригніченим", "«відчуває себе» — калька"),
    (10729, "example_uk", "Я доволі розхвилюваний",
     "Я доволі схвильований", "«розхвилюваний» — не форма"),
    (11780, "example_uk", "Озеро було повністю замерзле",
     "Озеро було повністю замерзлим", "падеж"),
    (8962, "example_uk", "Директор школи дуже сувора",
     "Директорка школи дуже сувора", "род не согласован"),
    (12705, "example_uk", "Бажаю вам швидкого одужання",
     "Бажаю тобі швидкого одужання", "в немецком обращение на «ты»"),
    (12704, "example_uk", "Я беру знеболювальне від головного болю",
     "Я приймаю знеболювальне від головного болю", "«беру» — не то слово"),
    (10739, "example_uk", "Вона дуже люб'язна і мила",
     "Вона дуже люб'язна людина",
     "немецкий «eine liebenswürdige Person»"),
    (1181, "example_uk", "Концерт скасовується через дощ",
     "Заняття сьогодні скасовуються",
     "немецкий «Der Unterricht fällt heute aus»"),
    (8956, "example_uk", "Я гострю ніж перед вечерею",
     "Мені потрібно заточити ніж, він затупився",
     "немецкий «Ich muss mein Messer schleifen, es ist stumpf geworden»"),
    (9825, "example_uk", "Вона носила красиве намисто з перлин",
     "Вона носила красиву перлину як намисто",
     "немецкий «Sie trug eine schöne Perle als Halskette»"),
    (14089, "example_uk", "Про них у селі ходять плітки",
     "Це просто плітки, я цьому не вірю",
     "немецкий «Das ist ja nur Klatsch, ich glaube das nicht»"),
    (1628, "example_uk", "Цей вентилятор добре охолоджує кімнату",
     "Охолоди, будь ласка, напій",
     "немецкий «Kühl bitte das Getränk»"),
    (16338, "example_uk", "Він противився цьому рішенню до кінця",
     "Я противлюся цьому рішенню",
     "немецкий «Ich widersetze mich dieser Entscheidung»"),
    (589, "example_uk", "М'ясник зважив мені кілограм телятини",
     "Я йду до м'ясника і купую м'ясо",
     "немецкий «Ich gehe zum Metzger und kaufe Fleisch»"),
    (7433, "example_uk", "Лікар швидко прибіг",
     "Лікар швидко прибіг сюди", "потеряно «сюда»"),
    (2796, "example_uk", "Суддя свистить",
     "Суддя свистком завершує матч", "потеряно «abpfeifen»"),
    (3067, "example_uk", "Спільне життя гармонійне",
     "Спільне життя з моїми батьками гармонійне", "потеряны родители"),
    (7428, "example_uk", "Цей хлопець справжній гігант, дуже високий",
     "Цей хлопець справжній велетень", "«дуже високий» приписано"),
    (7428, "translation_uk", "велетень, гігант, силач",
     "велетень, гігант, титан", "«силач» — силач, а не великан"),
    (13693, "example_uk", "Він надів свій синій піджак для конференції",
     "Він надів свій синій піджак на конференцію", "предлог"),

    # --- русские -------------------------------------------------------------
    (16334, "example_ru", "Политик был вынужден уйти в ссылку",
     "Политик был вынужден уйти в изгнание", "«уйти в ссылку» — не говорят"),
    (16331, "example_ru", "Приговор преступнику был горячо обсуждён",
     "Приговор преступнику горячо обсуждали", "страдательный залог тут лишний"),
    (17194, "example_ru", "Поворачивай направо у светофора",
     "Ты должен повернуть на следующей улице",
     "немецкий «Du musst an der nächsten Straße abbiegen»"),
    (10725, "example_ru", "Это очень изысканная идея",
     "Это довольно хитроумная идея", "«ziemlich» — довольно, не очень"),
    (16336, "example_ru", "Этот чиновник коррупционный",
     "Этот чиновник был коррумпирован", "«коррупционный» — не о человеке"),
    (16337, "example_ru", "Командир приказал солдатам идти в атаку",
     "Командир приказал солдатам маршировать", "«marschieren» — маршировать"),
    (16338, "example_ru", "Я возражаю против этого решения",
     "Я противлюсь этому решению", "в значениях первое «противиться»"),
    (18774, "example_ru", "Мы живём в эпоху цифровизации",
     "Мы живём в цифровую эпоху", "«цифровизации» приписано"),
    (18771, "example_ru", "По субботам вечером мы всегда ходим в кино",
     "В субботний вечер мы всегда ходим в кино", "в немецком единственное"),

    # --- турецкие небывальщины и падежи --------------------------------------
    (8959, "example_tr", "Portyer bagajlarımı taşımama yardım etti",
     "Kapıcı bagajlarımı taşımama yardım etti", "«Portyer» — не слово"),
    (589, "example_tr", "Kasapçıya gidip et alıyorum",
     "Kasaba gidip et alıyorum", "«Kasapçı» — не слово"),
    (7425, "example_tr", "Tartışma sonsuzydu ve hiçbir yere varmadı",
     "Tartışma sonsuzdu ve hiçbir yere varmadı", "«sonsuzydu» — опечатка"),
    (9826, "example_tr", "Büyük bir gıda stoğumuz var",
     "Büyük bir gıda stokumuz var", "«stoğumuz» — опечатка"),
    (7420, "example_tr", "Hediyemin üzerindeki kurde kırmızı ve parlak",
     "Hediyemin üzerindeki kurdele kırmızı ve parlak", "«kurde» — обрывок"),
    (7443, "example_tr", "Masa oldukça kararsız", "Masa oldukça dengesiz",
     "«kararsız» — нерешительный"),
    (15576, "example_tr", "Kuşlar sabah sabah ötüyor",
     "Horoz her sabah ötüyor", "в немецком петух, а не птицы"),
    (10719, "example_tr", "Güldüğümü bastıramıyorum",
     "Gülmemi bastıramıyorum", "неверная форма"),
    (14540, "example_tr", "Kral bir kripta içinde gömülü",
     "Kral bir kriptada gömülü", "«içinde» лишнее"),
    (17578, "example_tr", "Asansör bozuk, merdiveni kullanmalıyız",
     "Asansör bozuk, merdivenleri kullanmalıyız", "число"),
    (14087, "example_tr", "Bana ne demek istediğimi açıkla",
     "Ne demek istediğimi sana açıklayayım", "лицо перевёрнуто"),
    (10723, "example_tr", "Kediyi kucağına aldı ve yavaşça okşadı",
     "Kediyi okşuyorum", "немецкий «Ich streichele die Katze»"),
    (7421, "example_tr", "Partiden gözden kaçmış şekilde ayrıldı",
     "Partiden fark edilmeden ayrıldı", "«gözden kaçmış şekilde» — калька"),
    (12216, "example_tr", "Her sabah yarım saat jogging yapıyorum",
     "Her sabah yarım saat koşu yapıyorum", "«jogging» — не турецкое слово"),
    (12700, "example_tr", "Adrenalin yükseliyor",
     "Adrenalin boğazıma kadar yükseliyor", "потеряно «in den Hals»"),
    (16336, "example_tr", "Memur yolsuzdu", "Memur yozlaşmıştı",
     "«yolsuz» — без дороги"),
    (11777, "example_tr", "Akşam yemeği için tavuk var",
     "Akşam yemeğinde tavuk yiyoruz", "«var» вместо «едим»"),
    (13541, "example_tr", "Param yok, bir de şu var ki arabam yok",
     "Param yok, arabam olması bir yana", "фраза не собрана"),
    (10736, "example_tr", "Kalabalığın tepkisi ezici şekilde olumlu idi",
     "Kalabalığın tepkisi ezici şekilde olumluydu", "«idi» пишут слитно"),
    (8960, "example_tr", "Filmin oyuncu kadrosu harika idi",
     "Filmin oyuncu kadrosu harikaydı", "то же"),
    (12703, "example_tr", "Kürtaj konusu çok tartışmalıdır",
     "Kürtaj konusu çok tartışmalı", "«-dır»"),
    (690, "example_tr", "Paskalya bir bayramdır", "Paskalya bir bayram",
     "то же"),
    (16344, "example_tr", "Alkol kötüye kullanımı büyük bir sorundur",
     "Alkol kötüye kullanımı büyük bir sorun", "то же"),
    (7427, "example_tr", "Yeni restoran şu anda tamamen modadır",
     "Yeni restoran şu anda çok popüler", "то же"),
    (12706, "example_tr", "Bacak, kalça ile diz arasındaki vücut parçasıdır",
     "Uyluk, kalça ile diz arasındaki vücut bölümü",
     "«bacak» — нога целиком; и «-dır»"),
    (10732, "example_tr", "O çok inatçı ve basitçe vazgeçmiyor",
     "O çok inatçı ve bir türlü vazgeçmiyor", "«basitçe» — калька"),
    (10734, "example_tr", "O, babasını sevgiyle bakıyor",
     "Büyükannesine sevgiyle bakıyor", "в немецком бабушка, и падеж"),
    (10731, "example_tr", "Yemek tamamen aç durumu tatmin eder",
     "Yemek açlığımı tamamen gideriyor", "фраза не собрана"),
    (8957, "example_tr", "Onun bu işe adanmışlığı herkesi etkiledi",
     "Onun bu işe adanmışlığı takdire değer",
     "немецкий «ist bewundernswert»"),
    (8961, "example_tr", "Hastanede gece nöbeti çalışıyor",
     "Hastanede gece nöbetinde çalışıyor", "пропущен падеж"),
    (9517, "example_tr",
     "Kütüphaneden yeni kitaplar almak için gitmekten hoşlanırım",
     "Yeni kitaplar ödünç almak için kütüphaneye gitmeyi severim",
     "фраза перегружена"),
    (14091, "example_tr", "Yetkili makamlara bir sorgu sundum",
     "Yetkili makamlara bir başvuru yaptım", "«sorgu» — допрос"),
    (8962, "example_tr", "Okul müdürü çok katı", "Okul müdiresi çok katı",
     "в немецком женский род"),
    (16343, "example_tr", "Hakim akıllıca bir karar verdi",
     "Kadın hâkim akıllıca bir karar verdi", "то же"),
    (16345, "example_tr", "Öğrenciler dikkat çekmek için dersi işgal ediyorlar",
     "Öğrenciler dikkat çekmek için amfiyi işgal ediyor",
     "«ders» — занятие, а не аудитория"),
    (7439, "example_tr", "Göz yaşları döktü", "Gözyaşı döktü",
     "«gözyaşı» пишется слитно"),
    (7433, "example_tr", "Doktor hızlı buraya geldi",
     "Doktor hızla buraya geldi", "«hızlı» — прилагательное"),
    (14541, "example_tr", "Dini ailem yılda birçok tatili kutluyor",
     "Dindar ailem yılda birçok bayram kutluyor",
     "«tatil» — отпуск, а не праздник"),
    (2796, "example_tr", "Hakem düdük çalıyor",
     "Hakem maçı düdükle bitiriyor", "потеряно «abpfeifen»"),
    (3067, "example_tr", "Birlikte yaşamak uyumlu",
     "Ailemle birlikte yaşamak uyumlu", "потеряны родители"),
    (10735, "example_tr", "Savaşı bir hile ile kazandı",
     "Kavgayı bir hileyle kazandı", "«savaş» — война, а не бой"),

    # --- потерянное и приписанное --------------------------------------------
    (7414, "example_en", "That's a really strange question",
     "That's a strange idea", "немецкий «eine sonderbare Idee»"),
    (10725, "example_en", "That's a clever idea, very smart",
     "That's quite a clever idea", "«very smart» приписано"),
    (10725, "example_tr", "Bu kurnaz bir fikir, çok akıllıca",
     "Bu oldukça incelikli bir fikir", "то же"),
    (10725, "example_uk", "Це дуже витончена ідея",
     "Це досить хитромудра ідея", "«ziemlich» — довольно"),
    (7428, "example_en", "This guy is a real giant, super tall",
     "This guy is a real giant", "«super tall» приписано"),
    (7428, "example_tr", "Bu adam gerçek bir dev, çok uzun",
     "Bu adam gerçek bir dev", "то же"),
    (12219, "example_en", "The score is still tied",
     "The game ends in a draw", "немецкий «Das Spiel endet unentschieden»"),
    (12219, "example_uk", "Гра закінчилася внічию",
     "Гра закінчується внічию", "в немецком настоящее время"),
    (12700, "example_en", "The adrenaline is rising",
     "The adrenaline is rising in my throat", "потеряно «in den Hals»"),
    (2796, "example_en", "The referee blows the whistle",
     "The referee blows the final whistle", "потеряно «abpfeifen»"),
    (3067, "example_en", "The coexistence is harmonious",
     "Living together with my parents is harmonious", "потеряны родители"),
    (13692, "example_pl", "Jego przebranie za pirata było zabawne",
     "Jego przebranie za pirata było naprawdę zabawne", "потеряно «echt»"),
    (12218, "example_pl", "Dzieci skaczą po łóżku",
     "Dzieci skaczą wszędzie i bawią się",
     "немецкий «Die Kinder hüpfen überall herum und haben Spaß»"),
    (12216, "example_pl", "Codziennie rano biegam w parku",
     "Codziennie rano biegam przez pół godziny", "парк приписан"),
    (13694, "example_pl", "Twoje nowe strzyżenie wygląda super",
     "Moja nowa fryzura wygląda super", "в немецком «мой»"),
    (12217, "example_pl", "Choroba jest w początkowym stadium",
     "Projekt jest w początkowym stadium",
     "немецкий «Das Projekt befindet sich in einem frühen Stadium»"),
    (16339, "example_pl", "Rzeczoznawca wydał ekspertyzę mieszkania",
     "Ekspertyza pokazuje, że to bezpieczne",
     "немецкий «Das Gutachten zeigt, dass es sicher ist»"),
    (16340, "example_pl", "Saperzy rozbroili bombę w centrum miasta",
     "Ekspert rozbroił bombę",
     "немецкий «Der Sprengstoffexperte entschärfte die Bombe»"),
    (16341, "example_pl", "Policja zabezpieczyła ważny dowód rzeczowy",
     "Dowód rzeczowy pokazuje jego winę",
     "немецкий «Das Beweisstück zeigt seine Schuld»"),
    (11779, "example_pl", "Dodaj trochę pieprzu do zupy",
     "Uważaj, pieprz jest dość ostry",
     "немецкий «Pass auf, der Pfeffer ist ziemlich scharf»"),
    (16342, "example_pl", "Mój sąsiad to zagorzały republikanin",
     "Republikanin namiętnie bronił swoich przekonań",
     "немецкий «Der Republikaner verteidigte seine Überzeugungen»"),
    (16345, "example_pl", "Ktoś zajął moje miejsce w pociągu",
     "Studenci zajmują audytorium, żeby zwrócić uwagę",
     "немецкий «Die Studenten besetzen den Hörsaal»"),
    (16344, "example_pl", "Nadużycie władzy to poważna sprawa",
     "Nadużywanie alkoholu to duży problem",
     "немецкий «Der Missbrauch von Alkohol ist ein großes Problem»"),
    (16343, "example_pl", "Sędzia wydała sprawiedliwy wyrok",
     "Sędzia wydała mądry wyrok", "«kluges» — мудрый"),
    (16333, "example_pl", "Cesarzowa mieszkała w wielkim pałacu",
     "Cesarzowa rządziła całym imperium",
     "немецкий «Die Kaiserin herrschte über das ganze Reich»"),
    (16332, "example_pl", "Oskarżono urzędnika o łapówkarstwo",
     "Urzędnik został aresztowany za łapówkarstwo",
     "«oskarżono» — обвинили, а не арестовали"),
    (10730, "translation_pl", "niesłyszany, skandaliczny, oburzający",
     "niesłychany, skandaliczny, oburzający",
     "«niesłyszany» — неслышимый"),
    (10730, "example_tr", "Böyle bir şey söylemek müstehcen",
     "Böyle bir şey söylemek rezalet", "«müstehcen» — непристойный"),
    (13543, "example_tr", "Bu plana karşıyım, kendi tavsiyeme rağmen",
     "Kendi isteğimin aksine hareket ediyorum",
     "немецкий «Ich handle wider meinen Willen»"),
    (13543, "example_pl", "To jest przeciw moim zasadom",
     "Działam wbrew własnej woli", "то же"),
    (18261, "example_pl", "Woda gotuje się w kotle",
     "Woda gotuje się w czajniku", "в остальных языках чайник"),
    (11776, "example_pl", "Na kolację zamówiliśmy sushi",
     "Na kolację jemy sushi", "немецкий «essen wir»"),
    (11777, "example_pl", "Na obiad mamy pieczonego kurczaka",
     "Na kolację mamy kurczaka", "«обед» и «запечённого» приписаны"),
    (16337, "example_pl", "Dowódca kazał żołnierzom ruszyć dalej",
     "Dowódca kazał żołnierzom marszować", "«marschieren» — маршировать"),
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
