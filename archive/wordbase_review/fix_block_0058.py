"""
Правки блока 58 (ряды 9901–10100, ранги 20087–20570).

Главная находка блока — не язык, а ЛОЖНЫЙ ДРУГ в английском переводе:

    de  Die Demonstranten riefen laute Parolen
    en  The prisoner was released on parole after five years

Немецкое `Parole` это лозунг, английское `parole` — условно-досрочное
освобождение. Перевод построен не на смысле немецкой фразы, а на
созвучии слова, и получился осмысленный, грамматически безупречный
английский про совершенно другое.

Прочие классы:
  · перевод другого предложения — больше пятидесяти рядов;
  · турецкие обрывки и разорванные слова: `vura biliriz`, `dansetti`,
    `varilı`, `şaraba sonra`, `sinirliği`, `dokunakıydı`,
    `önemli taslıyor`, `korunan idi`;
  · украинские несуществующие формы: `Судля`, `передпегляді`,
    `заархіровані`, `вибухлива`, `Цвітучі`, `Могильник`, `трас`;
  · русское «Страна была введена в военное положение» — страну нельзя
    ввести в положение, его вводят в стране.

    python -m app.scripts.fix_block_0058            # показать
    python -m app.scripts.fix_block_0058 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 9901 verscheuchen
    (8300, "example_pl", "Pies spłoszył ptaki z ogrodu",
     "Pies płoszy ptaki z ogrodu",
     "эталон в настоящем времени"),
    # 9902 nieder — четыре языка переводят другое предложение
    (8301, "example_en", "He comes from lower social circumstances",
     "Down with the king!",
     "перевод другого предложения"),
    (8301, "example_ru", "Низложить короля!",
     "Долой короля!",
     "«Nieder mit» это возглас «долой», а не «низложить»"),
    (8301, "example_uk", "Тут ціни нижчі, ніж у місті",
     "Геть короля!",
     "перевод другого предложения"),
    (8301, "example_tr", "Daha düşük sosyal koşullardan geliyor",
     "Kahrolsun kral!",
     "перевод другого предложения"),
    (8301, "example_pl", "Pochodzi z niskiego stanu",
     "Precz z królem!",
     "перевод другого предложения"),
    # 9903 Lämmchen
    (15784, "example_uk", "Мале ягня бігло позаду своєї мами",
     "Миле ягнятко бігло за своєю мамою",
     "перевод слова — «ягнятко», и «süß» это миле"),
    # 9904 Personenschutz
    (9203, "example_uk", "Охорона супроводжувала міністра скрізь",
     "Особиста охорона супроводжувала міністра скрізь",
     "потеряно «Personen-»"),
    # 9905 Strumpfhose
    (13761, "example_en",
     "She put on black pantyhose before going out",
     "I put on black tights before going out",
     "эталон о «я»"),
    (13761, "example_uk", "Надінь теплі колготки, на вулиці холодно",
     "Я надягла чорні колготки, перш ніж вийти",
     "перевод другого предложения"),
    (13761, "example_tr",
     "Çıkmadan önce siyah külotlu çorap giydi",
     "Çıkmadan önce siyah külotlu çorap giydim",
     "эталон о «я»"),
    # 9906 unerlaubt
    (16749, "example_ru", "Парковка здесь запрещена и будет дорогой",
     "Парковка здесь запрещена и дорого тебе обойдётся",
     "«будет дорогой» теряет «für dich»"),
    (16749, "example_uk", "Паркування тут заборонене і буде дорогим",
     "Паркування тут заборонене і дорого тобі обійдеться",
     "«буде дорогим» теряет «für dich»"),
    # 9907 Macke
    (11371, "example_en",
     "He has a quirk for old cars – he's obsessed with them",
     "He has a quirk for old cars",
     "второй половины в эталоне нет"),
    (11371, "example_uk",
     "У нього дивацтво — він одержимо збирає старі автомобілі",
     "У нього дивацтво — старі автомобілі",
     "второй половины в эталоне нет"),
    (11371, "example_pl", "Każdy ma swoje małe dziwactwa",
     "Ma dziwactwo do starych samochodów",
     "перевод другого предложения"),
    # 9910 Gewissen
    (11372, "example_tr",
     "Vicdanı çatışması onu her gece işkence çekiyordu",
     "Vicdan çatışması ona her gece işkence ediyordu",
     "«işkence çekiyordu» переворачивает роли"),
    (11372, "example_pl", "Mam wyrzuty sumienia po tej kłótni",
     "Konflikt sumienia dręczył go każdej nocy",
     "перевод другого предложения"),
    # 9911 Fragezeichen
    (14267, "example_pl", "Na końcu pytania stawiamy znak zapytania",
     "Nad jego decyzją stoi wielki znak zapytania",
     "перевод другого предложения"),
    # 9913 Vermählung
    (15273, "example_tr",
     "Prensinin evliliği tüm ülkede büyük bir olay oldu",
     "Prensin evliliği tüm ülkede büyük bir olay oldu",
     "«Prensinin» — двойное притяжание"),
    (15273, "example_pl", "Zaślubiny księcia oglądał cały kraj",
     "Zaślubiny księcia były wielkim wydarzeniem w całym kraju",
     "перевод другого предложения"),
    # 9914 Eingabe
    (17695, "example_ru", "Ввод пароля неправильный",
     "Твой ввод был неправильным, попробуй ещё раз",
     "перевод другого предложения"),
    (17695, "example_uk", "Введення паролю неправильне",
     "Твоє введення було неправильним, спробуй ще раз",
     "перевод другого предложения"),
    (17695, "example_tr", "Şifre girişi yanlış",
     "Girişin yanlıştı, tekrar dene",
     "перевод другого предложения"),
    # 9915 Totenschein
    (13021, "example_pl", "Lekarz wypisał akt zgonu",
     "Lekarz wypisał akt zgonu po zbadaniu pacjenta",
     "потеряно «nachdem er den Patienten untersucht hat»"),
    # 9916 Agenda
    (9205, "example_uk",
     "У нас повна програма на цей тиждень, але ми впораємося",
     "У нас повний порядок денний на цей тиждень, але ми впораємося",
     "перевод слова — «порядок денний»"),
    # 9917 ordinär
    (11373, "example_en",
     "His behavior was really vulgar and inappropriate for such a "
     "formal event",
     "His behaviour was vulgar and inappropriate for the party",
     "в эталоне «Fest», а не формальное событие"),
    (11373, "example_uk",
     "Його поведінка була дійсно вульгарною та невідповідною для такої "
     "формальної події",
     "Його поведінка була вульгарною та невідповідною для свята",
     "в эталоне «Fest», а не формальное событие"),
    (11373, "example_tr",
     "Davranışı böyle resmi bir etkinlik için gerçekten kabaydı ve "
     "uygunsuzdu",
     "Davranışı kutlama için kaba ve uygunsuzdu",
     "в эталоне «Fest», а не формальное событие"),
    (11373, "example_pl", "Jego żarty były ordynarne i niesmaczne",
     "Jego zachowanie było ordynarne i niestosowne na tym święcie",
     "перевод другого предложения"),
    # 9920 prachtvoll
    (8302, "example_pl", "Ten pałac jest naprawdę wspaniały",
     "Zamek był naprawdę wspaniały ze swoimi złotymi ozdobami",
     "«Schloss» это замок, и потеряны украшения"),
    # 9922 Bauarbeiten
    (9206, "example_tr",
     "Cadededeki inşaat işleri korkunç bir gürültü yapıyor",
     "Caddedeki inşaat işleri korkunç bir gürültü yapıyor",
     "«Cadededeki» — лишний слог"),
    # 9923 Blindgänger
    (16750, "example_ru",
     "Саперы должны были удалить несколько неразорвавшихся боеприпасов "
     "из войны",
     "Саперы должны были убрать несколько неразорвавшихся боеприпасов, "
     "оставшихся от войны",
     "«боеприпасов из войны» — не то управление"),
    (16750, "example_uk",
     "Мінери повинні були видалити кілька невибухлих боєприпасів",
     "Сапери мусили прибрати кілька нерозірваних боєприпасів, "
     "що залишилися від війни",
     "«мінери» не те слово, и потеряна война"),
    # 9924 Raketenwerfer
    (16751, "example_ru", "Боец нёс пусковую установку на плече",
     "Солдат нёс ракетную установку на плече",
     "«Soldat» это солдат, и перевод слова — «ракетная установка»"),
    (16751, "example_uk", "Боєць ніс гранатомет на плечі",
     "Солдат ніс ракетну установку на плечі",
     "«Soldat» это солдат, и перевод слова — «ракетна установка»"),
    # 9925 Sense
    (8303, "example_tr", "Dedem otları tırpanla biçiyor",
     "Bu tırpanla otları biçtim",
     "перевод другого предложения"),
    (8303, "example_pl", "Dziadek kosił trawę kosą",
     "Tą kosą skosiłem trawę",
     "перевод другого предложения"),
    # 9927 Vorschau
    (17697, "example_uk",
     "У передпегляді фільм виглядав дійсно цікаво",
     "У попередньому перегляді фільм виглядав дійсно цікаво",
     "«передпегляді» — разваленное слово"),
    # 9929 Absicherung
    (17870, "example_tr", "Mali güvenlik olmadan rahat uyuyamıyorum",
     "Mali güvence olmadan rahat uyuyamazdım",
     "эталон в сослагательном, и перевод слова — «güvence»"),
    (17870, "example_pl",
     "Bez finansowego zabezpieczenia trudno spać spokojnie",
     "Bez finansowego zabezpieczenia nie mógłbym spać spokojnie",
     "эталон в сослагательном и о «я»"),
    # 9930 Absprung
    (12356, "example_tr",
     "Paraşütçü uçaktan mükemmel bir atılış yaptı",
     "Paraşütçü uçaktan mükemmel bir atlayış yaptı",
     "«atılış» это рывок, а прыжок — «atlayış»"),
    # 9931 Symphonie
    (14736, "example_uk", "Дев'ята симфонія Бетховена світовідома",
     "Дев'ята симфонія Бетховена всесвітньо відома",
     "«світовідома» — нет такого слова"),
    (14736, "example_tr",
     "Beethovenin dokuzuncu senfonisi dünya ünlüdür",
     "Beethoven'in dokuzuncu senfonisi dünyaca ünlüdür",
     "потерян апостроф, и «dünya ünlü» — калька"),
    # 9932 Krankenakte
    (13023, "example_tr",
     "Doktor öyküyü kontrol etmek için tıbbi dosyaya baktı",
     "Doktor hastalık öyküsünü kontrol etmek için hasta dosyasına baktı",
     "«öykü» без «hastalık» это просто рассказ"),
    (13023, "example_pl", "Lekarz zajrzał do mojej karty pacjenta",
     "Lekarz zajrzał do karty pacjenta, żeby sprawdzić historię choroby",
     "«mojej» в эталоне нет, и потеряна цель"),
    # 9934 Kriegsrecht
    (16752, "example_ru",
     "Страна была введена в военное положение, чтобы сохранить порядок",
     "В стране ввели военное положение, чтобы сохранить порядок",
     "страну нельзя ввести в положение"),
    (16752, "example_uk",
     "Країна була введена в військовий стан, щоб зберегти порядок",
     "У країні запровадили воєнний стан, щоб зберегти порядок",
     "країну нельзя ввести в стан, и термин «воєнний»"),
    (16752, "example_tr",
     "Ülke düzeni sağlamak için savaş halına alındı",
     "Düzeni sağlamak için ülkede sıkıyönetim ilan edildi",
     "«savaş halına» — разваленная форма"),
    # 9936 Weingut
    (11954, "example_uk",
     "Ми відвідали маленьку винницю в Тоскані і спробували різні вина",
     "Ми відвідали маленьку винарню в Тоскані і спробували різні вина",
     "перевод слова — «винарня»"),
    (11954, "example_tr",
     "Toskanada küçük bir şarap işletmesini ziyaret ettik ve "
     "farklı şarapları tattık",
     "Toskana'da küçük bir şaraphaneyi ziyaret ettik ve "
     "farklı şarapları tattık",
     "потерян апостроф, и перевод слова — «şaraphane»"),
    (11954, "example_pl", "W Toskanii zwiedziliśmy małą winnicę",
     "W Toskanii zwiedziliśmy małą winnicę i spróbowaliśmy różnych win",
     "потеряна дегустация"),
    # 9937 einflussreich
    (8304, "example_pl", "To bardzo wpływowy polityk",
     "To bardzo wpływowy polityk z wielką władzą",
     "потеряно «mit großer Macht»"),
    # 9938 verbogen
    (8305, "example_pl", "Ten widelec jest cały wygięty",
     "Wygięta antena starego radia już nie działa porządnie",
     "перевод другого предложения"),
    # 9939 Waffenruhe
    (16753, "example_uk",
     "Два країни домовилися про перемир'я, щоб говорити про мир",
     "Дві країни домовилися про перемир'я, щоб говорити про мир",
     "«два країни» — рассогласование"),
    (16753, "example_tr",
     "İki ülke barış hakkında konuşmak için ateşkes anlaştılar",
     "İki ülke barış hakkında konuşmak için ateşkeste anlaştı",
     "«ateşkes anlaştılar» без падежа"),
    # 9941 Zeitlupe
    (18892, "example_ru",
     "Замедленная съемка показала каждую деталь аварии очень ясно",
     "Замедленная съёмка показала каждую деталь аварии очень ясно",
     "«е» вместо «ё»"),
    # 9942 einwickeln
    (8306, "example_tr",
     "Hediyeyi kağıda sarıyorum, böyle güzel görünsün",
     "Hediyeyi kâğıda sarıyorum, daha güzel görünsün diye",
     "«böyle güzel görünsün» теряет сравнение"),
    (8306, "example_pl", "Zawinę prezent w kolorowy papier",
     "Zawijam prezent w papier, żeby ładniej wyglądał",
     "перевод другого предложения"),
    # 9943 ausspielen
    (8307, "example_tr", "İşi almak için bütün tanıdıklarını kullandı",
     "İşi almak için tanıdıklarını kullandı",
     "«bütün» в эталоне нет"),
    (8307, "example_pl",
     "Wykorzystał swoje znajomości żeby dostać tę pracę",
     "Wykorzystał swoje znajomości, żeby dostać tę pracę",
     "пропущена запятая"),
    # 9944 kribbeln
    (13024, "example_uk",
     "У мене щипає шкіру, коли я довго пробуду на сонці",
     "У мене поколює шкіру, коли я довго пробуду на сонці",
     "перевод слова — «поколювати»"),
    (13024, "example_tr",
     "Çok uzun güneşte kaldığımda derim kaşınıyor",
     "Uzun süre güneşte kaldığımda derim karıncalanıyor",
     "«kaşınmak» это чесаться, а «kribbeln» — karıncalanmak"),
    (13024, "example_pl", "Mrowi mnie w nogach od długiego siedzenia",
     "Mrowi mnie skóra, kiedy długo byłem na słońcu",
     "перевод другого предложения"),
    # 9946 Sicherheitsstufe
    (16754, "example_tr",
     "Belgenin en yüksek güvenlik seviyesi var ve kesinlikle gizli",
     "Belge en yüksek güvenlik seviyesine sahip ve kesinlikle gizli",
     "«Belgenin ... var» — сломанная связка"),
    # 9947 Marker
    (17698, "example_tr",
     "Kırmızı marker kalemle flipchart üzerine yazıyorum",
     "Kırmızı keçeli kalemle flipchart üzerine yazıyorum",
     "«marker kalem» — калька, по-турецки «keçeli kalem»"),
    # 9949 Banjo
    (14738, "example_tr",
     "Banjo çok iyi çalıyor ve sık sık sahne alıyor",
     "Çok iyi banço çalıyor ve sık sık sahne alıyor",
     "фраза читается так, будто банджо играет само"),
    # 9950 vorlaut
    (11374, "example_en",
     "The impudent boy constantly interrupts without thinking",
     "The impudent boy constantly interrupts",
     "«without thinking» в эталоне нет"),
    (11374, "example_uk",
     "Нахабний хлопчик постійно перебиває, не думаючи",
     "Зухвалий хлопчик постійно перебиває",
     "«не думаючи» в эталоне нет"),
    (11374, "example_tr",
     "Arsız çocuk hep arasına giriyor, düşünmüyor",
     "Arsız çocuk sürekli araya giriyor",
     "«arasına giriyor» без дополнения, и лишнее «düşünmüyor»"),
    # 9951 Monarch
    (16755, "example_pl", "Monarcha rządzi krajem z władzą absolutną",
     "Monarcha rządzi krajem absolutną władzą",
     "«z władzą» — калька"),
    # 9952 lallen
    (14269, "example_tr", "Heyecandan bir şeyler geveledi",
     "Küçük çocuk agucuk yapıyor ve konuşmaya çalışıyor",
     "перевод другого предложения"),
    (14269, "example_pl", "Mały gaworzy w łóżeczku i próbuje mówić",
     "Małe dziecko gaworzy i próbuje mówić",
     "«w łóżeczku» в эталоне нет"),
    # 9953 qualvoll
    (11375, "example_tr", "Eziyetli ölüm aile için dayanması zor oldu",
     "Eziyetli ölüme ailenin dayanması zordu",
     "«ölüm ... dayanması» — сломанная связка"),
    (11375, "example_pl", "To była długa i bolesna śmierć",
     "Bolesna śmierć była trudna do zniesienia dla rodziny",
     "перевод другого предложения"),
    # 9955 gewünscht
    (8309, "example_pl", "Osiągnęliśmy w końcu pożądany efekt",
     "To był dokładnie ten pożądany wynik, na który liczyliśmy",
     "перевод другого предложения"),
    # 9956 Wichtigtuer
    (11376, "example_uk",
     "Цей хвалько сидить в офісі й завжди видається важним",
     "Цей хвалько сидить в офісі й завжди вдає із себе важливого",
     "«видається важним» — калька"),
    (11376, "example_tr",
     "Bu kendini beğenmiş kişi ofiste hep önemli taslıyor",
     "Bu ukala ofiste oturup hep önemli biri gibi davranıyor",
     "«önemli taslıyor» — разваленное выражение"),
    (11376, "example_pl", "Z niego to straszny ważniak",
     "Ważniak siedzi w biurze i zawsze udaje ważnego",
     "перевод другого предложения"),
    # 9957 Schussweite
    (12357, "example_tr",
     "Hedef atış mesafesi içindedir ve onu vura biliriz",
     "Hedef atış mesafesi içinde ve onu vurabiliriz",
     "«vura biliriz» — разорванное слово"),
    # 9958 stottern
    (13025, "example_tr",
     "Sinirlendiğinde ve birçok kişinin önünde konuştuğunda kekeler",
     "Sinirlendiğinde kekeliyor",
     "второй половины в эталоне нет"),
    # 9959 hergerichtet
    (8310, "example_uk", "Стіл гарно прибраний з квітами та свічками",
     "Стіл гарно накритий квітами та свічками",
     "«прибраний» это убранный, а не накрытый"),
    (8310, "example_pl", "Stół jest ładnie przygotowany do kolacji",
     "Stół jest ładnie przygotowany z kwiatami i świecami",
     "в эталоне цветы и свечи, а не ужин"),
    # 9961 Hungersnot
    (15785, "example_pl", "W tym kraju panuje straszny głód",
     "Straszna klęska głodu zabiła miliony ludzi w tym kraju",
     "перевод другого предложения"),
    # 9963 verstummen
    (14270, "example_tr", "Müzik bitince herkes sustu",
     "Gürültü aniden kesildi ve ortam sessizleşti",
     "перевод другого предложения"),
    (14270, "example_pl", "Nagle wszyscy zamilkli",
     "Hałas nagle ucichł i zrobiło się całkiem cicho",
     "перевод другого предложения"),
    # 9964 duften
    (8312, "example_pl", "Te kwiaty pięknie pachną",
     "Kwiaty w ogrodzie pięknie pachną",
     "потеряно «in dem Garten»"),
    # 9965 Gegenangriff
    (12358, "example_uk", "Після голу суперника пішла наша контратака",
     "Після голу суперника негайно пішла наша контратака",
     "потеряно «sofort»"),
    # 9966 Piste
    (12359, "translation_uk",
     "трас, гірськолижна траса, траса, злітна смуга",
     "траса, гірськолижна траса, злітна смуга",
     "«трас» — обрубок, и «траса» дважды"),
    (12359, "translation_tr", "pist, kayak pisti, piste",
     "pist, kayak pisti, uçak pisti",
     "«piste» это склонённая форма того же слова"),
    (12359, "example_uk", "Траса була ідеальною для катання на лижах",
     "Траса була сьогодні ідеальною для катання на лижах",
     "потеряно «heute»"),
    # 9967 auffrischen
    (8313, "example_tr",
     "Londraya gitmeden önce İngilizceyi tazelemem gerekiyor",
     "Londra'ya gitmeden önce İngilizcemi tazelemem gerekiyor",
     "потерян апостроф и притяжание"),
    (8313, "example_pl", "Muszę odświeżyć angielski przed wyjazdem",
     "Muszę odświeżyć angielski przed wyjazdem do Londynu",
     "потерян Лондон"),
    # 9968 Beschleunigung
    (17345, "example_en", "The cars acceleration was impressive",
     "The car's acceleration was impressive",
     "потерян апостроф"),
    # 9969 deponieren
    (9920, "example_ru", "Ценности были депонированы в сейфе",
     "Ценности сдали на хранение в сейф",
     "«депонированы» — канцелярит"),
    (9920, "example_uk", "Цінності були депоновані в сейфі",
     "Цінності здали на зберігання в сейф",
     "«депоновані» — канцелярит"),
    (9920, "example_pl", "Zdeponowałem biżuterię w hotelowym sejfie",
     "Kosztowności zdeponowano w sejfie",
     "перевод другого предложения"),
    # 9970 mobil
    (14271, "example_tr", "Yeni mobil uygulamayı telefonuma indirdim",
     "Bu, yolculuk için mobil bir çözüm",
     "перевод другого предложения"),
    (14271, "example_pl", "Dzięki samochodowi jestem bardziej mobilny",
     "To mobilne rozwiązanie w podróży",
     "перевод другого предложения"),
    # 9971 schwachsinnig
    (11377, "example_uk", "Це була ідіотська ідея з самого початку",
     "Це була ідіотська ідея, яка ніколи б не запрацювала",
     "перевод другого предложения"),
    (11377, "example_pl", "To był kompletnie idiotyczny pomysł",
     "To był idiotyczny pomysł, który nigdy by nie zadziałał",
     "потеряна вторая половина"),
    # 9973 Heiligtum
    (14740, "example_uk",
     "Це було для нього святилищем, яке ніхто не міг торкатися",
     "Це було для нього святилищем, якого ніхто не міг торкатися",
     "«торкатися» требует родительного"),
    # 9974 Präsidentschaft
    (16756, "example_uk",
     "Під час його президентства були проведено важливі реформи",
     "Під час його президентства провели важливі реформи",
     "«були проведено» — сломанная форма"),
    # 9975 Relais
    (17699, "example_en",
     "The relay in the car was broken and needed to be replaced",
     "A relay in the car burned out",
     "перевод другого предложения"),
    (17699, "example_ru",
     "Реле в машине было неисправно и требовало замены",
     "В машине перегорело реле",
     "перевод другого предложения"),
    (17699, "example_uk",
     "Реле в машині було несправне і потребувало заміни",
     "У машині перегоріло реле",
     "перевод другого предложения"),
    (17699, "example_tr", "Arabanın rölesi bozulmuş, değiştirmek gerek",
     "Arabada bir röle yanmış",
     "перевод другого предложения"),
    # 9976 Eilmeldung
    (14272, "example_en", "There was important breaking news on TV",
     "There was important breaking news in the news",
     "в эталоне «in den Nachrichten», а не телевизор"),
    (14272, "example_tr", "Haberlerde önemli bir son haber vardı",
     "Haberlerde önemli bir son dakika haberi vardı",
     "перевод слова — «son dakika haberi»"),
    # 9977 Flussufer
    (15786, "example_uk",
     "Ми гуляли по берегу річки й насолоджувалися природою",
     "Ми гуляли берегом річки й насолоджувалися природою",
     "«по берегу» — калька"),
    (15786, "example_tr",
     "Nehir kıyısında yürüdük ve doğayı tadına vardık",
     "Nehir kıyısında yürüdük ve doğanın tadını çıkardık",
     "«doğayı tadına vardık» — разваленное выражение"),
    (15786, "example_pl", "Spacerowaliśmy brzegiem rzeki",
     "Spacerowaliśmy brzegiem rzeki i cieszyliśmy się naturą",
     "потеряна природа"),
    # 9979 Katakombe
    (14741, "example_tr",
     "Romanın altındaki eski katakombları ziyaret ettik",
     "Roma'nın altındaki eski katakompları ziyaret ettik",
     "потерян апостроф, и перевод слова — «katakomp»"),
    # 9985 Parole — английский перевод построен на созвучии
    (14273, "example_en",
     "The prisoner was released on parole after five years",
     "The demonstrators shouted loud slogans",
     "английское parole это условное освобождение, а не лозунг"),
    (14273, "example_uk", "Їхнє гасло — свобода і рівність",
     "Демонстранти вигукували гучні гасла",
     "перевод другого предложения"),
    (14273, "example_tr", "Kalabalık slogan atmaya başladı",
     "Göstericiler yüksek sesle slogan attı",
     "перевод другого предложения"),
    (14273, "example_pl", "Na murze ktoś napisał hasło wyborcze",
     "Demonstranci krzyczeli głośne hasła",
     "перевод другого предложения"),
    # 9987 anzapfen
    (11955, "example_tr", "Biraları sunmak için varilı açmak istediler",
     "Birayı servis etmek için fıçıyı açmak istediler",
     "«varilı» — сломанный аккузатив"),
    (11955, "example_pl", "Otworzyli beczkę piwa na festynie",
     "Chcieli otworzyć beczkę, żeby podać piwo",
     "перевод другого предложения"),
    # 9988 benebelt
    (13026, "example_uk", "Він повернувся додому трохи напідпитку",
     "Після трьох склянок вина він був трохи напідпитку",
     "перевод другого предложения"),
    (13026, "example_tr", "Üç bardak şaraba sonra hafif sarhoş olmuştu",
     "Üç bardak şaraptan sonra hafif çakırkeyif olmuştu",
     "«şaraba sonra» — сломанный падеж"),
    (13026, "example_pl", "Po dwóch piwach był lekko podpity",
     "Po trzech kieliszkach wina był lekko podpity",
     "в эталоне три бокала вина, а не два пива"),
    # 9989 Fitness
    (1424, "example_en", "She does fitness training every morning",
     "I go to the gym regularly for my health",
     "перевод другого предложения"),
    (1424, "example_uk",
     "Я регулярно ходжу в спортзал для своєї фізичної форми",
     "Я регулярно ходжу у фітнес-студію для свого здоров'я",
     "в эталоне «für meine Gesundheit»"),
    # 9990 detailliert
    (8314, "example_en",
     "He gave a detailed explanation that we all understood well",
     "You gave me a detailed explanation that I understood well",
     "эталон обращается на «ты»"),
    (8314, "example_tr",
     "Hepimizin iyi anladığı ayrıntılı bir açıklama yaptı",
     "Bana iyi anladığım ayrıntılı bir açıklama yaptın",
     "эталон обращается на «ты»"),
    (8314, "example_pl", "Dał mi szczegółowy opis drogi",
     "Dałeś mi szczegółowe wyjaśnienie, które dobrze zrozumiałem",
     "перевод другого предложения"),
    # 9991 Sphäre
    (18060, "example_tr",
     "O toplumdaki en yüksek kürelerde hareket ediyor",
     "Toplumun en üst çevrelerinde dolaşıyor",
     "«küre» это шар, а не круг общества"),
    # 9992 irre
    (11379, "example_uk",
     "Це була божевільна удача, що у нього ще було час",
     "Це була божевільна удача, що в нього ще був час",
     "«було час» — рассогласование рода"),
    (11379, "example_pl", "To był szalony pomysł ale się udało",
     "To było szalone szczęście, że miał jeszcze czas",
     "перевод другого предложения"),
    # 9994 Haupttor
    (18423, "example_tr", "Kalenin ana kapısı kapalı ve korunan idi",
     "Kalenin ana kapısı kapalıydı ve korunuyordu",
     "«korunan idi» — разваленная связка"),
    # 9995 schmuggeln
    (16759, "example_ru",
     "Он пытался контрабандить сигареты через границу",
     "Он пытался провезти сигареты контрабандой через границу",
     "«контрабандить» — просторечие"),
    (16759, "example_uk",
     "Він намагався контрабандити сигарети через кордон",
     "Він намагався провезти сигарети контрабандою через кордон",
     "«контрабандити» — нет такого слова"),
    (16759, "example_tr", "Sınırdan sigara kaçak geçirmek denedi",
     "Sınırdan sigara kaçırmaya çalıştı",
     "«kaçak geçirmek denedi» — сломанная связка"),
    # 9997 indirekt
    (8316, "example_en", "That is an indirect question",
     "That is an indirect question, not a direct one",
     "потеряна вторая половина"),
    (8316, "example_tr", "Bu dolaylı bir soru",
     "Bu dolaylı bir soru, doğrudan değil",
     "потеряна вторая половина"),
    (8316, "example_pl", "Zadał to pytanie w sposób pośredni",
     "To pytanie pośrednie, a nie bezpośrednie",
     "перевод другого предложения"),
    # 9998 Pflock
    (8317, "example_uk", "Я забив кілок в землю",
     "Кілок для намету був міцно вбитий у землю",
     "перевод другого предложения"),
    (8317, "example_pl", "Wbij kołek głębiej w ziemię",
     "Kołek namiotowy był mocno wbity w ziemię",
     "перевод другого предложения"),
    # 9999 kontaminiert
    (13028, "example_tr", "Su kirli idi ve içilmezdi",
     "Su kontamine olmuştu ve içilemezdi",
     "«idi» отдельно, и «kirli» это просто грязный"),
    (13028, "example_pl", "Woda w tej studni jest skażona",
     "Woda była skażona i nie można jej było pić",
     "перевод другого предложения"),
    # 10001 hören
    (14274, "example_en",
     "He listened attentively and wanted to hear everything",
     "He listened attentively and wanted to understand everything",
     "в эталоне «verstehen», а не «hören»"),
    (14274, "example_uk", "Він уважно слухав і хотів все почути",
     "Він уважно слухав і хотів усе зрозуміти",
     "в эталоне «verstehen», а не «hören»"),
    (14274, "example_tr", "Dikkatle dinledi ve her şeyi duymak istedi",
     "Dikkatle dinledi ve her şeyi anlamak istedi",
     "в эталоне «verstehen», а не «hören»"),
    (14274, "example_pl", "Nie słyszę cię dobrze przez telefon",
     "Słuchał uważnie i chciał wszystko zrozumieć",
     "перевод другого предложения"),
    # 10002 spöttisch
    (11380, "example_uk",
     "Його глузливий тон був образливим і всім не подобався",
     "Його глузливий тон був образливим і нікому не подобався",
     "«всім не подобався» — двойное отрицание наоборот"),
    (11380, "example_tr",
     "Onun alay edici tonu incitici idi ve kimse beğenmedi",
     "Onun alaycı tonu inciticiydi ve kimse hoşlanmadı",
     "«idi» отдельно, и «alay edici» — калька"),
    (11380, "example_pl", "Powiedział to drwiącym tonem",
     "Jego drwiący ton był raniący i nikomu się nie podobał",
     "перевод другого предложения"),
    # 10003 Sprengsatz
    (16760, "example_tr",
     "Patlayıcı cihaz zamanında keşfedildi ve etkisiz hale getirildi",
     "Patlayıcı düzenek zamanında keşfedildi ve etkisiz hale getirildi",
     "перевод слова — «patlayıcı düzenek»"),
    # 10006 unscharf
    (8318, "example_pl", "To zdjęcie jest całkiem nieostre",
     "Zdjęcie jest nieostre i nic nie widać wyraźnie",
     "потеряна вторая половина"),
    # 10007 optimal
    (8319, "example_en",
     "The conditions were optimal for the experiment",
     "The conditions were optimal for the test",
     "в эталоне «Test», а не эксперимент"),
    (8319, "example_tr", "Şartlar test için optimaldir",
     "Şartlar test için optimaldi",
     "эталон в прошедшем времени"),
    (8319, "example_pl", "Warunki były optymalne do jazdy",
     "Warunki były optymalne do testu",
     "перевод другого предложения"),
    # 10008 kraftvoll
    (8320, "example_en",
     "The powerful voice of the singer moved everyone",
     "The powerful voice of the singer thrilled me",
     "в эталоне «mich», а не «everyone»"),
    (8320, "example_pl", "Ten piosenkarz ma bardzo mocny głos",
     "Mocny głos piosenkarza mnie zachwycił",
     "перевод другого предложения"),
    # 10009 Tänze
    (14744, "example_en",
     "The various dances from around the world fascinated me",
     "The dances from different cultures fascinate me",
     "в эталоне «aus verschiedenen Kulturen», и время"),
    (14744, "example_tr", "Dünyanın çeşitli dansları beni büyüledi",
     "Farklı kültürlerin dansları beni büyülüyor",
     "в эталоне «aus verschiedenen Kulturen», и время"),
    # 10010 Schnauzbart
    (15275, "example_tr",
     "Onun kalın bıyığı onun ayırıcı özelliğiydi",
     "Gür bıyığı onun ayırt edici özelliğiydi",
     "«onun» дважды, и «kalın» это толстый"),
    # 10011 erhaben
    (8321, "example_en",
     "The sublime mountains reminded me of greatness",
     "The sublimity of these mountains impresses me",
     "перевод другого предложения"),
    (8321, "example_uk", "Велич цих гір мене вразила",
     "Велич цих гір мене вражає",
     "эталон в настоящем времени"),
    (8321, "example_tr", "Bu dağların görkemliği beni etkiledi",
     "Bu dağların görkemi beni etkiliyor",
     "«görkemliği» — не форма, и время"),
    (8321, "example_pl", "Ten widok był naprawdę wzniosły",
     "Wzniosłość tych gór mnie zachwyca",
     "перевод другого предложения"),
    # 10012 Hirngespinst
    (11381, "example_tr", "Bu sadece hayali bir şeydi, gerçek değil",
     "Bu sadece bir hayal ürünüydü, gerçek değil",
     "перевод слова — «hayal ürünü»"),
    (11381, "example_pl", "To tylko wymysł twojej wyobraźni",
     "To był tylko wymysł, a nie rzeczywistość",
     "«twojej wyobraźni» в эталоне нет"),
    # 10013 zurücklegen
    (8322, "example_en",
     "We had to cover 300 kilometers to arrive on time",
     "We had to cover 300 kilometres",
     "второй половины в эталоне нет"),
    (8322, "example_pl", "Przebyliśmy dziś trzysta kilometrów",
     "Musieliśmy przebyć trzysta kilometrów",
     "потеряно «mussten»"),
    # 10014 Tierchen
    (15787, "example_tr", "Küçük hayvan taşın altına saklandı",
     "Küçük hayvancık taşın altına saklandı",
     "перевод слова — «hayvancık»"),
    (15787, "example_pl", "Jakieś zwierzątko przebiegło przez ogród",
     "Małe zwierzątko schowało się pod kamieniem",
     "перевод другого предложения"),
    # 10016 Schauer
    (11382, "example_uk", "При цій історії мене охопив мороз",
     "Від цієї історії мене пройняв дрож",
     "перевод слова — «дрож»"),
    (11382, "example_tr",
     "Bu hikayede sırtımda bir ürperti hissettim",
     "Bu hikâyeyi duyunca sırtımdan bir ürperti geçti",
     "«hikayede» — не то управление"),
    (11382, "example_pl", "Przeszedł mnie dreszcz ze strachu",
     "Przy tej historii przeszedł mnie dreszcz",
     "«ze strachu» в эталоне нет"),
    # 10017 Neandertaler
    (18061, "example_tr",
     "Neanderthal nesli tükenmiş bir insan türüydü",
     "Neandertal insanı nesli tükenmiş bir insan türüydü",
     "«Neanderthal» английское написание"),
    # 10018 schrill
    (8323, "example_tr", "Bahçeden tiz bir çığlık geldi",
     "Sirenin tiz sesi dayanılmazdı",
     "перевод другого предложения"),
    (8323, "example_pl", "Piskliwy dźwięk syreny mnie obudził",
     "Piskliwy dźwięk syreny był nie do zniesienia",
     "перевод другого предложения"),
    # 10019 drohen
    (16762, "example_en", "I felt threatened by his tone",
     "A thunderstorm is looming",
     "перевод другого предложения"),
    (16762, "example_ru", "Грозит гроза",
     "Надвигается гроза",
     "«грозит гроза» — тавтология"),
    (16762, "example_uk", "Йому загрожували по телефону",
     "Насувається гроза",
     "перевод другого предложения"),
    (16762, "example_tr", "Bir fırtına tehdit ediyor",
     "Fırtına yaklaşıyor",
     "«tehdit ediyor» о погоде — калька"),
    # 10021 Kap
    (12457, "example_tr",
     "İyi Umut Burnunun etrafında yelken açtık",
     "İyi Umut Burnu'nun etrafında yelken açtık",
     "потерян апостроф в названии"),
    # 10022 geschmeidig
    (8324, "example_tr", "Bir dansçı gibi esnek hareketleri vardı",
     "Bir dansçı gibi kıvrak hareket ediyordu",
     "в эталоне «bewegte sich», а не «были движения»"),
    # 10023 Tollpatsch
    (11383, "example_uk", "Яка невміха! Він розбив вазу",
     "Ото недотепа! Він розбив вазу",
     "«невміха» женского рода, а речь о нём"),
    (11383, "example_tr", "Ne hantallık! Vazoyu kırdı",
     "Ne sakar biri! Vazoyu kırdı",
     "«hantallık» это свойство, а не человек"),
    (11383, "example_pl",
     "Ale jestem niezdara znowu wylałem kawę",
     "Ale niezdara! Stłukł wazon",
     "перевод другого предложения"),
    # 10024 stampfen
    (8325, "example_uk", "Коні нетерпляче топтають копитами",
     "Коні нетерпляче тупотять копитами",
     "«топтати» требует дополнения"),
    (8325, "example_tr", "Atlar sabırsızca ayaklarıyla vuruyordu",
     "Atlar sabırsızca toynaklarını yere vuruyor",
     "в эталоне «Hufe» — копыта, и время"),
    (8325, "example_pl", "Dziecko tupało nogami ze złości",
     "Konie tupią niecierpliwie kopytami",
     "перевод другого предложения"),
    # 10025 Anschrift
    (1146, "example_uk", "Будь ласка, вкажіть поштову адресу",
     "Будь ласка, вкажіть вашу адресу",
     "в эталоне «Ihre Anschrift»"),
    # 10026 nachhelfen
    (8326, "example_uk", "Іноді я мав допомогти долі",
     "Іноді я мусив трохи допомогти долі",
     "потеряно «ein bisschen»"),
    # 10027 Ekstase
    (11384, "example_tr", "Coşkuyla dans pistinde dansetti",
     "Coşkuyla dans pistinde dans etti",
     "«dansetti» пишется раздельно"),
    (11384, "example_pl", "Tańczyła w ekstazie całą noc",
     "W ekstazie tańczyła po parkiecie",
     "«całą noc» в эталоне нет"),
    # 10028 Frischling
    (15367, "example_uk", "Маленьке поросятко гралось в бруді",
     "Маленький кабанчик грається в болоті",
     "перевод слова — «кабанчик», и время"),
    # 10029 durchsichtig
    (8327, "example_en", "The glass is completely transparent",
     "The glass is completely transparent, you can see everything",
     "потеряна вторая половина"),
    (8327, "example_uk", "Скло абсолютно прозоре",
     "Скло абсолютно прозоре, усе видно",
     "потеряна вторая половина"),
    (8327, "example_tr", "Cam tamamen şeffaftır",
     "Cam tamamen şeffaf, her şey görünüyor",
     "потеряна вторая половина"),
    (8327, "example_pl", "Woda w jeziorze jest zupełnie przezroczysta",
     "Szkło jest całkiem przezroczyste, wszystko widać",
     "перевод другого предложения"),
    # 10030 Sadist
    (11385, "example_uk",
     "Вбивця був справжнім садистом, який отримував задоволення "
     "від страждання",
     "Злочинець був справжнім садистом, який отримував задоволення "
     "від страждань",
     "«Täter» это злочинець, а не вбивця"),
    (11385, "example_tr",
     "Katil gerçek bir sadist idi ve acıdan zevk alıyordu",
     "Fail gerçek bir sadistti ve acıdan zevk alıyordu",
     "«katil» это убийца, и «idi» отдельно"),
    (11385, "example_pl", "Ten facet to prawdziwy sadysta",
     "Sprawca był prawdziwym sadystą, który delektował się cierpieniem",
     "перевод другого предложения"),
    # 10031 Radiosender
    (17700, "example_tr",
     "Benim favori radyo istasyonu her zaman iyi müzik çalar",
     "Benim favori radyo istasyonum her zaman iyi müzik çalar",
     "потеряно притяжание"),
    # 10032 Nervosität
    (11386, "example_uk",
     "Його нервозність була явно видна перед промовою",
     "Його нервозність було явно видно перед тим, як він виголосив промову",
     "«видна» — не форма, и фраза урезана"),
    (11386, "example_tr",
     "Konuşmadan önce onun sinirliği açıkça görülüyordu",
     "Konuşmadan önce onun sinirliliği açıkça görülüyordu",
     "«sinirliği» — обрубленное слово"),
    (11386, "example_pl", "Nie mogła ukryć nerwowości przed egzaminem",
     "Jego nerwowość była wyraźnie widoczna, zanim wygłosił mowę",
     "перевод другого предложения"),
    # 10033 strategisch
    (8328, "example_pl", "Wybrali strategiczne miejsce na sklep",
     "Miasto ma strategicznie ważną pozycję",
     "перевод другого предложения"),
    # 10035 Rennstrecke
    (12362, "translation_uk",
     "гоночна трасса, гоночна траса, трек, траса",
     "гоночна траса, трек",
     "«трасса» с двойной «с», и то же слово трижды"),
    (12362, "example_uk", "Нова траса довжиною 5 кілометрів",
     "Нова гоночна траса має 5 кілометрів довжини",
     "потеряно «гоночна», и фраза без сказуемого"),
    # 10036 Mikrofilm
    (17701, "example_uk",
     "Документи були заархіровані на мікрофільм",
     "Документи заархівували на мікрофільмі",
     "«заархіровані» — нет такой формы"),
    # 10037 ausrücken
    (8329, "example_en",
     "The fire department had to deploy to put out the fire",
     "The fire department had to deploy",
     "второй половины в эталоне нет"),
    (8329, "example_uk", "Пожежники мусили виїхати гасити пожежу",
     "Пожежники мусили виїхати",
     "второй половины в эталоне нет"),
    (8329, "example_tr",
     "İtfaiye yangını söndürmek için çıkmak zorunda kaldı",
     "İtfaiye yola çıkmak zorunda kaldı",
     "второй половины в эталоне нет"),
    (8329, "example_pl",
     "Strażacy musieli natychmiast wyjechać do pożaru",
     "Straż pożarna musiała wyjechać",
     "второй половины в эталоне нет"),
    # 10038 Doppel
    (8330, "example_en", "I'll have a double espresso, please",
     "This is a duplicate of the original",
     "перевод совершенно другого предложения"),
    (8330, "example_uk", "Ти справжній двійник мого брата",
     "Це дублікат оригіналу",
     "перевод совершенно другого предложения"),
    (8330, "example_pl", "Zostaw sobie duplikat umowy",
     "To duplikat oryginału",
     "перевод другого предложения"),
    # 10039 vertagen
    (16765, "example_tr", "Hakim duruşmayı bir hafta ertelemiştir",
     "Hâkim duruşmayı bir hafta erteledi",
     "«-miştir» книжное, и потеряна шляпка"),
    # 10042 Hitzkopf
    (11387, "example_uk",
     "Твій брат — справжня вибухлива людина, він дуже швидко розлючується",
     "Твій брат — справжня гаряча голова, він надто швидко виходить із себе",
     "«вибухлива» — нет такого слова"),
    (11387, "example_tr",
     "Patronum çabuk öfkelenen biri, dikkat et",
     "Kardeşin çabuk öfkelenen biri, çok hızlı sinirleniyor",
     "перевод другого предложения"),
    # 10043 kämmen
    (18894, "example_uk", "Вона розчісує волосся кожного ранку",
     "Вона розчісує волосся щоранку",
     "«кожного ранку» — калька"),
    (18894, "example_pl", "Ona czesze włosy każdego ranka",
     "Ona czesze włosy codziennie rano",
     "«każdego ranka» — калька"),
    # 10044 hüllen
    (13762, "example_tr", "Heykel plastik filmle sarılmıştır",
     "Heykel plastik filme sarılmıştı",
     "«-mıştır» книжное, и не тот падеж"),
    # 10045 inkognito
    (8331, "example_tr",
     "Ünlü kişi tanınmamak için gizli bir şekilde seyahat etti",
     "Ünlü kişi tanınmamak için gizlice seyahat etti",
     "перевод слова — «gizlice»"),
    (8331, "example_pl", "Aktor podróżował incognito po całym kraju",
     "Gwiazda podróżowała incognito, żeby jej nie rozpoznano",
     "перевод другого предложения"),
    # 10046 unwissend
    (9608, "example_uk", "Нам невідомо про його плани",
     "Вона була абсолютно необізнана про те, що її чоловік її зраджував",
     "перевод другого предложения"),
    # 10047 blühend
    (15788, "example_ru",
     "Цветущие вишневые деревья были чудесны",
     "Цветущие вишнёвые деревья были чудесны",
     "«е» вместо «ё»"),
    (15788, "example_uk", "Цвітучі вишневі дерева були чудовими",
     "Квітучі вишневі дерева були чудовими",
     "«цвітучий» — нет такой формы"),
    (15788, "example_pl", "Kwitnące wiśnie pięknie wyglądają",
     "Kwitnące wiśnie wyglądały wspaniale",
     "эталон в прошедшем времени"),
    # 10049 Totengräber
    (9212, "example_uk", "Могильник копав яму для поховання",
     "Гробар копав могилу для похорону",
     "«могильник» это место, а не человек"),
    # 10050 eidesstattlich
    (16767, "example_ru", "Присяжное заявление имеет силу в суде",
     "Заявление под присягой имеет силу в суде",
     "«присяжное заявление» — не по-русски"),
    (16767, "example_uk", "Присяжна заява має силу в суді",
     "Заява під присягою має силу в суді",
     "«присяжна заява» — не по-украински"),
    # 10057 salutieren
    (16769, "example_ru", "Солдаты салютовали флагу на параде",
     "Солдат отдал честь своему офицеру",
     "перевод другого предложения"),
    (16769, "example_uk", "Солдати салютували прапору",
     "Солдат віддав честь своєму офіцерові",
     "перевод другого предложения"),
    # 10058 reibungslos
    (8332, "example_uk", "Робота пройшла без перешкод",
     "Співпраця з новою командою пройшла без перешкод",
     "перевод другого предложения"),
    (8332, "example_pl", "Wszystko przebiegło bezproblemowo",
     "Współpraca z nowym zespołem przebiegła bezproblemowo",
     "перевод другого предложения"),
    # 10059 losmachen
    (8333, "example_en",
     "Can you please let the dog loose? It needs to go out",
     "Can you please let the dog loose? He wants to play",
     "в эталоне «Er will spielen»"),
    (8333, "example_uk", "Можеш відпустити собаку? Вона хоче грати",
     "Можеш, будь ласка, відв'язати собаку? Вона хоче гратися",
     "потеряно «bitte», и «грати» без «-ся»"),
    (8333, "example_pl", "Odwiąż psa, chce pobiegać",
     "Możesz odwiązać psa? Chce się pobawić",
     "в эталоне вопрос и «играть»"),
    # 10060 Erreger
    (13029, "example_tr",
     "Doktorlar hastalığın etkeni olarak patojeni belirlediler",
     "Doktorlar hastalığın etkenini belirlediler",
     "«etkeni olarak patojeni» — тавтология"),
    # 10062 ergänzen
    (8334, "example_uk", "Можеш ти доповнити моє речення?",
     "Можеш доповнити моє речення?",
     "порядок слов"),
    # 10063 angesehen
    (11389, "example_uk", "Він поважний професор в університеті",
     "Він шанований професор в університеті",
     "перевод слова — «шанований»"),
    (11389, "example_pl", "To bardzo szanowany lekarz w naszym mieście",
     "To szanowany profesor na uniwersytecie",
     "перевод другого предложения"),
    # 10064 bücken
    (18895, "example_ru", "Мне больно нагибаться",
     "Мне нужно нагнуться, чтобы пройти через дверь",
     "перевод другого предложения"),
    # 10065 Widmung
    (14746, "example_tr", "Kitaptaki adanış çok dokunakıydı",
     "Kitaptaki ithaf çok dokunaklıydı",
     "«adanış» не то слово, и «dokunakıydı» — опечатка"),
    # 10066 Kot
    (15791, "example_en", "Bird excrement covered the whole car",
     "The dog left droppings on the pavement again",
     "перевод другого предложения"),
    (15791, "example_ru", "Врач попросил сдать кал на анализ",
     "Собака опять оставила кал на тротуаре",
     "перевод другого предложения"),
    (15791, "example_uk", "На газоні повно собачих екскрементів",
     "Собака знову залишив кал на тротуарі",
     "перевод другого предложения"),
    # 10070 Speisekammer
    (18424, "example_uk", "Я кладу консерви в кладову",
     "Я кладу консерви в комору",
     "перевод слова — «комора»"),
    # 10072 peitschen
    (8336, "example_uk", "Не смій бити собаку!",
     "Вітер шмагає по вікну",
     "перевод другого предложения"),
    (8336, "example_tr", "Rüzgar pencereye çarpıyor",
     "Rüzgâr pencereye şiddetle çarpıyor",
     "«çarpmak» без «şiddetle» теряет хлёсткость"),
    (8336, "example_pl", "Deszcz smagał nas po twarzy",
     "Wiatr smaga o szybę",
     "перевод другого предложения"),
    # 10075 Gaumen
    (13030, "example_uk", "Солодка їжа щекотала мій піднебіння",
     "Солодка їжа лоскотала моє піднебіння",
     "«щекотала» — русизм, и рассогласование рода"),
    (13030, "example_tr", "Tatlı yemek damağımı kıpırdattı",
     "Tatlı yemek damağımı gıdıklıyor",
     "«kıpırdatmak» это шевелить"),
    (13030, "example_pl", "Gorąca zupa poparzyła mi podniebienie",
     "Słodkie jedzenie łaskocze moje podniebienie",
     "перевод другого предложения"),
    # 10076 erklingen
    (14747, "example_uk", "Музика звучить із сусідної кімнати",
     "Музика гучно звучить із сусідньої кімнати",
     "«сусідної» — не форма, и потеряно «laut»"),
    (14747, "example_tr", "Müzik bitişik odadan geliyor",
     "Müzik yan odadan yüksek sesle geliyor",
     "потеряно «laut»"),
    # 10077 Spiritus
    (8337, "example_en", "Alcohol burns cleaner than wood",
     "Methylated spirits burn cleaner than wood",
     "«Spiritus» это денатурат, а не алкоголь вообще"),
    (8337, "example_tr", "Alkol ahşaptan daha temiz yanıyor",
     "İspirto ahşaptan daha temiz yanıyor",
     "перевод слова — «ispirto»"),
    # 10078 unausstehlich
    (11390, "example_tr",
     "Dayanılmaz davranışı onu popüler olmaktan engelledi",
     "Dayanılmaz davranışı onu sevilmeyen biri yapıyor",
     "«popüler olmaktan engelledi» — калька"),
    (11390, "example_pl", "Dzisiaj jesteś naprawdę nieznośny",
     "Jego nieznośne zachowanie czyni go niepopularnym",
     "перевод другого предложения"),
    # 10079 Durchsuchungsbeschluss
    (16771, "example_uk", "Суддя видав наказ про обшук",
     "Суддя видав ордер на обшук",
     "перевод слова — «ордер на обшук»"),
    # 10080 Morgendämmerung
    (18896, "example_ru", "На рассвете я люблю пробегать",
     "На рассвете я люблю бегать",
     "«пробегать» — не та форма"),
    # 10081 Erwähnung
    (14277, "example_uk", "Його згадка в звіті була несподіванною",
     "Його згадка у звіті була несподіваною",
     "«несподіванною» с двойной «н», и «в» перед согласной"),
    (14277, "example_tr", "Adımın anılması bile beni rahatsız etti",
     "Raporda anılması şaşırtıcıydı",
     "перевод другого предложения"),
    # 10082 Konzentrationslager
    (16772, "example_uk",
     "Концентраційний табір — це темна глава історії",
     "Концентраційний табір — це темний розділ історії",
     "«глава» в значении раздела — русизм"),
    # 10083 Vene
    (13031, "example_tr", "Damar cildin altında açıkça görülüyordu",
     "Toplardamar cildin altında açıkça görülüyordu",
     "перевод слова — «toplardamar»"),
    (13031, "example_pl", "Pielęgniarka długo szukała żyły",
     "Żyła była wyraźnie widoczna pod skórą",
     "перевод другого предложения"),
    # 10084 kosmisch
    (18062, "example_ru",
     "Космическая радиация приходит отовсюду из космоса",
     "Космическое излучение приходит отовсюду из космоса",
     "«Strahlung» это излучение, а не радиация"),
    # 10087 auslegen
    (8340, "example_uk", "Я розставляю товари в магазині",
     "Я викладаю товари в магазині",
     "перевод слова — «викладати»"),
    (8340, "example_tr", "Mağazada mal sergilerim",
     "Mağazada malları sergiliyorum",
     "потерян аккузатив"),
    # 10089 Verwüstung
    (15793, "example_tr", "Savaştan sonraki yıkım devasa idi",
     "Savaştan sonraki yıkım devasaydı",
     "«idi» отдельно"),
    # 10090 jaulen
    (15794, "example_ru", "Волки воют на луну",
     "Собака воет по ночам",
     "перевод другого предложения"),
    # 10095 Mündel
    (16775, "example_uk", "Судля піклується про підопічного",
     "Суддя піклується про підопічного",
     "«Судля» — опечатка"),
    # 10097 Epoche
    (18897, "example_ru", "Эпоха Ренессанса была важной",
     "Ренессанс был важной эпохой",
     "подлежащее подменено"),
    (18897, "example_tr", "Rönesans önemli bir dönem idi",
     "Rönesans önemli bir dönemdi",
     "«idi» отдельно"),
    # 10098 prüde
    (11391, "example_uk", "У неї манірне ставлення до таких тем",
     "У неї манірне ставлення до сексуальності",
     "«до таких тем» в эталоне нет"),
    (11391, "example_tr", "Cinsiyete karşı soğuk bir tutumu var",
     "Cinselliğe karşı aşırı utangaç bir tutumu var",
     "«cinsiyet» это пол, а «Sexualität» — cinsellik"),
    (11391, "example_pl", "Jest zbyt pruderyjna na takie rozmowy",
     "Ma pruderyjne podejście do seksualności",
     "перевод другого предложения"),
    # 10099 unverheiratet
    (15276, "example_tr", "Kardeşim hâlâ bekâr",
     "Evlenmemiş ve iki çocuğu var",
     "перевод другого предложения"),
    (15276, "example_pl", "Mój brat jest jeszcze nieżonaty",
     "Jest nieżonaty i ma dwoje dzieci",
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
