"""
Сплошная вычитка, блок 33: ряды 4901–5100 по рангу частотности
(id первого 14062, id последнего 16309).

Главное за блок:

* `Heute is unser Jahrestag` — в немецком эталоне `is` вместо `ist`.
* `ausbrechen`, `nahen`, `erwachen`, `Mehl`, `willens`, `allerseits`,
  `nachgehen`, `dastehen`, `fügen` — ряды, где немецкий говорит одно, а
  четыре языка переводят другое. У `ausbrechen` немецкий про «вот-вот
  расплачется», а английский, русский, украинский и турецкий — про
  войну, которая вспыхнула.
* `Sauerei` — турецкий пример про загрязнение воздуха в городе, к слову
  «свинство» отношения не имеющий вовсе.
* `Kreislauf` — русское «Круговорот природы фасцинирует»: слова
  «фасцинировать» в русском нет.
* Турецкие небывальщины: `kan banyo`, `pire` на месте `lapa`, `kap`
  вместо `kasket`, `fındık` вместо `kuruyemiş`.
* Украинское `позвоночник` в значениях к `Rückgrat` и `стержень` в
  примере — оба русские слова.

    python -m app.scripts.fix_block_0033            # показать
    python -m app.scripts.fix_block_0033 --apply    # применить
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
    (18755, "example_de", "Heute is unser Jahrestag",
     "Heute ist unser Jahrestag", "«is» вместо «ist»"),
    (18757, "example_de", "Jedes Mal wenn ich dich seh, lächelst du",
     "Jedes Mal wenn ich dich sehe, lächelst du", "«seh» — усечение"),
    (7370, "example_de", "Lass mich, ich zieh mir gerade einen Film rein",
     "Lass mich, ich ziehe mir gerade einen Film rein",
     "«zieh» — усечение при строчном «ich»"),
    (7366, "example_de", "Das ist eine wahrhaft schöne Geschichte",
     "Das ist eine wahrhaftig schöne Geschichte",
     "в примере «wahrhaft», а слово ряда «wahrhaftig»"),

    # --- ausbrechen: четыре языка про войну ----------------------------------
    (16302, "example_en", "The war suddenly broke out",
     "She could burst into tears at any moment",
     "немецкий «Sie könnte jeden Moment in Tränen ausbrechen»"),
    (16302, "example_ru", "Война внезапно вспыхнула",
     "Она в любой момент может разрыдаться", "то же"),
    (16302, "example_uk", "Війна раптово спалахнула",
     "Вона будь-якої миті може розплакатися", "то же"),
    (16302, "example_tr", "Savaş aniden patladı",
     "Her an gözyaşlarına boğulabilir", "то же"),

    # --- nahen, erwachen, Mehl, willens --------------------------------------
    (7360, "example_en", "Winter is approaching, we need to hurry",
     "The summer holidays are finally approaching",
     "немецкий «Die Sommerferien nahen endlich»"),
    (7360, "example_uk", "Зима наближається, нам треба поспішати",
     "Літні канікули нарешті наближаються", "то же"),
    (7360, "example_tr", "Kış yaklaşıyor, hızlanmamız gerekiyor",
     "Yaz tatili sonunda yaklaşıyor", "то же"),
    (7367, "example_en", "I wake up every morning at seven",
     "The children wake up at first light",
     "немецкий «Die Kinder erwachen beim ersten Licht»"),
    (7367, "example_uk", "Я прокидаюся кожного ранку о сьомій",
     "Діти прокидаються з першими променями світла", "то же"),
    (7367, "example_tr", "Her sabah saat yedide uyanırım",
     "Çocuklar ilk ışıkta uyanır", "то же"),
    (579, "example_en", "She buys flour", "I need flour for baking",
     "немецкий «Ich brauche Mehl zum Backen»"),
    (579, "example_uk", "Вона купує борошно",
     "Мені потрібне борошно для випічки", "то же"),
    (579, "example_tr", "Un alıyor", "Pişirmek için un gerekiyor", "то же"),
    (10685, "example_en", "Are you willing to help me",
     "I am willing to help you",
     "немецкий «Ich bin willens, dir zu helfen»"),
    (10685, "example_uk", "Ти готовий мені допомогти",
     "Я готовий тобі допомогти", "то же"),
    (10685, "example_tr", "Bana yardım etmeye istekli misin",
     "Sana yardım etmeye istekliyim", "то же"),

    # --- allerseits, nachgehen, dastehen, fügen ------------------------------
    (14063, "example_en", "All the best in your new job!",
     "Good morning everyone", "немецкий «Guten Morgen allerseits»"),
    (14063, "example_uk", "Всього найкращого тобі й родині!",
     "Доброго ранку всім", "то же"),
    (14063, "example_tr", "Herkese iyi geceler!", "Herkese günaydın",
     "то же"),
    (7330, "example_en", "I'll look into the problem tomorrow",
     "I'll look into the matter",
     "немецкий «Ich werde der Sache nachgehen»"),
    (7330, "example_uk", "Він займається своєю пристрастю",
     "Я розберуся в цій справі", "то же"),
    (7330, "example_tr", "Tutkusunun peşinden gidiyor",
     "Bu meseleyi araştıracağım", "то же"),
    (7331, "example_en", "He stood there and didn't know what to do",
     "I don't want to look stupid",
     "немецкий «Ich will nicht dumm dastehen»"),
    (7331, "example_uk", "Він стояв і не знав, що робити",
     "Я не хочу виглядати дурнем", "то же"),
    (7331, "example_tr", "Orada durdu ve ne yapacağını bilmedi",
     "Aptal görünmek istemiyorum", "то же"),
    (7358, "example_en", "Everything fits together wonderfully",
     "The puzzle pieces fit together",
     "немецкий «Die Puzzleteile fügen sich zusammen»"),
    (7358, "example_uk", "Все чудово збігається",
     "Частини пазла складаються разом", "то же"),
    (7358, "example_tr", "Her şey harika şekilde uyuşuyor",
     "Yapboz parçaları birbirine uyuyor", "то же"),

    # --- Sauerei: турецкий про загрязнение воздуха ---------------------------
    (10667, "example_tr", "Şehirde hava kirliliği çok arttı",
     "Burası tam bir pislik",
     "немецкий «Das ist ja eine Sauerei hier»"),
    (10667, "example_uk", "Та яка це бруд", "Ну й свинство тут!",
     "фраза не собрана, и род"),

    # --- русские -------------------------------------------------------------
    (15558, "example_ru", "Круговорот природы фасцинирует",
     "Круговорот природы завораживает", "«фасцинировать» — не русское слово"),
    (16299, "example_ru", "Кровавая баня на войне была ужасна",
     "Кровавая бойня на войне была ужасна",
     "в значениях первое «кровавая бойня»"),
    (18250, "example_ru", "Мне нужно почистить дом перед гостями",
     "Мне нужно почистить дом", "гости приписаны"),
    (15557, "example_ru", "Кони начали ржать в конюшне",
     "Конь громко ржёт", "немецкий «Das Pferd wiehert laut»"),
    (16297, "example_ru", "Забитое животное лежало на полу",
     "Забитое животное лежало на земле", "«auf dem Boden» — на земле"),
    (17188, "example_ru", "Рецепция на первом этаже",
     "Рецепция отеля на первом этаже", "потерян отель"),
    (18754, "example_ru", "Я работал неделями",
     "Я неделями работал тяжело", "потеряно «hart»"),

    # --- украинские опечатки и русизмы ---------------------------------------
    (12686, "translation_uk",
     "хребет, позвоночник, стержень, твердість характеру",
     "хребет, кістяк, стрижень, твердість характеру",
     "«позвоночник» и «стержень» — русские слова"),
    (12686, "example_uk", "У нього немає стержня, немає мужності",
     "У нього немає стрижня, немає мужності", "«стержень» — русизм"),
    (1960, "translation_uk", "тонна, бак для смітт, бочка",
     "тонна, бак для сміття, бочка", "«смітт» — обрывок"),
    (10666, "example_uk", "Це поведінка була просто жахливою",
     "Ця поведінка була просто жахливою", "род не согласован"),
    (16295, "example_uk", "Домагання на роботі повинне припинитися",
     "Домагання на роботі повинні припинитися", "число не согласовано"),
    (10670, "example_uk", "Будь ласка, відніся до цього конфіденційно",
     "Будь ласка, постався до цього делікатно", "«віднестися» — русизм"),
    (14064, "example_uk", "Похвала вчителя дуже обрадувала мене",
     "Похвала вчителя дуже мене порадувала", "«обрадувати» — русизм"),
    (9813, "example_uk", "Задаток за автомобіль становить 5000 євро",
     "Завдаток за автомобіль становить 5000 євро",
     "в значениях «завдаток»"),
    (7332, "example_uk", "Собаку залишили, і вона мала сама себе харчувати",
     "Собаку покинули, і вона мала сама про себе дбати",
     "«harchувати» — кормить; в немецком заботиться"),
    (12678, "example_uk", "Важливо використовувати кондом під час сексу",
     "Важливо використовувати презерватив під час сексу",
     "в значениях первое «презерватив»"),
    (15087, "example_uk", "Моя невістка чудово готує", "Моя невістка мила",
     "немецкий «Meine Schwägerin ist nett»"),
    (11762, "example_uk",
     "М'ясо було занадто жорстким для того, щоб його їсти",
     "М'ясо було занадто жорстке, щоб його їсти", "канцелярит"),
    (15088, "example_uk", "Він ударився потилицею",
     "Він травмував потилицю", "«verletzt» — травмировал"),
    (7351, "example_uk", "Я обійдуся без твоєї допомоги",
     "Мені вистачає моєї зарплати",
     "немецкий «Ich komme mit meinem Gehalt aus»"),
    (2205, "example_uk", "Він сьогодні якийсь дратівливий",
     "Це справді досадно", "немецкий «Das ist echt ärgerlich»"),
    (7345, "example_uk", "Ми живемо у східній частині міста",
     "Це розташовано на схід звідси",
     "немецкий «Das liegt östlich von hier»"),
    (1101, "example_uk", "Я знімаю гроші в банкоматі",
     "Я хочу зняти 100 євро", "немецкий «Ich möchte 100 Euro abheben»"),
    (7361, "example_uk", "На вулиці гримить, буде гроза",
     "З кухні чути гуркіт!", "немецкий «Es poltert aus der Küche!»"),
    (8936, "example_uk", "Він втратив засоби до існування",
     "Він заробляє на життя вчителем",
     "немецкий «Er verdient seinen Lebensunterhalt als Lehrer»"),
    (7353, "example_uk", "Паркан вільний, нам потрібно його відремонтувати",
     "Паркан розхитаний, нам потрібно його відремонтувати",
     "«вільний» — не то значение"),
    (13689, "example_uk", "На вечір в опері надівають чорний смокінг",
     "На гала-вечір надівають чорний смокінг", "в немецком гала-вечер"),
    (7365, "example_uk", "Якими ресурсами ти маєш?",
     "Якими ресурсами ти розпоряджаєшся?", "«мати» не берёт этот падеж"),
    (7368, "example_uk", "Я швидко охоплю ситуацію",
     "Я швидко розумію ситуацію", "«охопити ситуацію» — калька"),
    (17565, "example_uk", "Я повинен сканувати фотографії",
     "Мені потрібно відсканувати фотографії", "вид глагола"),
    (10679, "example_uk", "Він був дратівливий, тому що погано спав",
     "Він був роздратований, тому що погано спав",
     "«дратівливий» — свойство, а не состояние"),
    (18760, "example_uk", "Виключно сьогодні ми на відпустці",
     "Як виняток ми сьогодні відпочиваємо",
     "«виключно» — только, а не в порядке исключения"),
    (10683, "example_uk", "Він просив у мене послугу",
     "Він просив у мене прихильності", "в значениях «прихильність»"),
    (7374, "example_uk", "У мене є запас грошей",
     "У мене є ще трохи грошей у запасі", "потеряно «etwas»"),
    (16301, "example_uk", "Шеф вимагає звіту про брак документів",
     "Шеф вимагає звіту за відсутні документи",
     "«брак документів» — нехватка, а не отсутствующие"),
    (7362, "example_uk", "Можеш мені це показати?",
     "Можеш показати мені, як це робиться?", "потеряно «как»"),
    (7364, "example_uk", "Згинай папір обережно",
     "Зігни папір обережно!", "вид глагола и знак"),
    (7370, "example_uk", "Лиш мене в спокої, я зараз дивлюся фільм",
     "Облиш мене, я саме дивлюся фільм", "«Лиш мене в спокої» — калька"),
    (7354, "example_uk", "Входи, ми як раз у вітальні",
     "Заходь, ми саме у вітальні", "«як раз» — русизм"),
    (16299, "example_uk", "Кривава баня на війні була жахливою",
     "Кровопролиття на війні було жахливим",
     "«кривава баня» — калька"),
    (16297, "example_uk", "Забита тварина лежала на підлозі",
     "Забита тварина лежала на землі", "«auf dem Boden» — на земле"),
    (18250, "example_uk", "Я повинен чистити будинок",
     "Мені потрібно почистити будинок", "вид глагола"),
    (11766, "example_uk", "До картопляної соломки я хочу кетчуп",
     "До картоплі фрі я хочу кетчуп", "«картопляна соломка» — не то"),
    (9815, "example_uk", "Можеш ти мені позичити п'ять євро?",
     "Можеш позичити мені п'ять євро?", "порядок слов"),

    # --- турецкие небывальщины и падежи --------------------------------------
    (16299, "example_tr", "Savaştaki kan banyo korkunç idi",
     "Savaştaki kan gölü korkunçtu", "«kan banyo» — не слово"),
    (11760, "example_tr", "Bebek için pire sıcak olmalı",
     "Bebek için lapa sıcak olmalı", "«pire» — блоха"),
    (13688, "example_tr", "Siyah bir kap takıyor",
     "Siyah bir kasket takıyor", "«kap» — посуда"),
    (2691, "example_tr", "Fındık yemeyi severim",
     "Kuruyemiş yemeyi severim", "«fındık» — только лесной орех"),
    (11761, "example_tr", "Lütfen büyük bir pasta porsiyonu istiyorum",
     "Lütfen büyük bir makarna porsiyonu istiyorum",
     "по-турецки «pasta» — торт"),
    (10664, "example_tr", "İçimde ani bir kaçma dürtüsü doğdu",
     "İçimde ani bir dans etme dürtüsü doğdu",
     "«kaçma» — убежать; в немецком танцевать"),
    (16303, "example_tr", "Gece evde bir hırsız vardı",
     "Gece evde izinsiz giren biri vardı",
     "«hırsız» — вор, а слово ряда про вторжение"),
    (18253, "example_tr",
     "Apartmanı elektrik süpürgesiyle temizlemem gerekiyor",
     "Daireyi elektrik süpürgesiyle süpürmem gerekiyor",
     "«apartman» — дом целиком"),
    (12681, "example_tr", "Burası gerçek bir deli hastanesi gibi",
     "Burası tam bir tımarhane gibi", "«deli hastanesi» — не слово"),
    (10661, "example_tr", "Cam gibi bakışla öne bakıyordu",
     "Donuk bir bakışla öne bakıyordu", "«cam gibi bakış» — не выражение"),
    (7369, "example_tr", "Dün bana garip bir şey başına geldi",
     "Dün başıma garip bir şey geldi", "два дополнения подряд"),
    (10683, "example_tr", "Kralın lütfunu kazanmak hiç kolay değildi",
     "Benden lütuf istedi", "немецкий «Er bat mich um Gunst»"),
    (7342, "example_tr", "Onun çevresi onda büyük bir etki yapıyor",
     "Çevresinin onun üzerinde büyük etkisi var", "«etki yapmak» — не форма"),
    (1960, "example_tr", "Çöp konteyneri yine ağzına kadar dolmuş",
     "Bir ton 1000 kilo", "немецкий «Eine Tonne wiegt 1000 Kilogramm»"),
    (18760, "example_tr", "İstisna olarak bugün tatilde",
     "İstisna olarak bugün tatil yapıyoruz", "потеряно подлежащее"),
    (7377, "example_tr", "Bu duvarı kırmalıyız",
     "Bu duvarı kırıp geçmeliyiz", "в значениях «kırıp geçmek»"),
    (15561, "example_tr", "Baykuş gece ses çıkardı",
     "Baykuş gece seslendi", "«ses çıkardı» — слишком общее"),
    (17565, "example_tr", "Fotoğrafları taraması gerekiyor",
     "Fotoğrafları taramam gerekiyor", "лицо не согласовано"),
    (11764, "example_tr", "Bu gece restorana birlikte yemek yiyeceğiz",
     "Bu gece restoranda birlikte yemek yiyeceğiz", "падеж"),
    (10677, "example_tr", "Müzikten tutkuyla hoşlanıyor ve her gün çalıyor",
     "Müziği tutkuyla seviyor ve her gün çalıyor",
     "«hoşlanmak» слабее, чем «lieben»"),
    (7364, "example_tr", "Kağıdı dikkatlice bükmek",
     "Kağıdı dikkatlice bük", "инфинитив вместо повелительного"),
    (7365, "example_tr", "Hangi kaynaklar üzerinde tasarrufun var?",
     "Hangi kaynaklara sahipsin?", "канцелярит"),
    (17189, "example_tr", "Antartika ekspedisyonu tehlikeli idi",
     "Antarktika seferi tehlikeliydi", "«Antartika» и «idi»"),
    (7368, "example_tr", "Durumu hızlı kavradım",
     "Durumu hızlı kavrıyorum", "в немецком настоящее время"),
    (10672, "example_tr", "Bu aptal bir karardı",
     "Bu aptalca bir karardı", "«aptal karar» — не форма"),
    (10662, "example_tr", "O senin aptalca bir fikriydi",
     "Bu aptalca bir fikirdi", "фраза не собрана"),
    (14062, "example_tr", "Onun yorumu çok kaba idi",
     "Onun yorumu çok kabaydı", "«idi» пишут слитно"),
    (10663, "example_tr", "Gerçekten duygulandırıcı bir hikaye idi",
     "Gerçekten duygulandırıcı bir hikayeydi", "то же"),
    (8935, "example_tr", "Restoranda hizmet harika idi",
     "Restoranda servis harikaydı", "то же"),
    (10668, "example_tr", "Bu korkunç bir gün idi", "Korkunç bir gündü",
     "то же"),
    (11762, "example_tr", "Et yemek için çok sert idi",
     "Et yemek için çok sertti", "то же"),
    (10666, "example_tr", "Onun davranışı basitçe iğrenç idi",
     "Davranışı tam anlamıyla iğrençti", "«basitçe» — не то, и «idi»"),
    (16298, "example_tr", "Bu ona karşı bir baskı aracı idi",
     "Bu ona karşı bir baskı aracıydı", "«idi»"),
    (7371, "example_tr", "Bu temelsiz bir korku idi",
     "Bu temelsiz bir korkuydu", "то же"),
    (10681, "example_tr", "Oyunla ilgili obsesyonu çok güçlü idi",
     "Oyunla ilgili takıntısı çok güçlüydü", "то же"),
    (10679, "example_tr", "Kötü uyuduğu için sinirli idi",
     "Kötü uyuduğu için sinirliydi", "то же"),
    (18, "example_tr", "Trafik ışığı kırmızıdır", "Trafik ışığı kırmızı",
     "«-dır»"),
    (7348, "example_tr", "Larva küçük ve beyazdır",
     "Kurtçuk küçük ve beyaz", "то же, и в значениях «kurtçuk»"),
    (10671, "example_tr", "Çocukların büyük hayali vardır",
     "Çocukların hayal gücü çok geniş", "«hayali» — мечта; и «-dır»"),
    (10678, "example_tr", "Sigara içmek kırılması zor bir alışkanlıktır",
     "Sigara içmek bırakılması zor bir alışkanlık",
     "«kırılması» — калька с английского"),
    (17188, "example_tr", "Otel resepsiyonu zemin kattadır",
     "Otel resepsiyonu zemin katta", "«-dır»"),
    (7363, "example_tr", "Bir anlamda bu bir uzlaşmadır",
     "Bir anlamda bu bir uzlaşma", "то же"),
    (17966, "example_tr", "Bu nadir bir olaydır", "Bu nadir bir olgu",
     "то же, и в значениях «olgu»"),
    (7376, "example_tr", "Bu çok daha iyidir",
     "Bu eskisinden çok daha iyi", "«-dir», и потеряно «zuvor»"),
    (10669, "example_tr", "Bu adam tamamen çılgın",
     "Bu adam tamamen kafayı yemiş", "в значениях «kafayı yemiş»"),
    (14522, "example_tr", "Ailenin hikayesi ilginç",
     "Ailenin destanı çok ilginç", "в значениях «destan», и потеряно «sehr»"),
    (18251, "example_tr", "Kiracı kira parasını zamanında ödedi",
     "Kiracı kirasını zamanında ödüyor", "время"),
    (12683, "example_tr", "Hastalığa karşı bağışık",
     "O, hastalığa karşı bağışık", "потеряно подлежащее"),
    (10675, "example_tr", "Havadan şikayet ediyor",
     "Havadan şikayet ediyorum", "лицо не согласовано"),
    (17184, "example_tr", "Köye dolambaçlı yoldan gittik",
     "Şehirden dolambaçlı yoldan geçiyoruz",
     "немецкий «Wir nehmen einen Umweg durch die Stadt»"),
    (7357, "example_tr", "Spor ilgisi az", "Spora ilgisi az",
     "пропущен падеж"),
    (2381, "example_tr", "Bu yıl gelirimin arttığını görüyorum",
     "Bu yıl gelirim arttı", "канцелярит"),
    (11766, "example_tr", "Patates kızartmasında ketçap istiyorum",
     "Patates kızartmasının yanına ketçap istiyorum", "падеж"),
    (15088, "example_tr", "Başının arkasına çarptı",
     "Başının arkasını yaraladı", "«verletzt» — травмировал"),

    # --- потерянное и приписанное --------------------------------------------
    (708, "example_uk", "Вона наклеює пластир",
     "Вона наклеює пластир на рану", "потеряна рана"),
    (708, "example_tr", "Bir yara bandı yapıştırıyor",
     "Yaraya bir yara bandı yapıştırıyor", "то же"),
    (15088, "example_en", "He hit the back of his head",
     "He injured the back of his head", "«verletzt» — травмировал"),
    (18754, "example_en", "I worked for weeks",
     "I worked hard for weeks", "потеряно «hart»"),
    (18754, "example_uk", "Я працював тижнями",
     "Я тижнями тяжко працював", "то же"),
    (2092, "example_en", "The sex is female", "The baby is female",
     "немецкий «Das Baby ist weiblich»"),
    (11764, "example_en", "We dine at eight tonight",
     "We dine together at the restaurant tonight",
     "немецкий «Wir speisen heute Abend zusammen im Restaurant»"),
    (7333, "example_en", "I went to the cinema together with all my friends",
     "I went to the cinema together with my friends", "«all» приписано"),
    (7333, "example_uk", "Я пішов у кіно разом з усіма своїми друзями",
     "Я пішов у кіно разом зі своїми друзями", "то же"),
    (7333, "example_tr", "Bütün arkadaşlarımla birlikte sinemaya gittim",
     "Arkadaşlarımla birlikte sinemaya gittim", "то же"),
    (12678, "example_pl", "Kup prezerwatywy w aptece",
     "Ważne jest używanie prezerwatywy podczas seksu",
     "немецкий «Es ist wichtig, beim Sex ein Kondom zu benutzen»"),
    (11761, "example_pl", "Poproszę dużą porcję frytek",
     "Poproszę dużą porcję makaronu", "в немецком паста, а не фри"),
    (12679, "example_pl", "Od kilku miesięcy walczy z depresją",
     "Walczy ze swoją depresją", "«od kilku miesięcy» приписано"),
    (12681, "example_pl", "W biurze jest dziś istny dom wariatów",
     "Tu jest istny dom wariatów", "офис приписан"),
    (12682, "example_pl", "Mój tata chrapie całą noc",
     "Mój tata chrapie każdej nocy", "«jede Nacht» — каждую ночь"),
    (16297, "translation_pl", "zarżnięty, zabity, wyrzezany",
     "zarżnięty, zabity, wymordowany", "«wyrzezany» — не слово"),
    (13687, "example_pl", "Dostałam srebrny naszyjnik na urodziny",
     "Nosi srebrny naszyjnik",
     "немецкий «Sie trägt eine silberne Halskette»"),
    (13538, "example_pl", "A po trzecie, nie mam na to czasu",
     "Po pierwsze, po drugie i po trzecie są problemy",
     "немецкий «Erstens, zweitens, und drittens gibt es Probleme»"),
    (13688, "example_pl", "Włóż czapkę, bo jest zimno",
     "Nosi czarną czapkę", "немецкий «Er trägt eine schwarze Kappe»"),
    (13689, "example_pl", "Na wesele założył czarny smoking",
     "Na galę zakłada się czarny smoking", "в немецком гала-вечер"),
    (12684, "example_pl", "Lekarz przepisał mi antybiotyki na gardło",
     "Lekarz przepisał mi antybiotyki na infekcję",
     "в немецком инфекция, а не горло"),
    (247, "example_pl", "Kupiłem bilet na pociąg do Krakowa",
     "Kupuję bilet", "немецкий «Ich kaufe eine Fahrkarte»"),
    (18760, "example_en", "As an exception, I'll allow it today",
     "As an exception, we're taking the day off today",
     "немецкий «Ausnahmsweise machen wir heute mal Urlaub»"),
    (18760, "example_ru", "Исключительно сегодня мы в отпуске",
     "В порядке исключения мы сегодня отдыхаем", "то же"),
    (12686, "example_tr", "Bu adamın hiç omurgası yok",
     "Omurgası yok, cesareti de yok", "потеряно «kein Mut»"),
    (7374, "example_tr", "Biraz paranın yedek var",
     "Yedekte biraz param var", "фраза не собрана"),
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
