"""B1, блок 39: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15465: (LIST, {"t_ru": "холод, холодность", "t_uk": "холод, мороз", "t_tr": "soğuk, soğukluk", "t_pl": "zimno, chłód"}),
    6909: (EN + " («movie» — американское)", {"x_en": "That was undoubtedly a good film"}),
    12556: ("убрать пометку (hovor.)", {"t_cs": "ošetřovna, marodka"}),
    12557: ("«Ich fühle mich fit» — пусто; " + LIST, {
        "t_ru": "в форме, бодрый", "t_uk": "у формі, бадьорий", "t_en": "fit, in shape", "t_tr": "formda, zinde",
        "t_pl": "w formie, sprawny",
        **all_x("Mit 70 ist mein Opa noch total fit", "В 70 мой дед ещё в отличной форме", "У 70 мій дід ще в чудовій формі",
                "At 70 my grandad is still really fit", "Dedem 70 yaşında hâlâ çok formda",
                "Mój dziadek w wieku 70 lat jest jeszcze w świetnej formie", "A 70 anni mio nonno è ancora in formissima",
                "Con 70 años mi abuelo sigue en plena forma", "À 70 ans, mon grand-père est encore en pleine forme",
                "Děda je v sedmdesáti pořád ve formě")}),
    2925: ("«Das ist unnötig» — пусто", {**all_x(
        "Mach dir keine unnötigen Sorgen", "Не волнуйся понапрасну", "Не хвилюйся марно", "Don't worry unnecessarily",
        "Boşuna endişelenme", "Nie martw się niepotrzebnie", "Non preoccuparti inutilmente",
        "No te preocupes innecesariamente", "Ne t'inquiète pas inutilement", "Zbytečně si nedělej starosti")}),
    10371: ("ru «Ты должен защищаться» — калька", {"x_ru": "Тебе надо защищаться от травли",
                                                  "x_uk": "Тобі треба захищатися від цькування"}),
    6912: (LIST, {"t_ru": "отношение, чехол", "t_uk": "відношення, чохол", "t_en": "relation, cover", "t_tr": "ilişki, kılıf",
                  "t_pl": "odniesienie, poszewka", "t_it": "il riferimento, la federa", "t_es": "la relación, la funda",
                  "t_fr": "le rapport, la housse", "t_cs": "souvislost, potah"}),
    10372: ("«Lass dich nicht von ihm schrecken» — так не говорят; " + LIST, {
        "t_ru": "пугать, испугать", "t_uk": "лякати, злякати", "t_en": "to scare, to frighten", "t_tr": "korkutmak, ürkütmek",
        "t_pl": "straszyć, przestraszyć",
        **all_x("Mich schreckt so schnell nichts", "Меня так просто не напугаешь", "Мене так просто не налякаєш",
                "It takes a lot to scare me", "Beni kolay kolay hiçbir şey korkutamaz", "Mnie tak łatwo nic nie przestraszy",
                "Non mi spaventa niente così facilmente", "A mí no me asusta nada tan fácilmente",
                "Rien ne m'effraie si facilement", "Mě jen tak něco nevystraší")}),
    14443: ("en «midget» — оскорбительно", {"t_en": "dwarf, gnome", "t_ru": "гном, карлик", "t_uk": "гном, карлик",
                                           "t_tr": "cüce, gnom", "t_pl": "krasnal, karzeł"}),
    13656: ("«den Helm … anzuziehen» — шлем надевают «aufsetzen»; убрать пометку (hovor.)", {
        "t_cs": "přilba, helma", "t_en": "helmet",
        **all_x("Vergiss nicht, beim Radfahren deinen Helm aufzusetzen", "Не забудь надеть шлем, когда едешь на велосипеде",
                "Не забудь надіти шолом, коли їдеш на велосипеді", "Don't forget to put your helmet on when you're cycling",
                "Bisiklete binerken kaskını takmayı unutma", "Nie zapomnij założyć kasku na rower",
                "Non dimenticare di mettere il casco quando vai in bici", "No olvides ponerte el casco cuando vayas en bici",
                "N'oublie pas de mettre ton casque quand tu fais du vélo", "Nezapomeň si na kolo nasadit helmu")}),
    12558: ("ru «ты должен быть натощак» — калька", {"x_ru": "Кровь сдают натощак", "x_uk": "Кров здають натщесерце"}),
    2629: (EN, {"x_en": "The car's got a scratch"}),
    18182: ("«… in diesem Café ist sehr gemütlich» — шаблон Atmosphäre; " + LIST, {
        "t_ru": "обстановка, учреждение", "t_uk": "обстановка, заклад", "t_en": "furnishings, institution",
        "t_tr": "mobilya, kurum", "t_pl": "umeblowanie, placówka", "t_it": "l'arredamento, la struttura",
        "t_es": "el mobiliario, la institución", "t_fr": "la décoration, l'établissement", "t_cs": "vybavení, instituce",
        **all_x("Die ganze Einrichtung ist neu", "Вся обстановка новая", "Уся обстановка нова", "All the furnishings are new",
                "Bütün mobilyalar yeni", "Całe umeblowanie jest nowe", "Tutto l'arredamento è nuovo",
                "Todo el mobiliario es nuevo", "Toute la décoration est neuve", "Celé vybavení je nové")}),
    17115: ("«Es gab einen schweren Autounfall» — шаблон Überfall; " + LIST, {
        "t_ru": "автомобильная авария, ДТП", "t_uk": "автомобільна аварія, ДТП", "t_pl": "wypadek samochodowy, kolizja",
        **all_x("Er hatte letztes Jahr einen Autounfall", "В прошлом году он попал в автомобильную аварию",
                "Торік він потрапив в автомобільну аварію", "He had a car accident last year",
                "Geçen yıl trafik kazası geçirdi", "W zeszłym roku miał wypadek samochodowy",
                "L'anno scorso ha avuto un incidente d'auto", "El año pasado tuvo un accidente de coche",
                "L'année dernière, il a eu un accident de voiture", "Loni měl autonehodu")}),
    1601: ("«Kommunikation ist wichtig» — пусто", {**all_x(
        "Bei uns hapert es an der Kommunikation", "У нас проблемы с общением", "У нас проблеми зі спілкуванням",
        "We've got a communication problem", "Bizde iletişim sorunu var", "U nas kuleje komunikacja",
        "Da noi la comunicazione non funziona", "Nos falla la comunicación", "Chez nous, c'est la communication qui coince",
        "U nás vázne komunikace")}),
    6913: ("снова Projekt; en «Your project really succeeded» — так не говорят", {"t_es": "logrado, exitoso", **all_x(
        "Die Party war echt gelungen", "Вечеринка действительно удалась", "Вечірка справді вдалася",
        "The party was a real success", "Parti gerçekten çok başarılıydı", "Impreza była naprawdę udana",
        "La festa è stata davvero riuscita", "La fiesta ha sido realmente exitosa", "La fête était vraiment réussie",
        "Ta párty se fakt povedla")}),
    17931: (EN + " («centimeter» — американское)", {"t_en": "centimetre", "x_en": "The child is 120 centimetres tall"}),
    14445: ("«Wir gehen heute zur Oper» — шаблон «gehen»", {**all_x(
        "Ich war noch nie in der Oper", "Я никогда не был в опере", "Я ніколи не був в опері", "I've never been to the opera",
        "Hiç operaya gitmedim", "Nigdy nie byłem w operze", "Non sono mai stato all'opera", "Nunca he ido a la ópera",
        "Je ne suis jamais allé à l'opéra", "Nikdy jsem nebyl v opeře")}),
    16077: ("«Die Polizei sucht den kriminellen Mann» — так не говорят", {**all_x(
        "So teure Preise sind ja fast schon kriminell!", "Такие цены — это уже почти криминал!",
        "Такі ціни — це вже майже кримінал!", "Prices like that are almost criminal!", "Bu fiyatlar neredeyse suç!",
        "Takie ceny to prawie przestępstwo!", "Prezzi così sono quasi criminali!", "¡Estos precios son casi criminales!",
        "Ces prix, c'est presque criminel!", "Takové ceny jsou skoro kriminální!")}),
    10375: ("«Das Kind gehorcht seinen Eltern» — учебник", {**all_x(
        "Der Hund gehorcht mir einfach nicht", "Собака меня просто не слушается", "Собака мене просто не слухається",
        "The dog just won't obey me", "Köpek bir türlü söz dinlemiyor", "Pies po prostu mnie nie słucha",
        "Il cane non mi ubbidisce proprio", "El perro no me obedece", "Le chien ne m'obéit pas du tout",
        "Pes mě vůbec neposlouchá")}),
}

SPLIT_LATER = {}
