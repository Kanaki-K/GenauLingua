"""
Правки блока 60 (ряды 10301–10500, ранги 21070–21408).

Главная находка — новый класс: ПЕРЕВОД ПО КОРНЮ ВНУТРИ СЛОВА.

    de  Sie haben den Dieb richtig vermöbelt
    en  They furnished the room with old furniture
    ru  Они обставили комнату старой мебелью
    uk  Вони заставили кімнату старими меблями
    tr  Odayı eski mobilyalarla döştüler
    pl  Nieźle pobili tego złodzieja

`vermöbeln` значит «избить», но внутри слова видно `Möbel` — мебель.
Четыре языка из пяти перевели «обставить мебелью» и построили вокруг
этого целую осмысленную фразу. Правильно перевёл только польский.

Это не ложный друг между языками (как `Parole`/`parole` в блоке 58) и
не омоним (как `Latte`): здесь машина разобрала НЕМЕЦКОЕ слово по
ложному корню. Отличить такое приметой нельзя: ошибка не в форме, а в
морфологическом разборе, и результат грамматически безупречен.

Второй сломанный эталон того же рода:

    de  Das Haus sieht total untergekommen aus

`untergekommen` значит «нашедший приют», и так говорят все пять
словарных статей. А фраза написана в значении `runtergekommen` —
«обветшавший». Два почти одинаковых немецких слова, и эталон взял не
то.

    python -m app.scripts.fix_block_0060            # показать
    python -m app.scripts.fix_block_0060 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 10301 lebensgefährlich
    (13046, "example_pl", "Taka jazda jest niebezpieczna dla życia",
     "To była niebezpieczna dla życia sytuacja na autostradzie",
     "перевод другого предложения"),
    # 10302 sechzig
    (13593, "example_uk", "Мій дідусь уже шістдесят років",
     "Моєму дідусеві вже шістдесят років",
     "фраза без сказуемого и не в том падеже"),
    # 10303 konsequent
    (11411, "example_uk",
     "Він послідовно тренується кожного дня, щоб покращитися",
     "Він послідовно тренується щодня, щоб покращитися",
     "«кожного дня» — калька"),
    (11411, "example_pl", "Musisz być konsekwentny wobec dzieci",
     "Trenuje konsekwentnie codziennie, żeby być lepszym",
     "перевод другого предложения"),
    # 10304 Pianist
    (14760, "example_tr", "Piyanist Chopini harika çalıyor",
     "Piyanist Chopin'i harika çalıyor",
     "потерян апостроф в имени"),
    # 10306 erkenntlich
    (8380, "translation_uk", "вдячний, удячний",
     "вдячний, зобов'язаний",
     "«удячний» — нет такой формы"),
    # 10308 abgelegen
    (8381, "example_tr", "Köy dağlarda çok uzak",
     "Köy dağlarda çok ücra bir yerde",
     "«uzak» без дополнения повисает"),
    # 10309 verblieben
    (8382, "translation_uk", "решта, залишковий",
     "залишковий, що залишився",
     "«решта» это существительное, а ряд о прилагательном"),
    (8382, "example_uk",
     "З грошима, що залишилися, він не міг багато зробити",
     "Із залишковими коштами він не міг багато зробити",
     "в эталоне «Mittel» — кошти, а не гроші"),
    (8382, "example_pl", "Za pozostałe pieniądze kupimy chleb",
     "Z pozostałymi środkami nie mógł wiele zdziałać",
     "перевод другого предложения"),
    # 10310 Animation
    (17709, "example_tr", "Filmdeki animasyon etkileyici idi",
     "Filmdeki animasyon etkileyiciydi",
     "«idi» отдельно"),
    # 10312 angeblich
    (8383, "example_uk", "Нібито сюрприз уже не був таємницею",
     "Гаданий сюрприз уже не був таємницею",
     "«нібито» это частица, а тут нужно определение"),
    (8383, "example_pl", "To jego rzekomy przyjaciel",
     "Rzekoma niespodzianka nie była już tajemnicą",
     "перевод другого предложения"),
    # 10313 verurteilt
    (16805, "example_tr", "Mahkum suçlu hâlâ cezaevinde",
     "Hükümlü suçlu hâlâ cezaevinde",
     "«mahkum suçlu» — тавтология"),
    (16805, "example_pl",
     "Skazany mężczyzna siedzi jeszcze w więzieniu",
     "Skazany przestępca siedzi jeszcze w więzieniu",
     "в эталоне «Kriminelle» — преступник"),
    # 10314 Anhieb
    (8384, "example_uk", "Одразу він не зміг розв'язати завдання",
     "З першої спроби він не зміг розв'язати завдання",
     "«Auf Anhieb» это с первой попытки"),
    # 10315 polizeilich
    (16806, "example_en", "The police investigation took weeks",
     "The police check was very thorough",
     "перевод другого предложения"),
    (16806, "example_tr", "Polis soruşturması haftalarca sürdü",
     "Polis kontrolü çok titizdi",
     "перевод другого предложения"),
    # 10316 missfallen
    (11412, "example_tr", "Bu karar bana çok hoşlanmıyor",
     "Bu karar hiç hoşuma gitmiyor",
     "«hoşlanmak» требует человека подлежащим"),
    # 10317 urkomisch
    (11413, "translation_uk",
     "страшенно смішний, умерти зі смуху можна",
     "страшенно смішний, украй смішний",
     "«зі смуху» — разваленная форма"),
    (11413, "example_uk", "Жарт був абсолютно смішний",
     "Жарт був просто страшенно смішний",
     "потеряна усилительная приставка «ur-»"),
    (11413, "example_tr", "Şaka tamamen komikti",
     "Şaka kesinlikle çok komikti",
     "потеряна усилительная приставка «ur-»"),
    (11413, "example_pl", "Ten film jest naprawdę przekomiczny",
     "Żart był absolutnie przekomiczny",
     "перевод другого предложения"),
    # 10319 Kammerdiener
    (9226, "example_uk", "Лакей короля був дуже вірний",
     "Камердинер короля був дуже вірний",
     "перевод слова — «камердинер»"),
    (9226, "example_tr", "Kralın hizmetçisi çok sadık idi",
     "Kralın uşağı çok sadıktı",
     "«hizmetçi» это прислуга вообще, и «idi» отдельно"),
    # 10320 Testosteron
    (13047, "example_pl", "Lekarz zbadał poziom testosteronu",
     "Poziom testosteronu jest wyższy u mężczyzn",
     "перевод другого предложения"),
    # 10321 Wasserstoff
    (18066, "example_tr",
     "Hidrojen önemli bir enerji taşıyıcısıdır",
     "Hidrojen roketler için yakıt olarak kullanılıyor",
     "перевод другого предложения"),
    # 10324 Manifest
    (16807, "translation_uk", "манифест, програмна заява",
     "маніфест, програмна заява",
     "«манифест» — русское написание"),
    (16807, "example_pl", "Partia ogłosiła swój manifest",
     "Manifest opisuje cele ruchu",
     "перевод другого предложения"),
    # 10325 einlochen
    (12368, "example_uk", "Гравець у гольф легко закинув м'яч",
     "Гравець у гольф легко закотив м'яч у лунку",
     "потеряна лунка"),
    (12368, "example_tr",
     "Golfer topu deliğe koymakta sorun yaşamadı",
     "Golfçü topu deliğe sokmakta sorun yaşamadı",
     "«Golfer» — английское слово"),
    # 10326 Puma
    (15805, "example_ru", "Пума прыгнула из куста",
     "Пума прыгнула из кустов",
     "«из куста» — не то число"),
    # 10327 Plastiktüte
    (9923, "example_tr", "Alışverişimi plastik torbada taşıyorum",
     "Eşyalarımı plastik poşette taşıyorum",
     "в эталоне «meine Sachen», а не покупки"),
    # 10330 anschreiben
    (14290, "example_pl", "Napiszę do ciebie jutro wieczorem",
     "Napiszę do ciebie, kiedy będę mieć więcej informacji",
     "перевод другого предложения"),
    # 10331 Polizeiauto
    (16808, "example_ru",
     "Полицейская машина припаркована перед домом",
     "Полицейская машина стояла перед домом",
     "эталон в прошедшем времени"),
    (16808, "example_uk",
     "Поліцейський автомобіль припаркований перед будинком",
     "Поліцейська машина стояла перед будинком",
     "эталон в прошедшем времени"),
    (16808, "example_tr", "Polis arabası evin önünde parklandı",
     "Polis arabası evin önünde duruyordu",
     "«parklandı» — нет такой формы"),
    # 10332 obendrauf
    (8386, "example_pl", "Połóż ciastka na wierzchu",
     "Samochód się zepsuł, a na dodatek straciłem pracę",
     "перевод другого предложения"),
    # 10333 Abhang
    (15806, "example_uk",
     "Схил був крутий і небезпечний, ми обережно спускалися",
     "Схил був крутий і небезпечний, нам довелося обережно спускатися",
     "потеряно «mussten»"),
    (15806, "example_tr",
     "Yamaç dik ve tehlikeliydi, dikkatli bir şekilde ineceğiz",
     "Yamaç dik ve tehlikeliydi, dikkatli bir şekilde inmemiz gerekti",
     "время рассогласовано: прошедшее и будущее в одной фразе"),
    # 10334 vorab
    (18900, "example_ru", "Говорю заранее — это будет дорого",
     "Говорю тебе заранее, что это будет недёшево",
     "в эталоне «nicht billig» и обращение «dir»"),
    # 10335 Reifenquietschen
    (17355, "example_ru",
     "Писк шин был очень громким во время гонки",
     "Визг шин был очень громким во время гонки",
     "перевод слова — «визг шин»"),
    (17355, "example_uk",
     "Писк шин автомобілів був дуже голосним під час гонки",
     "Вереск шин був дуже голосним під час гонки",
     "перевод слова — «вереск шин», и «автомобілів» в эталоне нет"),
    (17355, "example_tr",
     "Lastik çığlığı yarış sırasında çok yüksek olmuştu",
     "Lastik gıcırtısı yarış sırasında çok yüksekti",
     "«çığlık» это вопль человека"),
    # 10336 Gewölbe
    (18440, "example_ru",
     "Старый свод под церковью был темным и таинственным",
     "Старый свод под церковью был тёмным и таинственным",
     "«е» вместо «ё»"),
    (18440, "example_tr",
     "Kilisinin altındaki eski kemer karanlık ve gizemli idi",
     "Kilisenin altındaki eski tonoz karanlık ve gizemliydi",
     "«Kilisinin» — опечатка, и «idi» отдельно"),
    # 10337 Waffensystem
    (16809, "example_uk",
     "Сучасні системи озброєння дуже дорогі",
     "Сучасні системи озброєння неймовірно складні й дорогі",
     "потеряно «komplex»"),
    (16809, "example_pl",
     "Nowe systemy uzbrojenia są bardzo drogie",
     "Nowoczesne systemy uzbrojenia są niewiarygodnie złożone i drogie",
     "потеряно «komplex»"),
    # 10338 Windmühle
    (15807, "example_uk",
     "Стара вітряна млинниця на пагорбі — це туристична визначна пам'ятка",
     "Старий вітряк на пагорбі — це туристична визначна пам'ятка",
     "«млинниця» — нет такого слова"),
    (15807, "example_tr",
     "Tepedeki eski değirmen turist çekiciliğidir",
     "Tepedeki eski yel değirmeni bir turistik cazibe merkezi",
     "«turist çekiciliği» — не выражение"),
    # 10339 Slum
    (18441, "example_en",
     "Thousands of poor people live in the slums of the big city",
     "Many poor people live in the slums of the big city",
     "в эталоне «viele», а не тысячи"),
    (18441, "example_ru",
     "В трущобах большого города живут тысячи бедных людей",
     "В трущобах большого города живёт много бедных людей",
     "в эталоне «viele», а не тысячи"),
    (18441, "example_uk",
     "У трущобах великого міста живуть тисячі бідних людей",
     "У нетрях великого міста живе багато бідних людей",
     "«трущоби» — русизм, и в эталоне «viele»"),
    (18441, "example_tr",
     "Büyük şehrin gecekondu mahallelerinde binlerce fakir insan yaşıyor",
     "Büyük şehrin gecekondu mahallelerinde birçok fakir insan yaşıyor",
     "в эталоне «viele», а не тысячи"),
    # 10341 Gerichtstermin
    (16810, "example_uk",
     "Судовий розгляд перенесли на наступний тиждень",
     "Судове засідання перенесли на наступний тиждень",
     "перевод слова — «судове засідання»"),
    (16810, "example_pl", "Mam termin rozprawy w przyszły wtorek",
     "Termin rozprawy przesunięto na następny tydzień",
     "перевод другого предложения"),
    # 10342 Wassermelone
    (11964, "example_uk",
     "Кавун був солодким і освіжуючим у цей спекотний літній день",
     "Кавун був солодким і освіжав у цей спекотний літній день",
     "«освіжуючий» — калька активного дієприкметника"),
    (11964, "example_pl", "Latem najlepszy jest zimny arbuz",
     "Arbuz był słodki i orzeźwiający w ten gorący letni dzień",
     "перевод другого предложения"),
    # 10343 rückfällig
    (16811, "example_ru",
     "Преступник был рецидивистом и снова арестован",
     "Преступник оказался рецидивистом и был снова арестован",
     "сказуемые рассогласованы"),
    (16811, "example_uk",
     "Злочинець був рецидивістом і знову арештований",
     "Злочинець виявився рецидивістом і був знову арештований",
     "сказуемые рассогласованы"),
    (16811, "example_pl",
     "Jego choroba jest nawracająca i trudna do leczenia",
     "Przestępca był recydywistą i został znowu aresztowany",
     "перевод другого предложения"),
    # 10344 suspendieren
    (9227, "example_uk",
     "Учня відстранили, оскільки він занадто часто відсутнював",
     "Учня відсторонили, бо він занадто часто був відсутній",
     "«відстранили» и «відсутнював» — нет таких форм"),
    # 10345 unterlaufen
    (8388, "example_en", "I made a stupid mistake",
     "A stupid mistake slipped past me",
     "«unterlaufen» значит «вышло по недосмотру», а не «я сделал»"),
    (8388, "example_uk",
     "Програмісту трапилася помилка під час розробки",
     "Мені трапилася дурна помилка",
     "перевод другого предложения"),
    (8388, "example_tr", "Hesapta küçük bir yanlışlık olmuş",
     "Aptalca bir hata yapmışım",
     "перевод другого предложения"),
    # 10347 Selbstjustiz
    (16812, "example_tr", "Kalabalık hırsızı linç etmeye kalktı",
     "Linç yasal değildir ve polis tarafından kovuşturulur",
     "перевод другого предложения"),
    (16812, "example_pl", "Nie popieram samosądu na ulicach",
     "Samosąd jest nielegalny i ścigany przez policję",
     "перевод другого предложения"),
    # 10349 Türschwelle
    (18443, "example_uk",
     "Будь обережний з порогом, інакше ти поткнешся",
     "Будь обережний з порогом, інакше ти спіткнешся",
     "«поткнешся» — нет такой формы"),
    # 10351 vorbringen
    (8389, "example_en", "Would you like to add anything?",
     "Would you like to put anything else forward?",
     "«vorbringen» это высказать, а не добавить"),
    (8389, "example_uk", "Хочеш ще щось додати?",
     "Хочеш ще щось висловити?",
     "«vorbringen» это высказать, а не добавить"),
    (8389, "example_tr", "Eklemek istediğin bir şey var mı?",
     "Dile getirmek istediğin başka bir şey var mı?",
     "«eklemek» это добавить"),
    (8389, "example_pl", "Chcesz jeszcze coś dodać?",
     "Chcesz jeszcze coś przedstawić?",
     "«dodać» это добавить"),
    # 10352 allzeit
    (18901, "example_uk", "Я бажаю тобі завжди удачи",
     "Я бажаю тобі завжди удачі",
     "«удачи» — русский падеж"),
    # 10353 Faser
    (18067, "example_tr", "Sebzelerde bol lif var",
     "Pamuklu kumaşın lifleri çok yumuşak",
     "перевод другого предложения"),
    # 10355 Prostata
    (13048, "example_pl", "Po czterdziestce warto badać prostatę",
     "Urolog zbadał prostatę pacjenta",
     "перевод другого предложения"),
    # 10356 vermöbeln — четыре языка прочли корень «Möbel»
    (18444, "example_en", "They furnished the room with old furniture",
     "They really beat up the thief",
     "«vermöbeln» это избить, а не обставить мебелью"),
    (18444, "example_ru", "Они обставили комнату старой мебелью",
     "Они здорово отлупили вора",
     "«vermöbeln» это избить, а не обставить мебелью"),
    (18444, "example_uk", "Вони заставили кімнату старими меблями",
     "Вони добряче відлупцювали злодія",
     "«vermöbeln» это избить, а не обставити меблями"),
    (18444, "example_tr", "Odayı eski mobilyalarla döştüler",
     "Hırsızı iyice pataklamışlar",
     "«vermöbeln» это избить, а не обставить мебелью"),
    # 10357 erstbest
    (8390, "example_uk",
     "Він прийняв першу попавшуюся роботу, не замислюючись",
     "Він прийняв першу-ліпшу роботу, не замислюючись",
     "«попавшуюся» — русский дієприкметник"),
    (8390, "example_pl", "Wziął pierwszą lepszą pracę",
     "Wziął pierwszą lepszą pracę bez zastanowienia",
     "потеряно «ohne zu überlegen»"),
    # 10360 simpel
    (8392, "example_tr", "Bu basit ve düz bir çözümdür",
     "Bu basit bir çözüm",
     "«düz» в эталоне нет"),
    # 10364 zwingend
    (8393, "example_tr", "Bu kesinlikle zorunlu değil",
     "Bu zorunlu olarak gerekli değil",
     "«kesinlikle» это безусловно, а «zwingend» — обязательно"),
    # 10365 fünfhundert
    (13594, "example_uk", "Книга має п'ятьсот сторінок",
     "Книга має п'ятсот сторінок",
     "в статье «п'ятсот», а в примере лишний знак"),
    (13594, "example_tr", "Kitap beş yüz sayfaya sahiptir",
     "Kitap beş yüz sayfa",
     "«sayfaya sahiptir» — калька"),
    # 10366 Programmierer
    (9228, "example_pl", "Mój brat jest programistą w dużej firmie",
     "Programista tworzy nową aplikację",
     "перевод другого предложения"),
    # 10367 schmerzvoll
    (13050, "example_tr", "Anı benim için çok acılı",
     "Bu anı benim için çok acı verici",
     "«acılı» о еде, и фраза без указания"),
    # 10369 Augapfel
    (15285, "example_uk", "Яблуко ока чутливий орган",
     "Очне яблуко — чутливий орган",
     "«яблуко ока» — калька, и нет тире"),
    (15285, "example_pl", "Po uderzeniu boli mnie gałka oczna",
     "Gałka oczna to wrażliwy organ",
     "перевод другого предложения"),
    # 10371 Peperoni
    (11965, "example_uk",
     "Мені подобається червоний перець у салаті",
     "Мені подобається червоний перець чилі в салаті",
     "потеряно «Peperoni» — острый перец"),
    (11965, "example_tr", "Salatada kırmızı biberi seviyorum",
     "Salatada kırmızı acı biber severim",
     "потеряно «acı», и лишний аккузатив"),
    (11965, "example_pl", "Dodaj ostrą papryczkę do sosu",
     "Lubię ostrą czerwoną papryczkę w sałatce",
     "перевод другого предложения"),
    # 10372 Ministerpräsident
    (16814, "example_uk", "Прем'єр-міністр виголосив мову",
     "Прем'єр-міністр виголосив промову",
     "«виголосити мову» — не то слово"),
    (16814, "example_pl",
     "Premier wygłosił krótkie przemówienie w telewizji",
     "Premier wygłosił przemówienie",
     "«krótkie» и «w telewizji» в эталоне нет"),
    # 10373 Zusatz
    (8394, "example_tr", "Katkı madde tadını iyileştirir",
     "Katkı maddesi tadı iyileştirir",
     "потерян изафет"),
    (8394, "example_pl", "Kupuję sok bez dodatku cukru",
     "Dodatek poprawia smak",
     "перевод другого предложения"),
    # 10374 Revolte
    (16815, "example_pl", "W więzieniu wybuchł bunt więźniów",
     "Bunt robotników był imponujący",
     "перевод другого предложения"),
    # 10376 kreuzigen
    (16816, "example_tr",
     "Romalılar tutsukları acı bir ceza olarak çarmıha germişlerdi",
     "Romalılar tutsakları zalim bir ceza olarak çarmıha gerdi",
     "«tutsukları» — опечатка, и «acı» это не «grausam»"),
    (16816, "example_pl", "Na tym wzgórzu ukrzyżowano skazanych",
     "Rzymianie krzyżowali jeńców jako okrutną karę",
     "перевод другого предложения"),
    # 10378 ungewohnt
    (11415, "example_pl", "To dla mnie nietypowa sytuacja",
     "Nietypowa pogoda mnie niepokoi",
     "перевод другого предложения"),
    # 10379 Anklagepunkt
    (16817, "example_pl",
     "Prokurator odczytał wszystkie zarzuty wobec oskarżonego",
     "Prokurator przedstawił wszystkie zarzuty w sądzie",
     "«wobec oskarżonego» в эталоне нет"),
    # 10380 Nachwelt
    (18902, "example_ru",
     "Потомство будет судить нас за наши поступки",
     "Потомки будут судить нас за наши поступки",
     "перевод слова — «потомки»"),
    # 10381 empfänglich
    (8395, "example_tr", "Yeni fikirler için çok alımlı",
     "Yeni fikirlere çok açık",
     "«alımlı» значит привлекательный"),
    (8395, "example_pl", "Jest bardzo podatny na przeziębienia",
     "Jest bardzo otwarty na nowe pomysły",
     "перевод другого предложения"),
    # 10382 Kriegserklärung
    (16818, "example_pl", "W radiu odczytali wypowiedzenie wojny",
     "Wypowiedzenie wojny zostało formalnie odczytane",
     "«w radiu» в эталоне нет"),
    # 10383 Gerüst
    (18445, "example_tr", "İskele ev önüne kuruldu",
     "İskele evin önüne kuruldu",
     "потерян родительный"),
    # 10384 schlaflos
    (13052, "example_tr",
     "Sınava kadar uyku kaçıran geceler geçirdi",
     "Sınavdan önce uykusuz geceler geçirdi",
     "«sınava kadar» это «до экзамена» во времени"),
    (13052, "example_pl", "Miałem bezsenną noc przed egzaminem",
     "Spędził bezsenne noce przed egzaminem",
     "в эталоне «er» и множественное"),
    # 10385 todernst
    (11416, "example_uk",
     "Його погляд був мертельно серйозним і страшним",
     "Його погляд був смертельно серйозним і страшним",
     "«мертельно» — опечатка"),
    (11416, "example_tr", "Bakışı çok ciddi ve korkutucu idi",
     "Bakışı ölesiye ciddi ve korkutucuydu",
     "потеряно «tod-», и «idi» отдельно"),
    (11416, "example_pl",
     "Powiedział to śmiertelnie poważnym tonem",
     "Jego spojrzenie było śmiertelnie poważne i przerażające",
     "перевод другого предложения"),
    # 10386 unentbehrlich
    (8396, "example_pl", "Telefon jest dziś niezbędny",
     "Woda jest niezbędna do życia",
     "перевод другого предложения"),
    # 10387 Pult
    (18446, "example_en",
     "The teacher stood behind his desk in the classroom",
     "The teacher stands behind his desk",
     "эталон в настоящем, и «в классе» в нём нет"),
    (18446, "example_ru",
     "Учитель стоял за своей кафедрой в классе",
     "Учитель стоит за своей кафедрой",
     "эталон в настоящем, и «в классе» в нём нет"),
    (18446, "example_uk",
     "Учитель стояв за своєю кафедрою в класі",
     "Учитель стоїть за своєю кафедрою",
     "эталон в настоящем, и «в класі» в нём нет"),
    (18446, "example_tr",
     "Öğretmen sınıfta kendi masasının arkasında durdu",
     "Öğretmen kürsüsünün arkasında duruyor",
     "эталон в настоящем, и «kendi» лишнее"),
    # 10388 kompensieren
    (8397, "example_pl", "Firma zrekompensowała nam opóźnienie",
     "Próbuje zrekompensować swój błąd",
     "перевод другого предложения"),
    # 10389 Zeugenschutz
    (16819, "example_pl", "Trafił do programu ochrony świadków",
     "Ochrona świadków jest bardzo ważna w sądzie",
     "перевод другого предложения"),
    # 10390 verschmiert
    (8398, "example_uk", "Вікно повністю забруднене брудом",
     "Вікно повністю замазане брудом",
     "«забруднене брудом» — тавтология"),
    (8398, "example_tr", "Pencere tamamen kir ile kirlenmiş",
     "Pencere tamamen kirle bulaşmış",
     "«kir ile kirlenmiş» — тавтология"),
    # 10391 Jammerlappen
    (11417, "example_uk",
     "Він така нюня, яка весь час скаржиться",
     "Він такий нюня, що весь час скаржиться",
     "рассогласование рода"),
    (11417, "example_tr", "Hep şikayet eden gerçek bir ağlak",
     "O, hep şikâyet eden gerçek bir ağlak",
     "фраза без подлежащего"),
    (11417, "example_pl", "Nie bądź takim mazgajem",
     "Jest takim mazgajem, który ciągle się skarży",
     "перевод другого предложения"),
    # 10392 Asservatenkammer
    (16820, "example_pl",
     "Broń zamknęli w magazynie dowodów rzeczowych",
     "Dowody były przechowywane w magazynie dowodów rzeczowych",
     "перевод другого предложения"),
    # 10394 untergekommen — эталон взял значение «runtergekommen»
    (8399, "example_de", "Das Haus sieht total untergekommen aus",
     "Wir sind bei Freunden untergekommen",
     "«untergekommen» это нашедший приют, обветшавший — "
     "«runtergekommen»"),
    (8399, "example_en", "The house looks completely run-down",
     "We were taken in by friends",
     "вслед за исправленным эталоном"),
    (8399, "example_ru",
     "Дом выглядит так, будто в нём кое-как приютились",
     "Мы приютились у друзей",
     "вслед за исправленным эталоном"),
    (8399, "example_uk", "Дім виглядає зовсім занедбаним",
     "Ми знайшли прихисток у друзів",
     "вслед за исправленным эталоном"),
    (8399, "example_tr", "Dedemin eski evi tam bir virane",
     "Arkadaşlarımızda kalacak yer bulduk",
     "вслед за исправленным эталоном"),
    (8399, "example_pl",
     "Na noc zostaliśmy zakwaterowani u znajomych",
     "Zostaliśmy zakwaterowani u znajomych",
     "«na noc» в эталоне нет"),
    # 10395 Elixier
    (13053, "example_uk",
     "Лікар рекомендував еліксир для укріплення здоров'я",
     "Лікар рекомендував еліксир для зміцнення здоров'я",
     "«укріплення» — русизм"),
    (13053, "example_pl", "W bajce czarownica warzyła eliksir",
     "Lekarz polecił eliksir na wzmocnienie zdrowia",
     "перевод другого предложения"),
    # 10397 Schläfe
    (15286, "example_tr", "Silahı şakaklığına tuttu",
     "Silahı şakağına dayadı",
     "«şakaklığına» — нет такой формы"),
    (15286, "example_pl", "Boli mnie głowa w skroniach",
     "Przyłożył broń do swojej skroni",
     "перевод другого предложения"),
    # 10399 Herzattacke
    (13054, "example_uk",
     "Він раптом отримав серцевий напад і його доставили до лікарні",
     "У нього раптом стався серцевий напад, і його доставили до лікарні",
     "«отримати напад» — калька"),
    (13054, "example_pl", "Dziadek dostał ataku serca w pracy",
     "Nagle dostał ataku serca i zabrano go do szpitala",
     "перевод другого предложения"),
    # 10400 hörbar
    (8400, "example_pl", "Jego szept był ledwo słyszalny",
     "Jego oddech był teraz wyraźnie słyszalny",
     "перевод другого предложения"),
    # 10402 managen
    (9229, "example_uk", "Він управляє великою фірмою",
     "Я керую великою командою на роботі",
     "перевод другого предложения"),
    (9229, "example_tr",
     "Tüm bu görevleri nasıl idare ediyorsun",
     "İşte büyük bir ekibi yönetiyorum",
     "перевод другого предложения"),
    # 10403 Pflichtverteidiger
    (16821, "example_tr",
     "Sanık avukat tutamadığı için dava avukatı tayin edildi",
     "Sanık avukat tutamadığı için kendisine zorunlu müdafi atandı",
     "«dava avukatı» — не термин"),
    (16821, "example_pl", "Sąd przydzielił mu obrońcę z urzędu",
     "Oskarżony otrzymał obrońcę z urzędu, bo nie mógł sobie pozwolić "
     "na adwokata",
     "потеряна причина"),
    # 10404 johlen
    (14292, "example_uk",
     "Фанати галасили і святкували під час матчу",
     "Фанати галасують і радіють під час футбольного матчу",
     "«галасили» — не форма, и время"),
    (14292, "example_tr",
     "Taraftarlar futbol maçında haykırıyor ve tezahürat yapıyordu",
     "Taraftarlar futbol maçında haykırıyor ve tezahürat yapıyor",
     "время рассогласовано внутри фразы"),
    (14292, "example_pl", "Kibice wrzeszczeli przez cały mecz",
     "Kibice wrzeszczą i wiwatują na meczu piłki nożnej",
     "перевод другого предложения"),
    # 10406 gerissen
    (11418, "example_uk",
     "Підступний злочинець, який роки залишався невиявленим",
     "Підступний злочинець, який роками залишався невиявленим",
     "«роки» вместо «роками»"),
    (11418, "example_pl", "To bardzo przebiegły człowiek",
     "Przebiegły przestępca, który latami pozostawał niewykryty",
     "перевод другого предложения"),
    # 10408 Geldstrafe
    (16822, "example_uk",
     "Йому довелося сплатити великий штраф за порушення правил "
     "дорожного руху",
     "Йому довелося сплатити великий штраф за порушення правил "
     "дорожнього руху",
     "«дорожного» — не форма"),
    (16822, "example_tr",
     "Trafik ihlali nedeniyle yüksek bir ceza ödemek zorunda kaldı",
     "Trafik ihlali nedeniyle yüksek bir para cezası ödemek zorunda kaldı",
     "перевод слова — «para cezası»"),
    (16822, "example_pl",
     "Zapłacił wysoką grzywnę za jazdę bez biletu",
     "Musiał zapłacić wysoką grzywnę za wykroczenie drogowe",
     "в эталоне нарушение правил дорожного движения"),
    # 10409 Alleinerziehende
    (15287, "example_en", "She's a single parent with two kids",
     "The single parent works hard to provide for her children",
     "перевод другого предложения"),
    (15287, "example_ru", "Она одинокий родитель двух детей",
     "Мать-одиночка много работает, чтобы содержать детей",
     "перевод другого предложения"),
    (15287, "example_uk", "Вона сама працює, щоб утримувати дітей",
     "Мати-одиначка багато працює, щоб утримувати дітей",
     "потеряно слово ряда"),
    (15287, "example_pl", "Samotna matka wychowuje dwoje dzieci",
     "Samotna matka ciężko pracuje, żeby utrzymać dzieci",
     "перевод другого предложения"),
    # 10410 Ankunftszeit
    (17356, "example_en", "The arrival time is at 2 pm",
     "The arrival time of the train is 2 pm",
     "потеряно «des Zuges»"),
    (17356, "example_uk", "Час прибуття — о 14:00",
     "Час прибуття поїзда — 14:00",
     "потеряно «des Zuges»"),
    (17356, "example_tr", "Varış saati 14:00",
     "Trenin varış saati 14:00",
     "потеряно «des Zuges»"),
    # 10411 Selbstjustizler
    (16823, "example_uk", "Лінчуючі взяли закон у свої руки",
     "Самосудники взяли закон у свої руки",
     "«лінчуючі» — калька активного дієприкметника"),
    (16823, "example_tr",
     "Kanunu kendi eline alan kişiyi kimse savunmaz",
     "Kanunu kendi ellerine aldılar",
     "перевод другого предложения"),
    # 10413 Brustkrebs
    (13055, "example_pl",
     "Badania pomagają wcześnie wykryć raka piersi",
     "Wczesne wykrycie raka piersi może ratować życie",
     "перевод другого предложения"),
    # 10416 Gerinnsel
    (13056, "example_uk",
     "Кров'яний згусток може привести до серйозних ускладнень",
     "Кров'яний згусток може призвести до серйозних ускладнень",
     "«привести до» — калька"),
    (13056, "example_pl", "Lekarz znalazł skrzep w nodze",
     "Skrzep krwi może prowadzić do poważnych komplikacji",
     "перевод другого предложения"),
    # 10417 Orchidee
    (15811, "example_uk",
     "Червона орхідея прекрасно цвітає на моєму балконі",
     "Червона орхідея прекрасно квітне на моєму балконі",
     "«цвітає» — не форма"),
    # 10418 Zahnfleisch
    (13057, "translation_uk", "ясна, піхва зуба",
     "ясна, десна",
     "«піхва зуба» — не анатомический термин"),
    # 10419 ausgehungert
    (11966, "example_uk",
     "Ці голодуючі тварини терміново потребували допомоги",
     "Виголоднілі тварини терміново потребували допомоги",
     "«голодуючі» — калька, и «Ці» в эталоне нет"),
    (11966, "example_tr",
     "Aç olan hayvanlar acilen yardıma ihtiyaçlarıydı",
     "Aç hayvanlar acilen yardıma ihtiyaç duyuyordu",
     "«ihtiyaçlarıydı» — разваленная форма"),
    (11966, "example_pl", "Wrócił do domu wygłodzony jak wilk",
     "Wygłodzone zwierzęta pilnie potrzebowały pomocy",
     "перевод другого предложения"),
    # 10420 Stromversorgung
    (17711, "example_uk", "Електропостачання дому було перервано",
     "Електропостачання будинку було перервано",
     "«дому» это домашнего очага, строения — «будинку»"),
    # 10421 explosiv
    (8402, "example_pl", "Ona ma bardzo wybuchowy charakter",
     "To była wybuchowa sytuacja między nimi dwoma",
     "перевод другого предложения"),
    # 10422 Hektik
    (1527, "example_en", "I hate the hectic pace here",
     "I don't like the hustle and bustle in the city",
     "в эталоне «ich mag nicht» и город"),
    # 10423 Aufmunterung
    (11419, "example_uk",
     "Невелике ободрення допомагає йому продовжувати",
     "Невелике підбадьорення допомагає йому продовжувати",
     "«ободрення» — русизм"),
    (11419, "example_pl",
     "Potrzebuję trochę pocieszenia po takim dniu",
     "Mała zachęta pomaga mu iść dalej",
     "перевод другого предложения"),
    # 10424 Herrscherin
    (16824, "example_ru",
     "Правительница управляла страной с твёрдой рукой",
     "Правительница управляла страной твёрдой рукой",
     "«с твёрдой рукой» — калька"),
    (16824, "example_uk", "Володарка керувала країною сильною рукою",
     "Правителька керувала країною твердою рукою",
     "перевод слова — «правителька», и «stark» это тверда рука"),
    (16824, "example_tr",
     "Hükümdar kadın ülkeyi sert bir şekilde yönetiyordu",
     "Kadın hükümdar ülkeyi sert bir elle yönetiyordu",
     "порядок слов, и потеряна «рука»"),
    # 10425 zehntausende
    (13596, "example_tr", "On binler kişi festivale geldi",
     "On binlerce kişi festivale geldi",
     "«on binler kişi» — сломанная форма"),
    # 10426 voreinander
    (8403, "example_pl", "Nie mieli przed sobą żadnych tajemnic",
     "Bali się siebie wzajemnie",
     "перевод другого предложения"),
    # 10427 zunehmen
    (3058, "example_tr", "Kilo alıyorum",
     "Çok fazla tatlı yediğimde kilo alıyorum",
     "потеряно условие"),
    # 10428 Promenade
    (17358, "example_uk", "Ми прогулялися вздовж променади",
     "Ми прогулялися вздовж променаду",
     "«променади» — не тот падеж"),
    # 10430 Schulglocke
    (9610, "example_uk",
     "Шкільний дзвонок дзвонить о восьмій ранку",
     "Шкільний дзвінок дзвонить о восьмій ранку",
     "«дзвонок» — русизм"),
    # 10431 Konserve
    (11967, "example_pl", "Otwórz konserwę z tuńczykiem",
     "W piwnicy przechowujemy różne konserwy",
     "перевод другого предложения"),
    # 10432 Abzweigung
    (17359, "example_ru", "Повернись направо на развилке",
     "Поверни направо на развилке",
     "«повернись» это обернись"),
    (17359, "example_tr", "Sapmanın sağında dönersin",
     "Sapaktan sağa dön",
     "«sapmanın sağında» — разваленная фраза"),
    # 10433 retro
    (8404, "example_uk",
     "Мені подобається цей ретро стиль із сімдесятих",
     "Мені подобається цей ретро-стиль із сімдесятих",
     "«ретро» пишется через дефис"),
    (8404, "example_tr",
     "Bu yetmişlerden retro stil bana hoşa gidiyor",
     "Yetmişlerden gelen bu retro stil hoşuma gidiyor",
     "«bana hoşa gidiyor» — двойное управление"),
    # 10436 flennen
    (11420, "example_en",
     "Stop whining and finish your homework",
     "The child is crying because it's tired",
     "перевод другого предложения"),
    (11420, "example_uk", "Дитина плаче, тому що втомилась",
     "Дитина рюмсає, бо втомилася",
     "перевод слова — «рюмсати»"),
    (11420, "example_pl", "Przestań beczeć, nic się nie stało",
     "Dziecko beczy, bo jest zmęczone",
     "перевод другого предложения"),
    # 10437 Luftröhre
    (13059, "example_en",
     "The trachea is an important breathing organ",
     "When I have a cold, my trachea hurts",
     "перевод другого предложения"),
    (13059, "example_tr",
     "Hava borusu önemli bir solunum organıdır",
     "Üşüttüğümde nefes borum ağrıyor",
     "перевод другого предложения"),
    (13059, "example_pl",
     "Coś mi wpadło do tchawicy i się zakrztusiłem",
     "Kiedy jestem przeziębiony, boli mnie tchawica",
     "перевод другого предложения"),
    # 10438 Interessent
    (17878, "example_en",
     "There were many interested parties in the house",
     "There were many interested parties for the house",
     "«in the house» значит «внутри дома»"),
    (17878, "example_ru", "Было много заинтересованных лиц в доме",
     "Было много желающих купить дом",
     "«в доме» значит «внутри дома»"),
    (17878, "example_uk", "Було багато зацікавлених осіб у дім",
     "Було багато зацікавлених у придбанні будинку",
     "«зацікавлених осіб у дім» — сломанное управление"),
    (17878, "example_tr", "Ev için birçok ilgileneni vardı",
     "Ev için birçok ilgilenen vardı",
     "лишний аккузатив"),
    # 10439 unermüdlich
    (11421, "example_pl", "Jest niezmordowana w pracy z dziećmi",
     "Pracuje niezmordowanie nad swoim projektem",
     "перевод другого предложения"),
    # 10440 Asphalt
    (17360, "example_ru", "Асфальт был мягким в жаре",
     "Асфальт был мягким от жары",
     "«в жаре» — не то управление"),
    # 10442 Statur
    (15288, "example_pl", "Ma atletyczną posturę jak sportowiec",
     "Jego atletyczna postura była imponująca",
     "перевод другого предложения"),
    # 10443 Schall
    (18072, "example_ru",
     "Звук колоколов доносился по всему городу",
     "Звук колоколов разносился по всему городу",
     "«доносился по» — не то управление"),
    # 10444 frühzeitig
    (18905, "example_ru",
     "Спасибо, что своевременно меня предупредил",
     "Нам следует заранее пойти на вокзал",
     "перевод другого предложения"),
    (18905, "example_uk", "Ми повинні рано йти на вокзал",
     "Ми повинні заздалегідь піти на вокзал",
     "«frühzeitig» это заздалегідь, а не рано"),
    # 10445 zusammenhängen
    (8406, "example_uk", "Усі ці речи пов'язані між собою",
     "Усі ці речі пов'язані між собою",
     "«речи» — русская форма"),
    # 10446 reinfallen
    (8407, "example_uk", "Він спіткнувся і впав",
     "Я попався на його хитрість",
     "перевод другого предложения"),
    (8407, "example_tr", "Onun tatlı sözlerine kandım",
     "Onun oyununa kandım",
     "в эталоне «Trick», а не сладкие речи"),
    # 10447 aufsagen
    (14293, "example_uk", "Учні повинні були декламувати поезію",
     "Учні мусили декламувати вірш",
     "«поезія» это род литературы, а не одно стихотворение"),
    (14293, "example_tr", "Öğrenciler şiiri söylemek zorundaydı",
     "Öğrenciler şiiri ezbere okumak zorundaydı",
     "«söylemek» теряет «наизусть»"),
    (14293, "example_pl", "Dziecko recytuje wierszyk na scenie",
     "Uczniowie musieli wyrecytować wiersz",
     "перевод другого предложения"),
    # 10449 galant
    (11423, "example_tr", "Çok kibar davrandı ve kapıyı açtı",
     "Çok centilmen davrandı ve ona kapıyı açtı",
     "потеряно «ihr»"),
    # 10451 Zucht
    (17879, "example_pl", "Prowadzą hodowlę koni pod miastem",
     "Hodowla koni wymaga dużo cierpliwości i doświadczenia",
     "перевод другого предложения"),
    # 10452 verwendeten
    (8408, "example_pl", "Do chleba używam tylko tego noża",
     "Użyli starych materiałów do projektu",
     "перевод другого предложения"),
    # 10453 Refrain
    (14764, "example_uk",
     "Припев цієї пісні дуже запам'ятовується",
     "Приспів цієї пісні дуже запам'ятовується",
     "«припев» — русское слово"),
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
