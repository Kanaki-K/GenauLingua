"""B1, блок 53: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15036: ("«Wir gedenken unseres verstorbenen Großvaters» — книжно", {**all_x(
        "Das ist ein Foto von meinem verstorbenen Opa", "Это фото моего покойного деда", "Це фото мого покійного діда",
        "This is a photo of my late grandad", "Bu, merhum dedemin fotoğrafı", "To zdjęcie mojego zmarłego dziadka",
        "Questa è una foto del mio defunto nonno", "Es una foto de mi difunto abuelo",
        "C'est une photo de mon défunt grand-père", "To je fotka mého zesnulého dědy")}),
    2719: ("«Wir machen ein Picknick» — шаблон Ufer («Wir machen ein Picknick am Ufer …»)", {**all_x(
        "Bei dem Wetter ist ein Picknick im Park perfekt", "В такую погоду пикник в парке — то, что надо",
        "У таку погоду пікнік у парку — саме те", "In this weather a picnic in the park is perfect",
        "Bu havada parkta piknik harika olur", "Przy takiej pogodzie piknik w parku jest idealny",
        "Con questo tempo un picnic al parco è perfetto", "Con este tiempo, un pícnic en el parque es perfecto",
        "Par ce temps, un pique-nique au parc, c'est parfait", "Za takového počasí je piknik v parku ideální")}),
    17940: ("«Ich messe die Länge des Tisches mit dem Lineal» — учебник", {**all_x(
        "Hast du schon Fieber gemessen?", "Ты уже мерил температуру?", "Ти вже міряв температуру?",
        "Have you measured your temperature yet?", "Ateşini ölçtün mü?", "Mierzyłeś już gorączkę?",
        "Ti sei misurato la febbre?", "¿Ya te has medido la fiebre?", "Tu as déjà mesuré ta fièvre?",
        "Už sis měřil teplotu?")}),
    17792: ("ru «в строительной отрасли» — не совпадает с de (Finanz)", {**all_x(
        "Die Branche hat es gerade schwer", "Отрасли сейчас тяжело", "Галузі зараз важко",
        "The industry is having a hard time right now", "Sektör şu an zor günler geçiriyor", "Branża ma teraz ciężko",
        "Il settore è in difficoltà in questo momento", "El sector lo está pasando mal ahora",
        "La branche traverse une période difficile", "Obor to má teď těžké")}),
    7068: ("«Der Boxer schlägt zu …» — спорт-хроника; " + LIST, {
        "t_ru": "ударить, воспользоваться моментом", "t_uk": "ударити, скористатися моментом",
        "t_en": "to strike, to jump at the chance", "t_tr": "vurmak, fırsatı kapmak", "t_pl": "uderzyć, skorzystać z okazji",
        "t_it": "colpire, cogliere l'occasione", "t_es": "golpear, aprovechar", "t_fr": "frapper, sauter sur l'occasion",
        "t_cs": "udeřit, využít příležitost",
        **all_x("Bei dem Angebot musst du sofort zuschlagen!", "Надо сразу воспользоваться таким предложением!",
                "Такою пропозицією треба одразу скористатися!", "You've got to jump at an offer like that!",
                "Böyle bir teklifi hemen kapmalısın!", "Z takiej oferty trzeba od razu skorzystać!",
                "Un'offerta così devi coglierla subito!", "¡Tienes que aprovechar esta oferta enseguida!",
                "Il faut sauter sur une offre pareille!", "Takovou nabídku musíš hned využít!")}),
    7070: ("«Die Zahlung steht noch aus …» — бухгалтерия; живое — «nicht ausstehen können»", {
        "t_ru": "терпеть, быть в ожидании", "t_uk": "терпіти, бути в очікуванні", "t_en": "to stand, to be outstanding",
        "t_tr": "tahammül etmek, beklemede olmak", "t_pl": "znosić, pozostawać nieuregulowanym",
        "t_it": "sopportare, essere in sospeso", "t_es": "aguantar, estar pendiente", "t_fr": "supporter, être en attente",
        "t_cs": "vystát, být nevyřízený",
        **all_x("Ich kann es nicht ausstehen, wenn man mich anlügt", "Терпеть не могу, когда мне врут",
                "Терпіти не можу, коли мені брешуть", "I can't stand it when people lie to me",
                "Bana yalan söylenmesine tahammül edemiyorum", "Nie znoszę, kiedy ktoś mnie okłamuje",
                "Non sopporto quando mi mentono", "No aguanto que me mientan", "Je ne supporte pas qu'on me mente",
                "Nemůžu vystát, když mi někdo lže")}),
    13661: ("«Ich nähe mit einem roten Faden» — пусто", {**all_x(
        "Jetzt habe ich den Faden verloren", "Теперь я потерял нить", "Тепер я загубив нитку", "Now I've lost the thread",
        "Şimdi konunun ipini kaçırdım", "Zgubiłem nić rozmowy", "Ho perso il filo", "He perdido el hilo",
        "J'ai perdu le fil", "Ztratil jsem nit")}),
    18202: ("«Die Werkzeuge sind im Kasten» — пусто", {**all_x(
        "Für die Party kaufen wir zwei Kästen Bier", "На вечеринку купим два ящика пива", "На вечірку купимо два ящики пива",
        "We'll buy two crates of beer for the party", "Parti için iki kasa bira alacağız", "Na imprezę kupimy dwie skrzynki piwa",
        "Per la festa compriamo due casse di birra", "Para la fiesta compramos dos cajas de cerveza",
        "Pour la fête, on achète deux caisses de bière", "Na párty koupíme dvě bedny piva")}),
    16138: ("«Man beschuldigt ihn des Gelddiebstahls» — книжно", {**all_x(
        "Beschuldig mich nicht, ich war es nicht!", "Не обвиняй меня, это был не я!", "Не звинувачуй мене, це не я!",
        "Don't blame me, it wasn't me!", "Beni suçlama, ben yapmadım!", "Nie obwiniaj mnie, to nie ja!",
        "Non accusarmi, non sono stato io!", "¡No me culpes, no fui yo!", "Ne m'accuse pas, ce n'est pas moi!",
        "Neobviňuj mě, já to nebyl!")}),
    9783: ("ru «Могу ли я позаимствовать» — книжно", {"x_ru": "Можно позаимствовать твою книгу?"}),
    7071: ("«Der alte Mann geht mit seinem Stab» — сказка; " + LIST, {
        "t_ru": "палка, штаб", "t_uk": "палиця, штаб", "t_en": "rod, staff", "t_tr": "çubuk, kurmay kadro", "t_pl": "pręt, sztab",
        "t_it": "il bastone, lo staff", "t_es": "el bastón, el equipo", "t_fr": "le bâton, l'état-major", "t_cs": "hůl, štáb",
        **all_x("Der Präsident ist mit seinem ganzen Stab gekommen", "Президент приехал со всем своим штабом",
                "Президент приїхав з усім своїм штабом", "The president has come with his whole staff",
                "Başkan bütün kurmay kadrosuyla geldi", "Prezydent przyjechał z całym sztabem",
                "Il presidente è venuto con tutto il suo staff", "El presidente ha venido con todo su equipo",
                "Le président est venu avec tout son état-major", "Prezident přijel s celým svým štábem")}),
    15497: ("«Das Fell des Wolfes ist grau» — пусто; en «gray»", {**all_x(
        "Unsere Katze hat ein ganz weiches Fell", "У нашей кошки очень мягкая шерсть", "У нашої кішки дуже м'яка шерсть",
        "Our cat has really soft fur", "Kedimizin tüyleri çok yumuşak", "Nasz kot ma bardzo miękką sierść",
        "La nostra gatta ha il pelo morbidissimo", "Nuestra gata tiene un pelaje muy suave", "Notre chat a un pelage très doux",
        "Naše kočka má hodně jemnou srst")}),
    7072: (EN + " (время не совпадает)", {"x_en": "The police are tracking down the thief"}),
    7073: ("ru «Ты не должен вмешиваться» — калька", {**all_x(
        "Misch dich nicht in ihre Angelegenheiten ein", "Не лезь в их дела", "Не лізь у їхні справи",
        "Don't meddle in their affairs", "Onların işlerine karışma", "Nie wtrącaj się w ich sprawy",
        "Non immischiarti nei loro affari", "No te metas en sus asuntos", "Ne te mêle pas de leurs affaires",
        "Nepleť se do jejich věcí")}),
    13662: ("ru «Мой гардероб нуждается в новой одежде» — калька", {**all_x(
        "Deine Jacke kannst du an der Garderobe abgeben", "Куртку можешь сдать в гардероб", "Куртку можеш здати в гардероб",
        "You can leave your jacket at the cloakroom", "Ceketini vestiyere bırakabilirsin", "Kurtkę możesz zostawić w szatni",
        "Puoi lasciare la giacca al guardaroba", "Puedes dejar la chaqueta en el guardarropa",
        "Tu peux laisser ta veste au vestiaire", "Bundu můžeš odložit v šatně")}),
    14461: ("«Der Regisseur führt Regie» — масло масляное", {**all_x(
        "Bei diesem Film hat Tarantino Regie geführt", "Режиссуру этого фильма делал Тарантино",
        "Режисуру цього фільму робив Тарантіно", "Tarantino was in charge of directing this film",
        "Bu filmin yönetmenliğini Tarantino yaptı", "Reżyserię tego filmu objął Tarantino",
        "La regia di questo film è di Tarantino", "La dirección de esta película es de Tarantino",
        "La réalisation de ce film est signée Tarantino", "Režii tohoto filmu měl Tarantino")}),
    12586: (LIST, {"t_ru": "жалить, колоть", "t_uk": "жалити, колоти", "t_en": "to sting, to prick", "t_tr": "sokmak, batırmak",
                   "t_pl": "żądlić, kłuć", "t_es": "picar, pinchar"}),
    2185: ("«Die Annahme dieser Bedingungen ist notwendig» — договор; " + LIST, {
        "t_ru": "предположение, принятие", "t_uk": "припущення, прийняття", "t_en": "assumption, acceptance",
        "t_tr": "varsayım, kabul", "t_pl": "założenie, przyjęcie", "t_it": "l'ipotesi, l'accettazione",
        "t_es": "la suposición, la aceptación", "t_fr": "l'hypothèse, l'acceptation", "t_cs": "předpoklad, přijetí",
        **all_x("Ich gehe von der Annahme aus, dass er kommt", "Я исхожу из предположения, что он придёт",
                "Я виходжу з припущення, що він прийде", "I'm working on the assumption that he'll come",
                "Geleceği varsayımından hareket ediyorum", "Wychodzę z założenia, że przyjdzie",
                "Parto dall'ipotesi che venga", "Parto de la suposición de que vendrá",
                "Je pars de l'hypothèse qu'il va venir", "Vycházím z předpokladu, že přijde")}),
    15498: ("«Wir fahren in die nördliche Region» — так не говорят", {**all_x(
        "Hamburg liegt nördlich von Hannover", "Гамбург находится к северу от Ганновера", "Гамбург розташований на північ від Ганновера",
        "Hamburg is north of Hanover", "Hamburg, Hannover'in kuzeyinde", "Hamburg leży na północ od Hanoweru",
        "Amburgo si trova a nord di Hannover", "Hamburgo está al norte de Hannover", "Hambourg se trouve au nord de Hanovre",
        "Hamburk leží severně od Hannoveru")}),
    12587: ("«Nach der Fahrt fühlte ich mich benommen» — претерит; убрать пометку (fam.)", {
        "t_fr": "étourdi, sonné",
        **all_x("Nach der Narkose bin ich noch ganz benommen", "После наркоза я ещё как в тумане", "Після наркозу я ще як у тумані",
                "I'm still groggy after the anaesthetic", "Narkozdan sonra hâlâ sersemim", "Po narkozie jestem jeszcze oszołomiony",
                "Dopo l'anestesia sono ancora intontito", "Después de la anestesia aún estoy aturdido",
                "Après l'anesthésie, je suis encore sonné", "Po narkóze jsem ještě omámený")}),
    10461: ("«Er bekam Prügel …» — претерит; убрать пометку (fam.)", {"t_fr": "les coups, la raclée", **all_x(
        "Früher haben Kinder in der Schule Prügel bekommen", "Раньше детям в школе устраивали трёпку",
        "Колись у школі дітям давали прочухана", "Children used to get beatings at school",
        "Eskiden okulda çocuklar dayak yerdi", "Kiedyś w szkole dzieci dostawały lanie",
        "Una volta a scuola i bambini prendevano le botte", "Antes, en el colegio, a los niños les daban palizas",
        "Avant, à l'école, les enfants recevaient des coups", "Dřív děti ve škole dostávaly výprask")}),
}

REPLACE = [{"id": 11712, "by": 11687, "lang": "de", "why": "rühr — повелительная форма rühren"}]

SPLIT_LATER = {}
