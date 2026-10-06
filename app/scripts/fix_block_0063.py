"""
Правки блока 63 (ряды 10901–11100, ранги 22466–22888).

Три находки блока.

ПЕРВАЯ: немецкое слово прочитано как английское.

    de  Hinter dem Haus blüht der Holder
    uk  Володар кубка захищає свій титул з великою честолюбивістю

`Holder` по-немецки это бузина. Украинская ячейка прочла его как
английское `holder` — «обладатель», и построила вокруг фразу про
обладателя кубка, который защищает свой титул. Фраза осмысленная,
грамотная и не имеет к ряду никакого отношения.

Это третий способ сломать слово, и все три разные. `vermöbeln` в блоке
60 был разобран по ложному КОРНЮ внутри немецкого. `Parole` в блоке 58
был взят за СОЗВУЧНОЕ слово другого языка. Здесь немецкое слово целиком
прочитано как слово другого языка, с другим значением. Приметой не
ловится ни один из трёх: все три дают безупречную фразу.

Рядом тот же механизм, но мягче: `abzüglich` (9940), словарная статья
`düşülerek, hariç, eksi`, а турецкий пример — `Dışarısı bugün eksi beş
derece`, «на улице минус пять». Слово `eksi` взято в температурном
смысле и под него придумана своя фраза.

ВТОРАЯ: эталон заменили после перевода — девять рядов за один блок.
8508, 11484, 9623, 12385, 11485, 11486, 14306, 16886, 11502, 12392.
Расклад тот же, что описан в блоке 61: переводы сходятся плотно между
собой на фразе, которой в немецком уже нет. За три блока это перестало
быть находкой и стало самым частым классом базы.

ТРЕТЬЯ: дыра в примете из блока 59, найденная глазами.

    de  Ich kann nicht zuzulassen, dass meine Freundin allein bleibt

Это ровно лишнее `zu` после модального — то, что `scan_de_zu_infinitive`
ищет с блока 59 и на чём показывала честный ноль. Но приставка здесь
сама «zu», форма выходит `zu` + `zu` + `lassen`, а в списке приставок
приметы «zu» не было. Четыре блока она проходила мимо. Список
дополнен, примета пере-прогнана: по всей базе такой ряд один.

    python -m app.scripts.fix_block_0063            # показать
    python -m app.scripts.fix_block_0063 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 10901 niedlich
    (8503, "example_uk", "Кошеня було таке миле з його великими очима",
     "Кошеня таке миле зі своїми великими очима",
     "эталон в настоящем, и «з його» вместо «зі своїми»"),
    (8503, "example_tr", "Yavru kedi, büyük gözleriyle çok sevimliydi",
     "Yavru kedi, büyük gözleriyle çok sevimli",
     "эталон в настоящем времени"),
    # 10902 Fehlverhalten
    (11478, "example_tr",
     "Öğrencinin kötü davranışı onun askıya alınmasına yol açtı",
     "Öğrencinin kötü davranışı okuldan uzaklaştırılmasına yol açtı",
     "«askıya almak» о счетах и платежах, а не об ученике"),
    # 10905 Schlupfloch
    (16862, "example_uk", "Уряд намагалася закрити всі податкові лазівки",
     "Уряд намагався закрити всі податкові лазівки",
     "рассогласование рода"),
    # 10908 Bauchweh
    (13096, "example_pl", "Dziecko ma ból brzucha i nie chce jeść",
     "Dziecko ma ból brzucha i nie może iść do szkoły",
     "перевод другого предложения"),
    # 10910 Palette
    (14785, "example_tr", "Ressam çok renkli geniş bir palete sahip",
     "Ressamın çok renkli geniş bir paleti var",
     "«sahip olmak» — калька"),
    (14785, "example_pl", "Malarz trzyma paletę z farbami",
     "Malarz ma dużą paletę z wieloma kolorami",
     "перевод другого предложения"),
    # 10912 Bai
    (15838, "example_tr", "Körfez sakindir ve su kristal berraklığındadır",
     "Körfez sakindi ve su kristal berraklığındaydı",
     "эталон в прошедшем времени"),
    # 10913 Angler
    (12383, "example_uk",
     "Рибалка сидів весь день у озері і чекав рибу",
     "Рибалка сидів весь день біля озера і чекав на рибу",
     "«у озері» значит внутри озера"),
    # 10914 Abfuhr
    (8506, "example_tr",
     "Onu randevuya çağırdığında ondan reddetme aldı",
     "Onu randevuya çağırdığında ondan ret cevabı aldı",
     "«reddetme almak» — не выражение"),
    # 10915 Morgenmantel
    (13769, "example_uk", "Вона носила свій халат і пила каву на балконі",
     "Вона була в халаті й пила каву на балконі",
     "«trug» здесь о том, что было надето, а не о привычке"),
    (13769, "example_tr", "Sabah kaftanını giydi ve balkonda kahve içti",
     "Sabahlığını giymiş, balkonda kahve içiyordu",
     "«sabah kaftanı» — не слово, в статье «sabahlık»"),
    # 10916 Getto
    (16863, "example_uk",
     "У Другій світовій війні євреїв змушували жити в гето",
     "Під час Другої світової війни євреїв змушували жити в гето",
     "«у війні» — не то управление"),
    (16863, "example_tr",
     "İkinci Dünya Savaşında Yahudiler gettolara zorlanmıştı",
     "İkinci Dünya Savaşı'nda Yahudiler gettolarda yaşamaya zorlandı",
     "потерян апостроф, и «gettolara zorlanmak» — не выражение"),
    # 10917 Hausschuh
    (13770, "example_uk",
     "Я надягаю домашні тапочки, коли прийду додому",
     "Я надягаю домашні капці, коли приходжу додому",
     "эталон о привычке, а не об однократном приходе"),
    (13770, "example_tr", "Evime gelince ev terliğimi giyerim",
     "Eve gelince ev terliğimi giyerim",
     "«evime gelince» — лишний притяжательный"),
    # 10918 Ketzerei — залог в эталоне
    (14786, "example_de",
     "Das war im Mittelalter als Ketzerei angesehen worden",
     "Das wurde im Mittelalter als Ketzerei angesehen",
     "«war angesehen worden» — предпрошедшее там, где нужно простое"),
    (14786, "example_tr", "Orta Çağda bu sapkınlık olarak görülüyordu",
     "Orta Çağ'da bu sapkınlık olarak görülüyordu",
     "потерян апостроф"),
    (14786, "example_pl", "Dawniej uznawano to za herezję",
     "W średniowieczu uznawano to za herezję",
     "«dawniej» вместо «im Mittelalter»"),
    # 10921 abgenutzt
    (8507, "example_pl", "Te buty są już całkiem zużyte",
     "Te buty są całkiem zużyte i trzeba je wymienić",
     "потеряна вторая половина"),
    # 10922 Überwachungsvideo
    (16866, "translation_uk",
     "запис з камери спостереження, відео зі камер стеження",
     "запис з камери спостереження, відео з камер стеження",
     "«зі» перед согласной"),
    # 10923 Hausarzt
    (13097, "example_pl", "Muszę zapisać się do lekarza rodzinnego",
     "Idę do lekarza rodzinnego, kiedy jestem chory",
     "перевод другого предложения"),
    # 10924 Gaspedal
    (17381, "example_ru",
     "Он нажал на педаль газа, и машина рвануло вперёд",
     "Он нажал на педаль газа, и машина рванула вперёд",
     "рассогласование рода"),
    (17381, "example_pl", "Nacisnął pedał gazu i ruszył",
     "Nacisnął pedał gazu i samochód wystrzelił do przodu",
     "потеряно подлежащее второй половины"),
    # 10926 erstgeboren
    (15307, "example_uk", "Перший син отримав все майно",
     "Первородний син отримав усе майно",
     "перевод слова — «первородний»"),
    # 10927 Sterbebett
    (13098, "example_uk",
     "На смертному ліжку він простив своїм дітям усі помилки",
     "На смертному ложі він простив своїм дітям усі помилки",
     "в статье «смертне ложе»"),
    (13098, "example_pl", "Na łożu śmierci wybaczył wszystkim",
     "Na łożu śmierci wybaczył swoim dzieciom wszystkie błędy",
     "потеряно «seinen Kindern alle Fehler»"),
    # 10929 Himmelreich
    (14787, "example_tr", "İyi insanların cennete gideceğine inanıyor",
     "İnananlar cennete gitmeyi umuyor",
     "перевод другого предложения"),
    (14787, "example_pl", "Wierzący marzą o królestwie niebieskim",
     "Wierzący ludzie mają nadzieję dostać się do królestwa niebieskiego",
     "«marzą» вместо «hoffen zu kommen»"),
    # 10930 Herberge
    (17382, "example_ru", "Мы ночевали в дешёвом хостеле",
     "Хостел предлагает дешёвое жильё для путешественников",
     "перевод другого предложения"),
    (17382, "example_tr", "Otel gezginler için ucuz konaklama sunuyor",
     "Hostel gezginler için ucuz konaklama sunuyor",
     "«otel» это не `Herberge`"),
    (17382, "example_pl", "Nocowaliśmy w tanim schronisku w górach",
     "Schronisko oferuje tanie zakwaterowanie dla podróżnych",
     "перевод другого предложения"),
    # 10931 Ruhestörung
    (16867, "example_uk",
     "Поліція була викликана через порушення спокою пізно ввечері",
     "Поліцію викликали через порушення спокою пізно ввечері",
     "тяжёлый пассив там, где эталон его не требует"),
    (16867, "example_tr", "Gece gürültü yapmak burada yasak",
     "Polis, akşam geç saatte huzuru bozma nedeniyle çağrıldı",
     "перевод другого предложения"),
    # 10932 verfüttern
    (15839, "example_uk", "Старий хліб скармлювали курам",
     "Старий хліб згодували курам",
     "«скармлювати» — русская основа"),
    (15839, "example_tr", "Eski ekmek tavuklara yemlenmiş",
     "Eski ekmek tavuklara yem olarak verildi",
     "«yemlenmek» — не та форма"),
    (15839, "example_pl", "Stary chleb skarmiono kurom",
     "Stary chleb dano kurom",
     "«skarmić» — диалектное"),
    # 10933 Entdecker
    (18081, "example_ru",
     "Колумб был знаменитым первооткрывателем, ищущим новые континенты",
     "Колумб был знаменитым первооткрывателем, который искал новые "
     "континенты",
     "«ищущим» — тяжёлый активный причастный оборот"),
    (18081, "example_tr",
     "Kolomb yeni kıtaları arayan ünlü bir keşfetçiydi",
     "Kolomb, yeni kıtalar arayan ünlü bir kaşifti",
     "«keşfetçi» — нет такого слова, в статье «kaşif»"),
    # 10934 rumschnüffeln — эталон заменили после перевода
    (8508, "example_en",
     "The kids are poking around in my room and wanting to look in all "
     "the cupboards",
     "You don't have to snoop around everywhere",
     "перевод остался от прежнего эталона"),
    (8508, "example_uk",
     "Діти совають ніс у мою кімнату й заглядають у всі шафи",
     "Тобі не треба всюди пхати носа",
     "перевод остался от прежнего эталона"),
    (8508, "example_tr", "Herkes benim işime burnunu sokuyor",
     "Her yerde burnunu sokmana gerek yok",
     "перевод другого предложения"),
    # 10935 zerfetzen
    (8509, "example_en", "The explosion tore the old building apart",
     "The explosion tore the old building into a thousand pieces",
     "потеряно «in tausend Stücke»"),
    (8509, "example_tr", "Patlama eski binayı bin parçaya ayırdı",
     "Patlama eski binayı bin parçaya böldü",
     "«ayırmak» это разделить, а `zerfetzen` — разорвать"),
    (8509, "example_pl", "Pies rozszarpał moją poduszkę",
     "Wybuch rozszarpał stary budynek na tysiąc kawałków",
     "перевод другого предложения"),
    # 10936 Melancholie
    (11480, "example_en",
     "A deep melancholy gripped him after he had to leave his home",
     "A deep melancholy gripped him after he had left his homeland",
     "«had to leave» добавляет принуждение, которого в эталоне нет"),
    (11480, "example_uk",
     "Глибока меланхолія охопила його, коли він мав залишити свою домівку",
     "Глибока меланхолія охопила його після того, як він залишив свою "
     "батьківщину",
     "«мав залишити» добавляет принуждение, и «домівка» это дом, "
     "а `Heimat` — батьківщина"),
    # 10937 Footballspieler — эталон заменили после перевода
    (12385, "example_en",
     "The American football player trains hard every day to stay in shape",
     "The American football player trains hard every day",
     "«to stay in shape» в эталоне нет"),
    (12385, "example_uk",
     "Футболіст тренується кожного дня, щоб залишатися в формі",
     "Гравець в американський футбол тренується щодня",
     "«футболіст» это другой вид спорта, и второй половины в эталоне нет"),
    (12385, "example_tr",
     "Amerikan futbolcusu formunda kalmak için her gün antrenman yapıyor",
     "Amerikan futbolu oyuncusu her gün sıkı antrenman yapıyor",
     "«formunda kalmak için» в эталоне нет, зато потеряно «hart»"),
    # 10939 begrenzen
    (8510, "example_uk",
     "Керівник обмежує робочий час восьмьма годинами на день",
     "Керівник обмежує робочий час вісьмома годинами на день",
     "«восьмьма» — нет такой формы"),
    (8510, "example_tr",
     "Patron çalışma saatini günde sekiz saatile sınırlandırıyor",
     "Patron çalışma saatini günde sekiz saatle sınırlandırıyor",
     "«saatile» — лишняя гласная"),
    (8510, "example_pl", "Musimy ograniczyć wydatki w tym miesiącu",
     "Szef ogranicza czas pracy do ośmiu godzin dziennie",
     "перевод другого предложения"),
    # 10940 Holder — немецкое слово прочитано как английское
    (8511, "example_uk",
     "Володар кубка захищає свій титул з великою честолюбивістю",
     "За будинком цвіте бузина",
     "`Holder` это бузина, а не английское holder — обладатель"),
    (8511, "example_en", "We picked elderberries for jam",
     "Behind the house the elder is in bloom",
     "перевод другого предложения"),
    (8511, "example_tr", "Bahçenin köşesinde bir mürver ağacı var",
     "Evin arkasında mürver çiçek açıyor",
     "перевод другого предложения"),
    # 10942 einwerfen
    (8513, "example_tr", "Topu bana at!",
     "Pencereden bir taş attı ve sonra kaçtı",
     "перевод другого предложения"),
    (8513, "example_pl", "Wrzuciłem list do skrzynki na poczcie",
     "Wrzucił kamień przez okno i potem uciekł",
     "перевод другого предложения"),
    # 10943 Macher
    (9247, "example_tr",
     "Gerçek bir eylemci ve her zaman projelerinde başarılı oluyor",
     "O gerçek bir işi bitiren adam ve projelerini her zaman başarıya "
     "ulaştırıyor",
     "«eylemci» это активист"),
    # 10944 Nötigung
    (16868, "example_ru",
     "Принуждение путем насилия является тяжким преступлением",
     "Принуждение путём насилия — тяжкое преступление",
     "«е» вместо «ё», и «является» — канцелярит"),
    # 10945 Otter
    (15840, "example_uk", "Видра ловко пливе по струмку й ловить рибу",
     "Видра вправно пливе по струмку й ловить рибу",
     "«ловко» — русское слово"),
    (15840, "example_tr",
     "Su samuru akışkanda akıllıca yüzüyor ve balık tutuyor",
     "Su samuru derede ustaca yüzüyor ve balık tutuyor",
     "«akışkan» это текучая среда, а не ручей"),
    # 10946 taktlos
    (11482, "example_uk",
     "Його безтактна зауваження глибоко її образила і розсердила",
     "Його безтактне зауваження глибоко її образило і розсердило",
     "рассогласование рода по всей фразе"),
    (11482, "example_tr",
     "Onun taksiz yorumu onu çok kırdı ve kızgın yaptı",
     "Onun düşüncesiz yorumu onu derinden kırdı ve öfkelendirdi",
     "«taksiz» — нет такого слова, и «kızgın yapmak» — калька"),
    # 10947 Fleischbällchen
    (11983, "example_pl", "Na obiad mamy pulpety w sosie",
     "Moja babcia robi pyszne klopsiki z puree ziemniaczanym",
     "перевод другого предложения"),
    # 10948 gottverlassen
    (11483, "example_uk",
     "Він жив у богом забутому маленькому містечку посередині пустині",
     "Він жив у богом забутому маленькому містечку посеред пустелі",
     "«пустиня» — не та форма"),
    (11483, "example_tr",
     "Çölün ortasındaki ıssız, dar bir kasabada yaşıyordu",
     "Çölün ortasındaki ıssız, küçük bir kasabada yaşıyordu",
     "«dar» это узкий, а в эталоне «klein»"),
    # 10949 Krake — род в эталоне
    (15841, "example_de",
     "Der riesige Kraken versteckt sich in der Tiefe des Ozeans",
     "Der riesige Krake versteckt sich in der Tiefe des Ozeans",
     "«Kraken» — косвенная форма, в именительном «der Krake»"),
    # 10951 prägen
    (8514, "example_uk",
     "Роки війни формували його характер і все життя",
     "Роки війни сформували все його життя і його особистість",
     "«Persönlichkeit» это особистість, а не характер"),
    (8514, "example_pl", "Wojna kształtowała całe jego życie",
     "Lata wojny ukształtowały całe jego życie i osobowość",
     "потеряно «und seine Persönlichkeit», и в эталоне годы войны"),
    # 10954 Termite
    (15842, "example_tr",
     "Termit eski ahşap evi içinden dışarı doğru yok ediyor",
     "Termit eski ahşap evi içten içe yok ediyor",
     "«içinden dışarı doğru» — дословная калька"),
    # 10955 tiefgründig — эталон заменили после перевода
    (11484, "example_en",
     "That was a profound philosophy that developed over many years",
     "That's a profound question I've been thinking about for a long time",
     "перевод остался от прежнего эталона"),
    (11484, "example_uk",
     "Це глибоке питання, над яким я довго роздумую",
     "Це глибоке питання, над яким я довго розмірковую",
     "«роздумувати» — не та форма"),
    (11484, "example_tr",
     "Bu, uzun yıllar boyunca geliştirilen derin bir felsefeydi",
     "Bu, uzun zamandır üzerinde düşündüğüm derin bir soru",
     "перевод остался от прежнего эталона"),
    # 10956 kantonesisch — эталон заменили после перевода
    (9623, "example_en", "The restaurant offers Cantonese specialties",
     "She speaks Cantonese fluently",
     "перевод остался от прежнего эталона"),
    (9623, "example_uk", "У ресторані пропонуються кантонські спеціалітети",
     "Вона вільно говорить кантонською",
     "перевод остался от прежнего эталона"),
    (9623, "example_tr", "Restoran Kantonca özel yemekleri sunuyor",
     "Kantonca'yı akıcı konuşuyor",
     "перевод остался от прежнего эталона"),
    # 10957 düsen
    (17383, "example_tr",
     "Arabalar otoyolda çılgın bir hızla fırladılar",
     "Arabalar otoyolda çılgın bir hızla uçuyor",
     "эталон в настоящем времени"),
    (17383, "example_pl", "Pędzimy autostradą nad morze",
     "Samochody pędzą autostradą z szaloną prędkością",
     "перевод другого предложения"),
    # 10958 Eiswasser
    (11984, "example_tr", "Buz suyuna düştü ve neredeyse nefes alamadı",
     "Buzlu suya düşüyor ve neredeyse nefes alamıyor",
     "эталон в настоящем, и в статье «buzlu su»"),
    (11984, "example_pl", "Wpadł do lodowatej wody i nie mógł oddychać",
     "Wpada do lodowatej wody i prawie nie może oddychać",
     "эталон в настоящем, и потеряно «kaum»"),
    # 10959 Gruppenführer
    (9248, "example_uk",
     "Керівник групи організує прогулянку й піклується про всіх",
     "Керівник групи організує похід й піклується про всіх",
     "`Wanderung` это похід, а не прогулянка"),
    # 10960 Stümper — эталон заменили после перевода
    (11485, "example_en",
     "You're a bungler and mess up everything you touch",
     "The guy is a real bungler, everything he touches goes wrong",
     "перевод остался от прежнего эталона"),
    (11485, "example_tr",
     "Sen beceriksiz birsin ve elleğine aldığın her şeyi yanlış yapıyorsun",
     "O adam gerçek bir beceriksiz, eline aldığı her şey ters gidiyor",
     "перевод остался от прежнего эталона, и «elleğine» — опечатка"),
    # 10961 Masseur
    (13099, "example_tr",
     "Masöz masaj salonunda çalışıyor ve müşterilerin rahatlamasına "
     "yardımcı oluyor",
     "Masör masaj salonunda çalışıyor ve müşterilerin rahatlamasına "
     "yardımcı oluyor",
     "«masöz» это женщина, а заголовок мужского рода"),
    (13099, "example_pl", "Masażysta rozluźnił mi plecy",
     "Masażysta pracuje w studiu wellness i pomaga klientom się odprężyć",
     "перевод другого предложения"),
    # 10962 Grat
    (15843, "example_tr", "Dağcı dar bir sırtta yürüymelidir",
     "Dağcı dar bir sırtta yürümelidir",
     "«yürüymeli» — лишняя буква"),
    # 10963 Mütterchen
    (15309, "example_uk", "Стара матінка сидить на лавці й дивиться на дітей",
     "Стара бабуся сидить на лавці й дивиться на дітей",
     "перевод слова первым значением"),
    (15309, "example_tr", "Yaşlı kadın bankta oturuyor ve çocuklara bakıyor",
     "Yaşlı kadıncağız bankta oturuyor ve çocuklara bakıyor",
     "потеряна уменьшительность слова ряда"),
    # 10964 zurückerobern
    (16871, "example_uk", "Армія хоче повернути місто й зупинити вторгнення",
     "Армія хоче відвоювати місто й зупинити вторгнення",
     "перевод слова первым значением"),
    # 10965 Aufmachung
    (13771, "example_en", "The guests outfit was very elegant",
     "The guests' outfit was very elegant",
     "потерян апостроф"),
    (13771, "example_tr", "Konuğun sunuşu çok şıktı",
     "Konukların kılığı çok şıktı",
     "«sunuş» это подача доклада, и гость в эталоне не один"),
    # 10966 Abendschule
    (9624, "example_pl",
     "Chodzi do szkoły wieczorowej, żeby skończyć szkołę",
     "Chodzi do szkoły wieczorowej, żeby zdobyć świadectwo",
     "«do szkoły, żeby skończyć szkołę» — тавтология"),
    # 10967 triumphieren — эталон заменили после перевода
    (11486, "example_en", "The athlete triumphed after his victory",
     "After years of hard work he finally triumphed",
     "перевод остался от прежнего эталона"),
    (11486, "example_uk",
     "Після багатьох років роботи він нарешті тріумфував",
     "Після багатьох років важкої праці він нарешті тріумфував",
     "потеряно «harter»"),
    (11486, "example_tr", "Yılların ardından sonunda galip geldi",
     "Yıllarca süren sıkı çalışmanın ardından sonunda galip geldi",
     "потеряно «harter Arbeit»"),
    # 10968 Vikar
    (14788, "example_pl", "Nowy wikary wygłosił kazanie w kościele",
     "Wikary wygłosił kazanie w kościele",
     "«nowy» в эталоне нет"),
    # 10969 Fraktur
    (13100, "example_pl", "Lekarz stwierdził złamanie nogi",
     "Złamanie nogi zagoiło się po trzech miesiącach",
     "перевод другого предложения"),
    # 10973 Galle
    (13101, "example_en", "He had the gall to ask again",
     "His words were full of bile and bitterness",
     "перевод взял другое значение слова и построил свою фразу"),
    (13101, "example_uk", "Його слова були повні жовчі й злості",
     "Його слова були повні жовчі й гіркоти",
     "«Bitterkeit» это гіркота, а не злість"),
    (13101, "example_tr", "Safra kesesinden ameliyat oldu",
     "Sözleri safra ve acılıkla doluydu",
     "перевод взял другое значение слова и построил свою фразу"),
    (13101, "example_pl", "Żółć pomaga trawić tłuste jedzenie",
     "Jego słowa były pełne żółci i goryczy",
     "перевод взял другое значение слова и построил свою фразу"),
    # 10975 Grashüpfer
    (15844, "example_uk", "Коник стрибав крізь траву",
     "Коник стрибав у траві",
     "«крізь траву» — дословная калька"),
    (15844, "example_tr", "Bir çekirge çimen arasında sıçradı",
     "Bir çekirge çimenlerin arasında sıçradı",
     "потерян родительный"),
    # 10976 Immobilienmakler
    (9249, "example_uk", "Агент нерухомості показав мені кілька будинків",
     "Агент з нерухомості показав мені кілька будинків",
     "потеряно «з»"),
    # 10977 abtrocknen
    (18460, "example_ru", "Можешь вытереть тарелки?",
     "Можешь вытереть тарелки, пожалуйста?",
     "потеряно «bitte»"),
    (18460, "example_uk", "Можеш ти витерти тарілки?",
     "Можеш витерти тарілки, будь ласка?",
     "порядок слов сломан, и потеряно «bitte»"),
    (18460, "example_pl", "Możesz wytrzeć talerze?",
     "Możesz wytrzeć talerze, proszę?",
     "потеряно «bitte»"),
    # 10979 Transfusion
    (13102, "example_uk", "Пацієнту терміново зробили трансфузію крові",
     "Пацієнту потрібне було переливання крові",
     "«терміново зробили» вместо «brauchte»"),
    # 10980 unentschlossen
    (11487, "example_tr", "Renk seçiminde hiç kararsız kalıyordu",
     "Renk seçiminde tamamen kararsızdı",
     "«hiç» переворачивает смысл в отрицание"),
    # 10981 skandalös
    (11488, "example_tr", "Bakanın davranışı gerçekten skandal yarattı",
     "Bakanın davranışı gerçekten utanç vericiydi",
     "«skandal yarattı» значит «вызвало скандал», а не «было скандальным»"),
    # 10982 unweigerlich
    (8516, "example_pl", "To nieuchronnie kończy się kłótnią",
     "Konsekwencje były nieuniknione",
     "перевод другого предложения"),
    # 10983 abzüglich — слово статьи взято в другом смысле
    (9940, "example_tr", "Dışarısı bugün eksi beş derece",
     "Fiyat, indirim düşülerek 100 euro",
     "«eksi» взято в температурном смысле и под него придумана "
     "своя фраза"),
    # 10985 verantwortungsbewusst
    (11489, "example_uk",
     "Вона відповідальна й турбується про своїх колег",
     "Вона справді відповідальна й турбується про своїх колег",
     "потеряно «echt»"),
    (11489, "example_tr",
     "O sorumlu birisi ve meslektaşlarının önemli olduğunu düşünüyor",
     "O gerçekten sorumluluk sahibi ve meslektaşlarıyla ilgileniyor",
     "вторая половина придумана"),
    # 10986 Bürgerwehr
    (16874, "example_ru", "Гражданский дозор патрулировал город по ночам",
     "Гражданский патруль патрулировал город по ночам",
     "перевод слова — «гражданский патруль»"),
    (16874, "example_uk", "Дружина патрулювала місто вночі",
     "Народна дружина патрулювала місто вночі",
     "«дружина» без «народна» значит жена"),
    (16874, "example_tr", "Sivil devriye gece şehri devriye gezmişti",
     "Sivil devriye geceleri şehirde devriye geziyordu",
     "«devriye … devriye» — повтор, и время не то"),
    # 10988 Gelassenheit
    (11490, "example_en", "With composure he took the bad news calmly",
     "He took the bad news with composure",
     "«with composure» и «calmly» — одно и то же дважды"),
    (11490, "example_tr", "Sakinlik ile kötü haberi sakin karşıladı",
     "Kötü haberi soğukkanlılıkla karşıladı",
     "«sakinlik … sakin» — одно и то же дважды"),
    # 10989 Mineral
    (11985, "example_tr", "Vücut mineraller ve vitaminlere ihtiyaç duyuyor",
     "Vücut mineral ve vitaminlere ihtiyaç duyuyor",
     "первое дополнение без нужного падежа"),
    (11985, "example_pl", "Ta woda ma dużo minerałów",
     "Organizm potrzebuje minerałów i witamin",
     "перевод другого предложения"),
    # 10990 Atomkrieg
    (16875, "example_ru", "Ядерная война уничтожит мир",
     "Ядерная война уничтожила бы мир",
     "«würde zerstören» — условное наклонение"),
    (16875, "example_uk", "Ядерна війна знищить світ",
     "Ядерна війна знищила б світ",
     "«würde zerstören» — условное наклонение"),
    # 10991 erkennbar
    (8517, "example_uk", "Різниця була ясно видима",
     "Різниця була ясно помітна",
     "«видима» это доступная зрению, а `erkennbar` — различимая"),
    (8517, "example_pl", "Z daleka jego twarz była już rozpoznawalna",
     "Różnica była wyraźnie rozpoznawalna",
     "перевод другого предложения"),
    # 10992 Rennen
    (12387, "example_tr", "Yarışta kazanan bir madalya aldı",
     "Yarışın kazananı bir madalya aldı",
     "«yarışta kazanan» это «победивший в гонке», а нужен «победитель "
     "гонки»"),
    # 10993 entsenden
    (16876, "example_uk", "Фірма відрядила його на конференцію",
     "Фірма відрядить представника на конференцію",
     "эталон в будущем, и в нём представитель, а не «он»"),
    # 10995 Flugplan
    (17384, "example_ru", "Расписание показывает все рейсы на эту неделю",
     "Расписание полётов показывает все рейсы на эту неделю",
     "потеряно слово ряда"),
    (17384, "example_pl", "Sprawdź rozkład lotów na jutro",
     "Rozkład lotów pokazuje wszystkie loty na ten tydzień",
     "перевод другого предложения"),
    # 10996 rülpsen
    (18927, "example_tr", "Pardon, yemekten sonra bir ses çıkardı",
     "Pardon, yemekten sonra geğirmek zorunda kaldım",
     "фраза собрана в третьем лице и теряет слово ряда"),
    # 10997 fettig
    (11986, "example_pl", "To jedzenie jest dla mnie za tłuste",
     "Jedzenie w tej restauracji było dla mnie za tłuste",
     "перевод другого предложения"),
    # 10998 Umbau
    (18461, "example_ru", "Реконструкция дома займет ещё три месяца",
     "Реконструкция дома займёт ещё три месяца",
     "«е» вместо «ё»"),
    (18461, "example_tr", "Evin tadilat işi henüz üç ay daha sürecek",
     "Evin tadilatı üç ay daha sürecek",
     "«tadilat işi» — лишнее слово"),
    # 10999 Formsache
    (16877, "example_pl", "To tylko formalność i tak dostaniesz zgodę",
     "To tylko formalność, i tak dostaniesz zgodę",
     "нет запятой"),
    # 11000 knackig
    (11987, "example_pl", "Te jabłka są naprawdę chrupiące",
     "Sałata jest chrupiąca i świeża",
     "перевод другого предложения"),
    # 11003 gähnen
    (13103, "example_uk",
     "Студент позіхає під час лекції, тому що стомлений",
     "Студент позіхає під час лекції, тому що втомився",
     "«стомлений» без связки повисает"),
    (13103, "example_pl", "Ziewam, bo jestem zmęczony",
     "Student ziewa na wykładzie, bo jest zmęczony",
     "перевод другого предложения"),
    # 11004 Beschuldigung
    (16878, "example_tr", "Ona karşı suçlamalar kanıtlanmamış",
     "Ona yönelik suçlamalar kanıtsız",
     "«ona karşı» это «против него» в споре, а не в обвинении"),
    (16878, "example_pl", "Te oskarżenia nie mają żadnych dowodów",
     "Oskarżenia przeciwko niemu są bez dowodów",
     "потеряно «gegen ihn»"),
    # 11006 Vita
    (8518, "example_pl", "Wyślij mi swój życiorys mailem",
     "Jego życiorys pokazuje imponującą karierę akademicką",
     "перевод другого предложения"),
    # 11007 Torwart
    (12389, "example_uk", "Воротар зупинив м'яч чудовим рухом",
     "Воротар зупинив м'яч ефектним кидком",
     "`Parade` это приём вратаря, а не просто движение"),
    (12389, "example_tr", "Kaleci topu spektaküler bir save ile tuttu",
     "Kaleci topu muhteşem bir kurtarışla tuttu",
     "«save» — английское слово"),
    # 11008 Lieblings-
    (11492, "example_tr", "Bu şehirdeki benim favori restoranım",
     "Bu, şehirdeki en sevdiğim restoran",
     "порядок слов сломан"),
    # 11009 verfrüht
    (18928, "example_tr", "Ölümü çok erkindi ve beklenmedikti",
     "Ölümü çok erkendi ve beklenmedikti",
     "«erkin» — другое слово"),
    # 11010 Auszug
    (2240, "example_uk", "Мені потрібна банківська виписка від мого банку",
     "Мені потрібна виписка з рахунку в моєму банку",
     "«банківська виписка від банку» — тавтология"),
    (2240, "example_tr", "Bankamdan bir hesap ekstresine ihtiyacım var",
     "Bankamdan bir hesap özetine ihtiyacım var",
     "в статье «hesap özeti»"),
    # 11011 Abschlussklasse
    (9625, "example_en", "The final class is preparing for the final exams",
     "The graduating class is preparing for the final exams",
     "«final class» это последний урок, а не выпускной класс"),
    (9625, "example_tr", "Mezun sınıfı final sınavlarına hazırlanıyor",
     "Son sınıf final sınavlarına hazırlanıyor",
     "«mezun sınıfı» — не выражение"),
    # 11012 weitersagen — эталон заменили после перевода
    (14306, "example_en", "It's a secret, please don't tell anyone",
     "Please don't pass that on to anyone!",
     "перевод остался от прежнего эталона"),
    (14306, "example_uk", "Це секрет, будь ласка не розповідай його",
     "Будь ласка, нікому цього не розповідай!",
     "перевод остался от прежнего эталона, и нет запятой"),
    (14306, "example_tr", "Bu bir sır, lütfen bunu başkasına söyleme",
     "Bunu lütfen kimseye söyleme!",
     "перевод остался от прежнего эталона"),
    # 11013 Probeaufnahme
    (14790, "example_en",
     "The test shoots for the film were very promising",
     "The test shots for the film were very promising",
     "«test shoots» — не та форма"),
    (14790, "example_uk",
     "Пробні знімання для фільму були дуже обнадійливими",
     "Пробні зйомки для фільму були дуже обнадійливими",
     "в статье «пробні зйомки»"),
    # 11014 Forelle
    (11988, "example_uk",
     "Форель — популярна комерційна риба в альпійських озерах",
     "Форель — популярна столова риба в Альпах",
     "`Speisefisch` это столовая рыба, и в эталоне Альпы, а не озёра"),
    (11988, "example_tr", "Alabalık Alplarda popüler bir yemek balığıdır",
     "Alabalık Alpler'de popüler bir yemek balığıdır",
     "«Alplarda» — не та форма названия"),
    (11988, "example_pl", "Na obiad jedliśmy smażonego pstrąga",
     "Pstrąg to popularna ryba jadalna w Alpach",
     "перевод другого предложения"),
    # 11015 Knebel
    (16880, "example_uk",
     "Диктатор накинув кляп на засоби масової інформації та придушив "
     "свободу преси",
     "Диктатор наклав кляп на засоби масової інформації та придушив "
     "свободу преси",
     "«накинути кляп» — не то управление"),
    (16880, "example_pl", "Porywacze wsadzili mu knebel do ust",
     "Dyktator założył mediom knebel i stłumił wolność prasy",
     "перевод другого предложения"),
    # 11016 Spielzeit
    (12390, "example_tr", "Orkestranın sezonı yılın dokuz ayını kapsar",
     "Orkestranın sezonu yılın dokuz ayını kapsar",
     "«sezonı» — не та гласная в суффиксе"),
    # 11017 Heuchlerin
    (11493, "example_uk",
     "Ця лицеміриця постійно говорить про мораль, але постійно бреше",
     "Ця лицемірка постійно говорить про мораль, але постійно бреше",
     "«лицеміриця» — нет такой формы"),
    (11493, "example_tr",
     "Bu ikiyüzlü kadın erdem vaazı verirken gizlice yalan söylüyor",
     "Bu ikiyüzlü kadın sürekli ahlaktan bahsediyor ama hep yalan "
     "söylüyor",
     "«erdem vaazı» и «gizlice» придуманы"),
    # 11018 Lebensmittelladen
    (9941, "example_ru",
     "В продуктовом магазине за углом я покупаю почти каждый день",
     "В продуктовом магазине за углом я делаю покупки почти каждый день",
     "«покупаю» без дополнения повисает"),
    (9941, "example_uk",
     "У сусідньому магазині я майже щодня роблю покупки",
     "У продуктовому магазині за рогом я майже щодня роблю покупки",
     "потеряно слово ряда и «um die Ecke»"),
    (9941, "example_tr",
     "Köşedeki bakkal dükkanında neredeyse her gün alışveriş yapıyorum",
     "Köşedeki bakkal dükkânında neredeyse her gün alışveriş yapıyorum",
     "потерян циркумфлекс"),
    # 11019 unterschlagen
    (16881, "example_ru", "Не присваивай чужие заслуги",
     "Бухгалтер присвоил миллионы и теперь в бегах",
     "перевод другого предложения"),
    (16881, "example_pl", "Księgowy zdefraudował pieniądze firmy",
     "Księgowy zdefraudował miliony i teraz jest w ukryciu",
     "перевод другого предложения"),
    # 11020 leuchtend
    (8519, "example_tr",
     "Onun parlak gözleri iyi habere duyduğu derin sevinçi gösterdi",
     "Onun parlak gözleri iyi habere duyduğu derin sevinci gösterdi",
     "«sevinçi» — не та согласная"),
    (8519, "example_pl", "W ciemności widać świecące gwiazdy",
     "Jej świecące oczy pokazywały głęboką radość z dobrej wiadomości",
     "перевод другого предложения"),
    # 11021 Gläubige
    (14791, "example_en",
     "The faithful people gathered every Sunday in the church",
     "The faithful gathered every Sunday in the church",
     "«the faithful people» — лишнее слово"),
    (14791, "example_uk", "Віруючі люди збирались кожної неділі в церкві",
     "Віруючі збиралися щонеділі в церкві",
     "«люди» в эталоне нет"),
    (14791, "example_pl", "Wierzący spotykają się w kościele w niedzielę",
     "Wierzący zbierali się w kościele każdej niedzieli",
     "эталон в прошедшем, и «jeden Sonntag» это каждое воскресенье"),
    # 11022 tolerant
    (11494, "example_uk",
     "Його терпиме ставлення до інших культур дійсно примітне",
     "Його терпиме ставлення до інших культур справді варте уваги",
     "«примітний» значит просто заметный"),
    # 11023 Ration
    (11989, "example_uk",
     "Кожний боєць отримує добову рацію з 2000 калорій",
     "Кожний солдат щодня отримує раціон на 2000 калорій",
     "«рація» это радиостанция, а нужен «раціон»"),
    (11989, "example_pl", "Każdy żołnierz dostaje dzienną rację",
     "Każdy żołnierz dostaje dzienną rację 2000 kalorii",
     "потеряно «von 2000 Kalorien»"),
    # 11024 seinerzeit
    (18929, "example_tr",
     "O zamanlar bu tamamen normaldu, ama bugün asla yapılmaz",
     "O zamanlar bu tamamen normaldi, ama bugün asla yapılmaz",
     "«normaldu» — не та гласная"),
    # 11025 Abendkleid
    (13773, "example_uk",
     "Вона одягла гарну чорну вечірню сукню на галу",
     "Вона одягла гарну чорну вечірню сукню на гала-вечір",
     "«гала» не склоняется"),
    # 11026 Befehlskette
    (9250, "example_uk", "В армії ланцюг командування має строго дотримуватись",
     "В армії ланцюга командування треба строго дотримуватися",
     "«ланцюг має дотримуватись» — залог наоборот"),
    (9250, "example_tr", "Orduda komuta zinciri kesinlikle gözlenmeli",
     "Orduda komuta zincirine kesinlikle uyulmalıdır",
     "«gözlenmek» это наблюдаться, а не соблюдаться"),
    # 11027 erleuchten
    (8520, "example_pl", "Świece oświetlają cały pokój",
     "Świece oświetlają pokój ciepłym światłem",
     "«cały» в эталоне нет, зато потеряно «in einem warmen Licht»"),
    # 11028 fraglich
    (8521, "example_pl", "Jej udział w konkursie jest wątpliwy",
     "Czy projekt się uda, jest wątpliwe i zależy od wielu czynników",
     "перевод другого предложения"),
    # 11029 Schatzsuche
    (12391, "example_uk",
     "Діти шукали скарб у саду зі схованими підказками",
     "Діти грали в пошук скарбу в саду зі схованими підказками",
     "«spielten eine Schatzsuche» это играли в игру"),
    # 11030 unfehlbar
    (11495, "example_en",
     "Nobody is infallible, we all make mistakes in life",
     "Nobody is infallible, we all make mistakes sometimes",
     "«in life» в эталоне нет, зато потеряно «mal»"),
    (11495, "example_uk", "Ніхто не непомильний, ми всі робимо помилки",
     "Ніхто не непогрішний, ми всі іноді робимо помилки",
     "перевод слова первым значением, и потеряно «mal»"),
    (11495, "example_tr",
     "Kimse yanılmaz değil, hepimiz hayatta hata yapıyoruz",
     "Kimse yanılmaz değil, hepimiz zaman zaman hata yapıyoruz",
     "«hayatta» в эталоне нет, зато потеряно «mal»"),
    # 11031 Fazit
    (8522, "example_ru",
     "Выводом нашего обсуждения было то, что у нас разные мнения",
     "Вывод нашего обсуждения был в том, что у нас разные мнения",
     "«выводом было то, что» — тяжёлая связка"),
    (8522, "example_pl", "Jaki jest wniosek z tej rozmowy",
     "Wnioskiem z naszej dyskusji było to, że mamy różne opinie",
     "перевод другого предложения, да ещё и вопрос без знака"),
    # 11032 fernbleiben
    (8523, "example_uk", "Цього разу я вирішив залишитися в стороні",
     "Я не прийду на захід, бо не маю часу",
     "перевод другого предложения"),
    (8523, "example_pl", "Znowu nie przyszedł do szkoły",
     "Nie przyjdę na to wydarzenie, bo nie mam czasu",
     "перевод другого предложения"),
    # 11033 Liedchen — чешская буква в польской ячейке
    (14792, "translation_pl", "piosenka, piosenečka",
     "piosenka, piosneczka",
     "«č» в польском алфавите нет — это чешская буква"),
    # 11034 abmachen — время в эталоне против пяти переводов
    (8524, "example_de",
     "Wir machen ab, dass wir uns morgen um zwei treffen",
     "Wir haben abgemacht, dass wir uns morgen um zwei treffen",
     "четыре перевода из пяти в прошедшем, эталон один в настоящем"),
    (8524, "example_ru",
     "Мы договариваемся, что встретимся завтра в два",
     "Мы договорились, что встретимся завтра в два",
     "вслед за исправленным эталоном"),
    (8524, "example_pl", "Umówiliśmy się na drugą po południu",
     "Umówiliśmy się, że spotkamy się jutro o drugiej",
     "потеряно «morgen», и добавлено «po południu»"),
    # 11035 Abgesandte
    (16882, "example_tr",
     "Hükümetin temsilcisi muhalefet ile müzakere etti",
     "Hükümetin temsilcisi muhalefetle müzakere etti",
     "«ile» здесь сливается с словом"),
    # 11036 stündlich
    (18930, "example_ru",
     "Автобус приходит каждый час, поэтому ты можешь не долго ждать",
     "Автобус приходит каждый час, поэтому тебе нужно недолго подождать",
     "«не долго» раздельно, и «можешь» вместо «нужно»"),
    (18930, "example_uk",
     "Автобус приходить щогодини, тому тобі потрібно чуть почекати",
     "Автобус приходить щогодини, тому тобі потрібно трохи почекати",
     "«чуть» — русское слово"),
    (18930, "example_tr",
     "Otobüs saatlik olarak geliyor, bu yüzden sadece biraz beklemen "
     "gerekiyor",
     "Otobüs saat başı geliyor, bu yüzden sadece biraz beklemen gerekiyor",
     "«saatlik olarak» — калька"),
    # 11037 Kriegsgebiet
    (16883, "example_ru",
     "Боевая зона слишком опасна для гражданских лиц и должна быть "
     "эвакуирована",
     "Зона боевых действий слишком опасна для гражданских лиц и должна "
     "быть эвакуирована",
     "перевод слова первым значением"),
    (16883, "example_uk",
     "Бойова зона надто небезпечна для цивільних осіб і повинна бути "
     "евакуйована",
     "Зона бойових дій надто небезпечна для цивільних осіб і повинна "
     "бути евакуйована",
     "перевод слова первым значением"),
    (16883, "example_pl", "Dziennikarze wjechali do strefy wojny",
     "Strefa wojny jest zbyt niebezpieczna dla cywilów i powinna zostać "
     "ewakuowana",
     "перевод другого предложения"),
    # 11038 zulassen — лишнее `zu` в эталоне
    (8525, "example_de",
     "Ich kann nicht zuzulassen, dass meine Freundin in dieser Situation "
     "allein bleibt",
     "Ich kann nicht zulassen, dass meine Freundin in dieser Situation "
     "allein bleibt",
     "после модального инфинитив без «zu»; примета блока 59 не видела "
     "этого, потому что приставка здесь сама «zu»"),
    (8525, "example_pl", "Nie możemy dopuścić do takiej sytuacji",
     "Nie mogę dopuścić, żeby moja przyjaciółka została sama w tej "
     "sytuacji",
     "перевод другого предложения"),
    # 11040 Promi
    (14793, "example_pl", "Celebryci pozują na czerwonym dywanie",
     "Celebryci spotykają się na czerwonym dywanie",
     "«pozują» вместо «treffen sich»"),
    # 11041 Streitigkeit
    (16884, "example_uk", "Суперечки між сусідами ставали дедалі гірше",
     "Суперечки між сусідами ставали дедалі гіршими",
     "«ставали гірше» — наречие вместо прилагательного"),
    (16884, "example_pl", "Ciągłe spory między sąsiadami męczą wszystkich",
     "Spory między sąsiadami stawały się coraz gorsze",
     "перевод другого предложения"),
    # 11042 abwegig
    (8526, "example_en",
     "His plan sounded completely absurd and unrealistic",
     "Your plan sounds completely absurd and unrealistic",
     "в эталоне «dein», и настоящее время"),
    (8526, "example_uk",
     "Його план звучав абсолютно абсурдно і нереалістично",
     "Твій план звучить абсолютно абсурдно і нереалістично",
     "в эталоне «dein», и настоящее время"),
    (8526, "example_tr",
     "Onun planı tamamen saçma ve gerçekçi olmayan görünüyordu",
     "Planın tamamen saçma ve gerçekçi olmayan görünüyor",
     "в эталоне «dein», и настоящее время"),
    (8526, "example_pl", "Ten pomysł jest zupełnie absurdalny",
     "Twój plan brzmi zupełnie absurdalnie i nierealistycznie",
     "перевод другого предложения"),
    # 11043 Diva
    (14794, "example_uk", "У короля багато років була коханка",
     "Дива відмовлялася працювати без свого особистого повара",
     "перевод совсем другого предложения"),
    (14794, "example_pl", "Ta diwa ma same kaprysy",
     "Diwa odmówiła pracy bez swojego osobistego kucharza",
     "перевод другого предложения"),
    # 11044 unrealistisch
    (8527, "example_tr",
     "Beklentilerin yaşın için tamamen gerçekçi değil",
     "Beklentilerin yaşına göre tamamen gerçekçi değil",
     "«yaşın için» — не то управление"),
    (8527, "example_pl", "Twoje plany są zupełnie nierealistyczne",
     "Twoje oczekiwania są zupełnie nierealistyczne na twój wiek",
     "«plany» вместо «Erwartungen», и потеряно «für dein Alter»"),
    # 11045 angezettelt — русское слово в украинской ячейке
    (8528, "example_uk",
     "Він розпочав всю цю ссору лише для уваги",
     "Він затіяв усю цю сварку лише щоб привернути увагу",
     "«ссора» — русское слово; в блоке 62 то же слово стояло "
     "наоборот — украинская «сварка» в русской ячейке"),
    (8528, "example_pl", "To on wszczął całą tę awanturę",
     "Wszczął całą tę kłótnię tylko po to, żeby zwrócić na siebie uwagę",
     "потеряно «nur um Aufmerksamkeit zu bekommen»"),
    # 11046 belauschen
    (14307, "example_tr",
     "Kapının arkasında iki adamın konuşmasını dinliyordu",
     "Kapının arkasında iki adamın konuşmasını gizlice dinledi",
     "«dinlemek» без «gizlice» теряет слово ряда"),
    # 11047 Leitartikel
    (14308, "example_uk", "Передова газети критикувала нову політику уряду",
     "Передовиця газети критикувала нову політику уряду",
     "в статье «передовиця»"),
    # 11048 Kondition
    (17885, "example_tr",
     "Yeni sözleşmenin şartları her iki taraf için kabul edilebiliydi",
     "Yeni sözleşmenin şartları her iki taraf için kabul edilebilirdi",
     "«edilebiliydi» — не та форма"),
    (17885, "example_pl", "Warunki tego kredytu są bardzo dobre",
     "Warunki nowej umowy były akceptowalne dla obu stron",
     "перевод другого предложения"),
    # 11049 reimen
    (14795, "example_uk", "Ці два слова ідеально римуються в пісні",
     "Ці два слова ідеально римуються для пісні",
     "«für das Lied» это для песни, а не в песне"),
    (14795, "example_pl", "Te dwa słowa ładnie się rymują",
     "Te dwa słowa idealnie się rymują w tej piosence",
     "потеряно «für das Lied»"),
    # 11052 Geschäftsführerin
    (9251, "example_uk",
     "Генеральна директриця вирішила, що офіс закриється з наступного "
     "тижня",
     "Директорка вирішила, що офіс закриється з наступного тижня",
     "«директриця» — не та форма, в статье «директорка»"),
    # 11056 desinfizieren
    (13104, "example_tr",
     "Yarayı dezenfekte etmesi gerekiyor, yoksa enfekte olur",
     "Yarayı dezenfekte etmek gerekiyor, yoksa enfekte olur",
     "«etmesi» это «он должен», а в эталоне «man muss»"),
    (13104, "example_pl", "Trzeba zdezynfekować ranę",
     "Trzeba zdezynfekować ranę, żeby się nie zakaziła",
     "потеряна вторая половина"),
    # 11057 Fehde
    (16885, "example_pl", "Między tymi rodzinami trwa stara waśń",
     "Stara waśń między dwiema rodzinami skończyła się dopiero po "
     "dziesięcioleciach",
     "перевод другого предложения"),
    # 11058 Filmmusik — тавтология в эталоне
    (14796, "example_de", "Die Filmmusik des Films war sehr spannend",
     "Die Filmmusik war sehr spannend",
     "«Filmmusik des Films» — одно и то же дважды"),
    (14796, "example_en", "The film music of the movie was very exciting",
     "The film music was very exciting",
     "вслед за исправленным эталоном"),
    (14796, "example_ru", "Киномузыка этого фильма была очень захватывающей",
     "Музыка из фильма была очень захватывающей",
     "вслед за исправленным эталоном"),
    (14796, "example_pl", "Muzyka filmowa w tym filmie jest świetna",
     "Muzyka filmowa była bardzo wciągająca",
     "та же тавтология, и время не то"),
    # 11059 angreifbar
    (8529, "example_en",
     "His argument was easily attackable and had many gaps",
     "His argument was easily assailable and had many gaps",
     "«attackable» о доводах не говорят"),
    (8529, "example_uk",
     "Його аргументація була легко піддатлива атаці і мала багато прогалин",
     "Його аргументація була легко вразлива і мала багато прогалин",
     "«піддатлива атаці» — разваленная фраза"),
    # 11060 Schuldner — эталон заменили после перевода
    (16886, "example_en",
     "The judge ordered that debtors be severely punished",
     "The debtor no longer pays his instalments",
     "перевод остался от прежнего эталона"),
    (16886, "example_ru",
     "Судья приказал, чтобы должники были строго наказаны",
     "Должник больше не платит свои взносы",
     "перевод остался от прежнего эталона"),
    (16886, "example_uk",
     "Суддя наказав, щоб боржники були суворо покарані",
     "Боржник більше не сплачує своїх внесків",
     "перевод остался от прежнего эталона"),
    (16886, "example_tr",
     "Hakim borçluların sert cezalandırılmasını emretti",
     "Borçlu artık taksitlerini ödemiyor",
     "перевод остался от прежнего эталона"),
    # 11061 Löffelchen
    (11990, "example_en", "The little spoon was too small for the soup",
     "The little spoon is too small for the soup",
     "эталон в настоящем времени"),
    (11990, "example_tr", "Küçük kaşık çorba için çok küçüktü",
     "Küçük kaşık çorba için çok küçük",
     "эталон в настоящем времени"),
    (11990, "example_pl", "Dodaj łyżeczkę cukru do herbaty",
     "Ta łyżeczka jest za mała do zupy",
     "перевод другого предложения"),
    # 11062 Töchterchen
    (15310, "example_tr", "Onun kızı bebeği tam beş yaşına girdi",
     "Onun küçük kızı henüz beş yaşına girdi",
     "«kızı bebeği» — два притяжательных подряд"),
    # 11064 Vibration
    (18083, "example_uk", "Вібрації машини невисліджувані",
     "Вібрації машини нестерпні",
     "«невисліджувані» — нет такого слова"),
    # 11065 durchwühlen
    (8530, "example_uk", "Я ройюся в ящику в пошуках ключів",
     "Я перериваю шухляду в пошуках ключів",
     "«ройюся» — нет такой формы"),
    (8530, "example_pl", "Przeszukałem całą szufladę w poszukiwaniu kluczy",
     "Przeszukuję szufladę w poszukiwaniu kluczy",
     "эталон в настоящем, и «całą» в нём нет"),
    # 11066 Anhang
    (8531, "example_uk", "Будь ласка, подивись додаток листа",
     "Будь ласка, подивись додаток до листа",
     "потеряно «до»"),
    (8531, "example_pl", "Wysłałem ci zdjęcia w załączniku",
     "Zobacz, proszę, załącznik do e-maila",
     "перевод другого предложения"),
    # 11068 geltend
    (16888, "example_pl", "To są obowiązujące przepisy w naszej firmie",
     "To obowiązująca zasada w naszym biurze",
     "в эталоне одно правило и офис, а не фирма"),
    # 11069 beleben
    (8533, "example_pl", "Kawa rano mnie ożywia",
     "Filiżanka kawy ożywia mnie z rana",
     "потеряно «eine Tasse»"),
    # 11070 Flugzeugträger
    (17385, "example_ru", "Авианосец находился в эксплуатации",
     "Авианосец был на задании",
     "«im Einsatz» это на задании, а не в эксплуатации"),
    (17385, "example_uk", "Авіаносець був у операції",
     "Авіаносець був на завданні",
     "«у операції» — разваленная фраза"),
    (17385, "example_pl", "Lotniskowiec wypłynął dziś z portu",
     "Lotniskowiec był w akcji",
     "перевод другого предложения"),
    # 11074 Befugnis
    (16889, "example_uk", "Офіцер діє лише в межах своїх повноважень",
     "Чиновник діє лише в межах своїх повноважень",
     "`Beamte` это чиновник, а не офицер"),
    # 11076 Elektrik
    (17723, "example_en", "The electrics are broken",
     "The electrics in the house are broken",
     "потеряно «im Haus»"),
    (17723, "example_uk", "Електрика несправна",
     "Електрика в будинку несправна",
     "потеряно «im Haus»"),
    (17723, "example_tr", "Elektrik tesisatı bozuk",
     "Evdeki elektrik tesisatı bozuk",
     "потеряно «im Haus»"),
    # 11082 Leichensack
    (13106, "example_tr", "Ceset bir ceset çantasına yerleştirildi",
     "Ceset bir ceset torbasına yerleştirildi",
     "в статье «ceset torbası»"),
    # 11083 schroff
    (11501, "example_uk", "Його відповідь була різка й недружелюбна",
     "Його відповідь була справді різка й непривітна",
     "потеряно «echt», и «недружелюбний» — русизм"),
    # 11084 Geldproblem
    (9942, "example_uk", "У нас є проблеми з грошима",
     "У нас зараз проблеми з грошима",
     "потеряно «gerade»"),
    # 11085 Wackelpudding
    (11992, "example_uk", "Діти люблять желе",
     "Діти дуже люблять желе",
     "потеряно «sehr gerne»"),
    # 11086 Pediküre
    (13107, "translation_pl", "pedikiur",
     "pedicure",
     "по-польски слово пишется «pedicure»"),
    (13107, "example_pl", "Idę dziś na pedikiur",
     "Idę dziś na pedicure",
     "по-польски слово пишется «pedicure»"),
    # 11087 Einigkeit — эталон заменили после перевода
    (11502, "example_en", "We can't reach agreement on this issue",
     "At last there is unity in the family",
     "перевод остался от прежнего эталона"),
    (11502, "example_uk", "У нас немає згоди з цього питання",
     "Нарешті в родині панує згода",
     "перевод остался от прежнего эталона"),
    (11502, "example_tr", "Bu konuda anlaşamıyoruz",
     "Sonunda ailede birlik var",
     "перевод остался от прежнего эталона"),
    # 11091 Dunst
    (15846, "example_ru", "Плотный туман висит над городом",
     "Плотная дымка висит над городом",
     "`Dunst` это дымка, туман это Nebel"),
    (15846, "example_uk", "Густий туман висить над містом",
     "Густа імла висить над містом",
     "`Dunst` это імла, туман это Nebel"),
    (15846, "example_tr", "Şehrin üzerinde kalın bir sis var",
     "Şehrin üzerinde yoğun bir pus var",
     "«sis» это туман, в статье «pus»"),
    # 11092 Anbau
    (2171, "example_uk", "Прибудова до дому дає більше місця",
     "Прибудова до будинку дає більше місця",
     "«до дому» это домой, а строение — «будинок»"),
    # 11093 Junggesellenparty — эталон заменили после перевода
    (12392, "example_en", "The bachelor party was Friday night",
     "The bachelor party was fun and lasted late into the night",
     "перевод остался от прежнего эталона"),
    (12392, "example_uk", "Холостяцька вечірка була в п'ятницю вечірою",
     "Холостяцька вечірка була весела й тривала до пізньої ночі",
     "перевод остался от прежнего эталона, и «вечірою» — не форма"),
    (12392, "example_tr", "Bekarlığa veda partisi cuma akşamıydı",
     "Bekarlığa veda partisi eğlenceliydi ve gece yarısına kadar sürdü",
     "перевод остался от прежнего эталона"),
    # 11094 Klitoris
    (13108, "example_tr",
     "Klitoris kadın cinsel yaşamında önemli bir rol oynamaktadır",
     "Klitoris kadın cinselliğinin önemli bir parçasıdır",
     "«rol oynamak» вместо «wichtiger Teil»"),
    (13108, "example_pl",
     "Lekarka wyjaśniła, gdzie znajduje się łechtaczka",
     "Łechtaczka jest ważną częścią kobiecej seksualności",
     "перевод другого предложения"),
    # 11096 Hagel
    (15847, "example_uk", "Йде град",
     "Іде сильний град",
     "потеряно «stark»"),
    # 11098 Kürbis
    (11993, "example_tr",
     "Sonbahar aylarında çorba için taze balkabak almayı seviyorum",
     "Sonbaharda çorba için taze balkabağı almayı seviyorum",
     "«balkabak» — не та форма"),
    (11993, "example_pl", "Na jesieni gotuję zupę z dyni",
     "Jesienią lubię kupować świeże dynie na zupę",
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
