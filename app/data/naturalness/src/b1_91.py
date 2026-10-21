"""B1, блок 91: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    9204: ("«… kam völlig unerwartet» — претерит; " + LIST, {
        "t_ru": "повышение, увеличение", "t_uk": "підвищення, збільшення", "t_en": "increase, rise", "t_tr": "artış, zam",
        "t_pl": "podwyżka, wzrost", "t_it": "l'aumento, il rialzo", "t_es": "el aumento, la subida", "t_fr": "l'augmentation, la hausse",
        "t_cs": "zvýšení",
        **all_x("Ab Januar gibt es eine Erhöhung der Miete um fünfzig Euro", "С января будет повышение аренды на пятьдесят евро",
                "З січня буде підвищення орендної плати на п'ятдесят євро",
                "From January there's going to be a rent increase of fifty euros",
                "Ocaktan itibaren kirada elli euro artış olacak", "Od stycznia będzie podwyżka czynszu o pięćdziesiąt euro",
                "Da gennaio ci sarà un aumento dell'affitto di cinquanta euro",
                "A partir de enero habrá una subida del alquiler de cincuenta euros",
                "À partir de janvier, il y aura une augmentation du loyer de cinquante euros",
                "Od ledna bude zvýšení nájmu o padesát eur")}),
    11372: ("в примере другое слово (Gewissenskonflikt), претерит", {**all_x(
        "Ich habe ein schlechtes Gewissen, weil ich Oma nicht angerufen habe",
        "Меня мучает совесть, потому что я не позвонил бабушке", "Мене мучить сумління, бо я не зателефонував бабусі",
        "I've got a guilty conscience because I didn't ring Grandma", "Anneanneme telefon etmediğim için vicdanım rahat değil",
        "Mam wyrzuty sumienia, bo nie zadzwoniłem do babci", "Ho la coscienza sporca perché non ho chiamato la nonna",
        "Me remuerde la conciencia porque no he llamado a la abuela",
        "J'ai mauvaise conscience parce que je n'ai pas appelé mamie", "Mám výčitky svědomí, protože jsem nezavolal babičce")}),
    14267: ("ru «над решением стоит вопросительный знак» — калька; " + LIST, {
        "t_ru": "вопросительный знак", "t_uk": "знак запитання", "t_en": "question mark", "t_tr": "soru işareti",
        "t_pl": "znak zapytania",
        **all_x("Im Spanischen steht das Fragezeichen auch am Anfang", "В испанском вопросительный знак ставят и в начале",
                "В іспанській знак запитання ставлять і на початку", "In Spanish the question mark goes at the beginning too",
                "İspanyolcada soru işareti başa da konuyor", "W hiszpańskim znak zapytania stawia się też na początku",
                "In spagnolo il punto interrogativo si mette anche all'inizio",
                "En español el signo de interrogación también va al principio",
                "En espagnol, le point d'interrogation se met aussi au début", "Ve španělštině se otazník píše i na začátku")}),
    17695: ("ru «твой ввод был неправильным» — так не говорят; " + LIST, {
        "t_ru": "ввод", "t_uk": "введення", "t_en": "input, entering", "t_tr": "giriş, girme", "t_pl": "wprowadzanie, wpisywanie",
        "t_it": "l'inserimento", "t_es": "la introducción, la entrada", "t_fr": "la saisie", "t_cs": "zadání, zadávání",
        **all_x("Bei der Eingabe vom Passwort habe ich mich vertippt", "При вводе пароля я опечатался",
                "Під час введення пароля я помилився", "I made a typo when I was entering the password",
                "Şifreyi girerken yanlış yazdım", "Przy wpisywaniu hasła zrobiłem literówkę",
                "Durante l'inserimento della password ho sbagliato a scrivere",
                "Me he equivocado en la introducción de la contraseña",
                "Je me suis trompé pendant la saisie du mot de passe", "Při zadávání hesla jsem se překlepl")}),
    2833: ("«Die Speise schmeckt gut» — пусто; " + LIST, {
        "t_ru": "блюдо, еда", "t_it": "il piatto, la pietanza", "t_fr": "le plat, le mets",
        **all_x("Warme Speisen gibt es bei uns nur bis 22 Uhr", "Горячие блюда у нас подают только до 22:00",
                "Гарячі страви в нас подають лише до 22:00", "We only serve hot food until 10 pm",
                "Sıcak yemekleri sadece saat 22'ye kadar servis ediyoruz", "Ciepłe potrawy podajemy tylko do 22:00",
                "I piatti caldi li serviamo solo fino alle 22", "Los platos calientes solo los servimos hasta las diez",
                "Nous servons des plats chauds seulement jusqu'à 22 heures", "Teplá jídla podáváme jen do deseti")}),
    1838: ("шаблон «gerne»; uk потерял «люблю»", {**all_x(
        "Bei Oma gibt es sonntags immer Schnitzel mit Pommes", "У бабушки по воскресеньям всегда шницель с картошкой фри",
        "У бабусі щонеділі завжди шніцель з картоплею фрі", "At Gran's we always have schnitzel and chips on Sundays",
        "Anneannemde pazar günleri hep patates kızartmalı şnitzel var", "U babci w niedziele zawsze jest sznycel z frytkami",
        "Dalla nonna la domenica c'è sempre la cotoletta con le patatine",
        "En casa de la abuela los domingos siempre hay escalope con patatas fritas",
        "Chez mamie, le dimanche, il y a toujours une escalope panée avec des frites",
        "U babičky je v neděli vždycky řízek s hranolky")}),
    14737: ("en «zodiac sign» → британское «star sign»", {
        "t_en": "star sign, zodiac sign", "x_en": "What's your star sign – Aries or Taurus?"}),
    9207: ("«kümmert sich um den Wald und die Bäume» — учебник", {**all_x(
        "Der Förster hat uns gezeigt, wo die Wildschweine schlafen", "Лесник показал нам, где спят кабаны",
        "Лісник показав нам, де сплять дики", "The forester showed us where the wild boar sleep",
        "Ormancı bize yaban domuzlarının nerede uyuduğunu gösterdi", "Leśniczy pokazał nam, gdzie śpią dziki",
        "Il guardaboschi ci ha mostrato dove dormono i cinghiali", "El guardabosques nos enseñó dónde duermen los jabalíes",
        "Le garde forestier nous a montré où dorment les sangliers", "Hajný nám ukázal, kde spí divočáci")}),
    17698: ("пометка (hovor.); " + LIST, {
        "t_ru": "маркер, фломастер", "t_uk": "маркер, фломастер", "t_en": "marker, marker pen", "t_tr": "keçeli kalem, işaretleyici",
        "t_pl": "marker, pisak", "t_it": "il pennarello, l'evidenziatore", "t_cs": "popisovač, fixa"}),
    8311: ("en «I just came home» — так не говорят", {
        "x_ru": "Я только что пришёл домой и совсем без сил",
        "x_en": "I've just got home and I'm completely knackered"}),
    8312: ("порядок слов «duften wunderbar im Garten»; " + LIST, {
        "t_ru": "пахнуть, благоухать", "t_uk": "пахнути, пахтіти", "t_tr": "güzel kokmak", "t_it": "profumare", "t_es": "oler bien",
        "t_fr": "sentir bon",
        **all_x("Im Garten duften die Rosen wunderbar", "В саду чудесно пахнут розы", "У саду чудово пахнуть троянди",
                "The roses smell wonderful in the garden", "Bahçede güller harika kokuyor", "W ogrodzie pięknie pachną róże",
                "In giardino le rose profumano meravigliosamente", "En el jardín las rosas huelen de maravilla",
                "Dans le jardin, les roses sentent merveilleusement bon", "Na zahradě nádherně voní růže")}),
    12359: (LIST + " (было четыре значения)", {
        "t_ru": "трасса, взлётная полоса", "t_uk": "траса, злітна смуга", "t_en": "slope, runway", "t_tr": "pist",
        "t_pl": "trasa narciarska, stok", "t_cs": "sjezdovka, dráha"}),
    8313: ("en «refresh my English» — так не говорят; " + LIST, {
        "t_ru": "освежить, подтянуть", "t_uk": "освіжити, підтягнути", "t_en": "to brush up, to refresh", "t_tr": "tazelemek",
        "t_pl": "odświeżyć, podszlifować", "t_cs": "oprášit, osvěžit",
        "x_en": "I need to brush up my English before I go to London"}),
    14271: ("«eine mobile Lösung für unterwegs» — реклама; " + LIST, {
        "t_ru": "мобильный, подвижный", "t_uk": "мобільний, рухливий", "t_en": "mobile", "t_tr": "mobil, hareketli",
        "t_pl": "mobilny", "t_it": "mobile", "t_es": "móvil, con movilidad", "t_fr": "mobile", "t_cs": "mobilní, pohyblivý",
        **all_x("Seit der Knie-OP ist Opa wieder richtig mobil", "После операции на колене дедушка снова подвижен",
                "Після операції на коліні дідусь знову рухливий", "Since his knee operation Grandad's been really mobile again",
                "Diz ameliyatından sonra dedem yine hareketli", "Od operacji kolana dziadek znowu jest mobilny",
                "Dopo l'operazione al ginocchio il nonno è di nuovo mobile",
                "Tras la operación de rodilla, el abuelo vuelve a tener movilidad",
                "Depuis son opération du genou, papi est de nouveau mobile", "Od operace kolena je děda zase pohyblivý")}),
    12361: (LIST, {"t_ru": "финал", "t_uk": "фінал", "t_en": "final", "t_tr": "final", "t_pl": "finał", "t_it": "la finale",
                   "t_es": "la final", "t_fr": "la finale", "t_cs": "finále"}),
    18893: ("en «came late to class» — так не говорят; " + LIST, {
        "t_ru": "зачастую, часто", "t_uk": "часто, нерідко", "t_en": "often, frequently", "t_tr": "sıklıkla, çoğu zaman",
        "t_pl": "często, niejednokrotnie", "t_es": "a menudo, con frecuencia", "x_en": "I was often late for class"}),
    14742: ("«… erklang laut, als der Präsident … betrat» — претерит, книжно; " + LIST, {
        "t_ru": "фанфара, фанфары", "t_uk": "фанфара", "t_en": "fanfare", "t_tr": "fanfar", "t_it": "la fanfara",
        "t_es": "la fanfarria", "t_fr": "la fanfare",
        **all_x("Wenn ein Tor fällt, spielt die Kapelle eine Fanfare", "Когда забивают гол, оркестр играет фанфары",
                "Коли забивають гол, оркестр грає фанфару", "When a goal goes in, the band plays a fanfare",
                "Gol olunca bando bir fanfar çalıyor", "Kiedy pada gol, orkiestra gra fanfarę",
                "Quando segnano un gol, la banda suona una fanfara", "Cuando hay un gol, la banda toca una fanfarria",
                "Quand il y a un but, l'orchestre joue une fanfare", "Když padne gól, kapela zahraje fanfáru")}),
    11378: ("en «I trust he will be able to complete this task» — книжно; " + LIST, {
        "t_ru": "считать способным, верить", "t_uk": "вважати здатним, вірити", "t_en": "to think someone capable, to trust",
        "t_tr": "yapabileceğine inanmak, kendine güvenmek", "t_pl": "wierzyć w kogoś, uważać za zdolnego",
        "t_it": "ritenere capace, osare", "t_es": "creer capaz, atreverse", "t_fr": "croire capable, oser",
        "t_cs": "věřit, troufnout si",
        "x_en": "I think he's capable of doing it", "x_tr": "Bu işi yapabileceğine inanıyorum"}),
    11955: ("«Sie wollten das Fass anzapfen …» — вымученно; " + LIST + " (было четыре значения)", {
        "t_ru": "откупорить бочку, подключиться", "t_uk": "відкрити бочку, підключитися", "t_en": "to tap",
        "t_tr": "fıçıyı açmak, hatta bağlanmak", "t_pl": "otworzyć beczkę, podłączyć się", "t_it": "spillare, intercettare",
        "t_es": "pinchar, intervenir", "t_fr": "mettre en perce, mettre sur écoute", "t_cs": "narazit, napíchnout",
        **all_x("Auf dem Dorffest zapft der Bürgermeister das erste Fass an",
                "На деревенском празднике мэр откупоривает первую бочку", "На сільському святі мер відкриває першу бочку",
                "At the village fete the mayor taps the first barrel", "Köy şenliğinde belediye başkanı ilk fıçıyı açıyor",
                "Na festynie wiejskim wójt otwiera pierwszą beczkę", "Alla festa del paese il sindaco spilla la prima botte",
                "En la fiesta del pueblo el alcalde pincha el primer barril",
                "À la fête du village, le maire met le premier fût en perce", "Na vesnické slavnosti starosta narazí první sud")}),
    13026: ("пометка (fam.); uk «склянок вина»; " + LIST, {
        "t_ru": "навеселе, затуманенный", "t_uk": "напідпитку, затуманений", "t_en": "tipsy, dazed", "t_tr": "çakırkeyif, sersem",
        "t_pl": "podpity, zamroczony", "t_it": "brillo, stordito", "t_es": "achispado, aturdido", "t_fr": "éméché, étourdi",
        "t_cs": "přiopilý, omámený", "x_uk": "Після трьох келихів вина він був трохи напідпитку"}),
    1424: ("в примере другое слово (Fitness-Studio); en потерял слово", {
        "t_tr": "fitness, form", "t_pl": "fitness, kondycja", "t_cs": "kondice, fitness",
        **all_x("Für meine Fitness gehe ich jeden Tag eine Stunde spazieren", "Для поддержания физической формы я каждый день час гуляю",
                "Для фізичної форми я щодня годину гуляю", "I go for an hour's walk every day for my fitness",
                "Formumu korumak için her gün bir saat yürüyorum", "Dla kondycji codziennie chodzę na godzinny spacer",
                "Per la forma fisica faccio ogni giorno un'ora di passeggiata",
                "Para mantener la forma física, paseo una hora cada día",
                "Pour ma forme physique, je marche une heure tous les jours",
                "Kvůli kondici chodím každý den hodinu na procházku")}),
    8314: ("«…, die ich gut verstanden hab» — натянуто; " + LIST, {
        "t_ru": "подробный, детальный", "t_en": "detailed, in detail", "t_tr": "ayrıntılı, detaylı", "t_pl": "szczegółowy",
        "t_it": "dettagliato", "t_es": "detallado", "t_fr": "détaillé", "t_cs": "podrobný, detailní",
        **all_x("Kannst du mir das bitte etwas detaillierter erklären?", "Можешь объяснить мне это чуть подробнее?",
                "Можеш пояснити мені це трохи детальніше?", "Could you explain that to me in a bit more detail?",
                "Bunu bana biraz daha ayrıntılı anlatabilir misin?", "Możesz mi to wyjaśnić trochę bardziej szczegółowo?",
                "Puoi spiegarmelo in modo un po' più dettagliato?", "¿Me lo puedes explicar de forma un poco más detallada?",
                "Tu peux m'expliquer ça de façon un peu plus détaillée?", "Můžeš mi to vysvětlit trochu podrobněji?")}),
    2954: ("en «gift» → британское «present»; " + LIST, {
        "t_ru": "упаковать, завернуть", "t_uk": "запакувати, загорнути", "t_en": "to wrap, to pack", "t_tr": "paketlemek, sarmak",
        "t_pl": "zapakować, owijać", "t_it": "impacchettare, incartare", "t_es": "envolver, empaquetar", "t_fr": "emballer, envelopper",
        "t_cs": "zabalit", "x_en": "Can you wrap the present nicely?"}),
    8316: ("«eine indirekte Frage, keine direkte» — пусто; " + LIST, {
        "t_ru": "косвенный, непрямой", "t_en": "indirect", "t_tr": "dolaylı",
        **all_x("Er hat mir indirekt gesagt, dass ich zu viel rede", "Он косвенно дал мне понять, что я слишком много говорю",
                "Він непрямо дав мені зрозуміти, що я забагато говорю", "He told me indirectly that I talk too much",
                "Bana dolaylı yoldan çok konuştuğumu söyledi", "Dał mi pośrednio do zrozumienia, że za dużo mówię",
                "Mi ha detto in modo indiretto che parlo troppo", "Me dijo de forma indirecta que hablo demasiado",
                "Il m'a dit de façon indirecte que je parle trop", "Nepřímo mi naznačil, že moc mluvím")}),
    8317: ("в примере другое слово (Zeltpflock); " + LIST, {
        "t_ru": "колышек, кол", "t_uk": "кілок, кіл", "t_en": "stake, peg", "t_tr": "kazık", "t_pl": "palik, kołek",
        "t_it": "il paletto, il picchetto", "t_es": "la estaca", "t_fr": "le piquet", "t_cs": "kolík, kůl",
        **all_x("Für die Tomaten habe ich einen Pflock in die Erde geschlagen", "Для помидоров я вбил в землю колышек",
                "Для помідорів я вбив у землю кілок", "I've knocked a stake into the ground for the tomatoes",
                "Domatesler için toprağa bir kazık çaktım", "Do pomidorów wbiłem w ziemię palik",
                "Per i pomodori ho piantato un paletto nel terreno", "Para los tomates he clavado una estaca en la tierra",
                "Pour les tomates, j'ai planté un piquet dans la terre", "K rajčatům jsem zatloukl do země kolík")}),
    15787: ("«… versteckte sich» — претерит; " + LIST, {
        "t_ru": "зверёк, букашка", "t_uk": "звірятко, комашка", "t_en": "little animal, little creature", "t_tr": "hayvancık, küçük hayvan",
        "t_pl": "zwierzątko, robaczek", "t_it": "l'animaletto, la bestiolina", "t_es": "el animalito, el bichito",
        "t_fr": "la petite bête, la bestiole", "t_cs": "zvířátko",
        **all_x("Schau mal, da krabbelt ein kleines Tierchen auf deinem Arm", "Смотри, у тебя по руке ползёт какая-то букашка",
                "Дивись, у тебе по руці повзе якась комашка", "Look, there's a little creature crawling on your arm",
                "Bak, kolunda küçük bir hayvancık yürüyor", "Patrz, po ręce chodzi ci jakiś robaczek",
                "Guarda, c'è una bestiolina che ti cammina sul braccio", "Mira, tienes un bichito subiéndote por el brazo",
                "Regarde, il y a une petite bête qui te grimpe sur le bras", "Podívej, leze ti po ruce nějaké zvířátko")}),
    2337: ("«Das ist eine demokratische Entscheidung» — пусто", {**all_x(
        "Wohin wir in den Urlaub fahren, entscheiden wir ganz demokratisch", "Куда поехать в отпуск, мы решаем демократично",
        "Куди поїхати у відпустку, ми вирішуємо демократично", "We decide democratically where we go on holiday",
        "Tatile nereye gideceğimize demokratik bir şekilde karar veriyoruz",
        "O tym, dokąd jedziemy na urlop, decydujemy demokratycznie",
        "Dove andare in vacanza lo decidiamo in modo democratico", "Adónde vamos de vacaciones lo decidimos de forma democrática",
        "On décide de manière démocratique où on part en vacances", "Kam pojedeme na dovolenou, rozhodujeme demokraticky")}),
    12457: ("«Wir segelten um …» — претерит", {
        "t_tr": "burun",
        **all_x("Am Kap weht fast immer ein starker Wind", "На мысе почти всегда дует сильный ветер",
                "На мисі майже завжди дме сильний вітер", "There's almost always a strong wind on the cape",
                "Burunda neredeyse her zaman sert bir rüzgâr esiyor", "Na przylądku prawie zawsze wieje silny wiatr",
                "Sul capo soffia quasi sempre un vento forte", "En el cabo casi siempre sopla un viento fuerte",
                "Sur le cap, il y a presque toujours un vent fort", "Na mysu skoro pořád fouká silný vítr")}),
    8325: (LIST + " (было четыре значения)", {
        "t_ru": "топать, толочь", "t_uk": "тупотіти, товкти", "t_en": "to stomp, to mash", "t_tr": "ayak vurmak, ezmek",
        "t_pl": "tupać, tłuc", "t_it": "battere i piedi, schiacciare", "t_es": "patear, machacar", "t_fr": "taper du pied, écraser",
        "t_cs": "dupat, rozmačkat",
        **all_x("Für das Püree stampfe ich die Kartoffeln einfach mit der Gabel", "Для пюре я просто толку картошку вилкой",
                "Для пюре я просто товчу картоплю виделкою", "For the mash I just mash the potatoes with a fork",
                "Püre için patatesleri çatalla eziyorum", "Na purée po prostu tłukę ziemniaki widelcem",
                "Per il purè schiaccio le patate con la forchetta", "Para el puré machaco las patatas con un tenedor",
                "Pour la purée, j'écrase les pommes de terre à la fourchette", "Na kaši brambory prostě rozmačkám vidličkou")}),
    1146: ("«Bitte geben Sie Ihre Anschrift an» — текст анкеты; " + LIST, {
        "t_ru": "адрес", "t_uk": "адреса", "t_en": "address", "t_tr": "adres", "t_pl": "adres", "t_es": "la dirección",
        **all_x("Schick mir deine Anschrift, dann kommt die Einladung per Post",
                "Пришли мне свой адрес, и приглашение придёт по почте", "Надішли мені свою адресу, і запрошення прийде поштою",
                "Send me your address and the invitation will come by post", "Bana adresini gönder, davetiye postayla gelsin",
                "Wyślij mi swój adres, to zaproszenie przyjdzie pocztą", "Mandami il tuo indirizzo e l'invito ti arriva per posta",
                "Mándame tu dirección y la invitación te llega por correo",
                "Envoie-moi ton adresse, et l'invitation arrivera par la poste", "Pošli mi svou adresu a pozvánka ti přijde poštou")}),
    15367: ("пометки (fam./hovor.); en «piglet» — просто поросёнок; " + LIST, {
        "t_ru": "кабанёнок, новичок", "t_uk": "кабанчик, новачок", "t_en": "boar piglet, newbie",
        "t_tr": "yaban domuzu yavrusu, çaylak", "t_pl": "warchlak, nowicjusz", "t_fr": "le marcassin, le bleu",
        "t_cs": "sele divočáka, zelenáč", "x_en": "The little boar piglet is playing in the mud",
        "x_uk": "Маленький кабанчик грається в багнюці"}),
    8327: ("«…, man sieht alles» — пусто", {**all_x(
        "Die Bluse ist ziemlich durchsichtig, zieh lieber ein Top drunter",
        "Блузка довольно прозрачная, надень лучше под неё топ", "Блузка досить прозора, краще вдягни під неї топ",
        "The blouse is quite see-through, better wear a top underneath", "Bluz epey şeffaf, altına bir atlet giysen iyi olur",
        "Bluzka jest dość prześwitująca, lepiej załóż pod spód top",
        "La camicetta è piuttosto trasparente, meglio mettere sotto una canottiera",
        "La blusa es bastante transparente, mejor ponte un top debajo",
        "Le chemisier est assez transparent, mets plutôt un top dessous", "Halenka je dost průhledná, radši si pod ni vezmi tílko")}),
    17700: ("en «favorite» — американское", {"x_en": "My favourite radio station always plays good music"}),
    12362: ("en «kilometers» — американское; " + LIST, {
        "t_ru": "гоночная трасса, трек", "t_en": "race track, circuit", "x_en": "The new race track is 5 kilometres long"}),
    8330: ("«Das ist ein Doppel vom Original» — пусто; " + LIST, {
        "t_ru": "дубликат, парный разряд", "t_uk": "дублікат, парний розряд", "t_en": "duplicate, doubles",
        "t_tr": "kopya, çiftler maçı", "t_pl": "duplikat, debel", "t_it": "il duplicato, il doppio", "t_es": "el duplicado, los dobles",
        "t_fr": "le double", "t_cs": "duplikát, čtyřhra",
        **all_x("Am Samstag spielen wir Tennis im Doppel", "В субботу мы играем в теннис в парном разряде",
                "У суботу ми граємо в теніс у парному розряді", "On Saturday we're playing doubles at tennis",
                "Cumartesi teniste çiftler maçı oynuyoruz", "W sobotę gramy w tenisa w deblu",
                "Sabato giochiamo un doppio a tennis", "El sábado jugamos un partido de dobles de tenis",
                "Samedi, on joue un double au tennis", "V sobotu hrajeme tenis ve čtyřhře")}),
    18894: (LIST, {"t_pl": "czesać", "t_it": "pettinare", "t_es": "peinar", "t_fr": "peigner"}),
}

REPLACE = [
    {"id": 8309, "by": 1064, "lang": "de", "why": "gewünscht — форма слова wünschen"},
]

SPLIT_LATER = {}
