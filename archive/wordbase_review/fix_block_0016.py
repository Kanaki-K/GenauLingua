"""
Сплошная вычитка, блок 16: ряды 1501–1700 по рангу частотности.

Находки:

* `die Vögel` — немецкое слово во множественном числе, а все пять переводов
  в единственном: «птица», «kuş», «ptak». Примеры при этом про стаю.
* `fein` — про еду сказано «изысканная», «витончена», «wykwintne», а
  немецкое «Das Essen ist sehr fein» значит просто «очень вкусно». Заодно
  турецкий пример был вообще про кольцо на пальце.
* `aufwachen`, `der West`, `erschrecken`, `irren`, `wie viel`, `drum` —
  примеры переводят другое предложение, причём сразу в трёх-четырёх языках.
* `die Treppe` — в украинском значении «драбина», то есть приставная
  лестница; она отдельным рядом идёт через сто рядов (`die Leiter`).
* `die Mitternacht` — украинское «полуніч» вместо «північ».
* `der Fluch` — в польском дважды одно слово, причём первое с опечаткой:
  «przeklęstwo, przekleństwo».
* `aufnehmen`, `streng`, `der Täter` — в списке значений не слово, а
  пояснение: «записывать на плёнку или видео», «резкий о запахе или вкусе»,
  «тот, кто совершил».
* `tschüs` — в украинском примере русское «пока»: «Ну все, пока, до завтра!»
* `der Zucker` — в украинском примере «кофе» вместо «кава».
* `beeindruckt`, `aufgrund`, `drum` — английские следы: слово приклеено
  через тире, «were» вместо «we're».

    python -m app.scripts.fix_block_0016            # показать
    python -m app.scripts.fix_block_0016 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- слово во множественном числе, переводы в единственном ---------------
    (15416, "translation_en", "bird", "birds",
     "немецкое слово «Vögel» — множественное число"),
    (15416, "translation_ru", "птица", "птицы",
     "немецкое слово «Vögel» — множественное число"),
    (15416, "translation_uk", "птах, пташка", "птахи, пташки",
     "немецкое слово «Vögel» — множественное число"),
    (15416, "translation_tr", "kuş", "kuşlar",
     "немецкое слово «Vögel» — множественное число"),
    (15416, "translation_pl", "ptak", "ptaki",
     "немецкое слово «Vögel» — множественное число"),

    # --- fein: про еду это «вкусно», а не «изысканно» ------------------------
    (6605, "example_en", "The food is very fine", "The food is excellent",
     "«very fine» о еде по-английски не говорят"),
    (6605, "translation_ru", "тонкий, мелкий, изысканный, хороший, чуткий",
     "тонкий, мелкий, изысканный, вкусный, чуткий",
     "про еду fein — это «вкусный»; добавлено значение"),
    (6605, "example_ru", "Еда очень изысканная", "Еда очень вкусная",
     "немецкий говорит просто, а здесь книжно"),
    (6605, "translation_uk", "тонкий, дрібний, вишуканий, гарний, чутливий",
     "тонкий, дрібний, вишуканий, смачний, чутливий",
     "про їжу fein — це «смачний»"),
    (6605, "example_uk", "Їжа дуже витончена", "Їжа дуже смачна",
     "«витончена їжа» так не кажуть"),
    (6605, "translation_tr", "ince, narin, kaliteli, hoş, hassas",
     "ince, narin, kaliteli, lezzetli, hassas",
     "yemek için fein — «lezzetli»"),
    (6605, "example_tr", "Parmağında ince bir yüzük var", "Yemek çok lezzetli",
     "пример был про кольцо, немецкий — про еду"),
    (6605, "translation_pl", "delikatny, drobny, wykwintny, świetny",
     "delikatny, drobny, wykwintny, smaczny",
     "o jedzeniu fein to «smaczny»"),
    (6605, "example_pl", "Jedzenie jest bardzo wykwintne",
     "Jedzenie jest bardzo smaczne",
     "«wykwintne» книжно там, где немецкий сказал просто"),

    # --- примеры переводят другое предложение --------------------------------
    (18649, "example_en", "I need to wake up early tomorrow",
     "Today I only woke up at ten",
     "немецкий о сегодняшнем утре, а не о завтрашнем"),
    (18649, "example_ru", "Завтра мне надо рано просыпаться",
     "Сегодня я проснулся только в десять",
     "немецкий о сегодняшнем утре, а не о завтрашнем"),
    (18649, "example_uk", "Мені потрібно завтра рано прокидатися",
     "Сьогодні я прокинувся лише о десятій",
     "немецкий о сегодняшнем утре, а не о завтрашнем"),
    (18649, "example_tr", "Yarın erken uyanmam gerek",
     "Bugün ancak saat onda uyandım",
     "немецкий о сегодняшнем утре, а не о завтрашнем"),

    (17073, "example_en", "The sun sets in the west",
     "We're driving towards the west",
     "немецкий пример про поездку на запад"),
    (17073, "example_ru", "Солнце садится на западе", "Мы едем на запад",
     "немецкий пример про поездку на запад"),
    (17073, "example_uk", "Наші вікна виходять на захід", "Ми їдемо на захід",
     "немецкий пример про поездку на запад"),
    (17073, "example_tr", "Odamızın penceresi batıya bakıyor",
     "Batıya doğru gidiyoruz",
     "немецкий пример про поездку на запад"),

    (10217, "example_en", "She is totally scared", "You really scared me!",
     "немецкий — «ты меня напугал», а не «она напугана»"),
    (10217, "example_uk", "Вона зовсім налякана", "Ти мене справді налякав!",
     "немецкий — «ты меня напугал», а не «она напугана»"),
    (10217, "example_tr", "Tamamen korkmuş", "Beni gerçekten korkuttun!",
     "немецкий — «ты меня напугал», а не «она напугана»"),

    (6604, "example_en", "I think you're wrong about the time",
     "Anyone can be wrong sometimes",
     "немецкий — общее «каждый может ошибиться»"),
    (6604, "example_uk", "Я думаю, ти помиляєшся з часом",
     "Кожен може колись помилитися",
     "немецкий — общее «каждый может ошибиться»"),
    (6604, "example_tr", "Bence saatte yanılıyorsun", "Herkes bazen yanılabilir",
     "немецкий — общее «каждый может ошибиться»"),

    (13474, "example_en", "How much does the bread cost?",
     "How much does the ticket cost?",
     "в немецком билет, а не хлеб"),
    (13474, "example_uk", "Скільки коштує хліб?", "Скільки коштує квиток?",
     "в немецком билет, а не хлеб"),
    (13474, "example_tr", "Ekmek ne kadar?", "Bilet ne kadar?",
     "в немецком билет, а не хлеб"),

    (6624, "example_en", "That's why were going home early today",
     "That's why we went home early today",
     "«were» вместо «we're», и немецкий в прошедшем"),
    (6624, "example_uk", "Тому ми йдемо додому раніше сьогодні",
     "Тому ми сьогодні пішли додому раніше",
     "немецкий в прошедшем времени, и порядок слов неживой"),
    (6624, "example_tr", "Bu yüzden bugün eve erken gidiyoruz",
     "Bu yüzden bugün eve erken gittik",
     "немецкий в прошедшем времени"),

    (6600, "example_en", "They live apart now",
     "The friends went their separate ways",
     "немецкий — «друзья разошлись»"),
    (6600, "example_uk", "Ми з ним живемо нарізно",
     "Друзі розійшлися в різні боки",
     "немецкий — «друзья разошлись»"),
    (6600, "example_tr", "Arkadaşlar ayrıldı", "Arkadaşlar ayrı yönlere gitti",
     "«auseinander» — в разные стороны, это потерялось"),

    (6599, "example_uk", "Він збив противника", "Він повалив противника додолу",
     "саме слово «додолу» у прикладі зникло"),
    (6599, "example_tr", "Merdivenlerden aşağı iniyorum", "Rakibini yere serdi",
     "пример был про спуск по лестнице, немецкий — про удар"),

    (6598, "example_uk", "У мене немає засобів на ремонт",
     "У мене немає на це коштів",
     "в немецком «на это», и ремонт взялся неизвестно откуда"),
    (6598, "example_tr", "Bunun için araçlarım yok", "Bunun için param yok",
     "«araç» — это инструмент, а в немецком речь о деньгах"),

    (15979, "example_uk", "Не примушуй мене чекати", "Ніхто не може мене змусити",
     "перевод переводил другое предложение"),
    (15979, "example_ru", "Никто не может меня принуждать",
     "Никто не может меня заставить",
     "по-русски здесь совершенный вид"),

    (8773, "example_tr", "Telefon hattı sürekli meşgul",
     "Patron projenin yönetimini devralıyor",
     "пример был про телефонную линию, немецкий — про руководство"),
    (8773, "example_uk", "Директор бере на себе керівництво проекту",
     "Начальник бере на себе керівництво проектом",
     "«керівництво проектом» — орудний відмінок"),

    (2973, "example_tr", "Kışın vitamin takviyesi alıyorum",
     "Takviyeye ihtiyacımız var",
     "пример был про витамины, немецкий — про подкрепление"),

    (10219, "example_tr", "Filmden çok heyecanlıyım", "Filme hayran kaldım",
     "«heyecanlıyım» — это волнение, а не восторг"),

    (10222, "example_tr", "O gerçekten yetenekli bir müzisyen",
     "O her şeyi yapabilir",
     "пример был про музыканта, немецкий — «способна на всё»"),

    (10210, "example_tr", "Bu bence gayet makul bir teklif",
     "Makul ol ve beni dinle",
     "немецкий — просьба, а не оценка предложения"),

    (6607, "example_en", "Can you direct me to the station?",
     "Can you straighten the picture?",
     "немецкий — про картину, которую надо выровнять"),

    (17072, "example_pl", "Pociąg wjechał do tunelu",
     "Ten tunel jest bardzo długi i ciemny",
     "пример был про поезд, немецкий — про сам туннель"),

    (12506, "example_en", "Pour me a mug of coffee", "Shut your gob",
     "«mug» прочли как кружку, а немецкий — «Halt die Fresse»"),
    (12506, "example_uk", "Заткнись", "Закрий пащеку",
     "у прикладі має бути саме слово ряду"),

    (1013, "example_tr", "Bu gömleği daha büyüğüyle değiştirdim",
     "Euro'yu dolara bozdurmak istiyorum",
     "пример был про рубашку, немецкий — про обмен валюты"),

    (2520, "example_tr", "Bu çorbanın tadı çok güzel", "Tadı güzel",
     "в немецком коротко «Der Geschmack ist gut», суп лишний"),

    (18647, "example_ru", "Однажды мы обязательно снова встретимся",
     "Здесь когда-то росло большое дерево",
     "перевод переводил другое предложение"),

    (13468, "example_tr", "Sana bin kere söyledim", "Bu araba bin euro",
     "пример был про «тысячу раз сказал», немецкий — про цену"),

    (12117, "example_tr", "Avcılık yarın sabah başlıyor",
     "Av yarın sabah başlıyor",
     "«avcılık» — охота как занятие, а здесь конкретная охота"),

    (1387, "example_uk", "Я розслабляюся у гарячій ванні", "Я хочу розслабитися",
     "перевод переводил другое предложение"),

    (686, "example_uk", "Наші вікна виходять на схід", "Берлін на сході",
     "перевод переводил другое предложение"),

    (705, "example_uk", "Я дізнався про це через друга", "Я надсилаю це поштою",
     "перевод переводил другое предложение"),

    (1008, "example_uk", "Мені треба прати білизну", "Я перу білизну",
     "немецкий — «я стираю», а не «мне надо стирать»"),

    # --- русизмы и ошибки в словах ------------------------------------------
    (1969, "translation_uk", "сходи, драбина", "сходи, східці",
     "«драбина» — приставна драбина, вона окремим рядом (die Leiter)"),
    (18646, "translation_uk", "полуніч, північ", "північ",
     "«полуніч» — не українське слово"),
    (13901, "example_uk", "Ну все, пока, до завтра!", "Бувай, до завтра",
     "«пока» — русское слово в украинском примере"),
    (1080, "example_uk", "Скільки цукру ти хочеш у свій кофе?",
     "Скільки цукру ти хочеш у свою каву?",
     "«кофе» — русское слово, і рід не той"),
    (2780, "translation_uk", "мішок, торба, куль", "мішок, торба",
     "«куль» українською — сніп, а не мішок"),
    (14392, "translation_pl", "klątwa, przeklęstwo, przekleństwo",
     "klątwa, przekleństwo",
     "одно слово дважды, и первое с опечаткой"),
    (10201, "example_tr", "Oğlum matematikde gerçek bir dahi",
     "Oğlum matematikte gerçek bir dahi",
     "«matematikde» — ошибка в согласных, нужно «matematikte»"),
    (15983, "example_tr", "Polis suç mahalini inceliyor",
     "Polis suç mahallini inceliyor",
     "«mahalini» — пропущена буква, нужно «mahallini»"),
    (6584, "example_tr", "Gerçeği öğrenmiş", "Gerçeği öğrendim",
     "немецкий в первом лице, турецкий — в третьем"),
    (6585, "example_tr", "Çabuk saklanıyorsun", "Çabuk saklan",
     "немецкий — повеление, турецкий был в изъявительном"),
    (6585, "example_uk", "Ти швидко сховаєшся", "Швидко ховайся!",
     "німецький — наказ, а не майбутній час"),
    (10221, "example_tr", "Bu senin çok akıllı bir fikriydi",
     "Bu gerçekten akıllı bir fikirdi",
     "«senin ... fikriydi» — ошибка в притяжательной форме"),
    (15417, "example_ru", "На поле растёт зерно", "На поле растёт пшеница",
     "«растёт зерно» так не говорят"),
    (15417, "example_uk", "На полі росте зерно", "На полі росте пшениця",
     "«росте зерно» так не кажуть"),
    (6612, "example_uk", "Гора вище, ніж думали", "Гора вища, ніж думали",
     "при іменнику потрібна форма «вища»"),
    (15985, "example_uk", "Імператор правив країну", "Імператор правив країною",
     "«правив» вимагає орудного відмінка"),
    (2599, "example_uk", "Покупка дому була вдалою",
     "Покупка будинку була хорошим рішенням",
     "«дому» замість «будинку», і рішення зникло"),
    (2599, "example_tr", "Satın alma iyiydi", "Evi satın almak iyi bir karardı",
     "немецкий — «покупка дома была хорошим решением»"),
    (2932, "example_uk", "Вирок оголошується", "Вирок буде оголошено",
     "німецький у майбутньому, і так кажуть живіше"),
    (1902, "example_tr", "Bir sonraki durak ana istasyonu",
     "Bir sonraki durak merkez istasyon",
     "«ana istasyonu» — зависший притяжательный, фраза не стоит"),
    (14961, "example_tr", "Kulübün üyesi", "O, kulübün üyesi",
     "без подлежащего это не предложение"),
    (18646, "example_tr", "Gece yarısını geçti", "Saat gece yarısını geçti",
     "без «saat» фраза висит без подлежащего"),
    (9733, "example_tr", "100 euro çek alıyorum", "100 euroluk bir çek alıyorum",
     "«100 euro çek» — нужна форма «euroluk»"),
    (14394, "example_tr", "Filmde vampir oynuyor", "Filmde vampir rolünü oynuyor",
     "«vampir oynuyor» — играет вампир, а не роль вампира"),
    (15420, "example_tr", "Bu ne gibi bir ses?", "Bu ne sesiydi?",
     "«ne gibi bir ses» — калька, по-турецки так не спрашивают"),
    (10216, "example_en", "Impressed – I'm really impressed", "I'm really impressed",
     "слово приклеено к фразе через тире — след прежней правки"),
    (6623, "example_en", "Due to the rain were staying home",
     "Due to the rain we're staying home",
     "«were» вместо «we're»"),

    # --- в списке значений пояснение вместо слова ----------------------------
    (6596, "translation_ru",
     "записывать, записывать на плёнку или видео, принимать, брать к себе, "
     "начинать, приступать, поднимать, подбирать, впитывать, усваивать",
     "записывать, принимать, брать к себе, начинать, поднимать, подбирать, "
     "впитывать, усваивать",
     "десять значений в карточке не читаются; пояснение убрано"),
    (6596, "translation_uk",
     "записувати, записувати на плівку або відео, приймати, брати до себе, "
     "починати, розпочинати, піднімати, підбирати, засвоювати",
     "записувати, приймати, брати до себе, починати, піднімати, підбирати, "
     "засвоювати",
     "дев'ять значень у картці не читаються; пояснення прибрано"),
    (1920, "translation_ru",
     "строгий, суровый, жёсткий, резкий о запахе или вкусе",
     "строгий, суровый, жёсткий, резкий",
     "в списке значений стояло пояснение, а не слово"),
    (15987, "translation_ru", "преступник, виновник, тот, кто совершил",
     "преступник, виновник",
     "в списке значений стояло пояснение, а не слово"),
    (2685, "translation_uk", "допитливий, цікавий, кмітливий до всього",
     "допитливий, цікавий, зацікавлений",
     "«кмітливий» — це тямущий, а не допитливий"),
    (2685, "translation_tr", "meraklı, merak eden, meraklı bir şekilde soran",
     "meraklı, merak eden, her şeyi bilmek isteyen",
     "«meraklı bir şekilde soran» — описание, а не слово"),
    (2685, "example_en", "I'm curious what's inside", "I'm curious",
     "в немецком коротко «Ich bin neugierig»"),
    (2685, "example_uk", "Він дуже допитливий хлопчик", "Я дуже допитливий",
     "німецький у першій особі"),
    (13469, "translation_uk", "і те і інше, обидва", "і те, і інше, обидва",
     "пропущена кома у парному сполучнику"),

    # --- по-людски: книжно там, где немецкий сказал просто -------------------
    (13466, "example_ru", "Мне следует чаще заниматься спортом",
     "Мне надо чаще заниматься спортом",
     "«следует» — канцелярит, немецкий «sollte» живее"),
    (13466, "example_uk", "Мені слід частіше займатися спортом",
     "Мені треба частіше займатися спортом",
     "«слід» — книжно, живіше «треба»"),
    (6597, "example_ru", "У нас различные мнения", "У нас разные мнения",
     "«различные» книжнее, чем «разные»"),
    (10215, "example_ru", "Эта потеря меня очень печалит",
     "Эта потеря меня очень расстраивает",
     "«печалит» — книжно"),
    (10215, "example_uk", "Ця втрата робить мене дуже сумною",
     "Ця втрата мене дуже засмучує",
     "калька з німецької і неузгоджений рід"),
    (12501, "example_ru", "Вирус делает многих людей больными",
     "Из-за вируса многие болеют",
     "калька с немецкого, по-русски так не говорят"),
    (12501, "example_uk", "Вірус робить багатьох людей хворими",
     "Через вірус багато людей хворіє",
     "калька з німецької"),
    (10207, "example_ru", "Я лопаюсь от ярости", "Я сейчас лопну от злости",
     "«лопаюсь» в настоящем времени так не говорят"),
    (10207, "example_uk", "Я лопаюся від гніву", "Я зараз лусну від злості",
     "«лопаюся» так не кажуть"),
    (10204, "example_ru", "Прошу о милости", "Прошу пощады",
     "«прошу о милости» — книжно, живое «прошу пощады»"),
    (10204, "example_uk", "Прошу про милість", "Прошу пощади",
     "«прошу про милість» — книжно"),
    (432, "example_uk", "Мені потрібна додаткова інформація",
     "Мені потрібно більше інформації",
     "«додаткова» — канцелярит, німецький сказав «mehr»"),
    (9729, "example_ru", "У него большое богатство", "У него большое состояние",
     "по-русски про деньги говорят «состояние»"),
    (9729, "example_uk", "У нього велике багатство", "У нього великий статок",
     "українською про гроші — «статок»"),
    (15976, "example_ru", "Сенатор приходит сегодня", "Сенатор сегодня приедет",
     "«приходит сегодня» — калька, живее «сегодня приедет»"),
    (15976, "example_uk", "Сенатор приходить сьогодні", "Сенатор сьогодні приїде",
     "калька з німецької"),
    (18651, "example_ru", "Я бегаю ежедневно час", "Я каждый день бегаю час",
     "порядок слов неживой"),
    (18651, "example_uk", "Я бігаю щодня годину", "Я щодня бігаю годину",
     "порядок слів неживий"),
    (18651, "example_tr", "Günlük bir saat koşarım", "Her gün bir saat koşuyorum",
     "«günlük koşarım» так не говорят"),
    (6583, "example_tr", "Birbirimize karşı karşılıklı duygularımız var",
     "Karşılıklı duygularımız var",
     "«birbirimize karşı karşılıklı» — дважды одно и то же"),
    (10205, "example_tr", "Bu gerçekten kötüydü", "Bu yaptığın gerçekten çok kötüydü",
     "в немецком есть «von dir» — это потерялось"),
    (10202, "example_tr", "Müzik için büyük yeteneği var",
     "Onun büyük bir müzik yeteneği var",
     "«müzik için yeteneği» — калька с немецкого"),
    (15415, "example_tr", "Zehirli yılan çimlerin içinde gizleniyor",
     "Zehirli yılan çimlerin arasında saklanıyor",
     "«gizleniyor» книжно, живое «saklanıyor»"),
    (599, "example_uk", "Ми їмо близько полудня", "Ми обідаємо",
     "німецький «zu Mittag essen» — це обідати"),
    (599, "example_tr", "Öğleye doğru yiyoruz", "Öğle yemeğini yiyoruz",
     "«öğleye doğru» — около полудня, а немецкий про сам обед"),
    (600, "example_en", "The lunch was good", "Lunch was good",
     "по-английски здесь без артикля"),
    (203, "example_en", "She cooks an egg", "She is boiling an egg",
     "«kocht ein Ei» — варит, а не готовит"),
    (2533, "example_en", "I start a company", "I'm starting a company",
     "немецкий о происходящем сейчас"),
    (8775, "example_en", "I need a ladder for climbing", "I need a ladder",
     "в немецком коротко «Ich brauch eine Leiter»"),
    (13465, "example_en", "The house behind belongs to me",
     "The house behind it belongs to me",
     "без «it» фраза обрывается"),
    (13465, "example_pl", "Dom stojący z tyłu należy do mnie",
     "Dom z tyłu należy do mnie",
     "«stojący» лишнее, немецкий сказал короче"),
    (6609, "example_en", "Where are the keys located?",
     "Where are your keys located?",
     "в немецком «deine Schlüssel»"),
    (6609, "example_uk", "Де знаходяться ключі?", "Де знаходяться твої ключі?",
     "у німецькому «deine»"),
    (14963, "example_en", "The father holds a mass today",
     "The priest is holding a mass today",
     "«father holds a mass» — не по-английски"),
    (14963, "example_uk", "Священик сьогодні служить літургію",
     "Патер сьогодні служить месу",
     "у ряді слово «патер», і меса, а не літургія"),
    (1750, "example_en", "That was just bad luck", "I had bad luck",
     "немецкий в первом лице: «Ich habe Pech gehabt»"),
    (1750, "example_uk", "Це була просто невдача", "Мені не пощастило",
     "німецький у першій особі"),
    (6613, "example_uk", "Як ти сюди приїхав?", "Як ти сюди прийшов?",
     "«herkommen» — прийти, а не приїхати"),
    (13901, "example_tr", "Görüşürüz, yarın görüşürüz",
     "Hoşça kal, yarın görüşürüz",
     "одно слово дважды в короткой фразе"),
    (572, "example_tr", "Uzun bir kaban giyiyor", "Uzun bir palto giyiyor",
     "«kaban» — куртка, а «Mantel» — пальто"),
    (18641, "example_pl", "Ciągle mi przerywasz", "Ciągle mi przeszkadzasz",
     "«przerywasz» — перебиваешь, а «stören» — мешаешь"),
    (2097, "example_pl", "Jest wolnych tylko niewiele miejsc",
     "Jest tylko niewiele wolnych miejsc",
     "порядок слов неживой"),
    (13469, "example_pl", "Lubię jedno i drugie", "Bardzo lubię jedno i drugie",
     "в немецком «sehr gerne» — это потерялось"),
    (12510, "example_pl", "Jedzenie niestety jest spalone",
     "Jedzenie niestety się przypaliło",
     "о еде по-польски говорят «przypaliło się»"),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
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
