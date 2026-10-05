"""
Сплошная вычитка, блок 34: ряды 5101–5300 по рангу частотности
(id первого 7381, id последнего 8951).

Главное за блок:

* `Base`, `auflösen`, `Kelch`, `wegrennen`, `kauen`, `engen`,
  `überstürzen`, `auffliegen` — ряды, где немецкий говорит одно, а
  половина языков другое. У `Base` английский перевёл «военная база
  хорошо защищена», украинский то же, турецкий «это чистящее средство
  содержит сильную щёлочь», а немецкий — «в лаборатории мы смешиваем
  кислоту и основание».
* `Luftwaffe` — русский пример про люфтваффе и Германию, при немецком
  «воздушное пространство страны» вообще.
* `I was at my moms` — притяжательное без апострофа.
* Турецкие небывальщины: `oturak` вместо `puf`, `hayal görür`,
  `teknesiyi`, `eminiyim`, `Kafeteriada`.
* Украинские русизмы и опечатки: `скалу`, `пойдемо`, `хвальбиця`,
  `настороживає`, `накаже учнів`, `прокляний`, `важного листа`,
  `стакан`, `в північ`.

    python -m app.scripts.fix_block_0034            # показать
    python -m app.scripts.fix_block_0034 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- Base: три языка про другое ------------------------------------------
    (15094, "example_en", "The military base is well protected",
     "In the lab we mix acid and base",
     "немецкий «Im Labor mischen wir Säure und Base»"),
    (15094, "example_uk", "Військова база добре захищена",
     "У лабораторії ми змішуємо кислоту і луг", "то же"),
    (15094, "example_tr", "Bu temizleyici güçlü bir baz içeriyor",
     "Laboratuvarda asit ve baz karıştırıyoruz", "то же"),

    # --- auflösen, Kelch, auffliegen -----------------------------------------
    (7395, "example_en", "Dissolve the tablet in warm water",
     "The sugar dissolves in water",
     "немецкий «Der Zucker löst sich im Wasser auf»"),
    (7395, "example_uk",
     "Ми повинні вирішити проблему, перш ніж буде занадто пізно",
     "Цукор розчиняється у воді", "то же"),
    (7395, "example_tr", "Çok geç olmadan önce sorunu çözmemiz gerekiyor",
     "Şeker suda çözünüyor", "то же"),
    (14531, "example_en", "The goblet was made of gold",
     "The chalice was handed to the priest",
     "немецкий «Der Kelch wurde dem Priester gereicht»"),
    (14531, "example_uk", "Він підняв чашу з вином",
     "Чашу подали священнику", "то же"),
    (14531, "example_tr", "Kadehi altından yapılmıştır",
     "Kadeh rahibe uzatıldı", "то же"),
    (16312, "example_en", "The fraud was exposed when the police arrived",
     "Soon the whole fraud will be exposed",
     "немецкий «Bald wird der ganze Schwindel auffliegen»"),
    (16312, "example_ru", "Мошенничество раскрылось, когда пришла полиция",
     "Скоро всё это мошенничество раскроется", "то же"),
    (16312, "example_uk", "Шахрайство розкрилось, коли прийшла поліція",
     "Скоро все це шахрайство розкриється", "то же"),
    (16312, "example_tr", "Dolandırıcılık polis geldiğinde ortaya çıktı",
     "Yakında bütün dolandırıcılık ortaya çıkacak", "то же"),

    # --- wegrennen, kauen, engen, überstürzen --------------------------------
    (7385, "example_en", "The child ran away when it saw the dog",
     "The dog runs away out of fear",
     "немецкий «Der Hund rennt vor Angst weg»"),
    (7385, "example_uk", "Дитина втекла, коли побачила собаку",
     "Собака тікає від страху", "то же"),
    (7385, "example_tr", "Çocuk köpeği gördüğünde kaçıp gitti",
     "Köpek korkudan kaçıyor", "то же"),
    (11771, "example_en", "The baby is chewing on his toy",
     "You have to chew more slowly",
     "немецкий «Du musst langsamer kauen»"),
    (11771, "example_uk", "Жуй повільніше, не поспішай",
     "Ти повинен жувати повільніше", "то же"),
    (11771, "example_tr", "Bebek oyuncağını çiğniyor",
     "Daha yavaş çiğnemelisin", "то же"),
    (11771, "example_pl", "Żuje gumę na lekcji",
     "Musisz żuć wolniej", "то же"),
    (7401, "example_en", "The street narrows significantly here",
     "These new shoes pinch my toes",
     "немецкий «Diese neuen Schuhe engen meine Zehen»"),
    (7401, "example_uk", "Вулиця сильно звужується тут",
     "Ці нові туфлі тиснуть мені пальці", "то же"),
    (10692, "example_en", "Don't rush, think first",
     "We shouldn't rush anything",
     "немецкий «Wir sollten nichts überstürzen»"),
    (10692, "example_uk", "Не поспішай, подумай спочатку",
     "Нам не варто з цим поспішати", "то же"),
    (10692, "example_tr", "Acele etme, önce düşün",
     "Hiçbir şeyi acele etmemeliyiz", "то же"),

    # --- Luftwaffe, Vormittag, Flugplatz, höchstwahrscheinlich ---------------
    (16310, "example_ru",
     "Люфтваффе защищали воздушное пространство Германии",
     "Военно-воздушные силы защищают воздушное пространство страны",
     "немецкий про страну вообще, а не про Германию"),
    (7402, "example_en", "He's very likely to be late",
     "He most likely won't come today",
     "немецкий «Er kommt höchstwahrscheinlich heute nicht»"),
    (7402, "example_uk", "Дуже імовірно, що буде дощ",
     "Він найімовірніше сьогодні не прийде", "то же"),
    (17192, "example_en", "My plane takes off from the airfield in an hour",
     "The plane takes off from the airfield in an hour",
     "немецкий «Das Flugzeug», а не «мой самолёт»"),
    (17192, "example_ru", "Мой самолёт вылетает с аэродрома через час",
     "Самолёт вылетает с аэродрома через час", "то же"),
    (17192, "example_uk", "Мій літак вилітає з аеродрому через годину",
     "Літак вилітає з аеродрому через годину", "то же"),
    (17192, "example_tr", "Uçağım hava alanından bir saat içinde kalkıyor",
     "Uçak havaalanından bir saat içinde kalkıyor",
     "то же, и «hava alanı» пишется слитно"),

    # --- английский апостроф -------------------------------------------------
    (13539, "example_en",
     "I was at my moms, and in the meantime my brother called me",
     "I was at my mom's, and in the meantime my brother called me",
     "пропущен апостроф притяжательного"),

    # --- немецкий эталон -----------------------------------------------------

    # --- украинские русизмы и опечатки ---------------------------------------
    (15565, "example_uk", "Корабель наскочив на скалу",
     "Корабель наскочив на скелю", "«скала» — русское слово"),
    (9819, "example_uk", "Завтра ми пойдемо по магазинах",
     "Завтра ми підемо по магазинах", "«пойдемо» — русская форма"),
    (10690, "example_uk", "Він хвальбиця, який завжди хвалиться",
     "Він хвалько, який завжди хвалиться", "«хвальбиця» — не слово"),
    (7387, "example_uk", "Він настороживає вуха, щоб краще чути",
     "Він насторожує вуха, щоб краще чути", "«настороживає» — не форма"),
    (16313, "example_uk", "Школа накаже учнів за поведінку",
     "Школа покарає учнів за поведінку", "«накаже» значит «прикажет»"),
    (14078, "example_uk", "Цей прокляний комп'ютер не працює",
     "Цей проклятий комп'ютер не працює", "«прокляний» — опечатка"),
    (14082, "example_uk", "Я отримав важного листа на електронну пошту",
     "Я отримав важливого листа на електронну пошту",
     "«важного» — русская форма"),
    (11774, "example_uk", "Кожного ранку я п'ю стакан апельсинового соку",
     "Кожного ранку я п'ю склянку апельсинового соку", "«стакан» — русизм"),
    (17573, "example_uk", "Сигналізація спрацьовує кожної ночі в північ",
     "Сигналізація спрацьовує кожної ночі опівночі", "«в північ» — не форма"),
    (11770, "example_uk", "Я люблю пити гарячий какао вранці",
     "Я люблю пити гаряче какао вранці", "«какао» среднего рода"),
    (7386, "example_uk", "Він мовчки вийшов із кімнати",
     "Він безшумно увійшов до кімнати",
     "«betrat» — вошёл, и «мовчки» не про шум"),
    (15102, "example_uk", "Усиновлення дитини був великим кроком",
     "Усиновлення дитини було великим кроком", "род не согласован"),
    (18763, "example_uk", "Була довга переривання в програмі",
     "Була довга перерва в програмі", "род не согласован"),
    (7381, "translation_uk", "пуф, публічний дім, штовхання, хлопок",
     "пуф, публічний дім, штовхання, глухий удар",
     "«хлопок» — русское слово"),
    (7382, "example_uk", "Місцеві влади це розслідували",
     "Місцева влада це розслідувала", "«влади» во множественном"),
    (14073, "example_uk", "Я тобі явно сказав не приходити",
     "Я тобі чітко сказав не приходити", "в значениях «чітко»"),
    (12693, "example_uk", "Кривавий перев'язок потрібно змінити",
     "Кривавий бинт потрібно змінити", "«перев'язок» — не то слово"),
    (16311, "example_uk", "Він контрабандно ввіз сигарети через кордон",
     "Він провіз сигарети через кордон контрабандою", "калька"),
    (2462, "example_uk", "Це відбувається дуже швидко",
     "Це відбувається дуже швидко, не хвилюйся", "потеряна вторая половина"),
    (14526, "example_uk", "Капелан розмовляє з вірними",
     "Капелан розмовляє з вірянами в церкві", "потеряна церковь"),
    (14528, "example_uk", "Священник благословляє громаду",
     "Священник благословив громаду", "в немецком прошедшее время"),
    (10695, "example_uk", "Він тримає образу на свого брата",
     "Він затаїв образу на свого брата", "«тримати образу» — калька"),
    (10697, "example_uk", "У нього добре судження для таких ситуацій",
     "У нього добра розсудливість у таких ситуаціях", "калька"),
    (14533, "example_uk", "Він добре може грати на сцені",
     "Він добре вміє грати", "сцена приписана"),
    (7398, "example_uk", "Мені треба точити ніж перед готуванням",
     "Мені треба наточити ніж перед готуванням", "вид глагола"),
    (7399, "example_uk", "Ну ти й заварив кашу!",
     "Ну ти й заварив кашу своєю ідеєю!", "потеряна идея"),
    (17568, "example_uk", "Я повинен накачувати повітря в шину",
     "Я повинен накачати повітря в шину", "вид глагола"),
    (8944, "example_uk", "Берегова охорона рятувала човен з води",
     "Берегова охорона врятувала човен з води", "вид глагола"),
    (15099, "example_uk", "Жебрак сидів на вулиці й просив гроші",
     "Жебрак сидів на вулиці й просив грошей", "падеж"),
    (10700, "example_uk", "Я не впевнений, чи він прийде",
     "У мене немає певності, чи він прийде", "потеряно само слово"),
    (10706, "example_uk", "Я не хочу піддаватися і змінювати свою думку",
     "Я не поступаюся і не змінюю своєї думки", "«не хочу» приписано"),
    (13540, "example_uk", "Ти повинен йти тепер, інакше ти пропустиш поїзд",
     "Ти повинен йти зараз, інакше ти пропустиш поїзд", "«тепер» — не то"),
    (17193, "example_uk", "Я маю швидко заправитися перед тим як виїхати",
     "Я маю швидко заправитися, перед тим як виїхати", "пропущена запятая"),

    # --- русские -------------------------------------------------------------
    (16311, "example_ru", "Он контрабандировал сигареты через границу",
     "Он провёз сигареты через границу контрабандой", "калька"),
    (17191, "example_ru", "Бензин снова дорожает",
     "Бензин снова подорожал", "в немецком совершённое действие"),
    (10697, "example_ru", "У него хорошее здравое суждение в таких ситуациях",
     "У него хорошая рассудительность в таких ситуациях", "канцелярит"),
    (14533, "example_ru", "Он хорошо умеет играть на сцене",
     "Он хорошо умеет играть", "сцена приписана"),

    # --- турецкие небывальщины и падежи --------------------------------------
    (7381, "example_tr", "Rahat oturak üzerine otur", "Rahat pufa otur",
     "«oturak» — это горшок"),
    (14535, "example_tr", "Birçok insan ölümsüzlüğü hayal görür",
     "Birçok insan ölümsüzlüğü hayal eder", "«hayal görmek» — не форма"),
    (8944, "example_tr", "Sahil güvenlik, teknesiyi sudan kurtardı",
     "Sahil güvenlik tekneyi sudan kurtardı", "«teknesiyi» — опечатка"),
    (10693, "example_tr", "Kazanacağımızdan eminiyim",
     "Kazanacağımızdan eminim", "«eminiyim» — опечатка"),
    (11772, "example_tr", "Kafeteriada öğlen yemeği yiyoruz",
     "Kafeteryada öğlen yemeği yiyoruz", "«Kafeteriada» — опечатка"),
    (17568, "example_tr", "Lastik içine hava pompalamam gerekiyor",
     "Lastiğe hava pompalamam gerekiyor", "«lastik içine» — калька"),
    (18256, "example_tr", "Ev sahibi kiraları yükseltti, bu adil değil",
     "Ev sahibi kirayı yükseltti, bu adil değil", "число"),
    (15100, "example_tr", "Parmağında altın evlilik yüzüğü taşıyor",
     "Parmağında altın bir alyans takıyor", "«yüzük taşımak» — не форма"),
    (14537, "example_tr", "Kahin gelecek görebileceğini iddia etti",
     "Medyum geleceği görebileceğini iddia etti", "пропущен винительный"),
    (16322, "example_tr", "Vekil parlamentoda konuştu",
     "Milletvekili parlamentoda konuştu", "«vekil» — слишком общее"),
    (17574, "example_tr", "Uydu Dünyanın etrafında dönüyor",
     "Uydu Dünya'nın etrafında dönüyor", "имя собственное берёт апостроф"),
    (15570, "example_tr", "İnsan Tanrının yaratılışıdır",
     "İnsan, Tanrı'nın bir yaratığı", "апостроф и «-dır»"),
    (179, "example_tr", "Bir diyalogu çalışıyorlar",
     "Bir diyalog çalışıyorlar", "лишний определённый падеж"),
    (14080, "example_tr", "Lütfen tuzunu bana verir misin?",
     "Lütfen tuzu bana uzatır mısın?", "«tuzunu» — твою соль"),
    (14536, "example_tr", "Bu konu bu ailede tabudur",
     "Bu konu ailede tabu", "«bu» дважды и «-dur»"),
    (16315, "example_tr", "Bu ciddi bir suçtur", "Bu ciddi bir suç",
     "«-tur»"),
    (14529, "example_tr", "Bu imanın bir meselesidir",
     "Bu bir inanç meselesi", "то же"),
    (7394, "example_tr", "Bebek beş kilogram ağırlığındadır",
     "Bebek beş kilo", "то же"),
    (14532, "example_tr", "O çok yaratıcı bir insandır",
     "O çok yaratıcı bir insan", "то же"),
    (10697, "example_tr", "Böyle durumlarda onun muhakemesi çok iyidir",
     "Böyle durumlarda muhakemesi çok iyi", "то же"),
    (10709, "example_tr", "Bu soğukkanlı bir karar olmuştur",
     "Bu soğukkanlı bir karardı", "«olmuştur» — канцелярит"),
    (7392, "example_tr", "Bunu yapmaya muktedirim",
     "Bunu yapabilecek durumdayım", "«muktedir» — книжное"),
    (7393, "example_tr", "Eski ev gittikçe bozuluyor",
     "Eski ev gittikçe harap oluyor", "«bozulmak» — сломаться"),
    (15096, "example_tr", "Düğünde sağdıcım en yakın arkadaşımdı",
     "Kardeşim benim sağdıcımdı",
     "немецкий «Mein Bruder war mein Trauzeuge»"),
    (7382, "example_tr", "Yerel otoriteler müdahale etti",
     "Yerel yetkililer bunu araştırdı",
     "«müdahale etti» — вмешались, а не расследовали"),
    (14073, "example_tr", "Sana açıkça gelme dediğimi söyledim",
     "Sana açıkça gelmemeni söyledim", "фраза собрана дважды"),
    (2462, "example_tr", "Bu çok hızlı olacak",
     "Bu çok hızlı olur, endişelenme", "потеряна вторая половина"),
    (995, "example_tr", "Sabah ben serbestim",
     "Öğleden önce boşum", "«serbest» — освобождённый, и лишнее «ben»"),
    (15095, "example_tr", "Yaşlı satranç oynamayı seviyor",
     "Yaşlı adam satranç oynamayı seviyor", "потеряно подлежащее"),
    (10690, "example_tr", "Övüngen biriyle konuşmak çok yorucu",
     "O, hep övünen bir havalı tip",
     "немецкий «Er ist ein Angeber, der immer prahlt»"),
    (14526, "example_tr", "Din görevlisi inananlarla konuşuyor",
     "Papaz yardımcısı kilisede inananlarla konuşuyor", "потеряна церковь"),
    (12693, "example_tr", "Kanlı bandaj değiştirilmesi gerekiyor",
     "Kanlı bandajın değiştirilmesi gerekiyor", "пропущен родительный"),
    (17570, "example_tr", "Kitap basılı ve şimdi hazır",
     "Kitap basılı ve 12 euro", "в немецком цена, а не готовность"),
    (12695, "example_tr", "O dilsiz ve konuşamıyor",
     "Bu 1920'lerden kalma sessiz bir film",
     "немецкий «Das ist ein stummer Film aus den 1920ern»"),
    (7399, "example_tr", "Bu yalan başını belaya sokacak",
     "Fikrinle başımı belaya soktun",
     "немецкий «Du hast mir ja was Schönes eingebrockt»"),
    (14077, "example_tr", "Trafikte sürekli küfrediyor",
     "Bir şey ters gittiğinde her zaman küfreder",
     "немецкий «Er flucht immer, wenn etwas schiefgeht»"),
    (11773, "example_tr", "Sarhoş olmak istemiyordu ama sonunda çok fazlaydı",
     "Sarhoş olmak istemiyordu ama sonunda çok fazla içti",
     "фраза не собрана"),
    (10700, "example_tr", "Geleceğinden emin değilim",
     "Geleceği konusunda kesinlik yok", "потеряно само слово"),
    (10706, "example_tr", "Bu konuda asla boyun eğmeyeceğim",
     "Boyun eğmiyorum ve fikrimi değiştirmiyorum",
     "немецкий «Ich gebe nicht nach und ändere meine Meinung nicht»"),
    (10707, "example_tr", "Planların hakkında netlik gerekiyor",
     "Planların konusunda netliğe ihtiyacım var", "«hakkında» требует другого"),
    (15101, "example_tr", "Dün ilginç bir tanışıklık yaptım",
     "Dün ilginç biriyle tanıştım", "«tanışıklık yapmak» — не форма"),
    (14079, "example_tr", "Kahve üzerinde güzel bir sohbet yaptık",
     "Kahve içerken güzel bir sohbet ettik", "«kahve üzerinde» — калька"),
    (17573, "example_tr", "Alarm sistemi her gece gece yarısında çalıyor",
     "Alarm sistemi her gece yarısı çalıyor", "«gece» дважды"),
    (8946, "example_tr", "Çalışan büyük bir ofiste çalışıyor",
     "Memur büyük bir ofiste görev yapıyor", "«çalışan çalışıyor» — дважды"),
    (8943, "example_tr", "Polis rozeti üniformasında gurur ile taşıyor",
     "Polis rozetini üniformasında gururla taşıyor", "падеж и «gurur ile»"),

    # --- потерянное и приписанное --------------------------------------------
    (14072, "example_en", "I need some information",
     "I need information about the opening hours",
     "потеряны часы работы"),
    (1764, "example_en", "Planning is important",
     "Planning the project is very important", "потерян проект"),
    (14528, "example_en", "The priest blesses the congregation",
     "The priest blessed the congregation", "в немецком прошедшее время"),
    (14526, "example_en", "The chaplain talks to the believers",
     "The chaplain talks to the believers in the church",
     "потеряна церковь"),
    (11770, "example_pl", "Dzieci piją ciepłe kakao na śniadanie",
     "Lubię pić gorące kakao rano",
     "немецкий «Ich trinke gerne heißen Kakao am Morgen»"),
    (262, "example_pl", "W święto sklepy są zamknięte",
     "W święto nie pracujemy",
     "немецкий «Am Feiertag arbeiten wir nicht»"),
    (16318, "example_pl", "Snajper leżał na dachu budynku",
     "Snajper był rozmieszczony na dachu", "«leżał» — не то же"),
    (16319, "example_pl", "Muszę iść do konsulatu po paszport",
     "Muszę iść do konsulatu, żeby złożyć wniosek o paszport",
     "потеряна подача заявления"),
    (16321, "example_pl", "Zgłosiłem kradzież na komisariacie",
     "Komisariat jest blisko mojego domu",
     "немецкий «Das Polizeirevier ist in der Nähe meines Hauses»"),
    (819, "example_uk", "Мій тесть любить рибалку",
     "Тесть допомагає в саду",
     "немецкий «Der Schwiegervater hilft im Garten»"),
    (16322, "example_pl", "Poseł odpowiadał na pytania dziennikarzy",
     "Poseł mówił w parlamencie",
     "немецкий «Der Abgeordnete sprach im Parlament»"),
    (12212, "example_pl", "Spotkajmy się w barze po pracy",
     "Na tej ulicy jest wiele barów",
     "немецкий «Es gibt viele Bars in dieser Straße»"),
    (11774, "example_pl", "Na śniadanie piję sok pomarańczowy",
     "Każdego ranka piję szklankę soku pomarańczowego",
     "потерян стакан и каждое утро"),
    (13540, "example_pl", "Pośpiesz się, w przeciwnym razie spóźnimy się",
     "Musisz teraz iść, w przeciwnym razie spóźnisz się na pociąg",
     "немецкий про поезд"),
    (15569, "example_tr", "Otelin yatağında tahtakurusu varmış",
     "Otelin yatağında bir tahtakurusu vardı", "«varmış» — пересказ"),
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
