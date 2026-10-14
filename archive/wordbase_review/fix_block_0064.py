"""
Правки блока 64 (ряды 11101–11300, ранги 22894–23146).

Находка блока — слово ряда подменено в эталоне ПОХОЖИМ ДРУГИМ, и дважды:

    ряд  der Skalp
    de   Der Chirurg benutzte das Skalpell für die Operation
    pl   Wojownik zdjął wrogowi skalp              ← один перевёл верно

    ряд  der Quell
    de   Die Quelle des Flusses liegt in den Bergen

`Skalp` это скальп, `Skalpell` — скальпель; слова похожи только
началом. Четыре перевода из пяти пошли за эталоном и написали про
хирурга; правильное значение взял только польский.

Это та же семья, что `Holder` (блок 63) и `vermöbeln` (блок 60), но
первая её часть, которую удалось поймать формально: похожее слово видно
по строению. Примета `scan_de_headword_swap` сделана и по базе даёт
ровно два ряда — этот и `Paradox`, где в примере стоит `Paradoxon`.
`Quell` она не находит, и почему — написано в её скрипте: `Quelle` это
`Quell` плюс законное окончание, и правилом эти два случая не
различить.

Попутно примета вывела семь рядов, где слово показано ТОЛЬКО внутри
составного: `Rubel` через `Rubelkurs`, `Chrom` через `Chromteile`,
`Parkett` через `Parkettboden`. Это не дефект — фраза верна и слово в
ней есть, — но ученику показывают не то слово, которое он учит. Решение
за владельцем, в правки не вошло.

Третий дефект в эталоне того же рода, что в блоках 60–63:

    Das Erdbeben hatte verheerend Folgen für die Stadt

`verheerend` перед существительным требует окончания: `verheerende`.

И четвёртый, который стоит записать особо:

    Die Gefangenen wurden mit Fesseln an den Beinen gefesselt

`mit Fesseln … gefesselt` — одно и то же слово дважды, как `Filmmusik
des Films` в блоке 63. Два раза за два блока, и оба раза в немецком.

    python -m app.scripts.fix_block_0064            # показать
    python -m app.scripts.fix_block_0064 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 11101 Minibar
    (11994, "example_uk", "Міні-бар у номері готелю зручний, але дорогий",
     "Мінібар у номері готелю зручний, але дорогий",
     "в статье «мінібар», без дефиса"),
    (11994, "example_pl", "W pokoju jest minibar z napojami",
     "Minibar w pokoju hotelowym jest praktyczny, ale drogi",
     "перевод другого предложения"),
    # 11102 Stärkung
    (11995, "translation_uk",
     "укріплення, зміцнення, перекус, підкріплення",
     "зміцнення, підсилення, перекус, підкріплення",
     "«укріплення» — русизм, и украинское слово рядом уже стоит"),
    (11995, "example_uk", "Ці вправи для зміцнення спини",
     "Невеликий перекус перед тренуванням дуже важливий",
     "перевод совсем другого предложения"),
    (11995, "example_pl", "Zjedz coś na wzmocnienie przed treningiem",
     "Mała przekąska przed treningiem jest bardzo ważna",
     "перевод другого предложения"),
    # 11103 rasseln
    (8540, "example_uk", "Ланцюги гримлять в ночі",
     "Ланцюги гримлять уночі",
     "«в ночі» — не та форма"),
    (8540, "example_tr", "Zincirler gece gürültü çıkarıyor",
     "Zincirler gece şıngırdıyor",
     "«gürültü çıkarmak» это шуметь вообще, а в статье «şıngırdamak»"),
    (8540, "example_pl", "Łańcuchy grzechotały w nocy",
     "Łańcuchy grzechoczą w nocy",
     "эталон в настоящем времени"),
    # 11105 Feuerwerkskörper
    (12393, "example_uk",
     "Феєрверки в ніч Нового року були особливо гучні",
     "Феєрверки новорічного вечора були особливо гучні",
     "`Silvesterabend` это вечер, а не ночь"),
    # 11106 Etappe
    (8541, "example_tr", "Yolculuğumuzun sonraki etabı Portekize gidiyor",
     "Yolculuğumuzun sonraki etabı Portekiz'e gidiyor",
     "потерян апостроф в названии"),
    # 11107 Sieb
    (11996, "example_pl", "Przesiej mąkę przez sitko",
     "Przesiewam mąkę przez sitko",
     "эталон от первого лица, а не в повелительном"),
    # 11108 durchbohren
    (8542, "example_uk", "Стріла пробиває броню",
     "Стріла проб'є броню",
     "эталон в будущем времени"),
    (8542, "example_pl", "Strzała przebiła zbroję na wylot",
     "Strzała przebije zbroję",
     "эталон в будущем, и «na wylot» в нём нет"),
    # 11110 Geschworener — сильное окончание в эталоне
    (16890, "example_de", "Der Geschworener muss unparteiisch bleiben",
     "Der Geschworene muss unparteiisch bleiben",
     "прилагательное-существительное после «der» берёт слабое окончание"),
    # 11111 offenkundig
    (8543, "example_uk", "Очевидно, що він брехує",
     "Очевидно, що він бреше",
     "«брехує» — нет такой формы"),
    # 11112 Hörgeschädigte
    (13109, "example_tr",
     "Olay işitme engelliler için tercüman sağladı",
     "Etkinlikte işitme engelliler için tercüman vardı",
     "«olay» это происшествие, а `Veranstaltung` — мероприятие"),
    # 11113 ungeheuer
    (8544, "example_tr", "Bu muazzam miktarda iştir",
     "Bu muazzam miktarda bir iş",
     "«iştir» без артикля повисает"),
    # 11114 vorzugsweise — глагол без дополнения в эталоне
    (8545, "example_de", "Sie sollten vorzugsweise am Wochenende besuchen",
     "Sie sollten uns vorzugsweise am Wochenende besuchen",
     "«besuchen» требует дополнения"),
    (8545, "example_en", "Preferably visit on the weekend",
     "You should preferably visit us on the weekend",
     "эталон не в повелительном, и потеряно дополнение"),
    (8545, "example_uk", "Переважно відвідуйте у вихідні",
     "Вам найкраще відвідати нас у вихідні",
     "эталон не в повелительном, и потеряно дополнение"),
    (8545, "example_tr", "Tercihen hafta sonu ziyaret edin",
     "Tercihen hafta sonu bizi ziyaret etmelisiniz",
     "эталон не в повелительном, и потеряно дополнение"),
    (8545, "example_pl", "Zadzwoń najlepiej wieczorem",
     "Powinniście odwiedzić nas najlepiej w weekend",
     "перевод другого предложения"),
    # 11119 Geruchssinn
    (13112, "example_tr",
     "Yaşlanmayla koku alma duyusu bazen bozulabilir",
     "Yaşla birlikte koku alma duyusu bazen zayıflar",
     "«yaşlanmayla» — калька, и «bozulabilir» это может сломаться"),
    (13112, "example_pl", "Po chorobie straciłem węch",
     "Z wiekiem węch czasami się pogarsza",
     "перевод другого предложения"),
    # 11120 Stieftochter
    (15312, "example_uk", "Його падчерка зараз навчається в Берліні",
     "Його пасербиця зараз навчається в Берліні",
     "перевод слова первым значением"),
    (15312, "example_tr", "Üvey kızı şu anda Berlinde okuyor",
     "Üvey kızı şu anda Berlin'de okuyor",
     "потерян апостроф в названии"),
    # 11121 mangelnd
    (8546, "example_uk",
     "Недостатня підготовка привела до поганих результатів",
     "Недостатня підготовка призвела до поганих результатів",
     "«привела до» — калька"),
    (8546, "example_pl", "Niedostateczne przygotowanie widać od razu",
     "Niedostateczne przygotowanie doprowadziło do słabych wyników",
     "перевод другого предложения"),
    # 11122 zurückfliegen
    (17386, "example_tr", "Tatilden sonra yarın Berline geri uçuyoruz",
     "Tatilden sonra yarın Berlin'e geri uçuyoruz",
     "потерян апостроф в названии"),
    # 11123 jämmerlich
    (11504, "example_uk", "Його результат був справді жалким",
     "Його результат був справді жалюгідним",
     "перевод слова первым значением"),
    # 11124 Warze
    (13113, "example_tr",
     "Dermatoloji doktoru elimdeki siğilleri çıkardı",
     "Cilt doktoru elimdeki siğilleri aldı",
     "«dermatoloji doktoru» — удвоение, и «çıkarmak» о родинках не "
     "говорят"),
    (13113, "example_pl", "Lekarz usunął mi brodawkę z ręki",
     "Dermatolog usunął mi brodawki z ręki",
     "в эталоне бородавок несколько, и врач — дерматолог"),
    # 11125 Fessel — одно слово дважды в эталоне
    (16892, "example_de",
     "Die Gefangenen wurden mit Fesseln an den Beinen gefesselt",
     "Die Gefangenen wurden an den Beinen gefesselt",
     "«mit Fesseln … gefesselt» — одно и то же слово дважды"),
    (16892, "example_tr",
     "Tutukluları bacaklarına zincir vurularak bağlandı",
     "Tutuklular bacaklarından zincirle bağlandı",
     "«tutukluları» в пассиве не бывает"),
    (16892, "example_pl", "Zdjęli mu kajdany z rąk",
     "Więźniom zakuto nogi w kajdany",
     "перевод другого предложения"),
    # 11126 Polster
    (18465, "example_uk", "Диван має дуже м'яку обивку",
     "Диван має дуже м'яку оббивку",
     "в статье «оббивка», с двумя б"),
    # 11127 Skalp — слово ряда подменено похожим
    (13114, "example_de",
     "Der Chirurg benutzte das Skalpell für die Operation",
     "Der Krieger nahm dem Feind den Skalp",
     "`Skalpell` это скальпель, а ряд о скальпе"),
    (13114, "example_en", "The surgeon used a scalpel for the operation",
     "The warrior took the enemy's scalp",
     "перевод пошёл за подменённым словом"),
    (13114, "example_ru", "Хирург использовал скальпель для операции",
     "Воин снял с врага скальп",
     "перевод пошёл за подменённым словом"),
    (13114, "example_uk", "Хірург використовував скальпель для операції",
     "Воїн зняв з ворога скальп",
     "перевод пошёл за подменённым словом"),
    (13114, "example_tr", "Cerrah operasyon için bistüri kullandı",
     "Savaşçı düşmanın kafa derisini yüzdü",
     "перевод пошёл за подменённым словом"),
    # 11128 Gefängniszelle
    (16893, "example_uk", "В'язень провів роки у в'язницькій камері",
     "В'язень провів роки в тюремній камері",
     "«в'язницький» — нет такой формы, в статье «тюремна камера»"),
    # 11130 Arbeitsamt
    (9254, "example_tr", "Yarın iş acentesine gidip kaydolmam gerekiyor",
     "Yarın iş kurumuna gidip kaydolmam gerekiyor",
     "«iş acentesi» — не термин, в статье «iş kurumu»"),
    # 11131 beglücken
    (11505, "example_en", "Your letter really delighted my grandmother",
     "She was delighted to see her old friend again",
     "перевод остался от прежнего эталона"),
    (11505, "example_uk", "Твій лист мене дуже порадував",
     "Вона була щаслива знову побачити свою давню подругу",
     "перевод остался от прежнего эталона"),
    (11505, "example_pl", "Jej uśmiech uszczęśliwia całą rodzinę",
     "Była szczęśliwa, że znów widzi swoją starą przyjaciółkę",
     "перевод другого предложения"),
    # 11132 Expansion
    (17886, "example_tr", "Şirket Avrupaya genişleme planlıyor",
     "Şirket Avrupa'ya genişlemeyi planlıyor",
     "потерян апостроф и аккузатив"),
    (17886, "example_pl", "Firma planuje ekspansję na rynek europejski",
     "Firma planuje ekspansję do Europy",
     "«na rynek europejski» в эталоне нет"),
    # 11133 Absturzstelle
    (17387, "example_pl",
     "Ratownicy dotarli na miejsce katastrofy samolotu",
     "Miejsce katastrofy samolotu zostało zbadane przez służby ratunkowe",
     "перевод другого предложения"),
    # 11134 Feingefühl
    (11506, "example_pl", "Mówił o tym z wielkim wyczuciem",
     "Mówił z wielkim wyczuciem o drażliwym temacie",
     "потеряно «über das heikle Thema»"),
    # 11135 zweierlei
    (8547, "example_en",
     "There are two kinds of ways to solve this problem",
     "There are two ways to solve this problem",
     "«two kinds of ways» — не по-английски"),
    (8547, "example_uk", "Є два види способів вирішити цю проблему",
     "Є два способи вирішити цю проблему",
     "«два види способів» — калька"),
    (8547, "example_tr", "Bu sorunu çözmek için iki çeşit yol vardır",
     "Bu sorunu çözmenin iki yolu var",
     "«iki çeşit yol» — калька"),
    (8547, "example_pl", "Mam dwojakie uczucia w tej sprawie",
     "Są dwa sposoby rozwiązania tego problemu",
     "перевод другого предложения"),
    # 11136 vormittags
    (18933, "example_uk", "У першій половині дня ми працюємо",
     "У першій половині дня ми працюємо в офісі",
     "потеряно «im Büro»"),
    (18933, "example_tr", "Sabahları çalışıyoruz",
     "Sabahları ofiste çalışıyoruz",
     "потеряно «im Büro»"),
    # 11137 letzterer
    (8548, "example_uk",
     "Я можу вибрати між чаєм і кавою, останнє я волію",
     "Я можу вибрати між чаєм і кавою — другому я віддаю перевагу",
     "«останнє я волію» — разваленная конструкция"),
    # 11157 Hepatitis
    (13116, "example_pl",
     "Zaszczepiłem się przeciwko zapaleniu wątroby",
     "Został przyjęty do szpitala z zapaleniem wątroby",
     "перевод другого предложения"),
    # 11158 Bibliothekarin
    (9255, "example_ru",
     "Библиотекарша помогла мне найти нужную книгу",
     "Библиотекарь помогла мне найти нужную книгу",
     "«библиотекарша» — пренебрежительное, в статье «библиотекарь»"),
    # 11159 Basislager
    (17388, "example_tr", "Dağın eteğindeki baz kamp iyi donanımlıydı",
     "Dağın eteğindeki ana kamp iyi donanımlıydı",
     "«baz kamp» — не термин, в статье «ana kamp»"),
    (17388, "example_pl",
     "Wspinacze wrócili do obozu bazowego przed zmrokiem",
     "Obóz bazowy u podnóża góry był dobrze wyposażony",
     "перевод другого предложения"),
    # 11160 anfeuern
    (12394, "example_tr",
     "Taraftarlar oyun sırasında takımlarını destekliyor",
     "Taraftarlar maç sırasında takımlarını destekliyor",
     "`Spiel` здесь матч, а не игра вообще"),
    # 11161 beharrlich
    (11511, "example_tr", "İsrarlı çabalarla sonunda başardı",
     "Israrlı çabalarla sonunda başardı",
     "в турецком заглавная «I» без точки"),
    (11511, "example_pl", "Był wytrwały i w końcu mu się udało",
     "Wytrwałymi staraniami w końcu mu się udało",
     "потеряно «mit beharrlichen Bemühungen»"),
    # 11163 Rundfunk
    (14309, "example_en",
     "The broadcasting company reported on the most important news",
     "The radio reported on the most important news",
     "«company» в эталоне нет"),
    # 11164 golfen
    (12395, "example_uk", "На вихідних я граю в гольф",
     "На вихідних я часто граю в гольф",
     "потеряно «oft»"),
    (12395, "example_tr", "Hafta sonunda golf oynuyorum",
     "Hafta sonları sık sık golf oynuyorum",
     "потеряно «oft»"),
    # 11166 abbrennen
    (8553, "example_uk", "Феєрверк буде горіти о півночі",
     "Феєрверк запустять опівночі",
     "`abbrennen` о фейерверке это запустить, а не горіти"),
    (8553, "example_tr", "Havai fişek gece yarısında ateş açacak",
     "Havai fişekler gece yarısı ateşlenecek",
     "«ateş açmak» значит открыть огонь из оружия"),
    # 11167 brünett — эталон заменили после перевода
    (15313, "example_en", "My sister is a tall brunette",
     "My sister is brunette, I am blonde",
     "перевод остался от прежнего эталона"),
    (15313, "example_ru", "Её брат высокий и темноволосый",
     "Моя сестра темноволосая, а я блондинка",
     "перевод остался от прежнего эталона, да ещё и про брата"),
    (15313, "example_uk", "Він високий і темноволосий",
     "Моя сестра темноволоса, а я блондинка",
     "перевод остался от прежнего эталона"),
    (15313, "example_tr", "Kardeşim esmer ve kıvırcık saçlı",
     "Kardeşim esmer, ben sarışınım",
     "перевод остался от прежнего эталона"),
    # 11168 Einweisung
    (13117, "example_pl", "Przed pracą dostaliśmy krótki instruktaż",
     "Skierowanie do szpitala nastąpiło zaraz po diagnozie",
     "перевод другого предложения"),
    # 11169 Scheide
    (13118, "example_en", "The doctor examined the patient",
     "The doctor examined the patient's vagina",
     "слово ряда из фразы выпало"),
    (13118, "example_uk", "Лікар оглянув пацієнтку",
     "Лікар оглянув піхву пацієнтки",
     "слово ряда из фразы выпало"),
    (13118, "example_tr", "Kılıç kınında taşınıyordu",
     "Doktor hastanın vajinasını inceledi",
     "перевод взял другое значение слова и построил свою фразу"),
    # 11171 melodramatisch
    (11512, "example_uk", "Його реакція була якась мелодраматична",
     "Його мелодраматична реакція була дещо перебільшеною",
     "потеряно «übertrieben», и «якась» в эталоне нет"),
    # 11173 sinnlich
    (11513, "example_uk",
     "Їжа була такою чуттєвою і ароматною, що у мене текла слина",
     "Запах був таким чуттєвим, що в мене потекла слина",
     "в эталоне запах, а не еда"),
    (11513, "example_tr",
     "Yemek o kadar lezzetli ve aromatikti ki ağzım sulandı",
     "Koku o kadar baştan çıkarıcıydı ki ağzım sulandı",
     "в эталоне запах, а не еда"),
    (11513, "example_pl", "Jej głos brzmiał bardzo zmysłowo",
     "Zapach był tak zmysłowy, że napłynęła mi woda do ust",
     "перевод другого предложения"),
    # 11174 Tupfer
    (13119, "example_pl", "Pielęgniarka przetarła ranę gazikiem",
     "Lekarz użył gazika, żeby oczyścić ranę",
     "перевод другого предложения"),
    # 11177 Arbeitslager
    (9257, "example_uk",
     "Історія трудових таборів — це темна та трагічна сторінка",
     "Історія трудових таборів темна й трагічна",
     "«сторінка» в эталоне нет"),
    # 11178 Einfaltspinsel
    (11514, "example_pl", "Nie bądź naiwniakiem, to oszustwo",
     "Ten naiwniak znowu mnie nabrał",
     "перевод другого предложения"),
    # 11179 fixieren
    (8555, "example_en", "He fixed his gaze on the target",
     "He fixes his gaze on the target",
     "эталон в настоящем времени"),
    (8555, "example_uk", "Він зафіксовує свій погляд на цілі",
     "Він фіксує свій погляд на цілі",
     "«зафіксовує» — нет такой формы"),
    (8555, "example_tr", "Gözünü hedefe dikti",
     "Gözünü hedefe dikiyor",
     "эталон в настоящем времени"),
    # 11180 verheerend — окончание прилагательного в эталоне
    (8556, "example_de",
     "Das Erdbeben hatte verheerend Folgen für die Stadt",
     "Das Erdbeben hatte verheerende Folgen für die Stadt",
     "прилагательное перед существительным требует окончания"),
    # 11181 Schikane
    (11515, "example_uk",
     "Переслідування на робочому місці зробило його хворим",
     "Цькування на робочому місці довело його до хвороби",
     "перевод слова первым значением, и «зробило хворим» — калька"),
    (11515, "example_tr", "İşyerindeki taciz onu hasta yaptı",
     "İşyerindeki taciz onu hasta etti",
     "«hasta yapmak» — калька"),
    # 11184 stumpfen
    (8557, "example_en", "Knives dull if you use them constantly",
     "The knife dulls if you use it constantly",
     "в эталоне один нож"),
    (8557, "example_uk",
     "Ножі тьмяніють, якщо їх постійно використовувати",
     "Ніж тупиться, якщо ним постійно користуватися",
     "«тьмяніти» это терять блеск, а не остроту"),
    (8557, "example_tr", "Bıçaklar sürekli kullanırsan körleşiyor",
     "Bıçak sürekli kullanırsan körleşir",
     "в эталоне один нож, и число рассогласовано со сказуемым"),
    # 11186 Flosse
    (15848, "example_ru", "Рыба изящно двигала плавник в воде",
     "Рыба изящно двигала плавником в воде",
     "«двигать» требует творительного"),
    (15848, "example_uk", "Риба елегантно рухала плавник у воді",
     "Риба елегантно рухала плавцем у воді",
     "«рухати» требует орудного"),
    (15848, "example_tr",
     "Balık yüzgeçini su içinde zarif bir şekilde hareket ettirdi",
     "Balık yüzgecini suda zarif bir şekilde hareket ettirdi",
     "«yüzgeçini» — не та согласная, и «su içinde» — калька"),
    # 11188 Zeitgefühl
    (18934, "example_tr", "Zaman hissi yok ve her zaman geç kalıyor",
     "Onun zaman hissi yok ve her zaman geç kalıyor",
     "фраза без подлежащего"),
    # 11189 Militärdienst
    (9258, "example_pl", "Po służbie wojskowej wrócił do domu",
     "Po służbie wojskowej chciał w końcu być cywilem",
     "перевод другого предложения"),
    # 11191 Quell — слово ряда подменено похожим
    (15849, "example_de", "Die Quelle des Flusses liegt in den Bergen",
     "Der Quell des Flusses liegt in den Bergen",
     "в ряду `der Quell`, а в примере `die Quelle` — другая форма "
     "с другим родом"),
    # 11192 Schund
    (8560, "example_uk", "Цей фільм — повна дрань",
     "Цей фільм — повний непотріб",
     "«дрань» — не украинское слово"),
    (8560, "example_tr", "Bu film saf çöptür",
     "Bu film tam bir çöp",
     "«saf» значит наивный или чистый, но не «полный»"),
    # 11193 Weihnachtszeit
    (18935, "example_ru",
     "В рождественский период магазины работают дольше",
     "В рождественский период мы украшаем дом огнями и украшениями",
     "перевод другого предложения"),
    (18935, "example_uk",
     "У різдвяний період ми прикрашаємо дім світлом і прикрасами",
     "У різдвяний період ми прикрашаємо дім гірляндами й прикрасами",
     "«Lichtern» это гирлянды, а не свет"),
    (18935, "example_tr",
     "Noel mevsiminde evi ışıklar ve dekorasyonlarla süsleriz",
     "Noel döneminde evi ışıklar ve süslerle süsleriz",
     "«mevsim» это время года по погоде, а не период"),
    # 11195 schluchzend
    (11516, "example_uk", "Ридаюча дитина шукала свою матір",
     "Дитина, що ридала, шукала свою матір",
     "«ридаюча» — калька активного дієприкметника; примета на этот "
     "класс её не взяла, слово короче восьми знаков"),
    # 11196 hochachtungsvoll
    (14311, "example_en",
     "He signed the letter respectfully as a business partner",
     "He ended his letter with a respectful greeting",
     "«as a business partner» придумано"),
    (14311, "example_tr",
     "Mektubu saygıyla bir işletme ortağı olarak imzaladı",
     "Mektubunu saygılarımla selamlayarak bitirdi",
     "«bir işletme ortağı olarak» придумано"),
    # 11199 trauernd
    (11517, "example_uk",
     "Скорбна сім'я стояла біля могили свого близька",
     "Скорботна сім'я стояла біля могили свого близького",
     "«скорбна» и «близька» — обе формы сломаны"),
    (11517, "example_pl",
     "Pogrążona w żałobie rodzina stała przy grobie",
     "Pogrążona w żałobie rodzina stała przy grobie bliskiej osoby",
     "потеряно «ihres Angehörigen»"),
    # 11200 Pokerspiel
    (12397, "example_uk",
     "Ми грали в покер з друзями до пізної ночі",
     "Ми грали в покер з друзями до пізньої ночі",
     "«пізної» — не та форма"),
    (12397, "example_tr",
     "Arkadaşlarla poker oyunu oynadık gece geç saatlere kadar",
     "Arkadaşlarla gece geç saatlere kadar poker oynadık",
     "обстоятельство оторвано в конец"),
    # 11201 zufriedenstellend
    (11518, "example_uk",
     "Продуктивність нового працівника була задовільною",
     "Робота нового працівника була задовільною",
     "`Leistung` это работа или результат, а не продуктивность"),
    (11518, "example_pl", "Wynik testu był zadowalający",
     "Wyniki nowego pracownika były zadowalające",
     "перевод другого предложения"),
    # 11202 Ladendiebstahl
    (16899, "example_uk",
     "Крадіжка в магазині — серйозний злочин із суровими наслідками",
     "Крадіжка в магазині — серйозний злочин із суворими наслідками",
     "«суровий» — русское слово"),
    (16899, "example_pl", "Złapali go na kradzieży w sklepie",
     "Kradzież w sklepie to przestępstwo z poważnymi konsekwencjami",
     "перевод другого предложения"),
    # 11203 Rezession
    (17887, "example_tr",
     "Resesyon birçok şirketi iflas ettirmesine neden oldu",
     "Resesyon birçok şirketin iflas etmesine neden oldu",
     "двойной каузатив разваливает фразу"),
    (17887, "example_pl", "W czasie recesji trudno znaleźć pracę",
     "Recesja doprowadziła wiele firm do upadku",
     "перевод другого предложения"),
    # 11204 Schlachthof
    (12002, "example_tr",
     "Hayvan kesim yeri hayvan refahı kuruluşları tarafından katı "
     "şekilde kontrol edilir",
     "Mezbaha, hayvan refahı kuruluşları tarafından sıkı şekilde "
     "denetlenir",
     "«hayvan … hayvan» — повтор, и в статье «mezbaha»"),
    (12002, "example_pl", "Krowy wiozą do rzeźni",
     "Rzeźnia jest surowo kontrolowana przez organizacje ochrony "
     "zwierząt",
     "перевод другого предложения"),
    # 11205 Verdeck
    (17390, "example_uk", "При дощу він не відкрив дах кабріолета",
     "Коли падав дощ, він не відкривав дах кабріолета",
     "«при дощу» — калька"),
    (17390, "example_pl",
     "Przy takiej pogodzie nie otwieraj dachu składanego",
     "Gdy padał deszcz, nie otwierał dachu kabrioletu",
     "перевод другого предложения"),
    # 11206 wacker
    (11519, "example_en", "The valiant soldier deserved a medal",
     "The valiantly fighting soldier deserved a medal",
     "потеряно «kämpfende»"),
    (11519, "example_uk", "Доблесний боєць заслужив медаль",
     "Солдат, що мужньо бився, заслужив медаль",
     "потеряно «kämpfende»"),
    (11519, "example_tr", "Cesur asker bir madalya hak etti",
     "Yiğitçe savaşan asker bir madalya hak etti",
     "потеряно «kämpfende»"),
    (11519, "example_pl", "Dzielny chłopak, wcale się nie bał",
     "Dzielnie walczący żołnierz zasłużył na medal",
     "перевод другого предложения"),
    # 11207 Bundesgefängnis
    (16900, "example_tr", "Suçları için federal hapishanede oturuyor",
     "Suçları için federal hapishanede yatıyor",
     "о сроке по-турецки говорят «yatmak»"),
    (16900, "example_pl", "Trafił do więzienia federalnego na pięć lat",
     "Siedzi w więzieniu federalnym za swoje zbrodnie",
     "перевод другого предложения"),
    # 11208 verfaulen
    (8562, "example_uk",
     "Якщо не зберігати рибу в холоді, вона буде гнити",
     "Якщо не зберігати рибу в холоді, вона згниє",
     "«wird verfaulen» это однократно, а не длительно"),
    # 11209 geigen
    (14802, "example_uk",
     "Вона грає на скрипці, але сьогодні вечором вона грає особливо гарно",
     "Вона грає на скрипці, але сьогодні ввечері грає особливо гарно",
     "«вечором» — не та форма"),
    (14802, "example_pl", "Dziadek pięknie gra na skrzypcach",
     "Gra na skrzypcach, ale dziś wieczorem gra szczególnie pięknie",
     "перевод другого предложения"),
    # 11210 imponieren
    (11520, "example_pl", "Jego spokój bardzo mi imponuje",
     "Jego sukces bardzo mi imponuje, chociaż jest młody",
     "перевод другого предложения"),
    # 11211 Professorin
    (9628, "example_uk", "Професор дуже ясно пояснила складну теорію",
     "Професорка дуже ясно пояснила складну теорію",
     "перевод слова первым значением"),
    # 11213 unhörbar
    (8564, "example_uk", "Непочутні звуки кажана людина не може сприйняти",
     "Нечутні звуки кажана людина не може сприйняти",
     "«непочутий» это неуслышанный, а `unhörbar` — нечутний"),
    # 8414 Paradox — найдено приметой, вне блока
    (8414, "example_de",
     "Das ist ein echtes Paradoxon, das ich nicht verstehe",
     "Das ist ein echtes Paradox, das ich nicht verstehe",
     "в ряду `Paradox`, а в примере `Paradoxon` — другая форма слова"),
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
