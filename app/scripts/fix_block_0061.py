"""
Правки блока 61 (ряды 10501–10700, ранги 21521–22018).

Две находки блока.

ПЕРВАЯ: эталон подменили после перевода. Четыре ряда одного строения:

    10560 Fernsteuerung
      de  Das kleine Boot hat eine Fernsteuerung
      pl  Ta mała łódka ma zdalne sterowanie        ← сходится
      en  The TV remote control broke               ← а эти четверо
      ru  Пульт от телевизора сломался                 сходятся между
      uk  Пульт від телевізора зламався                 собой на ДРУГОМ
      tr  Televizyon kumandası kırıldı                  предложении

То же в 10561 (`potentiell`), 10650 (`erringen`), 10655
(`Repräsentant`). Расклад везде один: меньшинство переводов совпадает
с немецким, большинство — друг с другом, и это большинство осмысленно
и согласованно.

Это НЕ тот случай, что описан в блоке 56. Там переводы расходились
врастопырку, и это выдавало сломанный эталон. Здесь они, наоборот,
плотно сходятся — просто не на эталоне. Значит эталон не сломан, а
ЗАМЕНЁН: его переписали после того, как перевели, и обновили один-два
языка из пяти.

Правило для чтения отсюда: смотреть не на то, сколько переводов
расходится с немецким, а на то, согласны ли они между собой. Согласны
и против эталона — эталон новее переводов, править переводы. Не
согласны ни с эталоном, ни друг с другом — сломан эталон.

ВТОРАЯ: девять дефектов в самих немецких примерах на 200 рядов —
больше, чем в любом блоке до сих пего:

    geniesst              → genießt            (ss вместо ß)
    Wir traffen uns       → Wir trafen uns     (лишняя f)
    Kuck mal              → Guck mal           (слово ряда `gucken`)
    Lärmemachen           → Der ständige Lärm  (нет такого слова)
    einen Streit anzetteln → anzuzetteln        (потеряно `zu`)
    gute Wodka            → guten Wodka        (род)
    vereinfachen für dich → für dich vereinfachen (порядок слов)
    Wetter-Vorhersage     → Wettervorhersage   (дефис лишний)
    sie … widersetzten    → widersetzte        (число внутри фразы)

Все девять разного рода, общей приметы под них нет. `anzetteln` —
обратная сторона приметы блока 59: там было ЛИШНЕЕ `zu` после
модального, здесь `zu` ПОТЕРЯНО после `versuchen`. Одно место в языке,
две противоположные ошибки — уже третий раз за проход.

    python -m app.scripts.fix_block_0061            # показать
    python -m app.scripts.fix_block_0061 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 10502 zumuten
    (8420, "example_uk",
     "Я не можу вимагати від тебе, щоб ти справився з цим один",
     "Я не можу вимагати від тебе, щоб ти справився з цим зовсім сам",
     "потеряно «ganz allein»"),
    (8420, "example_pl", "Nie mogę od ciebie wymagać, żebyś zrobił to sam",
     "Nie mogę od ciebie wymagać, żebyś zrobił to zupełnie sam",
     "потеряно «ganz»"),
    # 10503 Hemisphäre
    (18074, "example_ru",
     "Северное полушарие имеет совершенно другие сезоны, чем южное",
     "В Северном полушарии времена года совсем другие, чем в Южном",
     "«иметь сезоны» — калька, и «Jahreszeiten» это времена года"),
    (18074, "example_uk",
     "Північна півкуля має зовсім інші сезони, ніж південна",
     "У Північній півкулі зовсім інші пори року, ніж у Південній",
     "«мати сезони» — калька, и «Jahreszeiten» это пори року"),
    # 10504 ungesehen
    (8421, "example_pl", "Wyszedł z domu niezauważony przez nikogo",
     "Wszedł do pokoju niezauważony i znowu go opuścił",
     "перевод другого предложения"),
    # 10505 Enkeltochter
    (15292, "example_uk",
     "Моїй онучці в наступному місяці виповниться п'ять років",
     "Моїй онучці наступного місяця виповниться п'ять років",
     "«в наступному місяці» — калька"),
    (15292, "example_pl", "Moja wnuczka idzie już do szkoły",
     "Moja wnuczka w przyszłym miesiącu skończy pięć lat",
     "перевод другого предложения"),
    # 10506 verwickeln
    (8422, "example_pl", "Nie wplątuj mnie w swoje kłopoty",
     "Nie próbuj mnie wplątywać w swoje problemy",
     "потеряно «Versuche nicht»"),
    # 10507 schweigsam
    (11427, "example_pl", "Mój dziadek jest bardzo małomówny",
     "To małomówny typ, który niewiele mówi",
     "перевод другого предложения"),
    # 10508 mitfühlend
    (11428, "example_uk",
     "Вона була чутливою людиною, яка турбувалася про інших",
     "Вона була співчутливою людиною, яка турбувалася про інших",
     "«чутлива» это восприимчивая, а не сочувствующая"),
    (11428, "example_tr",
     "Diğerleriyle ilgilenen, sempati duyan bir insandı",
     "Başkalarıyla ilgilenen, şefkatli bir insandı",
     "«sempati duyan» — калька, нужно «şefkatli»"),
    (11428, "example_pl", "Ona jest bardzo współczująca wobec innych",
     "Była współczującą osobą, która troszczyła się o innych",
     "перевод другого предложения"),
    # 10510 unaufhörlich
    (18908, "example_tr",
     "Durmaksız yağan yağmur gezintileri imkansız kıldı",
     "Aralıksız yağan yağmur geziyi imkânsız kıldı",
     "«durmaksız» — нет такой формы, и в эталоне один Ausflug"),
    # 10511 Spazierfahrt
    (17363, "example_tr", "Dün Boğaz'da gemi gezisi yaptık",
     "Tekneyle güzel bir gezinti yaptık",
     "перевод другого предложения"),
    # 10513 lausig
    (8423, "example_uk", "Погода сьогодні абсолютно жахлива",
     "Погода сьогодні зовсім паршива",
     "перевод слова — «паршива»"),
    # 10514 verprügeln
    (16826, "example_ru", "Плохой человек избил собаку, что было ужасно",
     "Мужчина избил собаку, что было ужасно",
     "«плохой» в эталоне нет"),
    (16826, "example_uk", "Поганий чоловік побив собаку, що було жахливо",
     "Чоловік побив собаку, що було жахливо",
     "«поганий» в эталоне нет"),
    (16826, "example_tr", "Kötü adam köpeği dövdü, bu korkunçtu",
     "Adam köpeği dövdü, bu korkunçtu",
     "«kötü» в эталоне нет"),
    (16826, "example_pl", "Chłopcy pobili go na podwórku",
     "Mężczyzna pobił psa, co było straszne",
     "перевод другого предложения"),
    # 10516 Fernsehserie
    (14767, "example_tr", "Bu dizi gerçekten heyecan verici",
     "Bu dizi gerçekten heyecan vericiydi",
     "эталон в прошедшем времени"),
    # 10517 Nachruf
    (15293, "example_pl", "W gazecie ukazał się jego nekrolog",
     "Nekrolog opisał jego życie i osiągnięcia",
     "перевод другого предложения"),
    # 10518 Herzklopfen
    (13063, "example_uk",
     "Коли він її бачив, його серцебиття ставало сильнішим",
     "Коли він її побачив, серцебиття ставало все сильнішим",
     "«бачив» это многократно, а в эталоне один раз"),
    (13063, "example_pl", "Przed egzaminem miałam kołatanie serca",
     "Kołatanie serca stawało się coraz mocniejsze, gdy ją zobaczył",
     "перевод другого предложения"),
    # 10520 Ammoniak
    (18075, "example_uk",
     "Запах аміаку на фабриці був просто неприємний",
     "Запах аміаку на фабриці був просто нестерпний",
     "«unerträglich» это нестерпный, а не неприятный"),
    # 10522 Baumstamm
    (15818, "translation_uk", "стовбур дерева, колода, бревно",
     "стовбур дерева, колода, кругляк",
     "«бревно» — русское слово"),
    # 10523 Rehabilitation
    (13064, "example_de",
     "Nach dem Unfall in Berlin brauchte er lange Rehabilitation",
     "Nach dem Unfall brauchte er lange Rehabilitation",
     "«in Berlin» ничего не добавляет, и пять переводов из пяти его "
     "не взяли"),
    (13064, "example_ru",
     "После аварии в Берлине ему потребовалась долгая реабилитация",
     "После аварии ему потребовалась долгая реабилитация",
     "вслед за исправленным эталоном"),
    (13064, "example_pl", "Po wypadku czeka go długa rehabilitacja",
     "Po wypadku potrzebował długiej rehabilitacji",
     "эталон в прошедшем времени"),
    # 10524 untertrieben
    (14298, "example_uk", "Довго приховуваний гнів нарешті вирвався",
     "Його критика була применшеною, але достатньо ясною",
     "перевод совсем другого предложения"),
    (14298, "example_pl", "Jego ocena była wyraźnie pomniejszona",
     "Jego krytyka była pomniejszona, ale wystarczająco wyraźna",
     "«ocena» вместо «Kritik», и потеряна вторая половина"),
    # 10525 schwelgen
    (11430, "example_tr", "Çocukluklarının anılarında yaşanıyorlar",
     "Çocukluk anılarına dalıyorlar",
     "«yaşanıyorlar» — разваленный пассив"),
    # 10526 Wolkenkratzer
    (18450, "example_en", "The new skyscraper in the city is impressive",
     "The new skyscraper in Frankfurt is impressive",
     "в эталоне Франкфурт"),
    (18450, "example_uk", "Новий хмарочос у місті вражає",
     "Новий хмарочос у Франкфурті вражає",
     "в эталоне Франкфурт"),
    (18450, "example_tr", "Frankfurttaki yeni gökdelen etkileyici",
     "Frankfurt'taki yeni gökdelen etkileyici",
     "потерян апостроф в имени"),
    # 10527 geschwind
    (8424, "translation_uk", "швидкий, скорий, проворний",
     "швидкий, скорий, спритний",
     "«проворний» — русское слово"),
    (8424, "example_en", "The car is going very fast",
     "The car is going very fast along the motorway",
     "потеряно «die Autobahn entlang»"),
    (8424, "example_uk", "Машина їде дуже швидко",
     "Машина їде дуже швидко автобаном",
     "потеряно «die Autobahn entlang»"),
    (8424, "example_tr", "Araba çok hızlı gidiyor",
     "Araba otoyolda çok hızlı gidiyor",
     "потеряно «die Autobahn entlang»"),
    (8424, "example_pl", "Nasz nowy samochód jest bardzo szybki",
     "Samochód jedzie bardzo szybko autostradą",
     "перевод другого предложения"),
    # 10529 zuweilen
    (18909, "example_uk", "Іноді ідуть дощі цілий день",
     "Іноді дощ іде цілий день",
     "в эталоне «regnet es», один дождь"),
    (18909, "example_tr", "Bazen esir bütün gün yağıyor",
     "Bazen bütün gün yağmur yağıyor",
     "«esir» значит «пленник» — слово не из этой фразы"),
    # 10530 still
    (11969, "example_tr",
     "Gazlı mineralli sudan çok gazlı olmayan suyu tercih ederim",
     "Gazlı maden suyundan ziyade gazsız suyu tercih ederim",
     "«çok» разваливает сравнение"),
    (11969, "example_pl", "To bardzo cicha i spokojna okolica",
     "Wolę pić wodę niegazowaną niż wodę mineralną",
     "перевод другого предложения"),
    # 10531 Erdöl
    (17881, "example_ru", "Нефть является важным источником сырья",
     "Нефть — важный источник сырья",
     "«является» — канцелярит"),
    (17881, "example_pl", "Ceny ropy naftowej znowu poszły w górę",
     "Ropa naftowa jest ważnym źródłem surowców",
     "перевод другого предложения"),
    # 10532 Wiederauferstehung
    (14768, "example_tr", "Eski geleneklerin diriltilmesi önemlidir",
     "Eski geleneklerin yeniden canlanması önemlidir",
     "«diriltilmesi» это «что их оживили», а речь о возрождении"),
    # 10533 flussaufwärts
    (15819, "example_tr", "Tekne akıntıya karşı ırmak yukarısında gitti",
     "Tekne akıntıya karşı nehrin yukarısına doğru gitti",
     "«ırmak yukarısında» — разваленная фраза"),
    # 10534 Armaturenbrett
    (17364, "translation_uk", "панель приладів, приборна панель",
     "панель приладів, щиток приладів",
     "«приборна» — русизм"),
    (17364, "example_uk", "Прилади на панелі показують швидкість",
     "Прилади на щитку показують швидкість",
     "потеряно слово ряда"),
    # 10535 steril
    (13065, "example_pl", "Narzędzia muszą być sterylne",
     "Sala operacyjna musi być sterylna",
     "перевод другого предложения"),
    # 10536 krabbeln
    (8425, "example_tr", "Bebek yerde sürünüyor",
     "Bebek yerde emekliyor",
     "«sürünmek» это ползти на животе, а младенец «emekler»"),
    (8425, "example_pl", "Nasze dziecko już raczkuje po pokoju",
     "Dziecko raczkuje po podłodze",
     "перевод другого предложения"),
    # 10537 haarig
    (8583, "example_en", "The situation became quite tricky",
     "The situation is quite tricky",
     "эталон в настоящем времени"),
    (8583, "example_uk", "Ситуація стала досить складною",
     "Ситуація досить дражлива",
     "эталон в настоящем времени"),
    (8583, "example_tr", "Durum oldukça zor hale geldi",
     "Durum oldukça zor",
     "эталон в настоящем времени"),
    # 10538 vorherig
    (18910, "example_tr", "Önceki müdür çok başarılar elde etti",
     "Önceki müdür çok şey başardı",
     "«çok başarılar» — двойное множественное"),
    # 10539 Grübchen
    (15295, "example_uk",
     "У неї були дві мила ямочки на щоках, коли вона посміхалась",
     "У неї були дві милі ямочки на щоках, коли вона посміхалась",
     "«дві мила» — рассогласование"),
    (15295, "example_pl", "Ma śliczne dołki w policzkach, kiedy się śmieje",
     "Miała dwa śliczne dołeczki w policzkach, kiedy się uśmiechała",
     "эталон в прошедшем, и потеряно «два»"),
    # 10540 zugezogen
    (18451, "example_en",
     "The relocated residents of the district brought new perspectives",
     "The newly arrived residents of the district brought new perspectives",
     "«relocated» это переселённый кем-то, а `zugezogen` — приезжий"),
    (18451, "example_ru",
     "Переселившиеся жители района принесли с собой новые взгляды",
     "Приезжие жители района принесли с собой новые взгляды",
     "перевод слова — «приезжий»"),
    (18451, "example_uk",
     "Переселені жителі району принесли з собою нові погляди",
     "Приїжджі мешканці району принесли з собою нові погляди",
     "«переселені» это переселённые кем-то"),
    (18451, "example_tr",
     "Semtte taşınan sakinler yeni perspektifler getirdiler",
     "Semte sonradan taşınan sakinler yeni bakış açıları getirdiler",
     "«semtte taşınan» — не то управление"),
    # 10541 Untermieter
    (18452, "example_ru", "В соседней квартире новый жилец",
     "Мой квартирант всегда платит за аренду вовремя, первого числа месяца",
     "перевод другого предложения"),
    (18452, "example_uk",
     "Мій квартирант завжди платить аренду вчасно першого числа місяця",
     "Мій квартирант завжди платить за оренду вчасно першого числа місяця",
     "«аренду» — русское слово и не то управление"),
    # 10542 behütet
    (11431, "translation_uk", "захищений, оберігаємий, під опікою",
     "захищений, оберіганий, під опікою",
     "«оберігаємий» — русская форма пассивного причастия"),
    (11431, "example_uk",
     "Вона виросла в дуже охоронюваній сім'ї і не знала жорсткої реальності",
     "Вона виросла в дуже захищеній сім'ї і не знала суворої реальності",
     "«охоронювана» это под физической охраной, и «жорстка» это жёсткая"),
    (11431, "example_pl", "Wychowała się w bardzo chronionym domu",
     "Wychowała się w bardzo chronionej rodzinie i nie znała surowej "
     "rzeczywistości",
     "потеряна вторая половина, и в эталоне семья"),
    # 10543 unerlässlich
    (8426, "example_tr", "Bu iş için ehliyet gerekli",
     "Bu pozisyon için ehliyet şart",
     "«gerekli» теряет силу слова `unerlässlich`"),
    (8426, "example_pl", "Dobre buty są niezbędne w górach",
     "Prawo jazdy jest niezbędne na tym stanowisku",
     "перевод другого предложения"),
    # 10544 Overall
    (13765, "example_en",
     "The worker put on his overalls before going into the workshop",
     "The worker puts on his overalls before going into the workshop",
     "эталон в настоящем времени"),
    (13765, "example_uk",
     "Робітник надягнув свій комбінезон, перш ніж піти в майстерню",
     "Робітник надягає свій комбінезон, перш ніж піти в майстерню",
     "эталон в настоящем времени"),
    (13765, "example_tr",
     "İşçi, atölyeye gitmeden önce tulumunu giydi",
     "İşçi, atölyeye gitmeden önce tulumunu giyer",
     "эталон в настоящем времени"),
    # 10545 beurlaubt — ss вместо ß в эталоне
    (9232, "example_de",
     "Er ist derzeit beurlaubt und geniesst seinen Urlaub im Ausland",
     "Er ist derzeit beurlaubt und genießt seinen Urlaub im Ausland",
     "«geniesst» — ss вместо ß"),
    # 10547 Tortur
    (16827, "example_pl", "To czekanie było prawdziwą męką",
     "Długie czekanie było prawdziwą męką dla pacjentów",
     "потеряны «lange» и «für die Patienten»"),
    # 10549 trübe
    (8428, "translation_uk", "мутний, похмурий, тусклий, сумний",
     "мутний, похмурий, тьмяний, сумний",
     "«тусклий» — русское слово"),
    (8428, "example_pl", "Woda w rzece jest dziś mętna",
     "Niebo wyglądało pochmurnie, deszcz mógł spaść w każdej chwili",
     "перевод другого предложения"),
    # 10550 Bluterguss
    (13066, "example_pl", "Po upadku mam siniaka na kolanie",
     "Po wypadku miał kilka siniaków na nogach",
     "перевод другого предложения"),
    # 10551 barsch
    (11432, "example_uk",
     "Він відповів дуже різко і тим самим образив її",
     "Він відповів дуже різко і тим самим образив її почуття",
     "потеряно «ihre Gefühle»"),
    (11432, "example_pl", "Odpowiedział mi bardzo opryskliwym tonem",
     "Odpowiedział bardzo opryskliwie i zranił jej uczucia",
     "потеряна вторая половина"),
    # 10552 konsultieren
    (8429, "example_tr",
     "Karar vermeden önce avukatla danışmam gerekiyor",
     "Karar vermeden önce avukata danışmam gerekiyor",
     "«danışmak» требует датива, а не инструменталиса"),
    (8429, "example_pl", "Muszę się skonsultować z prawnikiem",
     "Muszę się skonsultować z prawnikiem, zanim podejmę decyzję",
     "потеряна вторая половина"),
    # 10554 Trüffel
    (11970, "example_uk",
     "Трюфель — дорога делікатес, яку люблять гурмани",
     "Трюфель — дорогий делікатес, який люблять гурмани",
     "рассогласование рода"),
    (11970, "example_tr",
     "Mantar, gurmeler tarafından sevilen pahalı bir lezzettir",
     "Trüf mantarı, gurmelerin sevdiği pahalı bir lezzettir",
     "«mantar» это гриб вообще, а ряд о трюфеле"),
    (11970, "example_pl", "Trufle są bardzo drogim przysmakiem",
     "Trufla to drogi przysmak, który kochają smakosze",
     "эталон в единственном числе"),
    # 10556 Kartoffelbrei
    (11971, "example_pl",
     "Na obiad zrobiłam puree ziemniaczane z kotletem",
     "Na obiad było puree ziemniaczane z klopsikami",
     "в эталоне фрикадельки, а не котлета"),
    # 10557 gefügig — число внутри немецкой фразы
    (11433, "example_de",
     "Er versuchte, sie gefügig zu machen, aber sie widersetzten sich",
     "Er versuchte, sie gefügig zu machen, aber sie widersetzte sich",
     "«sie» одна, а «widersetzten» о многих"),
    (11433, "translation_uk", "покірний, послушливий, безвольний",
     "покірний, податливий, безвольний",
     "«послушливий» — нет такого слова"),
    (11433, "example_ru",
     "Он пытался сделать их покорными, но они сопротивлялись",
     "Он пытался сделать её покорной, но она сопротивлялась",
     "вслед за исправленным эталоном"),
    (11433, "example_uk",
     "Він намагався зробити її послушною, але вона спиралася",
     "Він намагався зробити її покірною, але вона опиралася",
     "«послушною» — русское слово, «спиралася» значит «опиралась на что-то»"),
    (11433, "example_tr", "Onu itaatkar yapmaya çalıştı ama direndi",
     "Onu itaatkâr yapmaya çalıştı ama o direndi",
     "потерян циркумфлекс и подлежащее второй части"),
    (11433, "example_pl", "Chciał, żeby wszyscy byli mu ulegli",
     "Chciał ją sobie podporządkować, ale ona się opierała",
     "перевод другого предложения"),
    # 10558 Barbar
    (14769, "example_tr", "Romalılar Germanları barbar sayıyorlardı",
     "Romalılar Germenleri barbar sayıyordu",
     "«Germanları» — не турецкая форма названия"),
    # 10560 Fernsteuerung — эталон заменили после перевода
    (17714, "example_en", "The TV remote control broke",
     "The little boat has a remote control",
     "перевод остался от прежнего эталона"),
    (17714, "example_ru", "Пульт от телевизора сломался",
     "У маленькой лодки есть дистанционное управление",
     "перевод остался от прежнего эталона"),
    (17714, "example_uk", "Пульт від телевізора зламався",
     "Маленький човен має дистанційне керування",
     "перевод остался от прежнего эталона"),
    (17714, "example_tr", "Televizyon kumandası kırıldı",
     "Küçük teknenin uzaktan kumandası var",
     "перевод остался от прежнего эталона"),
    # 10561 potentiell — то же
    (8433, "example_en",
     "The potential danger was recognized by the authorities",
     "He is a potential customer",
     "перевод остался от прежнего эталона"),
    (8433, "example_uk", "Потенційна небезпека була визнана властями",
     "Він потенційний клієнт",
     "перевод остался от прежнего эталона, и «властями» — русизм"),
    (8433, "example_tr", "Potansiyel tehlike yetkili tarafından fark edildi",
     "O potansiyel bir müşteri",
     "перевод остался от прежнего эталона"),
    (8433, "example_pl", "To nasz potencjalny klient",
     "To potencjalny klient",
     "«nasz» в эталоне нет"),
    # 10562 wirr
    (11434, "example_pl", "Opowiadał jakieś pogmatwane historie",
     "Jego pogmatwane myśli utrudniały zrozumienie",
     "перевод другого предложения"),
    # 10563 beliebig
    (8434, "example_pl", "Wybierz dowolny kolor do pokoju",
     "Możesz wybrać dowolny kolor do swojego pokoju",
     "эталон не в повелительном"),
    # 10565 Abstecher
    (17365, "example_uk", "Ми зробили чималий крюк через ліс",
     "Ми зробили невеликий заїзд до міста, перш ніж повернулися до готелю",
     "перевод другого предложения, и «крюк» — русское слово"),
    # 10566 Altenheim
    (13067, "example_tr", "Büyükannem şimdi yaşlı evinde yaşıyor",
     "Büyükannem şimdi huzurevinde yaşıyor",
     "«yaşlı evi» — не слово, нужно «huzurevi»"),
    # 10567 flippen
    (11435, "example_uk", "Коли я це чую, я збожеволіюю",
     "Коли я це чую, я зовсім божеволію",
     "«збожеволіюю» — лишняя гласная"),
    # 10568 Hilferuf
    (14299, "example_pl", "Usłyszeliśmy wołanie o pomoc z ulicy",
     "Jego wołanie o pomoc zostało w końcu usłyszane",
     "перевод другого предложения"),
    # 10570 saure
    (11972, "example_tr", "Ekşi süt bana tat vermedi",
     "Ekşi süt hoşuma gitmiyor",
     "«tat vermedi» — разваленная идиома"),
    # 10571 virtuell — опечатка в эталоне
    (17715, "example_de", "Wir traffen uns in einer virtuellen Konferenz",
     "Wir trafen uns in einer virtuellen Konferenz",
     "«traffen» — лишняя f"),
    # 10572 Meeresfrüchte
    (11973, "example_pl", "Na kolację zamówiliśmy owoce morza",
     "Kocham owoce morza, ale mój mąż nie",
     "перевод другого предложения"),
    # 10575 Ställe
    (18453, "example_ru", "Конные стойла находятся за двором",
     "Конюшни находятся за двором",
     "«конные стойла» — калька"),
    (18453, "example_uk", "Кінні стійла знаходяться за двором",
     "Стайні розташовані за двором",
     "«кінні стійла» — калька"),
    # 10576 Klausel
    (16828, "example_pl", "Ta klauzula w umowie mi się nie podoba",
     "Ta klauzula jest bardzo ważna dla umowy",
     "перевод другого предложения"),
    # 10577 verdursten
    (13068, "example_pl", "Bez wody można umrzeć z pragnienia",
     "Na pustyni mogliby umrzeć z pragnienia",
     "перевод другого предложения"),
    # 10578 gepresst
    (8436, "example_uk", "Сік вичавлюється зі свіжих фруктів",
     "Сік зі свіжих фруктів свіжовичавлений",
     "ряд о прилагательном, а перевод сделал из него глагол"),
    (8436, "example_pl", "Na śniadanie piję świeżo wyciśnięty sok",
     "Sok ze świeżych owoców jest świeżo wyciśnięty",
     "перевод другого предложения"),
    # 10579 Unterwerfung
    (11436, "example_tr", "Nüfusun itaati onun amacıydı",
     "Halkı boyun eğdirmek onun amacıydı",
     "«itaat» это послушание, а `Unterwerfung` — подчинение силой"),
    (11436, "example_pl", "Chodziło mu tylko o podporządkowanie ludzi",
     "Podporządkowanie ludności było jego celem",
     "перевод другого предложения"),
    # 10580 wachsende
    (8437, "example_tr", "Büyüyen nüfus bir zorluk",
     "Büyüyen nüfus bir zorluk oluşturuyor",
     "потеряно «stellt dar»"),
    # 10581 Konkubine
    (14770, "example_uk", "У історії король мав наложницю",
     "У цій історії король мав наложницю",
     "«У історії» вместо «у цій історії»"),
    (14770, "example_tr", "Tarihte kral bir metresi vardı",
     "Tarihte kralın bir metresi vardı",
     "потерян родительный падеж"),
    # 10582 Halsschlagader
    (13069, "example_pl", "Lekarz zbadał mi tętnicę szyjną",
     "Przepływ krwi w tętnicy szyjnej jest prawidłowy",
     "перевод другого предложения"),
    # 10583 Rosenkranz
    (14771, "translation_ru", "чётки, розарий",
     "чётки, молитвенные чётки",
     "«розарий» по-русски это сад роз"),
    # 10584 Latinum
    (9611, "example_uk",
     "Для навчання в університеті тобі потрібен латинський сертифікат",
     "Для навчання в університеті тобі потрібен сертифікат знання латини",
     "«латинський сертифікат» — не то"),
    # 10586 eintauchen
    (8438, "example_tr", "Bu ülkenin kültürüne batılmak istiyorum",
     "Bu ülkenin kültürüne dalmak istiyorum",
     "«batılmak» — нет такой формы"),
    (8438, "example_pl", "Zanurz pędzel w farbie",
     "Chcę zanurzyć się w kulturze tego kraju",
     "перевод другого предложения"),
    # 10588 Gefängnisstrafe
    (16829, "example_uk", "Тюремний термін становить п'ять років",
     "Тюремний строк становить п'ять років",
     "в статье «строк», а в примере «термін»"),
    (16829, "example_pl", "Dostał karę więzienia za kradzież",
     "Kara więzienia wynosi pięć lat",
     "перевод другого предложения"),
    # 10591 Alkoholproblem
    (13070, "example_pl", "On od lat ma problem alkoholowy",
     "Jego problem alkoholowy jest znany od dawna",
     "перевод другого предложения"),
    # 10592 feststecken
    (8441, "example_uk", "Ми застрягли в затору",
     "Ми застрягли в заторі",
     "не тот падеж"),
    (8441, "example_tr", "Trafiklerde sıkışıp kaldık",
     "Trafikte sıkışıp kaldık",
     "«trafik» во множественном не ставится"),
    (8441, "example_pl", "Utknęliśmy w korku na godzinę",
     "Utknęliśmy w korku",
     "«na godzinę» в эталоне нет"),
    # 10593 Extras
    (8442, "example_en", "The package includes a few extras as a gift",
     "The package includes a few small extras",
     "«as a gift» в эталоне нет, зато потеряно «kleine»"),
    (8442, "example_uk", "Пакет містить кілька додатків у подарунок",
     "Пакет містить кілька невеликих додатків",
     "«у подарунок» в эталоне нет, зато потеряно «kleine»"),
    (8442, "example_tr", "Paket hediye olarak birkaç ekstralar içeriyor",
     "Paket birkaç küçük ekstra içeriyor",
     "«birkaç ekstralar» — двойное множественное"),
    # 10594 Homosexualität
    (15296, "example_pl", "O homoseksualności mówi się dziś otwarcie",
     "Homoseksualność powinna być akceptowana w społeczeństwie",
     "перевод другого предложения"),
    # 10595 getrübt
    (8443, "example_uk", "Вода помутніла через водорості",
     "Вода замутнена водоростями",
     "ряд о прилагательном, а перевод сделал из него глагол"),
    (8443, "example_pl", "Woda w stawie jest zmącona",
     "Woda jest zmącona przez algi",
     "перевод другого предложения"),
    # 10596 Wiedereintritt
    (16830, "example_en", "His re-entry into politics surprised everyone",
     "His re-entry into the party was controversial",
     "в эталоне партия, а не политика"),
    # 10597 Konkurs
    (17882, "example_ru", "Компания должна была объявить банкротство",
     "Компания должна была объявить о банкротстве",
     "«объявить банкротство» — не то управление"),
    (17882, "example_pl", "Firma ogłosiła bankructwo w zeszłym roku",
     "Firma musiała ogłosić bankructwo",
     "перевод другого предложения"),
    # 10598 unregelmäßig
    (8444, "example_pl", "Pracuję w nieregularnych godzinach",
     "Czas pracy jest nieregularny",
     "перевод другого предложения"),
    # 10599 Zugführer
    (17366, "example_ru", "Проводник поезда проверил билеты",
     "Начальник поезда проверил билеты",
     "«проводник» это Schaffner, а не Zugführer"),
    (17366, "example_uk", "Проводник потяга перевірив квитки",
     "Начальник поїзда перевірив квитки",
     "«проводник» — русское написание и не то слово"),
    # 10600 berauscht
    (13071, "example_pl", "Był odurzony alkoholem i ledwo stał",
     "Był odurzony i ledwo mógł chodzić",
     "«alkoholem» в эталоне нет, и «kaum laufen» это едва ходить"),
    # 10602 Kommune
    (16831, "example_en", "The commune has issued new rules",
     "The municipality has issued new rules",
     "немецкая Kommune это муниципалитет"),
    (16831, "example_ru", "Коммуна приняла новые правила",
     "Муниципалитет принял новые правила",
     "немецкая Kommune это муниципалитет"),
    (16831, "example_uk", "Комуна видала нові правила",
     "Громада ухвалила нові правила",
     "немецкая Kommune это громада"),
    (16831, "example_tr", "Komün yeni kurallar belirlemişti",
     "Belediye yeni kurallar koydu",
     "немецкая Kommune это belediye"),
    (16831, "example_pl", "Gmina remontuje drogę koło szkoły",
     "Gmina wydała nowe przepisy",
     "перевод другого предложения"),
    # 10603 akut
    (13072, "example_en", "This is an acute problem",
     "This is an acute problem that we must solve immediately",
     "потеряна вторая половина"),
    (13072, "example_tr", "Bu akut bir sorundur",
     "Bu, hemen çözmemiz gereken akut bir sorun",
     "потеряна вторая половина"),
    (13072, "example_pl", "To jest ostry problem i trzeba go rozwiązać",
     "To pilny problem, który musimy natychmiast rozwiązać",
     "потеряно «sofort»"),
    # 10605 beaufsichtigen
    (9238, "example_tr",
     "Anne oyun alanında çocukları gözetim altında tutuyor",
     "Anne oyun alanında çocuklara göz kulak oluyor",
     "«gözetim altında tutmak» это держать под надзором"),
    # 10608 Eingebung
    (11438, "example_uk", "Раптова ідея допомогла мені вирішити проблему",
     "Раптове осяяння допомогло мені вирішити проблему",
     "перевод слова — «осяяння»"),
    (11438, "example_pl", "Miałem nagłe olśnienie pod prysznicem",
     "Nagłe olśnienie pomogło mi rozwiązać problem",
     "перевод другого предложения"),
    # 10611 belanglos
    (8446, "example_pl", "To zupełnie błaha sprawa, nie martw się",
     "To błaha uwaga, która nie ma nic do rzeczy",
     "перевод другого предложения"),
    # 10612 Dienstboten
    (9239, "example_uk", "У старші часи багаті родини мали багато слуг у домі",
     "За давніх часів багаті родини мали багато слуг у домі",
     "«у старші часи» — не по-украински"),
    # 10613 Lavendel
    (15821, "example_tr", "Bahçedeki lavanta harika kokulu",
     "Bahçedeki lavanta harika kokuyor",
     "«kokulu» это прилагательное, а в эталоне глагол"),
    # 10615 erhitzt
    (8447, "example_uk", "У каміні вже розпалений вогонь",
     "Дискусія ставала все більш розпаленою",
     "перевод совсем другого предложения"),
    (8447, "example_pl", "Dyskusja stawała się coraz bardziej rozgrzana",
     "Dyskusja stawała się coraz bardziej rozgorączkowana",
     "«rozgrzana» о предмете, а не о споре"),
    # 10616 Gehweg
    (18454, "example_en", "Pedestrians can walk safely on the sidewalk",
     "You can walk safely on the sidewalk",
     "в эталоне «du», а не пешеходы"),
    (18454, "example_ru", "На тротуаре пешеходы ходят безопасно",
     "По тротуару ты можешь идти безопасно",
     "в эталоне «du», а не пешеходы"),
    (18454, "example_uk", "На тротуарі пішоходи можуть ходити безпечно",
     "На тротуарі ти можеш іти безпечно",
     "в эталоне «du», а не пешеходы"),
    (18454, "example_tr", "Yaya kaldırımda güvenli bir şekilde yürüyebilir",
     "Kaldırımda güvenle yürüyebilirsin",
     "в эталоне «du», а не пешеход"),
    # 10617 Bestrahlung
    (13073, "example_en", "Radiation is a treatment for cancer",
     "Radiation therapy is a treatment for cancer",
     "«radiation» это само излучение, а `Bestrahlung` — лечение"),
    (13073, "example_tr", "Radyasyon kanser tedavisidir",
     "Işın tedavisi kansere karşı bir tedavidir",
     "«radyasyon» это само излучение"),
    (13073, "example_pl", "Po operacji czeka go jeszcze naświetlanie",
     "Naświetlanie to metoda leczenia raka",
     "перевод другого предложения"),
    # 10618 zurückblicken
    (18911, "example_uk",
     "Коли я дивлюсь назад, то це були щасливі роки",
     "Коли я озираюся назад, це були щасливі роки",
     "«то» лишнее, и перевод слова — «озиратися»"),
    (18911, "example_tr",
     "Geçmişe baktığımda, bunlar mutlu yıllar olmuştur",
     "Geçmişe baktığımda, bunlar mutlu yıllardı",
     "«olmuştur» — не то время"),
    # 10619 gucken — слово ряда написано не так
    (8448, "example_de", "Kuck mal, was ich gefunden habe",
     "Guck mal, was ich gefunden habe",
     "ряд о `gucken`, а в примере «Kuck»"),
    (8448, "example_en", "Look, see what I found",
     "Look what I found",
     "«see» лишнее"),
    (8448, "example_tr", "Bak, bulduğum şeyi gör",
     "Bak, ne buldum",
     "«gör» лишнее"),
    (8448, "example_pl", "Popatrz, co znalazłem w szufladzie",
     "Popatrz, co znalazłem",
     "«w szufladzie» в эталоне нет"),
    # 10620 multipel
    (8449, "example_uk", "У нього множинні травми ноги",
     "У нього множинні проблеми в житті",
     "перевод другого предложения"),
    (8449, "example_pl", "Dostał już wielokrotne ostrzeżenia od szefa",
     "Ma wielokrotne problemy w swoim życiu",
     "перевод другого предложения"),
    # 10622 schmerzhaft
    (13074, "example_tr", "Bu acılı bir hatırası",
     "Bu benim için acı verici bir hatıra",
     "«acılı» о еде, и повис притяжательный"),
    (13074, "example_pl", "To bolesne wspomnienie z dzieciństwa",
     "To dla mnie bolesne wspomnienie",
     "«z dzieciństwa» в эталоне нет, зато потеряно «für mich»"),
    # 10625 Ärgernis — нет такого слова в эталоне
    (11439, "example_de",
     "Das ständige Lärmemachen ist ein Ärgernis für die Nachbarn",
     "Der ständige Lärm ist ein Ärgernis für die Nachbarn",
     "«Lärmemachen» — нет такого слова"),
    # 10626 Präzedenzfall
    (16833, "example_tr", "Bu dava önemli bir emsali olabilir",
     "Bu dava önemli bir emsal olabilir",
     "лишний притяжательный"),
    (16833, "example_pl", "To może być ważny precedens w sądzie",
     "Ta sprawa może być ważnym precedensem",
     "«w sądzie» в эталоне нет"),
    # 10627 anzetteln — потеряно `zu`
    (8450, "example_de", "Er versuchte, einen Streit anzetteln",
     "Er versuchte, einen Streit anzuzetteln",
     "после «versuchen» инфинитив с «zu»"),
    (8450, "example_tr", "Bir uyuşmazlık başlatmaya çalıştı",
     "Bir kavga çıkarmaya çalıştı",
     "«uyuşmazlık» это юридический спор, а `Streit` — ссора"),
    (8450, "example_pl", "Znowu chce wszcząć awanturę w barze",
     "Próbował wszcząć kłótnię",
     "перевод другого предложения"),
    # 10629 Amnestie
    (16834, "example_uk", "Уряд оголосив амністію для політичних засуджених",
     "Уряд оголосив амністію для політичних в'язнів",
     "«Gefangene» это в'язні, а не засуджені"),
    # 10630 Drogerie
    (9930, "example_uk",
     "Я купую зубну пасту в косметичному магазині біля дому",
     "Я купую зубну пасту в магазині побутової хімії за рогом",
     "«um die Ecke» это за рогом, и магазин не косметический"),
    (9930, "example_tr", "Diş macununu köşedeki drogeriden aldım",
     "Diş macunumu köşedeki drogeriden alıyorum",
     "эталон в настоящем времени"),
    # 10631 Magister
    (9612, "example_pl", "Skończył magistra z filozofii",
     "Ukończył studia magisterskie z filozofii",
     "«skończyć magistra» — разговорный обрубок"),
    # 10632 Zeugnis
    (9613, "example_tr", "Öğrenciler yıl sonunda karnelerini aldı",
     "Öğrenciler okul yılı sonunda karnelerini alır",
     "эталон в настоящем, и в нём учебный год"),
    # 10633 Lagune
    (15823, "example_uk", "Венеціанська лагуна гарна",
     "Венеціанська лагуна прекрасна",
     "«wunderschön» это прекрасна, а не просто гарна"),
    # 10634 Sauerkraut
    (11974, "example_uk", "На обід були сосиски з квашеною капустою",
     "На обід була смажена ковбаска з квашеною капустою",
     "`Bratwurst` это жареная колбаска, а не сосиски"),
    (11974, "example_tr", "Öğle yemeğinde sosisli turşu lahana vardı",
     "Öğle yemeğinde lahana turşusuyla sosis vardı",
     "«turşu lahana» — перевёрнутый изафет"),
    (11974, "example_pl", "Do kiełbasy podali kiszoną kapustę",
     "Na obiad była kiełbasa z kiszoną kapustą",
     "перевод другого предложения"),
    # 10635 Schnapsladen — род в эталоне
    (9931, "example_de",
     "Im Schnapsladen um die Ecke kann man gute Wodka kaufen",
     "Im Schnapsladen um die Ecke kann man guten Wodka kaufen",
     "«gute Wodka» — не тот род"),
    (9931, "example_uk",
     "У сусідньому винному магазині можна купити хорошу горілку",
     "У винному магазині за рогом можна купити хорошу горілку",
     "«um die Ecke» это за рогом, а не по соседству"),
    (9931, "example_tr", "Köşedeki içki dükkanından iyi votka alabilirsin",
     "Köşedeki içki dükkânından iyi votka alabilirsin",
     "потерян циркумфлекс, в статье он есть"),
    # 10636 Schärfe
    (8451, "example_pl", "Sprawdź ostrość noża przed krojeniem",
     "Ostrość noża jest ważna przy gotowaniu",
     "перевод другого предложения"),
    # 10637 vereinfachen — порядок слов в эталоне
    (8452, "example_de", "Lass mich das Problem vereinfachen für dich",
     "Lass mich das Problem für dich vereinfachen",
     "глагол в конце, а не перед дополнением"),
    (8452, "example_uk", "Дозволь мені спростити цю проблему",
     "Дозволь мені спростити цю проблему для тебе",
     "потеряно «für dich»"),
    (8452, "example_pl", "Trzeba uprościć te wszystkie formalności",
     "Pozwól mi uprościć dla ciebie ten problem",
     "перевод другого предложения"),
    # 10638 Zehenspitze
    (15297, "example_tr", "O, ayak uçları üzerinde dans etti",
     "Ayak uçlarında dans etti",
     "«O,» и «üzerinde» лишние"),
    # 10639 Automat
    (1204, "example_tr", "Otomattan bir şişe su aldım",
     "Otomat sadece madeni para kabul ediyor",
     "перевод другого предложения"),
    # 10640 amtlich
    (2169, "example_tr", "Bu resmi bir belge",
     "Bu resmî bir belge",
     "в статье «resmî», а в примере без циркумфлекса"),
    # 10643 Terroristin
    (16838, "example_tr", "Terörist dün gece tutuklandı",
     "Kadın terörist tutuklandı",
     "«dün gece» в эталоне нет, зато потерян женский род"),
    # 10644 Geizhals
    (11440, "example_uk",
     "Мій дід — старий скупий, ніколи не витрачає гроші",
     "Мій дід — старий скнара і ніколи не витрачає грошей",
     "«скупий» это прилагательное, а перевод слова — «скнара»"),
    (11440, "example_pl", "Mój dziadek to straszny skąpiec",
     "Mój dziadek to stary skąpiec i nigdy nie wydaje pieniędzy",
     "потеряна вторая половина"),
    # 10646 Fälscher
    (16839, "example_ru",
     "Подделыватель был пойман с поддельными документами",
     "Фальсификатор был пойман с поддельными документами",
     "«подделыватель» — нет такого слова"),
    (16839, "example_uk", "Підробник був спійманий з фальшивими документами",
     "Підробника спіймали з фальшивими документами",
     "тяжёлый пассив там, где эталон его не требует"),
    # 10647 Familiengeschichte
    (15298, "example_en", "The family history is long and complicated",
     "Our family history goes back to the 18th century",
     "перевод другого предложения"),
    (15298, "example_tr", "Aile tarihi uzun ve karmaşık",
     "Aile tarihimiz 18. yüzyıla kadar uzanıyor",
     "перевод другого предложения"),
    (15298, "example_pl", "Babcia opowiada nam historię rodziny",
     "Nasza historia rodziny sięga XVIII wieku",
     "перевод другого предложения"),
    # 10648 Küchenchef
    (11975, "example_pl", "Szef kuchni przygotował coś specjalnego",
     "Szef kuchni przygotowuje najlepsze dania",
     "перевод другого предложения"),
    # 10649 vordringen
    (8453, "example_uk", "Війська просуваються на вороже території",
     "Війська просуваються на ворожу територію",
     "рассогласование падежа"),
    (8453, "example_tr", "Birlikler düşman ülkesine doğru ilerliyor",
     "Birlikler düşman bölgesine ilerliyor",
     "`Gebiet` это область, а не страна"),
    (8453, "example_pl", "Wojska posuwają się naprzód",
     "Wojska posuwają się na terytorium wroga",
     "потеряно «in feindliches Gebiet»"),
    # 10650 erringen — эталон заменили после перевода
    (8454, "example_en", "The team achieved victory at the last moment",
     "She managed to achieve victory after all",
     "перевод остался от прежнего эталона"),
    (8454, "example_uk", "Команда здобула перемогу в останній момент",
     "Їй все ж таки вдалося здобути перемогу",
     "перевод остался от прежнего эталона"),
    (8454, "example_tr", "Takım son anda zafer kazandı",
     "Yine de zaferi elde etmeyi başardı",
     "перевод остался от прежнего эталона"),
    (8454, "example_pl", "W końcu odnieśli zwycięstwo",
     "W końcu udało jej się odnieść zwycięstwo",
     "в эталоне она, а не они"),
    # 10651 indiskret
    (11441, "example_tr", "Bunu söylemesi ağza alınmayacak bir söz oldu",
     "Bunu söylemesi patavatsızlıktı",
     "«ağza alınmayacak» это непристойный, а не бестактный"),
    (11441, "example_pl", "To było niedyskretne pytanie",
     "To było niedyskretne z jej strony, że to powiedziała",
     "перевод другого предложения"),
    # 10652 Unwesen
    (8455, "example_pl", "Plaga kradzieży w okolicy się nasila",
     "Plagę korupcji trzeba zwalczać",
     "перевод другого предложения"),
    # 10655 Repräsentant — эталон заменили после перевода
    (16840, "example_en", "The representatives of various countries met",
     "The country's representative took part in the conference",
     "перевод остался от прежнего эталона"),
    (16840, "example_uk", "Представники різних країн зустрілися",
     "Представник країни взяв участь у конференції",
     "перевод остался от прежнего эталона"),
    (16840, "example_tr", "Çeşitli ülkelerin temsilcileri buluştular",
     "Ülkenin temsilcisi konferansa katıldı",
     "перевод остался от прежнего эталона"),
    # 10656 kastriert
    (13076, "example_tr", "Kısırlaştırılan tom kedi çok daha sakin hale geldi",
     "Kısırlaştırılan erkek kedi çok daha sakin oldu",
     "«tom» — английское слово, оставшееся в турецкой фразе"),
    (13076, "example_pl", "Wykastrowany kot jest spokojniejszy",
     "Wykastrowany kocur stał się znacznie spokojniejszy",
     "эталон в прошедшем времени, и `Kater` это кот-самец"),
    # 10657 Monolog
    (14300, "example_tr", "Oyuncu sahne üzerinde uzun bir monolog yaptı",
     "Oyuncu sahnede uzun bir monolog yaptı",
     "«sahne üzerinde» — калька"),
    # 10658 Vorhersage — дефис в эталоне
    (18076, "example_de",
     "Die Wetter-Vorhersage für das Wochenende ist sehr unsicher",
     "Die Wettervorhersage für das Wochenende ist sehr unsicher",
     "составное слово пишется слитно"),
    (18076, "example_ru", "Прогноз погоды на выходные очень неопределённая",
     "Прогноз погоды на выходные очень неопределённый",
     "рассогласование рода"),
    # 10661 Karpfen
    (15824, "example_tr", "Noel yemeğine geleneksel olarak sazan pişirilir",
     "Noel yemeğinde geleneksel olarak sazan pişirilir",
     "не тот падеж"),
    # 10662 Katheter
    (13077, "example_tr", "Hastaya cerrahiden sonra kateter gerekiyor",
     "Hastaya ameliyattan sonra kateter gerekiyor",
     "«cerrahi» это хирургия как область, а не операция"),
    (13077, "example_pl", "Po operacji pacjent ma cewnik",
     "Pacjent potrzebuje cewnika po operacji",
     "в эталоне «benötigt», а не «имеет»"),
    # 10663 bereinigen
    (8457, "example_uk", "Усі спірні питання вже врегульовано",
     "Після врегульованого конфлікту ситуація стала набагато кращою",
     "перевод другого предложения"),
    (8457, "example_pl", "Musimy uregulować te zaległe sprawy",
     "Po uregulowaniu konfliktu sytuacja była znacznie lepsza",
     "перевод другого предложения"),
    # 10664 Insassin
    (16841, "example_en", "The female inmate was released from prison",
     "The female inmate of the prison is now free",
     "эталон в настоящем, и там «frei», а не «released»"),
    (16841, "example_ru", "Заключённая освобождена из тюрьмы",
     "Заключённая теперь на свободе",
     "эталон в настоящем времени"),
    (16841, "example_uk", "Ув'язнена була звільнена з в'язниці",
     "Ув'язнена тепер на волі",
     "эталон в настоящем времени"),
    (16841, "example_tr", "Mahpus kadın artık hapishaneden özgür",
     "Hapishanedeki kadın mahkûm artık özgür",
     "«hapishaneden özgür» — не то управление"),
    # 10665 Versteckspiel
    (12374, "example_uk", "Діти грають у хованку в саду",
     "Діти грають у хованки в саду",
     "игра называется «хованки», во множественном"),
    # 10666 Sketch
    (14776, "example_en", "The comedy sketch was very funny",
     "The sketch was very funny",
     "«comedy» в эталоне нет"),
    (14776, "example_uk", "Комедійний скетч був дуже смішним",
     "Скетч був дуже смішним",
     "«комедійний» в эталоне нет"),
    (14776, "example_tr", "Komedi skeçi çok komikti",
     "Skeç çok komikti",
     "«komedi» в эталоне нет"),
    # 10668 anbrennen
    (11976, "example_en", "The toast burned in the toaster",
     "Watch out, the soup must not burn",
     "перевод другого предложения"),
    (11976, "example_uk", "Їжа підгоріла, тому що я не стежив",
     "Обережно, суп не повинен підгоріти",
     "перевод другого предложения"),
    (11976, "example_tr", "Dikkat etmediğim için yemek yandı",
     "Dikkat et, çorba dibi tutmasın",
     "перевод другого предложения"),
    (11976, "example_pl", "Uważaj żeby zupa się nie przypaliła",
     "Uważaj, żeby zupa się nie przypaliła",
     "нет запятой перед «żeby»"),
    # 10669 Rückenmark
    (13078, "example_pl", "Uraz rdzenia kręgowego jest bardzo groźny",
     "Uraz rdzenia kręgowego może mieć poważne następstwa",
     "перевод другого предложения"),
    # 10670 Spielzug
    (12375, "example_tr", "Bu satrançta akıllıca bir hamledir",
     "Bu, satrançta akıllıca bir hamleydi",
     "эталон в прошедшем времени"),
    # 10672 ausgelaugt
    (11442, "example_tr", "Uzun yürüyüşten sonra tamamen tüketildim",
     "Uzun yürüyüşten sonra tamamen bitkindim",
     "«tüketildim» значит «меня израсходовали»"),
    (11442, "example_pl", "Po całym dniu w pracy jestem wyczerpany",
     "Po długiej wędrówce byłem całkowicie wyczerpany",
     "перевод другого предложения"),
    # 10673 verworfen
    (11443, "example_uk", "Його відкинуті плани могли б привести до проблем",
     "Його відкинуті плани могли б призвести до проблем",
     "«привести до» — калька"),
    (11443, "example_tr",
     "Onun başıboş düşünceleri onu zor dönemlere yöneltti",
     "Reddedilen planları sorunlara yol açardı",
     "перевод совсем другого предложения"),
    (11443, "example_pl", "Jego pomysł został odrzucony przez szefa",
     "Jego odrzucone plany doprowadziłyby do problemów",
     "перевод другого предложения"),
    # 10675 einschränken
    (8459, "example_pl", "Muszę ograniczyć słodycze i kawę",
     "Lekarz musi ograniczyć swoje aktywności",
     "перевод другого предложения"),
    # 10676 Spielschulden
    (9933, "example_en", "His gambling debts have become very high",
     "His gambling debts are very high",
     "эталон в настоящем времени"),
    (9933, "example_uk", "Його гральні борги стали дуже високими",
     "Його гральні борги дуже високі",
     "эталон в настоящем времени"),
    (9933, "example_tr", "Kumar borçlarını bir türlü ödeyemedi",
     "Kumar borçları çok yüksek",
     "перевод другого предложения"),
    # 10677 schnauben
    (8460, "example_uk", "Бик гарчить гнівно перед атакою",
     "Бик гнівно фиркає, перш ніж напасти",
     "«гарчить» о собаке, а перевод слова — «фиркати»"),
    (8460, "example_tr", "Boğa öfkeyle burnundan soluyordu",
     "Boğa saldırmadan önce öfkeyle burnundan soluyor",
     "эталон в настоящем, и потеряна вторая половина"),
    (8460, "example_pl", "Koń parsknął i ruszył z miejsca",
     "Byk parska wściekle, zanim zaatakuje",
     "перевод другого предложения"),
    # 10678 ironischerweise
    (8461, "example_uk", "Іронічно, саме поліцейський порушив правило",
     "За іронією долі, саме поліцейський порушив правило",
     "перевод слова — «за іронією долі»"),
    (8461, "example_pl", "Jak na ironię to policjant złamał przepisy",
     "Jak na ironię, to właśnie policjant złamał przepis",
     "нет запятой, и правило в эталоне одно"),
    # 10679 Polizeischule
    (9614, "example_uk", "Після атестату він подає заявку в поліцейську школу",
     "Після закінчення школи він подає заяву до поліцейської школи",
     "«після атестату» — не по-украински"),
    (9614, "example_tr", "Lise bitirdikten sonra polis okuluna başvuruyor",
     "Liseyi bitirdikten sonra polis okuluna başvuruyor",
     "потерян аккузатив"),
    # 10680 Vormarsch
    (8462, "example_pl", "Nowa moda jest w natarciu",
     "Marszu techniki nie da się zatrzymać",
     "перевод другого предложения"),
    # 10681 Landeerlaubnis
    (17367, "example_ru", "Самолёт ждёт разрешение на посадку от аэропорта",
     "Самолёт ждёт разрешения на посадку от аэропорта",
     "«ждёт» требует родительного"),
    (17367, "example_uk", "Літак чекає дозвіл на посадку від аеропорту",
     "Літак чекає на дозвіл на посадку від аеропорту",
     "«чекати» требует «на»"),
    # 10682 vorbehalten
    (8463, "example_uk", "Усі умови залишаються за роботодавцем",
     "Умови залишаються за роботодавцем",
     "«усі» в эталоне нет"),
    (8463, "example_tr", "Şartlar işverene ait kalmaktadır",
     "Şartlar işverene saklı tutulmaktadır",
     "«ait kalmak» — не выражение"),
    (8463, "example_pl", "Zastrzegamy sobie prawo do zmian",
     "Warunki pozostają zastrzeżone dla pracodawcy",
     "перевод другого предложения"),
    # 10683 egoistisch
    (11444, "example_pl", "Nie bądź taki egoistyczny wobec rodziny",
     "Jego egoistyczne decyzje zaszkodziły grupie",
     "перевод другого предложения"),
    # 10684 erheblich
    (8464, "example_pl", "To znaczna różnica w cenie",
     "Projekt powoduje znaczne koszty",
     "перевод другого предложения"),
    # 10685 anregend
    (11445, "example_tr", "Tartışma çok uyarıcı ve ilginçti",
     "Tartışma çok ilham verici ve ilginçti",
     "«uyarıcı» это возбуждающее средство или предупреждение"),
    (11445, "example_pl", "Rozmowa z nim była bardzo inspirująca",
     "Dyskusja była bardzo inspirująca i interesująca",
     "перевод другого предложения"),
    # 10687 zugegen
    (8465, "example_tr", "Kardeşin partide miydi?",
     "Kardeşin partide hazır bulundu mu?",
     "потеряно слово ряда"),
    # 10688 Eingangshalle
    (18456, "example_ru", "Входной холл музея очень впечатляющий",
     "Вестибюль музея очень впечатляет",
     "«входной холл» — калька, перевод слова — «вестибюль»"),
    (18456, "example_uk", "Вхідна зала музею дуже вражаюча",
     "Вестибюль музею дуже вражає",
     "«вхідна зала» — калька, перевод слова — «вестибюль»"),
    # 10690 Anlass
    (18912, "example_en", "For various occasions, he wears a suit",
     "For various occasions, you wear a suit",
     "в эталоне «du», а не «он»"),
    (18912, "example_ru", "К разным поводам он надевает костюм",
     "По разным поводам ты надеваешь костюм",
     "«к поводам» — не то управление, и в эталоне «du»"),
    (18912, "example_uk", "У нього завжди знайдуться приводи для свята",
     "З різних нагод ти вдягаєш костюм",
     "перевод другого предложения"),
    (18912, "example_tr", "Çeşitli fırsatlarda bir takım giyiyor",
     "Çeşitli vesilelerde takım elbise giyersin",
     "в эталоне «du», и «takım» без «elbise» это команда"),
    # 10691 Bedenkzeit
    (18913, "example_uk", "Дай мені 48 годин на роздум",
     "Дай мені 48 годин на роздуми",
     "«на роздум» — не та форма"),
    # 10692 Petroleum
    (17719, "translation_uk", "гас, керосин",
     "гас, лампова олія",
     "«керосин» — русское слово"),
    (17719, "example_uk", "Керосин використовується для опалення",
     "Гас використовується для опалення",
     "«керосин» — русское слово"),
    (17719, "example_tr", "Lamba gazyağıyla yanıyor",
     "Gazyağı ısıtmak için kullanılır",
     "перевод другого предложения"),
    # 10694 splitternackt
    (13766, "example_uk", "Малий бігав по хаті зовсім голий",
     "Він стояв зовсім голий у саду",
     "перевод другого предложения"),
    # 10695 Trampel
    (11446, "example_uk", "Він такий незграбний, завжди усе роняє",
     "Він такий незграба, завжди неповороткий",
     "ряд о существительном, и «роняє» — русское слово"),
    (11446, "example_pl", "Ale z ciebie niezdara, znowu coś zbiłeś",
     "Jest takim niezdarą, zawsze nieporadny",
     "перевод другого предложения"),
    # 10696 Harpune
    (12376, "example_uk", "Полювальник на китів кинув гарпун на кита",
     "Китобій кинув гарпун у кита",
     "«полювальник» — нет такого слова, и «на кита» — не то управление"),
    (12376, "example_tr", "Balina avı yapan kişi balinaya arpun attı",
     "Balina avcısı balinaya zıpkın attı",
     "«arpun» — нет такого слова, в статье «zıpkın»"),
    # 10697 versteinert
    (11447, "example_pl", "Jego twarz była skamieniała z przerażenia",
     "Jego twarz była skamieniała z szoku",
     "в эталоне «Schock», а не ужас"),
    # 10698 Genialität
    (11448, "example_uk", "Генійність його винаходу дивовижна",
     "Геніальність його винаходу справді вражає",
     "«генійність» — нет такого слова"),
    (11448, "example_pl", "Genialność tego pomysłu widać od razu",
     "Genialność jego wynalazku jest naprawdę imponująca",
     "перевод другого предложения"),
    # 10699 Jurastudium
    (9615, "example_uk", "Він проходить юридичну освіту в університеті",
     "Він здобуває юридичну освіту в університеті",
     "«проходити освіту» — калька"),
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
