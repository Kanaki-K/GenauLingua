"""
Сплошная вычитка, блок 32: ряды 4701–4900 по рангу частотности
(id первого 2221, id последнего 14521).

Главное за блок:

* `erheben` — ряд, где немецкий пример не содержит слова ряда вообще:
  `Die erhabenen Worte berührten sein Herz` — это `erhaben`, другое
  слово. Английский единственный перевёл слово ряда («The city raised
  the parking fees»), остальные четыре пошли за примером. Переписаны
  все шесть ячеек: пример приведён к слову ряда.
* `unversehrt` — немецкий эталон говорил `war das Auto nicht
  unversehrt, aber die Insassen waren unversehrt`: одно слово дважды в
  одной фразе, и все пять переводов его упростили. Эталон приведён к
  тому, что они и так говорят.
* `Das verstärkt mein Verdacht` — винительный падеж в эталоне.
* `The opponents attack was unexpected` — притяжательное без апострофа,
  которого примета `scan_en_apostrophe` поймать не может: `opponents
  attack` читается и как «противники атакуют». Такие ловятся только
  глазами.
* Украинские небывальщины: `буяниє`, `замітка` вместо «зауваження»,
  `нудота` вместо «зануда», `злодій у фільмі` внутри значений.
* Турецкие небывальщины: `genelevhane`, `Kuryeci`, `rendeleyle rendele
  ediyorum`, `durmmazsan`, `O filmteki`, `şakaydi`.

    python -m app.scripts.fix_block_0032            # показать
    python -m app.scripts.fix_block_0032 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- erheben: пример не содержал слова ряда ------------------------------
    (7318, "example_de", "Die erhabenen Worte berührten sein Herz",
     "Die Stadt erhebt eine Gebühr für das Parken",
     "«erhaben» — другое слово; пример не про слово ряда"),
    (7318, "example_en", "The city raised the parking fees",
     "The city levies a fee for parking", "то же"),
    (7318, "example_ru", "Возвышенные слова тронули его сердце",
     "Город взимает плату за парковку", "то же"),
    (7318, "example_uk", "Піднесені слова зворушили його серце",
     "Місто стягує плату за парковку", "то же"),
    (7318, "example_tr", "Yüksek sözler onun kalbine dokundu",
     "Şehir park için ücret alıyor", "то же"),
    (7318, "example_pl", "Wzniosłe słowa poruszyły jego serce",
     "Miasto pobiera opłatę za parkowanie", "то же"),

    # --- unversehrt: слово дважды в одной фразе ------------------------------
    (12669, "example_de",
     "Nach dem Unfall war das Auto nicht unversehrt, aber die Insassen "
     "waren unversehrt",
     "Nach dem Unfall war das Auto beschädigt, aber die Insassen blieben "
     "unversehrt",
     "«unversehrt» дважды в одной фразе; все пять переводов и так так говорят"),
    (12669, "example_tr",
     "Kazadan sonra araba hasar gördü, ama yolcular hasarsız kaldı",
     "Kazadan sonra araba hasar gördü, ama yolcular sağ salim kaldı",
     "«hasarsız» — о вещах, не о людях"),
    (12669, "example_pl",
     "Samochód był zniszczony, ale kierowca wyszedł nietknięty",
     "Samochód był uszkodzony, ale pasażerowie wyszli nietknięci",
     "в немецком пассажиры, а не водитель"),

    # --- немецкий эталон -----------------------------------------------------
    (7308, "example_de", "Das verstärkt mein Verdacht noch mehr",
     "Das verstärkt meinen Verdacht noch mehr", "винительный падеж"),

    # --- английский апостроф, который примета не видит -----------------------
    (7321, "example_en", "The opponents attack was unexpected",
     "The opponent's attack was unexpected",
     "пропущен апостроф; «opponents attack» читается и как «противники атакуют»"),

    # --- перевод переводит другую фразу --------------------------------------
    (15550, "example_en", "The female tiger is bigger than I thought",
     "The female tiger is bigger than expected",
     "немецкий «als erwartet»"),
    (15550, "example_uk", "Самиця тигра більша, ніж я думав",
     "Самиця тигра більша, ніж очікувалося", "то же"),
    (15550, "example_tr", "Dişi kaplan benim sanıldığından daha büyük",
     "Dişi kaplan beklenenden daha büyük", "то же"),
    (10619, "example_en", "I didn't realize how late it was",
     "You have to realize that!",
     "немецкий «Das musst du doch einsehen!»"),
    (10619, "example_uk", "Нарешті він визнав, що був неправий",
     "Ти ж повинен це зрозуміти!", "то же"),
    (10619, "example_tr", "Sonunda haksız olduğunu kabul etti",
     "Bunu anlaman gerek!", "то же"),
    (17961, "example_en", "The evolution of mankind is fascinating",
     "Evolution is a fascinating topic",
     "немецкий «Die Evolution ist ein faszinierendes Thema»"),
    (17961, "example_ru", "Эволюция человека — очень интересная тема",
     "Эволюция — очень интересная тема", "то же"),
    (17961, "example_uk", "Еволюція людини — дуже цікава тема",
     "Еволюція — дуже цікава тема", "то же"),
    (17961, "example_tr", "İnsanlığın evrimi büyüleyici",
     "Evrim büyüleyici bir konu", "то же"),
    (13683, "example_en", "He packed clean socks and underpants",
     "I need new underpants",
     "немецкий «Ich brauche eine neue Unterhose»"),
    (13536, "example_en", "Give the book to the one who lost it",
     "I mean the one with the red hat",
     "немецкий «Ich meine denjenigen mit dem roten Hut»"),
    (13536, "example_uk", "Дай книгу тому, хто її загубив",
     "Я маю на увазі того, хто в червоному капелюсі", "то же"),
    (13536, "example_tr", "Kitabı onu kaybedene ver",
     "Kırmızı şapkalı kişiyi kastediyorum", "то же"),
    (10651, "example_en", "This is a noble material",
     "This is a noble heart", "немецкий «Das ist ein edles Herz»"),
    (10651, "example_uk", "Це благородний матеріал",
     "Це благородне серце", "то же"),
    (10651, "example_tr", "Bu asil bir malzeme", "Bu asil bir kalp", "то же"),
    (17178, "example_en",
     "The brake on the car is not working properly, it's dangerous to drive",
     "The brake is not working properly",
     "немецкий «Die Bremse funktioniert nicht richtig»"),
    (17178, "example_uk", "Гальмо в машині не працює правильно",
     "Гальмо не працює правильно", "то же"),
    (17178, "example_tr",
     "Arabanın freni düzgün çalışmıyor, araç sürmek tehlikeli",
     "Fren düzgün çalışmıyor", "то же"),
    (2373, "example_en", "Someone broke into my house",
     "Thieves wanted to break into our place",
     "немецкий «Diebe wollten bei uns einbrechen»"),
    (2373, "example_uk", "Грабіжники вламалися в магазин уночі",
     "Злодії хотіли вламатися до нас", "то же"),
    (2373, "example_tr", "Birisi evime hırsızlık yaptı",
     "Hırsızlar bize girmek istedi", "то же"),
    (18751, "example_ru", "Опоздавших в зал не пускают",
     "Поезд опаздывает", "немецкий «Der Zug ist verspätet»"),
    (281, "example_en", "Fill out the form", "I fill out the form",
     "немецкий «Ich fülle das Formular aus»"),
    (281, "example_tr", "Lütfen formu doldurun", "Formu dolduruyorum",
     "то же"),
    (1759, "example_ru", "Физика — интересная наука", "Физика интересная",
     "«наука» приписана"),
    (1759, "example_uk", "Фізика — мій улюблений предмет",
     "Фізика цікава", "немецкий «Physik ist interessant»"),
    (10616, "example_pl", "Ta piosenka wzbudza we mnie wspomnienia",
     "To zdjęcie wzbudza we mnie wiele wspomnień",
     "в немецком картина, а не песня"),
    (9507, "example_en", "The topics of the lesson are very interesting",
     "The topic of the lesson is very interesting",
     "в немецком единственное число"),
    (9507, "example_tr", "Dersin konuları çok ilginç",
     "Dersin konusu çok ilginç", "то же"),
    (7310, "example_uk", "У мене є проміжок між зустрічами",
     "Завтра по обіді в мене є вікно в розкладі",
     "немецкий «eine Lücke in meinem Zeitplan morgen Nachmittag»"),
    (13535, "example_pl", "Ja lubię herbatę, on natomiast kawę",
     "Pierwszy film był nudny, drugi natomiast był bardzo ekscytujący",
     "немецкий про два фильма"),
    (10622, "example_pl", "Jeszcze chwila i zwariuję",
     "Jeśli nie przestaniesz, zwariuję",
     "немецкий «Wenn du nicht aufhörst, drehe ich durch»"),
    (10614, "example_pl", "Ta decyzja sprowadziła nieszczęście na całą rodzinę",
     "Wojna przynosi ludziom wiele nieszczęścia",
     "немецкий «Der Krieg bringt viel Unheil über die Menschen»"),
    (10615, "example_pl", "Jego nastrój jest zupełnie nieprzewidywalny",
     "Jego zachowanie jest zupełnie nieprzewidywalne, nikt nie wie, co "
     "zrobi dalej", "в немецком поведение, и потеряна вторая половина"),
    (10612, "example_pl", "Nie doceniaj tej drużyny, oni są mocni",
     "Wielu nie docenia siły tej drużyny",
     "немецкий «Viele unterschätzen die Stärke dieser Mannschaft»"),
    (10613, "example_pl", "Przekręcił moje słowa i wyszła z tego kłótnia",
     "Przekręcił fakty i teraz wszyscy są zdezorientowani",
     "немецкий «Er hat die Fakten verdreht»"),
    (11754, "example_pl", "Odgrzeję ci obiad w mikrofalówce",
     "Odgrzewam jedzenie", "немецкий «Ich wärme das Essen auf»"),
    (12670, "example_pl", "Mój brat jest dawcą krwi",
     "Dawca krwi pomaga wielu ludziom swoim darem",
     "немецкий «Der Blutspender hilft vielen Menschen mit seiner Spende»"),
    (17180, "example_ru", "Закажи ужин через обслуживание номеров",
     "Я звоню в обслуживание номеров",
     "немецкий «Ich rufe den Zimmerservice an»"),
    (17180, "example_uk", "Я звоню в кімнатний сервіс",
     "Я телефоную в службу обслуговування номерів",
     "«звоню» — русизм, и «кімнатний сервіс» — калька"),
    (12664, "example_pl", "Wyciągnij ręce do góry i rozluźnij się",
     "Wyciągam ręce do góry",
     "немецкий «Ich strecke meine Arme nach oben»"),
    (15081, "example_uk", "Маленьке хлопчисько сьогодні особливо буяниє",
     "Малий шибеник сьогодні особливо неспокійний",
     "«буяниє» — не слово"),
    (13684, "example_pl", "Na bal włożyła czarną pelerynę",
     "Peleryna króla jest czerwona",
     "немецкий «Der Umhang des Königs ist rot»"),
    (10657, "example_uk", "Який жах, я все забув!",
     "Машина несподівано виїхала мені назустріч, це був справжній переляк",
     "немецкий про машину"),
    (12210, "example_pl", "Idziesz tak szybko, że nie nadążam",
     "Próbuję nadążyć, ale inni są po prostu za szybcy",
     "немецкий «Ich versuche mitzuhalten»"),
    (17181, "example_tr", "Vapur iskeleye yanaştı",
     "Kaptan iskele tarafına dönmeyi emretti",
     "«iskele» тут причал, а в немецком левый борт"),
    (17181, "example_ru", "Капитан приказал плыть на левый борт",
     "Капитан приказал повернуть на левый борт", "«плыть на борт» — не говорят"),
    (17181, "example_uk", "Капітан наказав плисти на лівий борт",
     "Капітан наказав повернути на лівий борт", "то же"),

    # --- украинские опечатки и русизмы ---------------------------------------
    (13530, "example_uk",
     "Мому дідусю в наступному місяці виповниться п'ятдесят років",
     "Моєму дідусю в наступному місяці виповниться п'ятдесят років",
     "«Мому» — опечатка"),
    (16275, "example_uk",
     "Поліцейський шеф розмовляє з медіа про нові заходи",
     "Шеф поліції розмовляє з медіа про нові заходи",
     "«Поліцейський шеф» — порядок слов"),
    (10611, "example_uk",
     "Це було неповажно з твоєї сторони перебивати вчителя так",
     "Це було неповажно з твого боку так перебивати вчителя",
     "«з твоєї сторони» — русизм, и порядок слов"),
    (10632, "example_uk", "Це була підла замітка, ти не повинен був це говорити",
     "Це було підле зауваження, ти не повинен був цього говорити",
     "«замітка» — заметка в газете, а не замечание"),
    (10643, "example_uk", "Цей хлопець — справжня нудота",
     "Цей хлопець — справжній зануда", "«нудота» — тошнота"),
    (10647, "translation_uk", "негідник, злодій у фільмі, підлюка",
     "негідник, лиходій, підлюка",
     "«злодій у фільмі» — обрывок примера внутри значений"),
    (10647, "example_uk", "Негідник у фільмі дуже поганий",
     "Негідник у фільмі дуже злий", "«böse» — злой"),
    (10653, "translation_uk", "злодій, злочинець, лиходій, негідник",
     "лиходій, злочинець, негідник", "«злодій» — вор"),
    (10653, "example_uk", "Лиходій у цьому фільмі дійсно дуже підлий",
     "Лиходій у цьому фільмі дійсно підлий і жорстокий",
     "потеряна вторая половина"),
    (10622, "example_uk", "Якщо ти не зупиниш, я збожеволію",
     "Якщо ти не зупинишся, я збожеволію", "«не зупиниш» — без «-ся»"),
    (10634, "example_uk", "Я почував себе безпомічним, тому що не міг йому допомогти",
     "Я почувався безпорадним, тому що не міг йому допомогти",
     "«почував себе» и «безпомічний» — русизмы"),
    (15553, "example_uk", "Ми пройшли через глибоку ущілину",
     "Ми пройшли через глибоку ущелину", "«ущілина» — опечатка"),
    (10644, "example_uk", "Зі збентеженості вона нервово сміялась",
     "Від збентеження вона нервово засміялася", "падеж и вид"),
    (10645, "example_uk", "Концерт був нудний і скучний",
     "Концерт був нудний і понурий", "«скучний» — русизм"),
    (7322, "example_uk", "Це просте плаття", "Це проста сукня",
     "«плаття» — русское слово"),
    (17561, "example_uk", "У моєї бабусі в підвалі стоїть стара друкарська машина",
     "У моєї бабусі в підвалі стоїть стара друкарська машинка",
     "«машина» вместо «машинка»"),
    (8932, "example_uk", "Секретар працює в офісі й організовує зустрічі босса",
     "Секретар працює в офісі й організовує зустрічі шефа",
     "«босса» — двойная «с» и русизм"),
    (16287, "example_uk", "Спадщина мого дідуся була його старим щоденником",
     "Спадщиною мого дідуся був його старий щоденник", "падежи"),
    (10654, "example_uk", "Цей художник дуже бажаний і всі хочуть його роботи",
     "Цей художник дуже затребуваний, і всі хочуть його роботи",
     "«бажаний» — желанный, а не востребованный"),
    (10646, "example_uk", "Його хоробрість на війні була дивовижна",
     "Його хоробрість на війні була гідна подиву",
     "«bewundernswert» — достойна восхищения"),
    (10649, "example_uk", "Щади мене від своєї критики",
     "Звільни мене від своєї критики", "«щадити від» — так не говорят"),
    (10641, "example_uk", "Я більше не терплю цю образу",
     "Я більше не терпітиму цю образу", "«nicht länger» — впредь"),
    (10642, "example_uk", "Покажи трохи ввічливості й скажи дякую",
     "Прояви трохи ввічливості й скажи дякую", "«покажи ввічливість» — калька"),
    (7316, "example_uk", "М'ясо м'яке і смачне", "М'ясо ніжне і смачне",
     "в значениях первое «ніжний»"),
    (7306, "example_uk", "Його відповідь була дуже невизначена",
     "Його відповідь була дуже розпливчаста", "в значениях «розпливчастий»"),
    (11756, "example_uk", "Під час війни багато людей повинні були голодувати",
     "Під час війни багатьом людям довелося голодувати", "калька с немецкого"),
    (10652, "example_uk",
     "Мені набридло відповідати на одні й ті ж дратівні питання",
     "Мене дуже дратує постійно відповідати на одні й ті самі питання",
     "«дратівні питання» — так не говорят"),
    (15551, "example_uk", "Зозуля співає в лісі", "Зозуля кує в лісі",
     "кукушка кукует, а не поёт"),
    (10620, "example_uk", "Діти знову шкодять", "Діти знову бешкетують",
     "в значениях «бешкет»"),
    (12667, "example_uk", "Лікар дав мені ін'єкцію сироватки",
     "Лікар зробив мені ін'єкцію сироватки", "«дав ін'єкцію» — калька"),
    (9808, "example_uk", "Мені був потрібний авансовий платіж на зарплату",
     "Мені був потрібен аванс у рахунок зарплати", "канцелярит"),
    (7305, "example_uk", "Сіре небо робить мене сумною",
     "Від сірого неба мені сумно", "калька, и род говорящего"),
    (16280, "example_uk",
     "Звільнення від цього обтяження було для нього дуже важливо",
     "Звільнення від цього тягаря було для нього дуже важливим",
     "«обтяження» — обременение в праве; и падеж"),
    (18752, "example_uk", "У неділю я зазвичай ходжу гуляти або відвідую сім'ю",
     "По неділях я зазвичай ходжу гуляти або відвідую сім'ю",
     "«sonntags» — по воскресеньям, не в одно"),
    (7325, "example_uk", "Будь ласка, заповніть формуляр",
     "Будь ласка, заповни формуляр", "в немецком обращение на «ты»"),
    (12665, "translation_uk", "кружиться голова, запаморочення",
     "голова йде обертом, запаморочення", "«кружиться» — русизм"),
    (2193, "translation_uk",
     "заразний, інфекційний, що передається про смішок",
     "заразний, інфекційний, такий, що передається",
     "«смішок» — не то слово"),

    # --- русские -------------------------------------------------------------
    (7324, "translation_ru", "тереть, натирать, трать на тёрке",
     "тереть, натирать, тереть на тёрке", "«трать» — опечатка"),
    (2221, "example_ru", "Мы распределяем работу между собой",
     "Мы распределяем работу", "«между собой» приписано"),
    (14057, "example_ru", "Фото было на обложке",
     "Фото было на первой полосе", "в значениях первое «первая полоса»"),
    (10626, "example_ru",
     "Его выражение лица показало, что он действительно удивлён",
     "Его выражение лица показало, что он был действительно удивлён",
     "время не согласовано"),

    # --- турецкие небывальщины и падежи --------------------------------------
    (16288, "example_tr",
     "Bu bölgedeki genelevhane yasadışı ve polis tarafından izleniyor",
     "Bu bölgedeki genelev yasadışı ve polis tarafından izleniyor",
     "«genelevhane» — не слово"),
    (8931, "example_tr", "Kuryeci paketi getiriyor",
     "Kurye paketi getiriyor", "«Kuryeci» — не слово"),
    (7324, "example_tr", "Havuçları rendeleyle rendele ediyorum",
     "Havuçları rendeyle rendeliyorum", "две ошибки в одной фразе"),
    (10622, "example_tr", "Eğer durmmazsan, çılgına dönüceğim",
     "Eğer durmazsan, çılgına döneceğim", "две опечатки"),
    (10653, "example_tr", "O filmteki kötü adam gerçekten çok gaddar",
     "O filmdeki kötü adam gerçekten çok gaddar", "«filmteki» — опечатка"),
    (10628, "example_tr", "Bu sapık bir şakaydi, bunu komik bulmuyorum",
     "Bu sapık bir şakaydı, bunu komik bulmuyorum", "«şakaydi» — опечатка"),
    (18247, "example_tr", "Eski sandıkta büyükannenin mektuplarını bulduk",
     "Eski sandıkta büyükannemin mektuplarını bulduk",
     "«büyükannenin» — твоей бабушки"),
    (10618, "example_tr", "Başarından kıskanmıyorum, dürüst olmak gerekirse",
     "Başarını kıskanmıyorum, dürüst olmak gerekirse", "неверный падеж"),
    (16283, "example_tr", "Ona parayı çaldığı suçlaması yapılıyor",
     "Parayı çalmakla suçlanıyor", "фраза не собрана"),
    (15079, "example_tr", "Benim ailem bir çocuk evlat edinmek istiyor",
     "Ailem bir çocuk evlat edinmek istiyor", "лишнее «benim»"),
    (10631, "example_tr", "Karmaşık açıklama beni daha da kafa karıştırıyor",
     "Karmaşık açıklama kafamı daha da karıştırıyor", "фраза не собрана"),
    (10636, "example_tr", "Gelip gelmediğin bana tamamen kayıtsız",
     "Gelip gelmemen benim için tamamen fark etmez", "фраза не собрана"),
    (18752, "example_tr",
     "Pazar günleri genellikle yürüyüş yapıyor ya da ailemizi ziyaret ediyorum",
     "Pazar günleri genellikle yürüyüş yapıyorum ya da ailemi ziyaret ediyorum",
     "лицо не согласовано"),
    (10638, "example_tr", "Kazandıktan sonraki sevinç anlatılamazdı",
     "Galibiyetten sonraki zafer anlatılamazdı", "потерян сам триумф"),
    (12674, "example_tr", "Her nefesle zayıflıyor gitti",
     "Her nefeste daha da zayıflıyordu", "фраза не собрана"),
    (10630, "example_tr", "Bu acele bir karardı, daha uzun düşünmeliyiz",
     "Bu acele bir karardı, daha uzun düşünmeliydik", "время не согласовано"),
    (10632, "example_tr", "Bu çok adi bir yorumdu",
     "Bu adi bir yorumdu, bunu söylememeliydin", "потеряна вторая половина"),
    (13535, "example_tr",
     "İlk film sıkıcıydı, ikincisi bununla birlikte çok heyecanlıydı",
     "İlk film sıkıcıydı, ikincisi ise çok heyecanlıydı",
     "«bununla birlikte» не на месте"),
    (14058, "example_tr", "Patron bu hafta ulaşılabilir değil",
     "Patrona bu hafta ulaşılamıyor", "«ulaşılabilir değil» — калька"),
    (7317, "example_tr", "Kağıdı yarısında katla", "Kağıdı ortadan katla",
     "«yarısında» — не то"),
    (10643, "example_tr", "O çocuk gerçek bir baş belası",
     "Bu adam gerçek bir baş belası", "в немецком «Typ», а не ребёнок"),
    (10641, "example_tr", "Artık bu hakareti tolere etmeyeceğim",
     "Artık bu hakarete tahammül etmeyeceğim", "в значениях «tahammül etmek»"),
    (10658, "example_tr", "Bu ifadeye kesinlikle güvenmiyorum",
     "Bu ifadeye kesinlikle güvenmiyorum, buna inanmıyorum",
     "потеряна вторая половина"),
    (17561, "example_tr",
     "Büyükannem bodrumdaki eski yazı makinesini hâlâ tutuyor",
     "Büyükannemin bodrumda hâlâ eski bir daktilosu var", "фраза не собрана"),
    (17812, "example_tr", "Projede benim katılımım oldukça pasifti",
     "Projedeki katılımım oldukça pasifti", "лишнее «benim»"),
    (10654, "example_tr", "Bu sanatçı çok aranan ve herkes onun eserlerini istiyor",
     "Bu sanatçı çok aranıyor ve herkes onun eserlerini istiyor",
     "«çok aranan ve» — фраза не собрана"),
    (10657, "example_tr", "Araba bana çarpmak üzere geldi, beni korkuttu",
     "Araba aniden karşıma çıktı, beni fena korkuttu",
     "«çarpmak üzere geldi» — вот-вот ударит"),
    (10627, "example_tr", "Senin kız kardeşin müzikte gerçekten yetenekli",
     "Kız kardeşin müzikte gerçekten yetenekli", "лишнее «senin»"),
    (7303, "example_tr", "Yeni yasa birçok insanın okumasına izin veriyor",
     "Yeni yasa birçok insana okuma olanağı sağlıyor",
     "«izin veriyor» — разрешает, а не даёт возможность"),
    (8927, "example_tr", "Cesaret için bir ödül aldı",
     "Cesareti için bir ödül aldı", "потеряно притяжательное"),
    (9807, "example_tr", "Şirketin finansmanı iyi durumdadır",
     "Şirketin mali durumu iyi", "«finansman» — финансирование; и «-dır»"),
    (16276, "example_tr", "Bu silahın kalibresi çok tehlikelidir",
     "Bu silahın kalibresi çok tehlikeli", "«-dir»"),
    (17960, "example_tr", "Su, hayatın önemli bir elemanıdır",
     "Su, hayatın önemli bir unsuru", "«eleman» — сотрудник; и «-dır»"),
    (2193, "example_tr", "Hastalık bulaşıcıdır", "Hastalık bulaşıcı", "«-dır»"),
    (10623, "example_tr", "Bu rahatlatıcı bir haberdir",
     "Bu rahatlatıcı bir haber", "то же"),
    (14517, "example_tr", "Bu sanatın gerçek bir şaheseridir",
     "Bu sanatın gerçek bir şaheseri", "то же"),
    (10650, "example_tr", "Yemin ciddi bir şeydir", "Yemin ciddi bir şey",
     "то же"),
    (10656, "example_tr", "Anne ve çocuk arasındaki bağ çok güçlüdür",
     "Anne ve çocuk arasındaki bağ çok güçlü", "то же"),
    (7322, "example_tr", "Bu basit bir elbisedir", "Bu sade bir elbise",
     "то же, и в значениях первое «sade»"),
    (10624, "example_tr", "Kıskançlığı belirgin idi", "Kıskançlığı belliydi",
     "«idi» пишут слитно"),
    (16287, "example_tr", "Büyükbabamın mirası onun eski günlüğü idi",
     "Büyükbabamın mirası eski günlüğüydü", "то же"),
    (7321, "example_tr", "Rakibin saldırısı beklenmedik",
     "Rakibin saldırısı beklenmedikti", "потеряно прошедшее время"),

    # --- потерянное и приписанное --------------------------------------------
    (2221, "example_pl", "Dzielimy pracę między siebie", "Dzielimy pracę",
     "«между собой» приписано"),
    (10611, "example_pl", "To było lekceważące wobec nauczyciela",
     "To było lekceważące z twojej strony tak przerywać nauczycielowi",
     "потеряна половина фразы"),
    (10611, "example_tr", "Öğretmeni öyle kesip atmak saygısız bir davranıştı",
     "Öğretmenin sözünü öyle kesmek saygısızlıktı",
     "«kesip atmak» — отрезать, а не перебить"),
    (11752, "example_pl", "Kucharz ładnie podał danie na talerzu",
     "Kucharz ładnie podaje potrawy", "время и число"),
    (13682, "example_pl", "Włóż ciepły sweter bo jest zimno",
     "Zakładam ciepły sweter, bo jest zimno",
     "в немецком «я надеваю», и пропущена запятая"),
    (12666, "example_pl", "Lekarz sądowy zbadał ciało ofiary",
     "Lekarz sądowy zbadał ciało", "«ofiary» приписано"),
    (12667, "example_pl", "Lekarz podał mu surowicę",
     "Lekarz podał mi surowicę", "в немецком «мне»"),
    (9809, "example_en", "That was an expensive mistake",
     "That is an expensive mistake", "в немецком настоящее время"),
    (11755, "example_pl", "Wypił kieliszek koniaku", "Wypił drogi koniak",
     "«teuren» — дорогой"),
    (14057, "example_uk", "Фото було на обкладинці",
     "Фото було на першій шпальті", "в значениях первое «перша шпальта»"),
    (14057, "example_tr", "Fotoğraf kapakta vardı",
     "Fotoğraf ilk sayfadaydı", "то же"),
    (10624, "example_pl", "Nie mógł ukryć zazdrości",
     "Jego zazdrość była oczywista",
     "немецкий «Sein Neid war offensichtlich»"),
    (10626, "example_pl", "Miał bardzo dziwny wyraz twarzy",
     "Jego wyraz twarzy pokazał, że był naprawdę zaskoczony",
     "немецкий про удивление"),
    (10627, "example_pl", "Twoja siostra jest naprawdę utalentowana",
     "Twoja siostra jest naprawdę utalentowana muzycznie",
     "потеряна музыка"),
    (11756, "example_pl", "W czasie wojny ludzie głodowali",
     "W czasie wojny wielu ludzi musiało głodować",
     "потеряно «viele» и «mussten»"),
    (11757, "example_pl", "Zamówiłem koktajl w barze",
     "Zamawiam koktajl w barze", "в немецком настоящее время"),
    (14060, "example_en", "Notify me right away",
     "Notify me right away when he arrives", "потеряна вторая половина"),
    (14060, "example_uk", "Сповісти мене одразу",
     "Сповісти мене одразу, коли він прийде", "то же"),
    (14060, "example_tr", "Hemen bana haber ver",
     "O geldiğinde hemen bana haber ver", "то же"),
    (10637, "example_tr", "Bu bir aldatmaydı – o her zaman yalan söyledi",
     "Bu bir aldatmaydı – sürekli yalan söyledi",
     "«o her zaman» — порядок и лишнее местоимение"),
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
