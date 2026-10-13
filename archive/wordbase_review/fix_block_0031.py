"""
Сплошная вычитка, блок 31: ряды 4501–4700 по рангу частотности
(id первого 7269, id последнего 16274).

Главное за блок:

* `Luder` — ряд, где четыре языка из пяти переводят четыре разные чужие
  фразы. Немецкий «Dieses Luder hat ihn belogen», английский про
  стервятников над падалью, украинский «Приманка привертає рибу»
  (приманка привлекает рыбу), турецкий «не называй девушку шлюхой»,
  польский «не называй её шлюхой». Совпал только русский.
* `Metro`, `Scham`, `Fassung`, `einzeln`, `vorwerfen`, `hinsehen`,
  `rumhängen` — то же, но в меньшем масштабе. У `Metro` русский и
  украинский ещё и приписали себе города: «Метро в Москве», «Метро в
  Києві».
* `Fassung` — турецкий сказал ровно наоборот: `soğukkanlılığını
  kaybetmedi` значит «не потерял самообладания», а в немецком потерял.
* Польская «parka» — это куртка, а не парочка. В значениях и в примере.
* `Der Mythos der Atlantis` и `von einem Psychopath` — немецкий эталон
  с неверным падежом.
* Турецкие небывальщины: `pale` на месте `kürek`, `kuşçuk`, `başa bela`,
  `korku duşüyorum`, `alkış çalıyor`, `Otlakta ki`.

    python -m app.scripts.fix_block_0031            # показать
    python -m app.scripts.fix_block_0031 --apply    # применить
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
    (14508, "example_de", "Der Mythos der Atlantis fasziniert viele Menschen",
     "Der Mythos von Atlantis fasziniert viele Menschen",
     "«der Atlantis» — неверный падеж"),
    (12658, "example_de", "Der Film handelt von einem Psychopath",
     "Der Film handelt von einem Psychopathen",
     "слабое склонение: «von einem Psychopathen»"),

    # --- Luder: четыре языка переводят четыре разные фразы -------------------
    (10605, "example_en", "Vultures were circling above the carrion",
     "This hussy lied to him",
     "немецкий «Dieses Luder hat ihn belogen»"),
    (10605, "example_uk", "Приманка привертає рибу",
     "Ця шльондра йому збрехала", "то же"),
    (10605, "example_tr", "Kıza kaltak deme, çok ayıp",
     "Bu kaltak ona yalan söyledi", "то же"),
    (10605, "example_pl", "Nie nazywaj jej dziwką",
     "Ta dziwka go okłamała", "то же"),

    # --- Metro: с приписанными городами --------------------------------------
    (17171, "example_en", "The subway is faster than the car",
     "We take the metro to the station",
     "немецкий «Wir nehmen die Metro bis zum Bahnhof»"),
    (17171, "example_ru", "Метро в Москве быстрее, чем ездить на машине",
     "Мы едем на метро до вокзала", "то же, и Москва приписана"),
    (17171, "example_uk", "Метро в Києві швидше, ніж їхати на машині",
     "Ми їдемо на метро до вокзалу", "то же, и Киев приписан"),
    (17171, "example_tr", "Metro arabadan daha hızlı",
     "Gara kadar metroya biniyoruz", "то же"),

    # --- Scham ---------------------------------------------------------------
    (10593, "example_en", "I feel shame for my behavior",
     "She turned red with shame",
     "немецкий «Sie wurde rot vor Scham»"),
    (10593, "example_uk", "Мені сором за свою поведінку",
     "Вона почервоніла від сорому", "то же"),
    (10593, "example_tr", "Davranışım için utanç duyuyorum",
     "Utançtan yüzü kızardı", "то же"),
    (10593, "example_pl", "Poczułem wstyd za swoje zachowanie",
     "Zaczerwieniła się ze wstydu", "то же"),

    # --- Fassung, где турецкий сказал наоборот -------------------------------
    (10602, "example_en", "She lost her composure completely",
     "The news threw me off balance",
     "немецкий «Die Nachricht hat mich aus der Fassung gebracht»"),
    (10602, "example_uk", "Він швидко втратив самовладання",
     "Ця новина позбавила мене самовладання", "то же"),
    (10602, "example_tr", "Kazadan sonra bile soğukkanlılığını kaybetmedi",
     "Haber beni soğukkanlılığımdan çıkardı",
     "«kaybetmedi» — не потерял; в немецком наоборот"),
    (10602, "example_pl", "Stracił opanowanie i zaczął krzyczeć",
     "Ta wiadomość wyprowadziła mnie z równowagi", "то же"),

    # --- einzeln -------------------------------------------------------------
    (7291, "example_en", "I want a room with a single bed",
     "Each glass is packed individually",
     "немецкий «Jedes Glas wird einzeln verpackt»"),
    (7291, "example_uk", "Я хочу номер з одиночним ліжком",
     "Кожна склянка пакується окремо", "то же"),
    (7291, "example_tr", "Tek yataklı bir oda istiyorum",
     "Her bardak tek tek paketleniyor", "то же"),

    # --- vorwerfen, hinsehen, rumhängen --------------------------------------
    (10603, "example_en", "Don't reproach me for being late",
     "No one can reproach you for that",
     "немецкий «Das kann dir niemand vorwerfen»"),
    (10603, "example_uk", "Ти мені завжди докоряєш, що я запізнююся",
     "Ніхто не може тобі цього докорити", "то же"),
    (10603, "example_tr", "Beni hep geç kalmakla suçluyorsun",
     "Bunu kimse sana yükleyemez", "то же"),
    (7295, "example_en", "Can you take a look? Something's not right here",
     "I couldn't even look",
     "немецкий «Ich konnte gar nicht hinsehen»"),
    (7295, "example_uk", "Можеш подивитися? Щось тут не так",
     "Я взагалі не міг туди дивитися", "то же"),
    (7295, "example_tr", "Bir bakabilir misin? Burada bir şey yanlış",
     "O tarafa hiç bakamadım", "то же"),
    (12209, "example_en", "The guys hang around the park all day",
     "We just want to hang around at home today",
     "немецкий «Wir wollen heute nur zu Hause rumhängen»"),
    (12209, "example_uk", "Хлопці весь день мотаються в парку",
     "Сьогодні ми хочемо просто валятися вдома", "то же"),
    (12209, "example_tr", "Erkekler bütün gün parkta dolaşıyor",
     "Bugün sadece evde takılmak istiyoruz", "то же"),

    # --- польская «parka» ----------------------------------------------------
    (15068, "translation_pl", "parka, para", "para, zakochana para",
     "«parka» по-польски — куртка"),
    (15068, "example_pl", "Ta parka siedzi w parku i trzyma się za ręce",
     "Ta para siedzi w parku i trzyma się za ręce", "то же"),

    # --- украинские опечатки и русизмы ---------------------------------------
    (7269, "translation_uk", "уникати, стороннитися", "уникати, сторонитися",
     "«стороннитися» — лишняя «н»"),
    (7269, "example_uk", "Я уникаю головної дороги, там багато затору",
     "Я уникаю головної дороги, бо там великий рух",
     "«багато затору» — так не говорят"),
    (14504, "translation_uk", "полотно, екран, холст",
     "полотно, екран, канва", "«холст» — русское слово"),
    (12653, "example_uk", "Мені потрібно глибоко дихати й заспокоїтися",
     "Мені потрібно перевести дух і заспокоїтися",
     "«durchatmen» — перевести дух, а не дышать глубоко"),
    (16257, "example_uk", "В'язень сидить у тюрмі п'ять років",
     "В'язень сидить у в'язниці п'ять років", "«тюрма» — русизм"),
    (8913, "translation_uk", "страйк, забастовка",
     "страйк, припинення роботи", "«забастовка» — русское слово"),
    (8914, "example_uk", "Він був відстранений до завершення розслідування",
     "Він був відсторонений до завершення розслідування",
     "«відстранений» — русизм"),
    (17956, "example_uk", "Вчені припускають про червоточини у всесвіті",
     "Вчені міркують про червоточини у всесвіті",
     "«припускають про» — так не говорят"),
    (3035, "example_uk", "Я вмію чарувати", "Я вмію чаклувати",
     "в значениях «чаклувати»"),
    (1572, "example_uk", "Молодь збирається тут", "Підлітки збираються тут",
     "в значениях «підліток»"),
    (8916, "example_uk", "Обережно, тут будівельний майданчик!",
     "Будівельний майданчик перекриває весь рух",
     "немецкий «Die Baustelle blockiert den ganzen Verkehr»"),
    (14050, "example_uk", "Мені потрібна письмова підтвердка",
     "Мені потрібне письмове підтвердження", "«підтвердка» — не слово"),
    (15074, "example_uk", "Героїня історії врятовує своє село",
     "Героїня історії рятує своє село", "«врятовує» — не форма"),
    (18241, "example_uk", "Двері заперта", "Двері замкнені",
     "число и род не согласованы"),
    (7287, "example_uk", "Ми отримуємо нашу меблі від цього виробника",
     "Ми отримуємо наші меблі від цього виробника",
     "«меблі» множественного числа"),
    (2046, "example_uk", "Агентство посередничає квартири",
     "Агентство допомагає знайти квартиру",
     "«посередничає квартири» — так не говорят"),
    (8923, "example_uk", "Домогосподарка дбає про весь дім",
     "Домробітниця дбає про весь дім",
     "«домогосподарка» — хозяйка дома, не прислуга"),
    (14054, "example_uk", "Яка твоя прохання? Просто скажи",
     "Яке твоє прохання? Просто скажи", "род не согласован"),
    (10600, "example_uk", "Я впевнений, що ми це разом пережимемо",
     "Я впевнений, що ми це разом переживемо", "«пережимемо» — не форма"),
    (10601, "example_uk", "Я віддаю перевагу кавам замість чаю",
     "Я віддаю перевагу каві, а не чаю", "«кавам» — не форма"),
    (15076, "example_uk", "Можеш зайти сьогодні вечором?",
     "Можеш зайти сьогодні ввечері?", "«вечором» — русизм"),
    (14055, "example_uk", "Я сповіщу тебе, як тільки приду",
     "Я сповіщу тебе, як тільки прийду", "«приду» — русская форма"),
    (10607, "translation_uk", "докір, обвинення, закид",
     "докір, обвинувачення, закид", "«обвинення» — обрывок"),
    (10607, "example_uk", "Це несправедливе звинувачення",
     "Це несправедливий докір", "в значениях первое «докір»"),
    (12662, "example_uk", "Після аварії він впав у непритомність",
     "Після аварії він знепритомнів", "«впав у непритомність» — калька"),
    (16264, "example_uk", "Адміністрація схвалила заявку",
     "Адміністрація схвалює заявку", "в немецком настоящее время"),
    (16262, "example_uk", "Знищення було повним",
     "Знищення міста було повним", "потерян город"),
    (16261, "example_uk", "Захисник обвинуваченого був дуже умілий",
     "Захисник був дуже умілий", "подсудимый приписан"),
    (10587, "example_uk", "Жадна людина хотіла все більше й більше",
     "Цей тип жадібний, він хоче все більше й більше",
     "немецкий «Der Typ ist gierig»"),
    (12207, "example_uk", "Мій брат — скаут і любить походи",
     "Скаут допомагає іншим людям",
     "немецкий «Der Pfadfinder hilft anderen Menschen»"),
    (1234, "example_uk", "Я оплачую рахунки через інтернет",
     "Я хочу оплатити рахунок",
     "немецкий «Ich möchte die Rechnung begleichen»"),
    (1675, "example_uk", "Мені потрібен масаж",
     "Мені потрібен масаж від болю в спині", "потеряна спина"),
    (8921, "example_uk", "Чиновник при міській раді був дуже доступним",
     "Чиновник у ратуші був дуже корисним", "«доступним» — не то слово"),
    (377, "example_uk", "Я загубив одну рукавичку", "Я ношу рукавички",
     "немецкий «Ich trage Handschuhe»"),
    (2843, "example_uk", "Стадіон був переповнений",
     "Стадіон зовсім повний", "в немецком настоящее время"),

    # --- русские ------------------------------------------------------------
    (16271, "example_ru", "Воин бросает своё копье",
     "Воин бросает своё копьё", "потеряна «ё»"),
    (2382, "translation_ru",
     "вставлять, делать перерыв, маринавать, подавать жалобу",
     "вставлять, делать перерыв, маринировать, подавать жалобу",
     "«маринавать» — опечатка"),
    (2184, "translation_ru",
     "включать, заигрывать приставать, заправлять салат",
     "включать, заигрывать, приставать, заправлять салат",
     "пропущена запятая"),
    (18750, "example_ru",
     "На Канун Нового года мы всегда устраиваем вечеринку",
     "В канун Нового года мы всегда устраиваем вечеринку",
     "заглавная буква посреди фразы"),
    (16261, "example_ru", "Защитник подсудимого был очень умелым",
     "Защитник был очень умелым", "подсудимый приписан"),
    (16262, "example_ru", "Уничтожение было полным",
     "Уничтожение города было полным", "потерян город"),
    (18748, "example_ru", "Не буди ребёнка, он спит",
     "Я разбужу тебя завтра",
     "немецкий «Ich wecke dich morgen auf»"),
    (16263, "example_ru", "Я готов свидетельствовать в суде",
     "Я могу это подтвердить, я был там",
     "немецкий «Ich kann das bezeugen, ich war dabei»"),
    (16266, "example_ru", "Политика нельзя подкупить",
     "Политик не дал себя подкупить",
     "немецкий «Der Politiker ließ sich nicht bestechen»"),
    (1500, "example_ru", "Гриль уже горячий", "Гриль горячий",
     "«уже» приписано"),
    (3009, "example_ru", "Чем я могу тебе помочь?",
     "Могу я тебе помочь?", "в немецком вопрос «да или нет»"),

    # --- турецкие небывальщины и падежи --------------------------------------
    (18237, "example_tr", "Karı temizlemek için bir paleye ihtiyacım var",
     "Karı temizlemek için bir küreğe ihtiyacım var",
     "«pale» — лопасть, не лопата"),
    (15543, "translation_tr", "kuşçuk, minik kuş", "minik kuş, küçük kuş",
     "«kuşçuk» — не турецкое слово"),
    (15543, "example_tr", "Küçük kuşçuk çok tatlı şarkı söylüyor",
     "Küçük kuş çok tatlı şarkı söylüyor", "то же"),
    (7296, "example_tr", "Bu sivrisinekler bu yaz gerçek bir başa bela",
     "Bu sivrisinekler bu yaz gerçek bir baş belası",
     "«başa bela» — не форма"),
    (10606, "example_tr", "Sınavdan korku duşüyorum",
     "Sınavdan korku duyuyorum", "«duşüyorum» — опечатка"),
    (14512, "example_tr", "Seyirciler yüksek sesle alkış çalıyor",
     "Seyirciler yüksek sesle alkışlıyor", "«alkış çalmak» — не форма"),
    (15545, "example_tr", "Otlakta ki boğa çok vahşi görünüyor",
     "Otlaktaki boğa çok vahşi görünüyor", "«-ki» пишется слитно"),
    (7269, "example_tr", "Ana caddeyi kaçınıyorum çünkü orada çok trafik var",
     "Ana caddeden kaçınıyorum çünkü orada çok trafik var",
     "«kaçınmak» требует исходного падежа"),
    (16263, "example_tr", "Bunu şahitlik edebilirim, oradaydım",
     "Buna şahitlik edebilirim, oradaydım",
     "«şahitlik etmek» требует дательного"),
    (7282, "example_tr", "Numaraları değiş tokuş ediyoruz",
     "Numaralarımızı değiş tokuş ediyoruz", "потеряно «наши»"),
    (16270, "example_tr", "Hırsızlar her akşam turist soyuyorlar",
     "Hırsızlar her akşam turistleri soyuyor", "пропущен винительный"),
    (10600, "example_tr", "Bunun atlatacağımızdan eminim",
     "Bunu atlatacağımızdan eminim", "неверный падеж"),
    (16256, "example_tr", "Kod grubumuzda davranışı düzenliyor",
     "Kural bütünü grubumuzdaki davranışı düzenliyor",
     "«Kod» — программный код"),
    (10582, "example_tr", "Şehirde uyanık kalmalısın",
     "Şehirde tetikte kalmalısın", "«uyanık» — не спящий"),
    (12204, "example_tr", "Yüzme alanında altın madalya kazandı",
     "Yüzmede altın madalya kazandı", "«alanında» лишнее"),
    (11745, "example_tr",
     "Sucuğumun üzerine hardal koymaktan hoşlanıyorum",
     "Sosisimin üzerinde hardal severim", "фраза перегружена"),
    (17169, "example_tr",
     "Demir yolu daha önce ana ulaştırma aracı idi",
     "Demiryolu eskiden ana ulaşım aracıydı",
     "«Demir yolu» пишется слитно, и «idi»"),
    (10585, "example_tr",
     "Çok kendini beğenmiş ve kendini herkesten daha iyi düşünüyor",
     "Çok kendini beğenmiş ve kendini herkesten iyi sanıyor",
     "«daha iyi düşünüyor» — фраза не собрана"),
    (8916, "example_tr", "İnşaat alanı tüm trafiği engelledi",
     "İnşaat alanı tüm trafiği engelliyor", "в немецком настоящее время"),
    (15070, "example_tr", "Üvey babam çok iyi bir insandır",
     "Üvey babam çok iyi bir insan", "«-dır»"),
    (9501, "example_tr",
     "Kardeşim yakınlarda bir pansiyon okuluna gidiyor",
     "Kardeşim yakında bir yatılı okula gidiyor",
     "«pansiyon okulu» — не по-турецки"),
    (16268, "example_tr", "Bu kulübün üyesi olmak bir ayrıcalıktır",
     "Bu kulübün üyesi olmak bir ayrıcalık", "«-tır»"),
    (12208, "example_tr", "Spor sağlıklı bir aktivitedir",
     "Spor sağlıklı bir aktivite", "то же"),
    (14056, "example_tr", "Bir şirketin imajı çok önemlidir",
     "Bir şirketin imajı çok önemli", "то же"),
    (7290, "example_tr", "Sinemalara gidebiliriz, şartıyla zamanın varsa",
     "Zamanın varsa sinemaya gidebiliriz", "порядок слов сломан"),
    (10598, "example_tr", "Çocuk düştükten sonra ağlıyor",
     "Çocuk düştükten sonra hıçkırarak ağlıyor",
     "«schluchzen» — рыдать, а не просто плакать"),
    (1927, "example_tr", "Tango yapıyoruz", "Tango dansı yapıyoruz",
     "«tango yapmak» — так не говорят"),
    (2140, "example_tr", "Kalkış saat 10da", "Kalkış saat 10'da",
     "пропущен апостроф"),
    (8923, "example_tr", "Ev hizmetçisi bütün odaları temizledi",
     "Ev hizmetçisi bütün eve bakıyor",
     "немецкий «kümmert sich um das ganze Haus»"),
    (10591, "example_tr", "Seni sinir etmek istemiyorum",
     "Seni sinirlendirmek istemiyorum", "«sinir etmek» — не форма"),
    (16265, "example_tr", "Meşru müdafaa için hareket etti",
     "Meşru müdafaada bulundu", "«için» тут не к месту"),
    (17556, "example_tr", "Sunucu kapandı", "Sunucu çöktü",
     "«ausgefallen» — вышел из строя"),
    (16262, "example_tr", "Yok etme tamamen idi",
     "Şehir tamamen yok edildi", "фраза не собрана"),
    (2843, "example_tr", "Stadyum tamamen doluydu",
     "Stadyum tamamen dolu", "в немецком настоящее время"),
    (231, "example_tr", "Soğuk algınlığı var", "Onun soğuk algınlığı var",
     "потеряно подлежащее"),
    (18748, "example_tr", "Seni yarın uyandırmam gerekiyor",
     "Seni yarın uyandıracağım", "«gerekiyor» приписано"),
    (1134, "example_tr", "O her zaman övünüyor",
     "Burada adresini belirtmen gerekiyor",
     "немецкий «Du musst hier deine Adresse angeben»"),
    (9503, "example_tr", "Öğrenci derste oturuyor",
     "Kız öğrenci derste oturuyor", "в немецком женский род"),
    (7286, "example_tr", "Onu ikna etmeye çalışmak amaçsız",
     "Onu ikna etmeye çalışmak boşuna", "«amaçsız» — бесцельный"),
    (12663, "example_tr", "Kazadan sonra beyin sarsıntısı oldu",
     "Kazadan sonra beyin sarsıntısı geçirdi", "«oldu» — не та форма"),
    (11751, "example_tr", "Yeşil zeytinleri yemek severim",
     "Yeşil zeytin yemeyi severim", "лишний определённый падеж"),
    (10604, "translation_tr", "İronik, alaycı", "ironik, alaycı",
     "заглавная буква посреди значений"),
    (14509, "example_tr", "O, harika keman çalıyor",
     "Harika keman çalıyor", "лишнее «O»"),
    (13527, "example_tr", "Yine geç kaldın!", "Bu da başka bir sorun",
     "немецкий «Das ist wiederum ein anderes Problem»"),
    (16266, "example_tr", "Politikacı rüşvet almadı",
     "Politikacı rüşvete yenik düşmedi",
     "«rüşvet almadı» — не брал, а в немецком не поддался"),
    (12655, "example_tr", "Haberi duyunca histeri yaptı",
     "Haberi duyunca histerik oldu", "«histeri yaptı» — разговорное"),

    # --- перевод переводит другую фразу (остальное) --------------------------
    (10587, "example_tr", "Açgözlü adam her zaman daha fazlasını istedi",
     "Adam açgözlü, her zaman daha fazlasını istiyor",
     "немецкий в настоящем времени"),
    (10587, "example_en", "The greedy man always wanted more",
     "The guy is greedy, he always wants more", "то же"),
    (10587, "example_pl", "Nie bądź taki chciwy!",
     "Ten typ jest chciwy, zawsze chce więcej", "то же"),
    (16262, "example_en", "The destruction was total",
     "The destruction of the city was total", "потерян город"),
    (2843, "example_en", "The stadium was completely full",
     "The stadium is completely full", "в немецком настоящее время"),
    (231, "example_pl", "Mam przeziębienie i boli mnie gardło",
     "Ona ma przeziębienie", "немецкий «Sie hat eine Erkältung»"),
    (12206, "example_pl", "Musisz biegać po domu w piżamie?",
     "Musisz paradować w piżamie?", "дом приписан"),
    (1134, "example_en", "He always brags",
     "You must state your address here",
     "немецкий «Du musst hier deine Adresse angeben»"),
    (1134, "example_uk", "Зазнач у формі своє прізвище",
     "Тут ти повинен вказати свою адресу", "то же"),
    (17173, "example_uk", "Пасажир входить до літака",
     "Пасажир сідає в літак", "«входить до» — не говорят"),
    (16264, "example_en", "The administration approved the application",
     "The administration approves the application",
     "в немецком настоящее время"),
    (16264, "example_tr", "Yönetim başvuruyu onayladı",
     "Yönetim başvuruyu onaylıyor", "то же"),
    (10592, "example_pl", "Ta historia jest naprawdę tajemnicza",
     "To tajemnicza historia", "«naprawdę» приписано"),
    (392, "example_en", "The heating works", "The heating works well",
     "потеряно «gut»"),
    (392, "example_uk", "Опалення працює", "Опалення працює добре", "то же"),
    (392, "example_tr", "Kalorifer çalışıyor", "Kalorifer iyi çalışıyor",
     "то же"),
    (7278, "example_en", "Leave things as they are",
     "I leave things as they are", "в немецком «я оставляю»"),
    (7278, "example_uk", "Залиш все як є", "Я залишаю все як є", "то же"),
    (1429, "example_en", "He's flirting with her",
     "He's flirting with her all evening", "потерян вечер"),
    (1429, "example_uk", "Він фліртує з нею",
     "Він цілий вечір фліртує з нею", "то же"),
    (1429, "example_tr", "Onunla flört ediyor",
     "Bütün akşam onunla flört ediyor", "то же"),
    (2317, "example_en", "The civil war lasted for years",
     "The civil war lasted several years", "«mehrere Jahre» — несколько"),
    (2317, "example_uk", "Громадянська війна тривала роками",
     "Громадянська війна тривала кілька років", "то же"),
    (2317, "example_tr", "İç savaş yıllarca sürdü",
     "İç savaş birkaç yıl sürdü", "то же"),
    (17168, "example_en", "My son always sits in the back seat of the car",
     "The children sit in the back seat",
     "немецкий «Die Kinder sitzen auf dem Rücksitz»"),
    (17168, "example_ru", "Мой сын всегда сидит на заднем сиденье в машине",
     "Дети сидят на заднем сиденье", "то же"),
    (17168, "example_uk",
     "Мій син завжди сидить на задньому сидінні в машині",
     "Діти сидять на задньому сидінні", "то же"),
    (17168, "example_tr", "Oğlum her zaman arabada arka koltuğa oturuyor",
     "Çocuklar arka koltukta oturuyor", "то же"),
    (10584, "example_en", "That's just cheekiness, how he talks to you",
     "It's such a cheek, the way he talks to you", "фраза не собрана"),
    (10595, "example_pl", "Musisz odpowiadać za swoje decyzje",
     "Szef musi odpowiadać za tę decyzję",
     "немецкий «Der Chef muss die Entscheidung verantworten»"),
    (1675, "example_tr", "Bir masaja ihtiyacım var",
     "Sırt ağrım için masaja ihtiyacım var", "потеряна спина"),
    (14514, "example_pl", "W horrorze w zamku pojawia się fantom",
     "W horrorze w zamku pojawia się widmo",
     "«fantom» по-польски — манекен"),
    (10597, "example_pl", "Zejdź na dół na kolację",
     "Po stresie potrzebowałem czasu, żeby się wyluzować",
     "немецкий «Nach dem Stress brauchte ich Zeit, um runterzukommen»"),
    (377, "example_en", "He wears gloves", "I wear gloves",
     "в немецком «я»"),
    (377, "example_tr", "Eldiven giyiyor", "Eldiven takıyorum", "то же"),
    (12661, "example_pl", "Zapomniałem szczoteczki do zębów",
     "Myję zęby swoją szczoteczką",
     "немецкий «Ich putze mir die Zähne mit meiner Zahnbürste»"),
    (9504, "example_uk", "Випускний бал був гарний, усі були там",
     "Випускний бал був справді гарний, усі були там",
     "потеряно «echt»"),
    (9504, "example_pl", "Bal maturalny był naprawdę piękny, wszyscy byli",
     "Bal maturalny był naprawdę piękny, wszyscy tam byli",
     "фраза обрывается"),
    (10608, "example_pl", "On odmawia podpisania tego",
     "On odmawia zrobienia tego", "в немецком «это сделать»"),
    (12662, "example_pl", "Miała omdlenie z upału",
     "Po wypadku zemdlał", "немецкий «Nach dem Unfall fiel er in Ohnmacht»"),
    (10609, "example_pl", "Ten nowy wzór jest naprawdę przyjemny dla oka",
     "Nowy design jest naprawdę przyjemny dla oka i nowoczesny",
     "потеряно «modern»"),
    (2274, "example_uk", "Мене призначили керівником проєкту",
     "Директора призначать",
     "немецкий «Der Direktor wird berufen»"),
    (2274, "example_en", "He was appointed director",
     "The director is being appointed", "то же"),
    (2274, "example_tr", "Müdür olarak atandı", "Müdür atanıyor", "то же"),
    (10610, "example_pl", "Doceniam twoją gotowość do pomocy",
     "Jego gotowość do pomocy zrobiła na mnie wrażenie",
     "немецкий «Seine Bereitschaft zu helfen, hat mich beeindruckt»"),
    (12663, "example_pl", "Po upadku miał wstrząśnienie mózgu",
     "Po wypadku miał wstrząśnienie mózgu", "в немецком авария, не падение"),
    (12660, "example_pl", "Grozi mu pozbawienie prawa jazdy",
     "Odstawienie alkoholu jest trudne",
     "немецкий «Der Alkoholentzug ist hart»"),
    (11751, "example_pl", "Lubię zielone oliwki w sałatce",
     "Lubię jeść zielone oliwki", "салат приписан"),
    (10604, "example_pl", "Powiedział to ironicznym tonem",
     "Powiedział to z ironicznym uśmiechem", "в немецком улыбка"),
    (10607, "example_pl", "To niesprawiedliwy zarzut wobec mnie",
     "To niesprawiedliwy zarzut", "«ко мне» приписано"),
    (10606, "example_pl", "Strasznie mi przed tym egzaminem",
     "Boję się tego egzaminu", "фраза обрывается"),
    (12208, "example_pl", "Lubię aktywność na świeżym powietrzu",
     "Sport to zdrowa aktywność",
     "немецкий «Sport ist eine gesunde Aktivität»"),
    (18750, "example_uk", "На Новий рік ми завжди влаштовуємо вечірку",
     "У новорічну ніч ми завжди влаштовуємо вечірку",
     "Silvester — новогодняя ночь, не Новый год"),
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
