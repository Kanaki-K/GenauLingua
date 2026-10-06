"""
Правки блока 67 (ряды 11701–11900, ранги 24287–24751).

Сквозная примета блока — турецкий апостроф. По-турецки падежный суффикс
к имени собственному присоединяется через апостроф: `Berlin'de`,
`Mozart'ın`, `Noel'de`. Это орфография, не стиль, и такие ряды
попадались почти в каждом блоке с шестидесятого — правились по одному.
Собрано в класс: `scan_tr_apostrophe` даёт девять рядов по базе.

Три рода ложных срабатываний определили, каким вышел список имён:

  * НАЗВАНИЯ ЯЗЫКОВ апострофа не берут — `Almancayı akıcı konuşuyor`
    верно, и `Almanca` в список не вошла;
  * ОБЫЧНОЕ СЛОВО, КОНЧАЮЩЕЕСЯ КАК ИМЯ: `Romanın girişi` это «начало
    романа», но если отрезать `nın`, остаётся `roma`. Поэтому `Roma`
    убрана из списка, а `Roma'dan` в ряду 14833 правится вручную —
    лучше потерять одно настоящее попадание, чем выдать три ложных;
  * СЛОВО, КОТОРОЕ БЫВАЕТ И ИМЕНЕМ, И НЕТ: `dünya` это и «мир», и
    планета Земля. `Dünyanın her yerinde` апострофа не требует, а
    `Dünya'nın kutbu` требует. Четыре таких ряда разобраны глазами.

Из немецких дефектов блока стоит записать два.

    Die Gelee auf dem Kuchen sah wunderbar aus      → Das Gelee
    Die Polizei vereitelten den Überfall            → vereitelte

Первый — род: `das Gelee`, а не `die`. Второй — число: `die Polizei`
по-немецки единственного числа, и сказуемое при нём единственное.

И ещё один ряд того же класса, что `betrauen` (9284):

    de  Er wurde mit der Leitung betraut
    en  The priest married the couple in the cathedral
    uk  Священник вінчає пару у соборі
    tr  Rahip çifti katedralde evlendiriyor

Три перевода сошлись на фразе про священника в соборе, которая к
слову `betrauen` — «поручать» — отношения не имеет вовсе. Эталон
заменили после перевода; класс описан в блоке 61 и к блоку 65 стал
самым частым в базе.

    python -m app.scripts.fix_block_0067            # показать
    python -m app.scripts.fix_block_0067 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── правки по примете scan_tr_apostrophe, вся база ──────────────
    (16, "example_tr", "Güzel bir eski binada Berlinde oturuyor",
     "Güzel bir eski binada Berlin'de oturuyor",
     "имя собственное требует апострофа перед суффиксом"),
    (2238, "example_tr", "Birçok göçmen Amerikaya gitti",
     "Birçok göçmen Amerika'ya gitti",
     "имя собственное требует апострофа перед суффиксом"),
    (9949, "example_tr",
     "Londradaki ünlü müzayede evi bir tabloyu milyonlara sattı",
     "Londra'daki ünlü müzayede evi bir tabloyu milyonlara sattı",
     "имя собственное требует апострофа перед суффиксом"),
    (14591, "example_tr",
     "Yerli Amerikalılar uzun süre Amerikada yaşadılar",
     "Yerli Amerikalılar uzun süre Amerika'da yaşadılar",
     "имя собственное требует апострофа перед суффиксом"),
    (17238, "example_tr", "Münihe araç paylaşımı arıyorum",
     "Münih'e araç paylaşımı arıyorum",
     "имя собственное требует апострофа перед суффиксом"),
    (17362, "example_tr", "Kervan çölün içinden Mısıra gitti",
     "Kervan çölün içinden Mısır'a gitti",
     "имя собственное требует апострофа перед суффиксом"),
    (15301, "example_tr",
     "Her Noelde birlikte kutlamak bir aile geleneğidir",
     "Her Noel'de birlikte kutlamak bir aile geleneğidir",
     "имя собственное требует апострофа перед суффиксом"),
    (18946, "example_tr", "Noelde güzel bir hediye dağıtımı oldu",
     "Noel'de güzel bir hediye dağıtımı oldu",
     "имя собственное требует апострофа перед суффиксом"),
    # планета Земля — апостроф нужен; «мир» — нет, эти четыре разобраны
    # глазами, и примета их не берёт
    (17560, "example_tr", "Sonda Dünyaya veri gönderiyor",
     "Sonda Dünya'ya veri gönderiyor",
     "здесь `Dünya` это планета, а не «мир»"),
    (18059, "example_tr",
     "Dünyanın kutbu çok soğuk ve yaşam için elverişsizdir",
     "Dünya'nın kutbu çok soğuk ve yaşam için elverişsizdir",
     "здесь `Dünya` это планета, а не «мир»"),
    (18068, "example_tr", "Dünyanın küresel şekli iyi biliniyor",
     "Dünya'nın küresel şekli iyi biliniyor",
     "здесь `Dünya` это планета, а не «мир»"),
    (11188, "example_tr", "Dünyanın her yerinde birçok hayranı var",
     "dünyanın her yerinde birçok hayranı var",
     "здесь `dünya` это «мир», и с большой буквы его писать не нужно"),
    # ── блок 67 ────────────────────────────────────────────────────
    # 11701 schizophren
    (13156, "example_pl", "Lekarz stwierdził objawy schizofreniczne",
     "Wykazywał objawy schizofreniczne",
     "«lekarz» в эталоне нет"),
    # 11704 Kameradschaft
    (11581, "example_uk",
     "Бойове товариство між солдатами було вражаючим",
     "Товариськість між солдатами була гідна захоплення",
     "перевод слова первым значением, и `bewunderungswürdig` это "
     "гідний захоплення"),
    (11581, "example_pl",
     "Koleżeństwo między żołnierzami było naprawdę silne",
     "Koleżeństwo między żołnierzami było godne podziwu",
     "«naprawdę silne» вместо `bewunderungswürdig`"),
    # 11705 besonnen
    (11582, "example_tr", "Sakin lider doğru kararı aldı",
     "Sağduyulu lider doğru kararı aldı",
     "перевод слова первым значением"),
    (11582, "example_pl", "Ona jest spokojna i rozważna",
     "Rozważny przywódca podjął właściwą decyzję",
     "перевод другого предложения"),
    # 11706 Nervenklinik
    (13157, "example_tr", "Psikiyatrik klinikte tedavi görüyordu",
     "Psikiyatri hastanesinde tedavi gördü",
     "перевод слова первым значением"),
    # 11707 fummeln
    (8666, "example_uk", "Досить возитися, ми вже спізнюємось",
     "Він нервово вовтузився зі своїми ключами",
     "перевод совсем другого предложения"),
    (8666, "example_tr", "Telefonumu ellemeyi bırak!",
     "Anahtarlarıyla sinirli sinirli oynadı",
     "перевод совсем другого предложения"),
    # 11708 röcheln
    (13158, "example_tr", "Yaşlı adam gece ağır nefes alıyor",
     "Yaşlı adam geceleri ağır ağır hırıldıyor",
     "«ağır nefes almak» теряет хрип, в статье «hırıldamak»"),
    # 11710 gerieben
    (11583, "example_pl", "To przebiegły handlarz samochodów",
     "Był przebiegłym biznesmenem o wątpliwych metodach",
     "перевод другого предложения"),
    # 11713 Dienstgrad
    (9281, "example_uk", "Його військовий ранг був полковник",
     "Його військове звання — полковник",
     "в статье «звання», и падеж не тот"),
    (9281, "example_pl", "Jaki masz stopień wojskowy",
     "Jego stopień wojskowy to pułkownik",
     "перевод другого предложения, да ещё и вопрос без знака"),
    # 11714 Bajonett
    (16963, "example_uk", "Штик був прикріпований до гвинтівки",
     "Штик був прикріплений до гвинтівки",
     "«прикріпований» — нет такой формы"),
    # 11715 zanken
    (11584, "example_tr",
     "İki komşu sürekli küçük şeyler için tartışıyor",
     "İki komşu sürekli küçük şeyler için kavga ediyor",
     "«tartışmak» это обсуждать, а в статье «kavga etmek»"),
    # 11716 Benefizveranstaltung
    (14825, "example_uk",
     "Благодійна подія для бідних була великим успіхом",
     "Благодійний захід на допомогу бідним мав великий успіх",
     "перевод слова первым значением"),
    (14825, "example_tr",
     "Fakir için yapılan hayır işi etkinliği büyük bir başarı oldu",
     "Yoksullar için düzenlenen hayır etkinliği büyük bir başarı oldu",
     "«fakir» в единственном, и «hayır işi etkinliği» — лишнее слово"),
    # 11717 Nähmaschine
    (18483, "example_uk",
     "Стара швацька машина працює дуже добре",
     "Стара швейна машина досі працює дуже добре",
     "в статье «швейна машина», и потеряно «noch»"),
    # 11718 Fasan
    (15875, "example_uk", "Дикий фазан літав над полем",
     "Дикий фазан пролетів над полем",
     "«літав» это многократно, а в эталоне один раз"),
    (15875, "example_tr", "Bir yaban sülünü alanın üzerinde uçtu",
     "Bir yaban sülünü tarlanın üzerinde uçtu",
     "«alan» это площадь, а `Feld` — поле"),
    # 11719 Gelenke
    (13160, "example_pl", "Bolą mnie stawy po bieganiu",
     "Bolą mnie stawy po długim bieganiu",
     "потеряно «langen»"),
    # 11720 Jod
    (13161, "example_pl", "Lekarz kazał mi jeść więcej jodu",
     "Lekarz zalecił mi przyjmować więcej jodu",
     "«jeść jod» — не по-польски"),
    # 11721 weglocken
    (8667, "example_en", "She tried to lure the dog away with treats",
     "She tries to lure the dog away with treats",
     "эталон в настоящем времени"),
    (8667, "example_uk",
     "Вона намагалася завманити собаку геть ласощами",
     "Вона намагається виманити собаку ласощами",
     "«завманити» — нет такого слова, и эталон в настоящем"),
    (8667, "example_tr",
     "Köpeği ödüllerle uzaklaştırmaya çalışıyorum",
     "Köpeği ödüllerle uzaklaştırmaya çalışıyor",
     "в эталоне «sie», а не «я»"),
    (8667, "example_pl", "Zwabiła psa z podwórka smakołykami",
     "Próbuje zwabić psa smakołykami",
     "эталон в настоящем, и «z podwórka» в нём нет"),
    # 11722 verankert
    (8668, "example_tr", "Bu alışkanlık onda iyice yerleşmiş",
     "Umut onun kalbinde derinlemesine yerleşmiş",
     "перевод другого предложения"),
    (8668, "example_pl",
     "Ten zwyczaj jest głęboko zakorzeniony w naszej rodzinie",
     "Nadzieja jest głęboko zakorzeniona w jego sercu",
     "перевод другого предложения"),
    # 11723 Bettzeug
    (18484, "example_tr",
     "Yatak çarşaflarını yıkamam ve değiştirmem gerekiyor",
     "Yatak takımını yıkamam ve değiştirmem gerekiyor",
     "«çarşaf» это простыня, а в статье «yatak takımı»"),
    # 11724 Schaft — род в эталоне
    (8669, "example_de", "Die Schaft meines Stiefels ist zerrissen",
     "Der Schaft meines Stiefels ist zerrissen",
     "«der Schaft», а не «die»"),
    # 11725 schnuppern
    (8670, "example_en", "The cat sniffs at the new plant",
     "The cat sniffs at the new plants",
     "в эталоне растений несколько"),
    (8670, "example_uk", "Кіт нюхає нову рослину",
     "Кіт обнюхує нові рослини",
     "перевод слова первым значением, и в эталоне множественное"),
    (8670, "example_tr", "Kedi yeni bitki kokluyor",
     "Kedi yeni bitkileri kokluyor",
     "потерян аккузатив, и в эталоне множественное"),
    # 11727 Klavierspiel
    (14826, "example_uk", "Його гра на піаніно справді вражає",
     "Його гра на фортепіано справді вражає",
     "в статье «гра на фортепіано»"),
    # 11728 seelisch
    (11530, "example_uk",
     "Психічна перенапруга була занадто великою",
     "Душевне навантаження було занадто великим",
     "перевод слова первым значением"),
    # 11729 Bettdecke
    (18485, "example_pl", "W nocy naciąga kołdrę pod brodę",
     "W nocy naciąga kołdrę",
     "«pod brodę» в эталоне нет"),
    # 11730 belebt
    (8671, "example_tr", "Şehirdeki canlı bir sokaktu",
     "Şehirde hareketli bir sokaktı",
     "«sokaktu» — не та гласная, и порядок слов сломан"),
    # 11731 nachstellen
    (8672, "example_en", "The police pursued the thief down the street",
     "The dog stalks the cat",
     "перевод совсем другого предложения"),
    # 11732 zitternd
    (11586, "example_tr", "Titreyerek mektubu açtı",
     "Titreyen ellerle mektubu açtı",
     "потеряно «mit zitternden Händen»"),
    # 11733 Versagerin
    (11587, "example_tr", "Başarısız kişi olarak görülmek istemedi",
     "Başarısız bir kadın olarak görülmek istemedi",
     "потерян женский род слова ряда"),
    # 11735 Abriegelung
    (16964, "example_ru", "Блокада города была очень жесткой",
     "Блокирование города было очень жёстким",
     "перевод слова первым значением, и «е» вместо «ё»"),
    (16964, "example_uk", "Блокада міста була дуже суворою",
     "Блокування міста було дуже суворим",
     "перевод слова первым значением"),
    (16964, "example_tr", "Şehrin kapanması çok sıkıydı",
     "Şehrin kapatılması çok sıkıydı",
     "«kapanma» это «закрылся сам», а тут закрыли"),
    (16964, "example_pl", "Policja zarządziła blokadę całej dzielnicy",
     "Blokada miasta była bardzo surowa",
     "перевод другого предложения"),
    # 11736 unattraktiv
    (11589, "example_tr", "Teklif ekonomik açıdan çekici olmayan",
     "Teklif ekonomik açıdan çekici değildi",
     "фраза без сказуемого"),
    # 11737 Holzbein
    (13162, "example_uk",
     "Старий мореплавець носив дерев'яну ногу",
     "Старий моряк носив дерев'яну ногу",
     "`Seemann` это моряк, а не мореплавець"),
    (13162, "example_tr", "Yaşlı gemi kaptanı tahta bacak takıyordu",
     "Yaşlı denizci tahta bacak takıyordu",
     "«gemi kaptanı» это капитан"),
    (13162, "example_pl", "Pirat z bajki miał drewnianą nogę",
     "Stary marynarz nosił drewnianą nogę",
     "перевод другого предложения"),
    # 11738 zerstückeln — одно и то же дважды в эталоне
    (8673, "example_de", "Wir müssen das Fleisch in Stücke zerstückeln",
     "Wir müssen das Fleisch zerstückeln",
     "«in Stücke zerstückeln» — одно и то же дважды"),
    (8673, "example_uk", "Нам потрібно нарізати м'ясо шматками",
     "Нам потрібно розрізати м'ясо на шматки",
     "перевод слова первым значением"),
    (8673, "example_tr", "Eti parçalara dogramalıyız",
     "Eti parçalara doğramalıyız",
     "«dogramak» — потерян мягкий g"),
    # 11740 unmittelbar
    (8674, "example_tr", "İşten sonra doğrudan eve gittim",
     "Yakın çevre çok yeşildi",
     "перевод совсем другого предложения"),
    # 11741 Cartoon
    (14827, "example_uk", "Мультфільм дуже смішний",
     "Мультфільм був дуже смішний",
     "эталон в прошедшем времени"),
    (14827, "example_tr", "Çizgi film çok komik",
     "Çizgi film gerçekten komikti",
     "эталон в прошедшем времени"),
    # 11742 Krawall
    (16965, "example_pl", "Po meczu wybuchły zamieszki na ulicach",
     "Zamieszki wybuchły nagle",
     "перевод другого предложения"),
    # 11743 Knick
    (8675, "example_uk", "У плані був перегин",
     "У плані був різкий поворот",
     "«перегин» о плане не говорят"),
    (8675, "example_tr", "Gömleğin kolunda derin bir kırışık var",
     "Planda keskin bir dönüş vardı",
     "перевод другого предложения"),
    # 11746 Wiederkehr
    (18947, "example_tr", "Baharın geri dönüşü sevindi",
     "Baharın geri dönüşü sevindiriciydi",
     "«sevindi» значит «он обрадовался»"),
    # 11747 liegenlassen — эталон заменили после перевода
    (8678, "example_en", "I left my glasses behind",
     "I left my phone at the office",
     "перевод остался от прежнего эталона"),
    (8678, "example_uk", "Я залишив свої окуляри в кафе",
     "Я залишив телефон в офісі",
     "перевод остался от прежнего эталона"),
    (8678, "example_tr", "Gözlüklerimi bıraktım",
     "Telefonumu ofiste bıraktım",
     "перевод остался от прежнего эталона"),
    # 11750 Oberschwester
    (13164, "example_tr",
     "Başhemşire bölümdeki tüm hastaları denetliyor",
     "Başhemşire serviste tüm hastalarla ilgileniyor",
     "«denetlemek» это проверять, а `kümmert sich` — заботиться"),
    (13164, "example_pl",
     "Siostra przełożona rozmawiała z lekarzem na korytarzu",
     "Siostra przełożona opiekuje się wszystkimi pacjentami na oddziale",
     "перевод другого предложения"),
    # 11751 vortanzen
    (14828, "example_uk",
     "Він хоче мені танцювати й показати, як добре він танцює",
     "Він хоче потанцювати переді мною й показати, як добре він танцює",
     "«хоче мені танцювати» — сломанное управление"),
    (14828, "example_tr",
     "Bana karşısında dans etmek istiyor, ne kadar iyi dans ettiğini "
     "göstermek için",
     "Ne kadar iyi dans ettiğini göstermek için önümde dans etmek "
     "istiyor",
     "«bana karşısında» — два управления подряд"),
    # 11753 Logistik
    (9283, "example_pl", "Pracuje w logistyce od pięciu lat",
     "Logistyka naszej firmy jest bardzo dobrze zorganizowana",
     "перевод другого предложения"),
    # 11755 Sonntagabend
    (18948, "example_uk",
     "У неділю вечором ми завжди разом дивимось серіали",
     "У неділю ввечері ми завжди разом дивимося серіали",
     "«вечором» — не та форма"),
    # 11756 hinwollen — эталон заменили после перевода
    (8679, "example_en", "I want to go there, but the road is blocked",
     "I don't know where we want to go",
     "перевод остался от прежнего эталона"),
    (8679, "example_uk", "Я хочу туди, але дорога заблокована",
     "Я не знаю, куди ми хочемо дістатися",
     "перевод остался от прежнего эталона"),
    (8679, "example_tr", "Oraya gitmek istiyorum ama yol kapalı",
     "Nereye gitmek istediğimizi bilmiyorum",
     "перевод остался от прежнего эталона"),
    # 11757 robben
    (8680, "example_uk", "Військові мали повзати під перешкодами",
     "Солдати мусили повзти під перешкодами",
     "«військові» это военные вообще, и «повзати» это многократно"),
    (8680, "example_tr", "Asker çamurda sürünerek ilerledi",
     "Askerler engellerin altından sürünmek zorunda kaldı",
     "перевод другого предложения"),
    # 11758 Brathähnchen — число в эталоне
    (12024, "example_de",
     "Das Brathähnchen vom Markt schmeckt besser als gekochte Hähnchen",
     "Das Brathähnchen vom Markt schmeckt besser als gekochtes Hähnchen",
     "сравнение единственного с множественным"),
    (12024, "example_uk",
     "Запечена курка з ринку смакує краще, ніж варена",
     "Курча-гриль з ринку смакує краще, ніж варена курка",
     "перевод слова первым значением"),
    (12024, "example_tr",
     "Pazardan alınan ızgara tavuk kaynayan tavuktan daha lezzetli",
     "Pazardan alınan ızgara tavuk, haşlanmış tavuktan daha lezzetli",
     "«kaynayan» значит «кипящий», а нужно «отварной»"),
    (12024, "example_pl", "Kupiliśmy pieczonego kurczaka na obiad",
     "Pieczony kurczak z rynku smakuje lepiej niż gotowany",
     "перевод другого предложения"),
    # 11760 heimtückisch
    (11591, "example_uk", "Це був підступний посягання на його життя",
     "Це було підступне посягання на його життя",
     "рассогласование рода"),
    # 11761 Bildmaterial
    (14829, "example_uk",
     "Графічний матеріал для звіту ще не готовий",
     "Ілюстрації для звіту ще не готові",
     "перевод слова вторым значением из статьи"),
    (14829, "example_tr",
     "Rapor için görüntü materyali henüz hazır değil",
     "Rapor için görsel malzeme henüz hazır değil",
     "в статье «görsel malzeme»"),
    # 11763 Gebräu
    (12025, "example_pl", "Co to za dziwna mikstura w tym kubku",
     "Ta dziwna mikstura smakuje ziołami i miodem",
     "перевод другого предложения, да ещё и вопрос без знака"),
    # 11764 Arie
    (14830, "example_tr", "Mozartın operasındaki aryası harikaydi",
     "Mozart'ın operasındaki arya harikaydı",
     "потерян апостроф, лишний притяжательный и «harikaydi» — опечатка"),
    # 11765 Autowerkstatt
    (17405, "example_ru", "Мой автомобиль в автомастерской на ремонт",
     "Мой автомобиль в автомастерской на ремонте",
     "не тот падеж"),
    (17405, "example_uk", "Мій автомобіль в автомайстерні на ремонт",
     "Мій автомобіль в автомайстерні на ремонті",
     "не тот падеж"),
    (17405, "example_tr", "Arabam oto tamircisinde onarım için",
     "Arabam onarım için oto tamirhanesinde",
     "«tamirci» это мастер, а в статье «tamirhane»"),
    (17405, "example_pl", "Zostawiłem auto w warsztacie samochodowym",
     "Moje auto jest w warsztacie samochodowym na naprawie",
     "перевод другого предложения"),
    # 11766 Glamour
    (14831, "example_tr", "Onun cazibesine kimse karşı koyamıyor",
     "Bu Hollywood aktrisinin cazibesi eşsiz",
     "перевод другого предложения"),
    # 11767 Spezialeffekt
    (17743, "example_tr",
     "Bu filmindeki özel efektler gerçekten etkileyici",
     "Bu filmdeki özel efektler gerçekten etkileyici",
     "лишний притяжательный"),
    # 11769 Augenlider
    (13165, "example_uk",
     "Вона повільно закрила очі й подумала про нього",
     "Вона повільно закрила повіки й подумала про нього",
     "в эталоне веки, а не глаза"),
    # 11770 Mausoleum
    (14832, "example_uk",
     "Мавзолей знаменитого короля привертає тисячи відвідувачів",
     "Мавзолей знаменитого короля приваблює тисячі відвідувачів",
     "«тисячи» — русская форма"),
    # 11772 betrauen — эталон заменили после перевода
    (9284, "example_en", "The priest married the couple in the cathedral",
     "He was entrusted with the management",
     "перевод остался от прежнего эталона"),
    (9284, "example_uk", "Священник вінчає пару у соборі",
     "Йому доручили керівництво",
     "перевод остался от прежнего эталона"),
    (9284, "example_tr", "Rahip çifti katedralde evlendiriyor",
     "Yönetim ona emanet edildi",
     "перевод остался от прежнего эталона"),
    # 11773 antik
    (14833, "example_uk", "Вона купила стародавню вазу з Рима",
     "Вона купила античну вазу з Рима",
     "перевод слова первым значением"),
    (14833, "example_tr", "Romadan antika bir vazo aldı",
     "Roma'dan antika bir vazo aldı",
     "имя собственное требует апострофа; примета этого не берёт, "
     "потому что `Roma` из её списка убрана"),
    # 11774 Raffinerie
    (17890, "example_uk",
     "Нафтопереробний завод виробляє щодня тисячи барелів бензину",
     "Нафтопереробний завод виробляє щодня тисячі барелів бензину",
     "«тисячи» — русская форма"),
    (17890, "example_tr",
     "Rafinerisi günde binlerce varil benzin üretiyor",
     "Rafineri günde binlerce varil benzin üretiyor",
     "лишний притяжательный"),
    # 11775 Erntedankfest
    (14834, "example_tr",
     "Hasat festivali için tüm aile kendileri yetiştirdikleri meyveleri "
     "getiriyor",
     "Hasat bayramı için tüm aile kendi yetiştirdiği meyveleri getiriyor",
     "«kendileri yetiştirdikleri» — двойное согласование"),
    # 11776 aufrichten
    (8683, "example_uk", "Він встановив упавше дерево прямо",
     "Він знову випрямив повалене дерево",
     "«упавший» — русский дієприкметник"),
    (8683, "example_tr", "Düşen ağacı doğrultmaya çalıştı",
     "Düşen ağacı yeniden doğrulttu",
     "«çalıştı» значит «пытался», а в эталоне сделал"),
    # 11778 Videothek
    (14835, "example_tr",
     "Her cuma video kiralama dükkanından film kiralardık",
     "Her cuma video kiralama dükkânından film kiralardık",
     "потерян циркумфлекс, в статье он есть"),
    # 11780 verfrachten
    (17407, "example_pl", "Meble przewożą dużą ciężarówką",
     "Przewozi meble do ciężarówki",
     "перевод другого предложения"),
    # 11781 Tampon
    (13166, "example_pl", "Kupiła tampony w aptece",
     "Potrzebowała tamponu podczas okresu",
     "перевод другого предложения"),
    # 11783 Schwerverbrecher
    (16966, "example_ru",
     "Тяжёлый преступник был приговорён к пожизненному заключению",
     "Особо опасный преступник был приговорён к пожизненному заключению",
     "«тяжёлый преступник» — не по-русски"),
    (16966, "example_uk",
     "Серйозний злочинець був засуджений до довічного ув'язнення",
     "Особливо небезпечний злочинець був засуджений до довічного "
     "ув'язнення",
     "«серйозний злочинець» — не то"),
    # 11786 Tulpe
    (15876, "example_tr", "Bahçemizde sarı laleler açmış",
     "Annem için bir demet kırmızı lale aldım",
     "перевод другого предложения"),
    # 11787 Hotline
    (14325, "example_uk",
     "Ти можеш позвонити на гарячу лінію, якщо у тебе є проблеми",
     "Ти можеш подзвонити на гарячу лінію, якщо в тебе є проблеми",
     "«позвонити» — русское слово"),
    (14325, "example_tr",
     "Sorun yaşarsan müşteri hizmetlerine arayabilirsin",
     "Sorun yaşarsan müşteri hizmetlerini arayabilirsin",
     "«aramak» требует аккузатива"),
    # 11788 Schadensbericht
    (17891, "example_uk",
     "Агент страхової компанії потребував звіт про шкоду",
     "Агент страхової компанії затребував звіт про пошкодження",
     "«потребував» это нуждался, а `forderte an` — затребував"),
    # 11789 Strafverteidiger
    (16967, "example_ru", "Адвокат защищал своего клиента в суде",
     "Адвокат по уголовным делам защищал своего клиента в суде",
     "потеряно слово ряда"),
    (16967, "example_uk", "Адвокат захищав свого клієнта в суді",
     "Адвокат у кримінальних справах захищав свого клієнта в суді",
     "потеряно слово ряда"),
    (16967, "example_pl", "Jego obrońca wygrał sprawę w sądzie",
     "Obrońca w sprawach karnych bronił swojego klienta w sądzie",
     "перевод другого предложения"),
    # 11791 Alarmsystem
    (17744, "example_uk",
     "Систему сигналізації будинку активовано вночі",
     "Систему сигналізації будинку було активовано вночі",
     "безличный пассив вместо обычного"),
    # 11792 dämpfen
    (8684, "example_uk", "Вона намагалася придушити свій ентузіазм",
     "Вона намагалася приглушити свій захват",
     "перевод слова первым значением"),
    # 11795 gerichtlich
    (16969, "example_pl", "Sprawę załatwiliśmy drogą sądową",
     "Adwokat prowadził postępowanie sądowe",
     "перевод другого предложения"),
    # 11796 Krankengeschichte
    (13167, "example_pl", "Lekarz przejrzał moją historię choroby",
     "Historia choroby pacjenta zawierała ważne informacje",
     "перевод другого предложения"),
    # 11797 Schusswaffe
    (16970, "example_ru",
     "Огнестрельное оружие было сохранено как доказательство",
     "Огнестрельное оружие изъяли как доказательство",
     "`sichergestellt` это изъято, а не сохранено"),
    (16970, "example_uk", "Вогнепальну зброю зберегли як доказ",
     "Вогнепальну зброю вилучили як доказ",
     "`sichergestellt` это вилучено, а не збережено"),
    (16970, "example_pl", "Policjant wyciągnął broń palną z kabury",
     "Broń palną zabezpieczono jako dowód",
     "перевод другого предложения"),
    # 11799 Relikt
    (14837, "example_uk", "Цей звичай — пережиток з минулого",
     "Ця звичка — пережиток минулого",
     "`Gewohnheit` это привычка, а не обычай"),
    # 11801 Ingwer
    (12026, "example_uk",
     "Я додаю імбир в чай, тому що він корисний для здоров'я",
     "Я додаю імбир до чаю, бо він корисний для здоров'я",
     "«в чай» — не то управление"),
    (12026, "example_pl", "Dodaję imbir do herbaty",
     "Dodaję imbir do herbaty, bo jest dobry dla zdrowia",
     "потеряна вторая половина"),
    # 11802 Sonderkommando
    (16971, "example_pl", "Na miejsce wysłano oddział specjalny",
     "Oddział specjalny wysłano na akcję",
     "«na miejsce» вместо «zum Einsatz»"),
    # 11803 gelinde
    (8686, "example_uk", "Критика була м'яко кажучи необґрунтована",
     "Критика була, м'яко кажучи, необґрунтована",
     "вводный оборот не выделен запятыми"),
    (8686, "example_tr",
     "Hafif söylemek gerekirse eleştiri haklı değildi",
     "Hafifçe söylemek gerekirse, eleştiri haklı değildi",
     "«hafif söylemek» — не та форма, и нет запятой"),
    # 11804 Antiquität
    (14838, "example_uk",
     "Меблі — справжній антикваріат XVIII століття",
     "Цей предмет меблів — справжній антикваріат XVIII століття",
     "`Möbelstück` это один предмет, а не мебель вообще"),
    # 11805 Rattenloch
    (8687, "example_uk",
     "Старий підвал був як щурина нора, темний і брудний",
     "Старий підвал був як щуряча нора — темний і брудний",
     "в статье «щуряча», и тире вместо запятой"),
    # 11806 Ringrichter
    (12409, "example_tr",
     "Hakem bu kadar haksız bir karar vermememeliydi",
     "Ring hakemi bu kadar haksız bir karar vermemeliydi",
     "«vermememeliydi» — лишний слог, и потеряно «Ring-»"),
    # 11808 Eigentumswohnung
    (18488, "example_ru",
     "Они купили красивую квартиру в центре города",
     "Они купили красивую собственную квартиру в центре города",
     "потеряно «Eigentums-»"),
    (18488, "example_uk",
     "Вони купили гарну квартиру в центрі міста",
     "Вони купили гарну власну квартиру в центрі міста",
     "потеряно «Eigentums-»"),
    (18488, "example_tr",
     "Şehir merkezinde güzel bir apartman dairesi satın aldılar",
     "Şehir merkezinde güzel bir mülk daire satın aldılar",
     "потеряно «Eigentums-»"),
    # 11809 übereifrig
    (11593, "example_en", "His overeager behavior annoyed everyone",
     "His overeager behaviour made everyone nervous",
     "«annoyed» вместо «machte nervös»"),
    (11593, "example_uk",
     "Його надмірно палка поведінка дратувала всіх",
     "Його надміру запопадлива поведінка дратувала всіх",
     "«палка» значит страстная"),
    # 11811 Geständnis
    (16972, "example_tr", "İtirafları herkes için şok ve sürpriz oldu",
     "İtirafları herkes için şok edici ve şaşırtıcıydı",
     "«şok ve sürpriz oldu» — существительные вместо прилагательных"),
    (16972, "example_pl", "Jego przyznanie się zaskoczyło wszystkich",
     "Jego wyznania były szokujące i zaskakujące dla wszystkich",
     "потеряно «schockierend», и в эталоне множественное"),
    # 11812 Gefängnisdirektor
    (16973, "example_uk",
     "Директор в'язниці був відповідальний за безпеку в'язнів",
     "Начальник в'язниці був відповідальний за безпеку в'язнів",
     "перевод слова первым значением"),
    (16973, "example_tr",
     "Hapishane müdürü mahkumlara güvenlik sağlamaktan sorumluydu",
     "Hapishane müdürü mahkûmların güvenliğinden sorumluydu",
     "оборот раздут, и в статье «mahkûm» с циркумфлексом"),
    (16973, "example_pl",
     "Naczelnik więzienia rozmawiał z nowym strażnikiem",
     "Naczelnik więzienia był odpowiedzialny za bezpieczeństwo więźniów",
     "перевод другого предложения"),
    # 11813 Stöpsel
    (17745, "example_ru",
     "Пробка ванны была ослаблена и пропускала воду",
     "Пробка ванны расшаталась и пропускала воду",
     "«была ослаблена» — калька"),
    (17745, "example_uk",
     "Пробка ванни була послаблена й пускала воду",
     "Пробка ванни розхиталася й пропускала воду",
     "«була послаблена» — калька"),
    # 11815 Gelee — род в эталоне
    (12027, "example_de", "Die Gelee auf dem Kuchen sah wunderbar aus",
     "Das Gelee auf dem Kuchen sah wunderbar aus",
     "«das Gelee», а не «die»"),
    (12027, "example_pl", "Dzieci uwielbiają galaretkę z owocami",
     "Galaretka na ciastku wyglądała wspaniale",
     "перевод другого предложения"),
    # 11816 Hustensaft
    (13168, "example_pl", "Kup mi w aptece syrop na kaszel",
     "Weź syrop na kaszel",
     "перевод другого предложения"),
    # 11817 Einsatzteam
    (9287, "example_tr",
     "Görev kuvveti durumu kontrol etmek için hızlı hareket etti",
     "Müdahale ekibi durumu kontrol etmek için hızla harekete geçti",
     "«görev kuvveti» — калька, в статье «müdahale ekibi»"),
    # 11818 Aufgebot
    (16974, "example_uk",
     "Велике розгортання поліцейських було вражаючим",
     "Великий наряд поліцейських був вражаючим",
     "перевод слова вторым значением из статьи"),
    (16974, "example_pl", "Na ulice wysłano duże siły policji",
     "Duże siły policji były imponujące",
     "перевод другого предложения"),
    # 11820 Armreif
    (13780, "example_tr", "Bilekte altın bir bilezik taşıyordu",
     "Bileğinde altın bir bilezik takıyordu",
     "потерян притяжательный, и украшения «takmak», а не «taşımak»"),
    # 11822 Pute
    (12028, "example_uk", "На Різдво ми смажили індичку",
     "На Різдво ми засмажили індичку",
     "«смажили» это многократно"),
    (12028, "example_tr", "Noel günü hindi tavuğu kızarttık",
     "Noel'de hindi kızarttık",
     "«hindi tavuğu» — два названия птицы подряд"),
    # 11823 Lanze — число: четыре перевода против эталона
    (16975, "example_en",
     "Medieval warriors carried long lances into battle",
     "The medieval warrior carried a long lance into battle",
     "в эталоне один воин и одно копьё"),
    (16975, "example_ru", "Средневековые воины несли длинные копья в бой",
     "Средневековый воин нёс длинное копьё в бой",
     "в эталоне один воин и одно копьё"),
    (16975, "example_uk", "Середньовічні воїни несли довгі списи у битву",
     "Середньовічний воїн ніс довгий спис у битву",
     "в эталоне один воин и одно копьё"),
    (16975, "example_tr",
     "Ortaçağ savaşçıları uzun mızrakları savaşa taşıdılar",
     "Ortaçağ savaşçısı savaşa uzun bir mızrak taşıdı",
     "в эталоне один воин и одно копьё"),
    (16975, "example_pl", "Rycerz trzymał lancę w ręku",
     "Średniowieczny wojownik niósł do bitwy długą lancę",
     "перевод другого предложения"),
    # 11824 Gürtellinie
    (12410, "example_uk", "Боксер наніс удар нижче лінії поясу",
     "Боксер завдав удару нижче лінії пояса",
     "«наніс» — русская форма, и «поясу» — не тот падеж"),
    # 11825 Angeklagter
    (16976, "example_uk", "Підсудимий заперечував усі звинувачення в суді",
     "Підсудний заперечував усі звинувачення в суді",
     "«підсудимий» — русская форма"),
    (16976, "example_pl", "Oskarżony nie przyznał się do winy",
     "Oskarżony zaprzeczył wszystkim zarzutom w sądzie",
     "перевод другого предложения"),
    # 11826 überrumpeln
    (8690, "example_uk",
     "Вони спробували застати його врізку неочікуваним візитом",
     "Вони спробували застати його зненацька неочікуваним візитом",
     "«врізку» — нет такого слова"),
    (8690, "example_tr", "Bu soru beni gafil avladı",
     "Beklenmedik bir ziyaretle onu gafil avlamaya çalıştılar",
     "перевод другого предложения"),
    # 11828 Verbrecherin
    (16977, "example_uk",
     "Злочинниця була нарешті спійнята через багато років",
     "Злочинницю нарешті спіймали через багато років",
     "тяжёлый пассив там, где эталон его не требует"),
    (16977, "example_pl", "Przestępczyni uciekła z więzienia",
     "Przestępczynię w końcu złapano po wielu latach",
     "перевод другого предложения"),
    # 11829 leichtgläubig
    (11595, "example_tr", "O çok kolay inanır ve her hileden düşer",
     "O çok kolay inanır ve her hileye kanar",
     "«hileden düşmek» — не выражение"),
    # 11831 Wohltätigkeitsveranstaltung
    (14840, "example_uk",
     "Благодійна подія збирає пожертви для дитячого садка",
     "Благодійний захід збирає пожертви для дитячого садка",
     "перевод слова первым значением"),
    # 11833 Geometrie
    (9639, "example_tr", "Bu binanın geometrisi şaşırtıcıdır",
     "Bu binanın geometrisi nefes kesici",
     "«şaşırtıcı» это удивительный, а `atemberaubend` — захватывающий"),
    # 11834 Wettbüro
    (12411, "example_uk",
     "Букмекерська контора в центрі міста приймала ставки на футбол",
     "Букмекерська контора в центрі міста приймала ставки на футбольний "
     "матч",
     "потеряно «Spiel»"),
    # 11835 Bewegungsmelder
    (17746, "example_en",
     "The motion detector automatically switched the light on",
     "The motion detector automatically switches the light on",
     "эталон в настоящем времени"),
    (17746, "example_uk", "Датчик руху автоматично увімкнув світло",
     "Датчик руху автоматично вмикає світло",
     "эталон в настоящем времени"),
    (17746, "example_tr", "Hareket sensörü otomatik olarak ışığı açtı",
     "Hareket sensörü otomatik olarak ışığı açar",
     "эталон в настоящем времени"),
    # 11836 Traumwelt
    (11596, "example_uk", "Світ мрій у фільмі був абсолютно чарівним",
     "Світ снів у фільмі був абсолютно чарівним",
     "перевод слова первым значением"),
    (11596, "example_pl",
     "Świat marzeń przedstawiony w filmie był absolutnie fascynujący",
     "Świat snów w filmie był absolutnie fascynujący",
     "«przedstawiony» в эталоне нет"),
    # 11838 Fossil
    (18099, "example_ru",
     "Это ископаемое было не менее миллиона лет назад",
     "Этому ископаемому было не менее миллиона лет",
     "«было … лет назад» вместо «ему было … лет»"),
    (18099, "example_uk",
     "Ця копалина була старою щонайменше мільйон років",
     "Цій скам'янілості було щонайменше мільйон років",
     "«копалина» это минерал, а в статье «скам'янілість»"),
    # 11840 Boxershorts
    (13781, "example_uk",
     "Він носив дорогі італійські боксерські шорти",
     "Він носив дорогі італійські боксери",
     "в статье «боксери»"),
    (13781, "example_tr", "Mağazadan iki tane boxer aldım",
     "Pahalı İtalyan boxer giyiyordu",
     "перевод другого предложения"),
    # 11841 niederträchtig
    (11597, "example_uk", "Його підлий план був огидним і злим",
     "Його підлий план був огидним і мерзенним",
     "`gemein` это мерзенний, а не злий"),
    # 11842 Gelüst
    (11598, "example_en", "His wild desire's got him into trouble",
     "His wild desires got him into trouble",
     "лишний апостроф"),
    (11598, "example_uk", "Його шалені бажання привели його в біду",
     "Його шалені бажання довели його до біди",
     "«привели в біду» — не то управление"),
    # 11843 Hochsicherheitstrakt
    (16978, "example_ru",
     "Строгий раздел тюрьмы был практически неприступен",
     "Блок строгого режима в тюрьме был практически неприступен",
     "«строгий раздел» — не по-русски"),
    (16978, "example_uk", "Його перевели до блоку суворого режиму",
     "Блок суворого режиму у в'язниці був практично неприступний",
     "перевод другого предложения"),
    (16978, "example_tr", "Mahkûmu yüksek güvenlikli bölüme aldılar",
     "Hapishanenin yüksek güvenlikli bölümünden kaçmak neredeyse "
     "imkânsızdı",
     "перевод другого предложения"),
    (16978, "example_pl", "Trzymają go w oddziale o zaostrzonym rygorze",
     "Oddział o zaostrzonym rygorze w więzieniu był praktycznie nie do "
     "sforsowania",
     "перевод другого предложения"),
    # 11845 greifbar
    (8694, "example_pl", "Rozwiązanie problemu jest już niemal uchwytne",
     "Rozwiązanie problemu jest już w zasięgu ręki",
     "«niemal uchwytne» теряет «greifbar nah»"),
    # 11846 Schnösel
    (11599, "example_uk", "Цей франт поводить себе як король світу",
     "Цей франт поводиться як король світу",
     "«поводить себе» — калька"),
    (11599, "example_tr",
     "O hodbindi kendini dünyanın kralı gibi davranıyor",
     "Bu züppe kendini dünyanın kralı gibi görüyor",
     "«hodbindi» — нет такого слова, и управление сломано"),
    # 11847 Lebensfreude
    (11600, "example_uk", "Радість життя світить з його очей",
     "Радість життя сяє в його очах",
     "«світити з» — не то управление"),
    # 11849 aussenden
    (14327, "example_en",
     "The radio station sent out the message to all countries",
     "The radio station sends out the message to all countries",
     "эталон в настоящем времени"),
    (14327, "example_uk",
     "Радіостанція розсилала новину у всі країни",
     "Радіостанція розсилає новину у всі країни",
     "эталон в настоящем времени"),
    (14327, "example_tr",
     "Radyo istasyonu haberi tüm ülkelere yayınladı",
     "Radyo istasyonu haberi tüm ülkelere yayınlıyor",
     "эталон в настоящем времени"),
    # 11850 Bearbeitung
    (2249, "example_uk", "Обробка заявки займе близько трьох днів",
     "Обробка заявки займає близько трьох днів",
     "эталон в настоящем времени"),
    (2249, "example_tr",
     "Uygulamanın işlenmesi yaklaşık üç gün sürer",
     "Başvurunun işlenmesi yaklaşık üç gün sürer",
     "«uygulama» это приложение, а `Antrag` — заявка"),
    # 11851 Gemeinderat
    (16979, "example_pl", "Rada gminy zatwierdziła budowę nowej drogi",
     "Rada gminy spotkała się, by omówić nowe drogi",
     "перевод другого предложения"),
    # 11852 umbauen
    (18489, "example_tr",
     "Daha fazla yer için eski evi yeniden inşa ediyoruz",
     "Daha fazla yerimiz olsun diye eski evimizi tadil ediyoruz",
     "«yeniden inşa» это заново отстроить, и потеряно «unser»"),
    # 11854 einerlei
    (8695, "example_tr",
     "Şimdi mi yoksa sonra mı gidelim, bana farketmez",
     "Şimdi mi yoksa sonra mı gidelim, bana fark etmez",
     "«fark etmez» пишется раздельно"),
    # 11855 nachlaufen — эталон заменили после перевода
    (8696, "example_en", "The dog chased after the ball",
     "I won't run after you forever",
     "перевод остался от прежнего эталона"),
    (8696, "example_uk", "Собака біглася за м'ячем",
     "Я не буду вічно за тобою бігати",
     "перевод остался от прежнего эталона, и «біглася» — не форма"),
    (8696, "example_tr", "Köpek topun peşinden koştu",
     "Senin peşinden sonsuza kadar koşmayacağım",
     "перевод остался от прежнего эталона"),
    # 11856 unverschämt
    (11601, "example_tr", "Ondan utanmazca bir yalan söylendi",
     "Bu ondan utanmazca bir yalandı",
     "безличный пассив разваливает фразу"),
    # 11857 Zobel
    (15877, "example_uk",
     "Соболь — цінна тварина завдяки його хутру",
     "Соболь — цінна тварина завдяки своєму хутру",
     "«його» вместо «своєму»"),
    (15877, "example_tr", "Samur kürü için değerli bir hayvandır",
     "Samur, kürkü için değerli bir hayvandır",
     "«kürü» — потеряна согласная"),
    # 11858 Auftrieb
    (18100, "example_ru", "Новая реформа дала экономике новый подъём",
     "После реформы экономика получила новый подъём",
     "«новая реформа» в эталоне нет"),
    (18100, "example_uk", "Нова реформа дала економіці новий підйом",
     "Після реформи економіка отримала нове піднесення",
     "«нова реформа» в эталоне нет, и в статье «піднесення»"),
    # 11859 Kommentator
    (14328, "example_en", "The commentator explained the game very well",
     "The commentator explains the game very well",
     "эталон в настоящем времени"),
    (14328, "example_uk", "Коментатор дуже добре пояснював гру",
     "Коментатор дуже добре пояснює гру",
     "эталон в настоящем времени"),
    # 11860 Kastanie
    (15878, "example_uk", "Каштани падають з дерев осіню",
     "Каштани падають з дерев восени",
     "«осіню» — нет такой формы"),
    # 11863 Bügel
    (18490, "example_tr", "Gözlüğün çerçeve ayağı kırık",
     "Gözlüğün sapı kırık",
     "«çerçeve ayağı» — не термин, в статье «gözlük sapı»"),
    # 11864 Dienstzeit
    (9289, "example_uk", "Його період служби становив десять років",
     "Його термін служби становив десять років",
     "перевод слова первым значением"),
    # 11867 ungehobelt
    (11603, "example_en", "His rough manner is sometimes offensive",
     "His uncouth tone is sometimes hurtful",
     "«manner» вместо «Ton»"),
    (11603, "example_uk", "Його груба поведінка іноді образлива",
     "Його грубий тон іноді образливий",
     "«поведінка» вместо «Ton»"),
    (11603, "example_tr", "Onun kaba davranışı bazen rahatsız edici",
     "Onun kaba ses tonu bazen incitici",
     "«davranış» вместо «Ton»"),
    # 11868 erneut
    (8697, "example_tr", "Yeniden kontrolünün ardından her şey iyiydi",
     "Yeniden yapılan kontrolün ardından her şey yolundaydı",
     "лишний притяжательный"),
    # 11869 Flieder
    (15879, "example_uk", "Бузок гарно цвітає навесні",
     "Бузок гарно квітне навесні",
     "«цвітає» — нет такой формы"),
    # 11871 Antimaterie
    (18101, "example_ru",
     "Учёные изучают антиматерию уже много лет",
     "Антиматерия — захватывающее научное открытие",
     "перевод другого предложения"),
    # 11874 anstrengende
    (8699, "example_uk", "Виснажлива робота виснажила мене",
     "Виснажлива робота мене втомила",
     "одно и то же слово дважды"),
    # 11876 vereiteln — число в эталоне
    (8700, "example_de",
     "Die Polizei vereitelten den Überfall in letzter Sekunde",
     "Die Polizei vereitelte den Überfall in letzter Sekunde",
     "«die Polizei» единственного числа"),
    (8700, "example_uk", "Поліція запобігла грабежу в останню секунду",
     "Поліція запобігла нападу в останню секунду",
     "`Überfall` это нападение, а не грабёж"),
    # 11877 Oldtimer
    (17408, "example_uk",
     "Він їздить на прекрасному класичному автомобілі",
     "Він їздить на прекрасному класичному автомобілі 1960-х років",
     "потеряно «aus den 1960ern»"),
    (17408, "example_tr", "O klasik araba kullanıyor",
     "1960'lardan kalma güzel bir klasik otomobil kullanıyor",
     "потеряны «schön» и «aus den 1960ern»"),
    # «z lat 60.» первым заходом поймал гейт на числа: в немецком 1960,
    # в польском 60. Число написано словом — гейт такое пропускает.
    (17408, "example_pl", "Pod domem stał piękny zabytkowy samochód",
     "Jeździ pięknym zabytkowym samochodem z lat sześćdziesiątych",
     "перевод другого предложения"),
    # 11878 veralbern
    (11606, "example_tr", "Arkadaşlarını aptal şakalarla takıldı",
     "Arkadaşlarına aptal şakalarla takıldı",
     "«takılmak» требует датива"),
    # 11879 Donnerstagabend
    (18949, "example_uk", "У четверговий вечір ми йдемо в кіно",
     "У четвер увечері ми йдемо в кіно",
     "«четверговий вечір» — калька"),
    # 11880 triumphal
    (11607, "example_tr", "Zaferci bir gülümsemeyle bana baktı",
     "Muzaffer bir jestle elini kaldırdı",
     "перевод другого предложения"),
    # 11881 Warenhaus
    (9950, "example_uk", "У універсамі ми купуємо одяг і взуття",
     "В універмазі ми купуємо одяг і взуття",
     "«універсам» это продуктовый, а в статье «універмаг»"),
    (9950, "example_tr", "Mağazada elbise ve ayakkabı alıyoruz",
     "Büyük mağazada elbise ve ayakkabı alıyoruz",
     "потеряно «Waren-», в статье «büyük mağaza»"),
    # 11882 Krematorium
    (15336, "example_tr", "Ceset krematoriyuma götürülüyor",
     "Ceset krematoryuma götürülüyor",
     "в статье «krematoryum»"),
    # 11883 Abscheulichkeit
    (11608, "example_en",
     "The atrocities of the war shocked everyone",
     "The abomination of the war shocked him",
     "в эталоне единственное число и «ihn», а не «всех»"),
    # 11885 Ausnahmezustand
    (16980, "example_uk", "Уряд оголосив надзвичайне положення",
     "Уряд оголосив надзвичайний стан",
     "в статье «надзвичайний стан»"),
    (16980, "example_pl", "W kraju ogłoszono stan wyjątkowy",
     "Rząd ogłosił stan wyjątkowy",
     "в эталоне подлежащее — правительство"),
    # 11886 Übertreibung
    (14329, "example_uk",
     "Це було певне перебільшення з твоєї сторони",
     "Це було певне перебільшення з твого боку",
     "«з твоєї сторони» — калька"),
    (14329, "example_tr", "Bu senin tarafından biraz abartı değil mi",
     "Bu senin açından oldukça büyük bir abartıydı",
     "фраза превращена в вопрос, да ещё и без знака"),
    # 11887 Mündung
    (15880, "example_ru", "Река впадает в устье",
     "Река течёт к устью, где впадает в море",
     "река не впадает в собственное устье"),
    (15880, "example_uk", "Річка впадає в гирло моря",
     "Річка тече до гирла, де впадає в море",
     "«гирло моря» — разваленная фраза"),
    (15880, "example_tr", "Nehir denizin ağzına akıyor",
     "Nehir, denize döküldüğü ağza doğru akıyor",
     "«denizin ağzı» — у моря нет устья"),
    # 11889 Mordermittlung
    (16981, "example_tr",
     "Cinayet soruşturması zaten iki aydır sürüyor",
     "Cinayet soruşturması iki aydır sürüyor",
     "«zaten» здесь не к месту"),
    (16981, "example_pl",
     "Śledztwo w sprawie morderstwa trwa od miesięcy",
     "Śledztwo w sprawie morderstwa trwa już dwa miesiące",
     "«od miesięcy» вместо «zwei Monate»"),
    # 11890 Rechtsbeistand
    (16982, "example_uk", "Він позвонив своєму адвокату",
     "Він подзвонив своєму адвокату",
     "«позвонив» — русское слово"),
    (16982, "example_pl", "Mam prawo do obrońcy",
     "Zadzwonił do swojego obrońcy",
     "перевод другого предложения"),
    # 11892 Warnschuss
    (16983, "example_ru",
     "Полицейский дал предупредительный выстрел",
     "Полицейский сделал предупредительный выстрел",
     "«дать выстрел» — не по-русски"),
    (16983, "example_pl",
     "Policjant oddał strzał ostrzegawczy w powietrze",
     "Policjant oddał strzał ostrzegawczy",
     "«w powietrze» в эталоне нет"),
    # 11893 Fröhlichkeit
    (11609, "example_uk", "Її веселість була заразною",
     "Її веселість була заразливою",
     "«заразний» о болезни, а `ansteckend` о настроении — заразливий"),
    (11609, "example_tr", "Onun neşeliliği bulaşıcıydı",
     "Onun neşesi bulaşıcıydı",
     "«neşelilik» — не та форма, в статье «neşe»"),
    # 11894 Improvisation
    (14842, "example_tr", "İmprovasyon konseri özel yaptı",
     "Doğaçlama konseri özel kıldı",
     "«improvasyon» — не турецкое написание, и «özel yapmak» — калька"),
    # 11895 beknackt
    (11610, "example_en", "That idea is just crazy",
     "That idea is just daft",
     "«crazy» это безумный, а `beknackt` — глупый"),
    (11610, "example_uk", "Ця ідея просто божевільна",
     "Ця ідея просто дурна",
     "«божевільна» это безумная"),
    (11610, "example_tr", "Bu fikir sadece çılgın",
     "Bu fikir sadece saçma",
     "«çılgın» это безумный, в статье «saçma»"),
    # 11896 Wortschatz
    (9642, "example_tr", "Kelime dağarcığım her zaman büyüyor",
     "Kelime dağarcığım giderek büyüyor",
     "«her zaman» вместо «immer größer»"),
    # 11898 Zeichner
    (9292, "example_en",
     "She works as an illustrator for children's books",
     "The illustrator made a fantastic portrait of me",
     "перевод остался от прежнего эталона"),
    (9292, "example_ru",
     "Художник сделал фантастический портрет с меня",
     "Художник сделал мой фантастический портрет",
     "«портрет с меня» — не то управление"),
    (9292, "example_uk", "Художник зробив фантастичний портрет мене",
     "Художник зробив мій фантастичний портрет",
     "«портрет мене» — сломанное управление"),
    (9292, "example_tr", "Ressam benim harika bir portresini çizdi",
     "Ressam benim harika bir portremi çizdi",
     "притяжательный не на том слове"),
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
