"""A2, блок 10: слова 361–400 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist gemütlich/gut») — так о вещи не говорят"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
WEAR = "«trägt ein/eine …» — уже у Hose, Kleid, Anzug; у каждой одежды свой пример"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1016: (LIST, {"t_ru": "болеть, делать больно", "t_uk": "боліти, робити боляче", "t_en": "to hurt",
                  "t_tr": "ağrımak, acıtmak", "t_pl": "boleć"}),
    1561: ("ru «Меня это интересует» — тот же пример, что у Interesse; " + LIST, {
        "t_tr": "ilgilendirmek, ilgilenmek", "t_pl": "interesować, interesować się",
        **all_x("Interessierst du dich für Musik?", "Ты интересуешься музыкой?", "Ти цікавишся музикою?",
                "Are you interested in music?", "Müzikle ilgileniyor musun?", "Interesujesz się muzyką?",
                "Ti interessa la musica?", "¿Te interesa la música?", "Tu t'intéresses à la musique?",
                "Zajímáš se o hudbu?")}),
    1964: (EN + " («I dream of a trip»); " + LIST, {
        "t_ru": "мечтать, видеть сон", "t_uk": "мріяти, бачити сон", "t_en": "to dream",
        "t_tr": "hayal kurmak, rüya görmek",
        **all_x("Ich träume von einer Reise nach Japan", "Я мечтаю о поездке в Японию", "Я мрію про подорож до Японії",
                "I dream of going to Japan", "Japonya'ya gitmeyi hayal ediyorum", "Marzę o podróży do Japonii",
                "Sogno un viaggio in Giappone", "Sueño con viajar a Japón", "Je rêve d'aller au Japon",
                "Sním o cestě do Japonska")}),
    765: (TWO + " («рок» — омоним); " + WEAR, {
        "t_ru": "юбка", "t_uk": "спідниця", "t_en": "skirt", "t_tr": "etek", "t_pl": "spódnica", "t_it": "la gonna",
        "t_es": "la falda", "t_fr": "la jupe", "t_cs": "sukně",
        **all_x("Der Rock ist mir zu kurz", "Эта юбка мне коротковата", "Ця спідниця для мене закоротка",
                "This skirt is too short for me", "Bu etek bana çok kısa", "Ta spódnica jest dla mnie za krótka",
                "Questa gonna mi sta troppo corta", "Esta falda me queda demasiado corta",
                "Cette jupe est trop courte pour moi", "Ta sukně je mi moc krátká")}),
    2760: ("«верхом в парке» — так не катаются; " + LIST, {
        "t_ru": "ездить верхом", "t_uk": "їздити верхи", "t_en": "to ride (a horse)", "t_tr": "ata binmek",
        "t_pl": "jeździć konno", "t_it": "andare a cavallo", "t_es": "montar a caballo",
        "t_fr": "faire du cheval, monter à cheval",
        **all_x("Meine Tochter reitet seit zwei Jahren", "Моя дочь уже два года ездит верхом",
                "Моя донька вже два роки їздить верхи", "My daughter has been riding for two years",
                "Kızım iki yıldır ata biniyor", "Moja córka od dwóch lat jeździ konno",
                "Mia figlia va a cavallo da due anni", "Mi hija monta a caballo desde hace dos años",
                "Ma fille fait du cheval depuis deux ans", "Moje dcera jezdí na koni už dva roky")}),
    2128: ("«Ты должен сейчас … выслушать» — калька с musst; " + LIST, {
        "t_ru": "слушать, выслушивать", "t_uk": "слухати, вислуховувати", "t_en": "to listen", "t_tr": "dinlemek",
        "t_pl": "słuchać", "x_ru": "Сейчас послушай меня внимательно", "x_uk": "Тепер послухай мене уважно",
        "x_en": "Now listen to me carefully"}),
    1327: (LIST, {"t_ru": "чёткий, ясный", "t_uk": "чіткий, ясний", "t_en": "clear, distinct",
                  "t_tr": "anlaşılır, net", "t_pl": "wyraźny", "t_it": "chiaro, nitido", "t_es": "claro, nítido",
                  "t_fr": "clair, net", "t_cs": "zřetelný, jasný"}),
    397: (WEAR, {"t_ru": "рубашка", **all_x(
        "Das Hemd muss ich noch bügeln", "Эту рубашку мне ещё надо погладить", "Цю сорочку мені ще треба попрасувати",
        "I still need to iron this shirt", "Bu gömleği daha ütülemem lazım", "Muszę jeszcze wyprasować tę koszulę",
        "Devo ancora stirare questa camicia", "Todavía tengo que planchar esta camisa",
        "Je dois encore repasser cette chemise", "Tu košili ještě musím vyžehlit")}),
    794: (SKEL, {**all_x(
        "Die Wohnung hat zwei Schlafzimmer", "В квартире две спальни", "У квартирі дві спальні",
        "The flat has two bedrooms", "Dairede iki yatak odası var", "Mieszkanie ma dwie sypialnie",
        "L'appartamento ha due camere da letto", "El piso tiene dos dormitorios", "L'appartement a deux chambres",
        "Byt má dvě ložnice")}),
    2077: (LIST, {"t_ru": "предложение, идея", "t_uk": "пропозиція, ідея", "t_en": "suggestion, proposal",
                  "t_tr": "öneri, teklif", "t_pl": "propozycja, sugestia"}),
    9728: ("«У бедного человека нет денег» — масло масляное; " + LIST, {
        "t_ru": "бедный", "t_uk": "бідний", "t_en": "poor", "t_tr": "fakir, zavallı", "t_pl": "biedny",
        **all_x("Viele Familien hier sind arm", "Многие семьи здесь бедные", "Багато родин тут бідні",
                "Many families here are poor", "Buradaki birçok aile fakir", "Wiele rodzin tutaj jest biednych",
                "Molte famiglie qui sono povere", "Muchas familias aquí son pobres",
                "Beaucoup de familles ici sont pauvres", "Hodně rodin tady je chudých")}),
    331: (SKEL + "; " + LIST, {
        "t_ru": "прибор, устройство", "t_uk": "пристрій, прилад", "t_en": "device, appliance", "t_tr": "cihaz, alet",
        "t_pl": "urządzenie, sprzęt", "t_it": "l'apparecchio, il dispositivo",
        **all_x("Mach bitte alle Geräte aus", "Выключи, пожалуйста, все приборы", "Вимкни, будь ласка, всі прилади",
                "Please switch off all the devices", "Lütfen bütün cihazları kapat",
                "Wyłącz, proszę, wszystkie urządzenia", "Spegni tutti gli apparecchi, per favore",
                "Apaga todos los aparatos, por favor", "Éteins tous les appareils, s'il te plaît",
                "Vypni prosím všechny přístroje")}),
    13900: (LIST + "; tr «memnuniyetle» — книжно", {
        "t_ru": "отвечать (на что-то)", "t_uk": "відповідати (на щось)", "t_en": "to answer", "t_tr": "cevaplamak",
        "t_pl": "odpowiadać", "x_tr": "Bu soruyu seve seve cevaplarım", "x_es": "Respondo encantado a la pregunta"}),
    1065: ("«Die Zahl 42 ist meine Lieblingszahl» — неживо; " + LIST, {
        "t_ru": "число, цифра", "t_uk": "число, цифра", "t_en": "number, figure", "t_tr": "sayı, rakam",
        "t_pl": "liczba, cyfra", "t_cs": "číslo, číslice",
        **all_x("Kannst du die Zahl noch mal sagen?", "Можешь ещё раз назвать число?", "Можеш ще раз назвати число?",
                "Can you say the number again?", "Sayıyı bir daha söyler misin?",
                "Możesz jeszcze raz powtórzyć tę liczbę?", "Puoi ripetere il numero?", "¿Puedes repetir el número?",
                "Tu peux redire le nombre?", "Můžeš to číslo zopakovat?")}),
    123: (TWO + " («пьяный» — разговорное значение, своя строка)", {
        "t_ru": "синий, голубой", "t_uk": "синій, блакитний", "t_en": "blue", "t_tr": "mavi", "t_pl": "niebieski",
        "t_it": "blu, azzurro", "t_es": "azul", "t_fr": "bleu", "t_cs": "modrý"}),
    628: ("«Ich entsorge den Müll» — язык инструкций; " + LIST, {
        "t_ru": "мусор", "t_uk": "сміття", "t_en": "rubbish, trash", "t_tr": "çöp", "t_pl": "śmieci",
        **all_x("Bringst du bitte den Müll raus?", "Вынесешь, пожалуйста, мусор?", "Винесеш, будь ласка, сміття?",
                "Could you take the rubbish out, please?", "Çöpü çıkarır mısın lütfen?", "Wyniesiesz, proszę, śmieci?",
                "Puoi portare fuori la spazzatura, per favore?", "¿Puedes sacar la basura, por favor?",
                "Tu peux descendre les ordures, s'il te plaît?", "Vyneseš prosím odpadky?")}),
    15414: (EN, {"t_uk": "темрява", "x_en": "I can't see anything in the dark"}),
    726: ("«практичное решение проблемы» — канцелярски; " + LIST, {
        "t_ru": "практичный, удобный", "t_uk": "практичний, зручний", "t_en": "practical, handy",
        "t_tr": "pratik, kullanışlı", "t_pl": "praktyczny, wygodny", "t_it": "pratico, comodo",
        "t_es": "práctico, cómodo", "t_fr": "pratique", "t_cs": "praktický, šikovný",
        **all_x("Die Tasche ist echt praktisch", "Эта сумка очень удобная", "Ця сумка дуже зручна",
                "This bag is really handy", "Bu çanta çok kullanışlı", "Ta torba jest naprawdę praktyczna",
                "Questa borsa è davvero pratica", "Este bolso es muy práctico", "Ce sac est vraiment pratique",
                "Ta taška je fakt praktická")}),
    266: (SKEL, {**all_x(
        "Mach bitte den Fernseher leiser", "Сделай, пожалуйста, телевизор потише", "Зроби, будь ласка, телевізор тихіше",
        "Turn the TV down, please", "Televizyonun sesini kıs lütfen", "Przycisz, proszę, telewizor",
        "Abbassa la tv, per favore", "Baja la tele, por favor", "Baisse la télé, s'il te plaît",
        "Ztlum prosím televizi")}),
    2048: (LIST + "; uk «пропустив поїзд» — калька", {
        "t_ru": "пропустить, опоздать на", "t_uk": "пропустити, запізнитися на", "t_tr": "kaçırmak",
        "t_pl": "przegapić, spóźnić się na", "x_uk": "Я запізнився на поїзд"}),
    600: (SKEL, {**all_x(
        "Was gibt's zum Mittagessen?", "Что у нас на обед?", "Що в нас на обід?", "What's for lunch?",
        "Öğle yemeğinde ne var?", "Co jest na obiad?", "Cosa c'è per pranzo?", "¿Qué hay para almorzar?",
        "Qu'est-ce qu'il y a pour le déjeuner?", "Co je k obědu?")}),
    13901: (LIST, {"t_ru": "пока", "t_uk": "бувай", "t_en": "bye", "t_tr": "hoşça kal, görüşürüz",
                   "t_pl": "cześć, pa", "t_es": "adiós, chao"}),
    572: (WEAR + "; " + LIST, {
        "t_ru": "пальто", "t_uk": "пальто", "t_en": "coat", "t_tr": "palto, kaban", "t_pl": "płaszcz",
        **all_x("Nimm einen Mantel mit, es wird kalt", "Возьми пальто, будет холодно", "Візьми пальто, буде холодно",
                "Take a coat, it's going to be cold", "Yanına palto al, hava soğuyacak", "Weź płaszcz, będzie zimno",
                "Prendi il cappotto, farà freddo", "Llévate el abrigo, que va a hacer frío",
                "Prends un manteau, il va faire froid", "Vezmi si kabát, bude zima")}),
    1013: (LIST + "; «Я хочу обменять» — грубее, чем möchte", {
        "t_ru": "менять, обменивать", "t_uk": "міняти, обмінювати", "t_en": "to change, to exchange",
        "t_tr": "değiştirmek, bozdurmak", "t_pl": "wymieniać, zmieniać",
        "x_ru": "Я хотел бы обменять евро на доллары", "x_uk": "Я хотів би обміняти євро на долари",
        "x_en": "I'd like to change euros into dollars"}),
    6585: ("«Versteck dich schnell» — из игры в прятки; " + LIST, {
        "t_ru": "прятать, прятаться", "t_uk": "ховати, ховатися", "t_en": "to hide", "t_tr": "saklamak, saklanmak",
        "t_pl": "chować, ukrywać",
        **all_x("Wo hast du die Schlüssel versteckt?", "Куда ты спрятал ключи?", "Куди ти сховав ключі?",
                "Where did you hide the keys?", "Anahtarları nereye sakladın?", "Gdzie schowałeś klucze?",
                "Dove hai nascosto le chiavi?", "¿Dónde has escondido las llaves?", "Où est-ce que tu as caché les clés?",
                "Kam jsi schoval klíče?")}),
    1920: (LIST, {"t_ru": "строгий", "t_uk": "суворий, строгий", "t_en": "strict", "t_tr": "katı, sert",
                  "t_pl": "surowy",
                  **all_x("Unsere Lehrerin ist sehr streng", "Наша учительница очень строгая", "Наша вчителька дуже сувора",
                          "Our teacher is very strict", "Öğretmenimiz çok katı", "Nasza nauczycielka jest bardzo surowa",
                          "La nostra maestra è molto severa", "Nuestra profesora es muy estricta",
                          "Notre prof est très stricte", "Naše učitelka je hodně přísná")}),
    2810: ("«о 20 годині», «at 8 in the evening» — так время не называют; " + LIST, {
        "t_ru": "передача, посылка", "t_uk": "передача, посилка", "t_en": "show, shipment", "t_tr": "program, gönderi",
        "t_pl": "program, przesyłka", "t_it": "la trasmissione, la spedizione", "t_es": "el programa, el envío",
        "t_fr": "l'émission, l'envoi", "t_cs": "pořad, zásilka",
        "x_ru": "Передача идёт в восемь вечера", "x_uk": "Передача йде о восьмій вечора",
        "x_en": "The show is on at 8 pm", "x_tr": "Program saat sekizde", "x_pl": "Program leci o ósmej",
        "x_it": "La trasmissione va in onda alle otto", "x_es": "El programa es a las ocho",
        "x_cs": "Pořad běží ve 20 hodin"}),
    6598: ("перевод — список из семи слов; «Mir fehlen die Mittel» — книжно", {
        "t_ru": "средство, лекарство", "t_uk": "засіб, ліки", "t_en": "means, remedy", "t_tr": "araç, ilaç",
        "t_pl": "środek, lekarstwo", "t_it": "il mezzo, il rimedio", "t_es": "el medio, el remedio",
        "t_fr": "le moyen, le remède", "t_cs": "prostředek, lék",
        **all_x("Hast du ein Mittel gegen Kopfschmerzen?", "У тебя есть какое-нибудь средство от головной боли?",
                "У тебе є якийсь засіб від головного болю?", "Do you have a good remedy for headaches?",
                "Baş ağrısına iyi gelen bir ilacın var mı?", "Masz jakiś środek na ból głowy?",
                "Hai un rimedio per il mal di testa?", "¿Tienes algún remedio para el dolor de cabeza?",
                "Tu as un remède contre le mal de tête?", "Máš nějaký lék na bolest hlavy?")}),
    2529: ("«Das passierte gleichzeitig» — пусто; " + LIST, {
        "t_ru": "одновременно", "t_uk": "одночасно, водночас", "t_en": "at the same time", "t_tr": "aynı anda",
        "t_pl": "jednocześnie",
        **all_x("Ich kann nicht zwei Dinge gleichzeitig machen", "Я не могу делать два дела одновременно",
                "Я не можу робити дві справи одночасно", "I can't do two things at the same time",
                "Aynı anda iki iş yapamam", "Nie mogę robić dwóch rzeczy jednocześnie",
                "Non posso fare due cose contemporaneamente", "No puedo hacer dos cosas al mismo tiempo",
                "Je ne peux pas faire deux choses en même temps", "Nemůžu dělat dvě věci současně")}),
    12500: (LIST, {"t_en": "glasses"}),
    802: ("«Es fällt Schnee» — книжно, в речи «es schneit» или так", {**all_x(
        "Morgen soll es Schnee geben", "Завтра обещают снег", "Завтра обіцяють сніг",
        "They say there'll be snow tomorrow", "Yarın kar yağacakmış", "Jutro ma padać śnieg",
        "Domani dovrebbe arrivare la neve", "Mañana dicen que va a haber nieve",
        "Il paraît qu'il va y avoir de la neige demain", "Zítra má být sníh")}),
    1767: ("«Ich interessiere mich für Politik» повторял interessieren; " + LIST, {
        "t_ru": "политика", "t_uk": "політика", "t_tr": "siyaset",
        **all_x("Über Politik reden wir zu Hause nicht", "Дома мы о политике не говорим",
                "Удома ми про політику не говоримо", "We don't talk about politics at home", "Evde siyaset konuşmayız",
                "W domu nie rozmawiamy o polityce", "A casa non parliamo di politica", "En casa no hablamos de política",
                "À la maison, on ne parle pas de politique", "Doma o politice nemluvíme")}),
    13472: ("«Среди прочего она тоже была там» — смысла нет; " + LIST, {
        "t_ru": "среди прочего, в том числе", "t_uk": "серед іншого, зокрема", "t_en": "among other things",
        "t_tr": "diğerlerinin yanı sıra", "t_pl": "między innymi", "t_it": "tra l'altro",
        **all_x("Ich war unter anderem schon in Rom und Paris", "Я был, среди прочего, в Риме и Париже",
                "Я був, серед іншого, у Римі й Парижі", "I've been to Rome and Paris, among other places",
                "Başka yerlerin yanı sıra Roma'ya ve Paris'e de gittim", "Byłem między innymi w Rzymie i Paryżu",
                "Sono stato, tra l'altro, a Roma e a Parigi", "He estado, entre otros sitios, en Roma y París",
                "Je suis allé entre autres à Rome et à Paris", "Byl jsem mimo jiné v Římě a v Paříži")}),
    10210: (LIST, {"t_ru": "разумный, нормальный", "t_uk": "розумний, розсудливий", "t_en": "sensible, reasonable",
                   "t_tr": "makul, aklı başında", "t_pl": "rozsądny, porządny", "t_cs": "rozumný"}),
    1008: ("«Ich wasche die Wäsche» — масло масляное", {"t_en": "to wash", **all_x(
        "Ich muss mir noch die Haare waschen", "Мне ещё надо помыть голову", "Мені ще треба помити голову",
        "I still need to wash my hair", "Daha saçımı yıkamam lazım", "Muszę jeszcze umyć włosy",
        "Devo ancora lavarmi i capelli", "Todavía tengo que lavarme el pelo", "Je dois encore me laver les cheveux",
        "Ještě si musím umýt vlasy")}),
    712: (SKEL + " («Ich esse Pizza», en «I eat pizza»)", {**all_x(
        "Sollen wir heute Abend Pizza bestellen?", "Закажем сегодня вечером пиццу?", "Замовимо сьогодні ввечері піцу?",
        "Shall we order pizza tonight?", "Bu akşam pizza söyleyelim mi?", "Zamówimy dziś wieczorem pizzę?",
        "Ordiniamo una pizza stasera?", "¿Pedimos pizza esta noche?", "On commande une pizza ce soir?",
        "Objednáme si dneska večer pizzu?")}),
    686: ("«Berlin ist im Osten» — как у Norden; у каждой стороны света свой пример", {**all_x(
        "Wir fahren Richtung Osten", "Мы едем на восток", "Ми їдемо на схід", "We're heading east",
        "Doğuya doğru gidiyoruz", "Jedziemy na wschód", "Andiamo verso est", "Vamos hacia el este",
        "On roule vers l'est", "Jedeme na východ")}),
    6613: (LIST, {"t_ru": "прийти сюда, подойти", "t_uk": "прийти сюди, підійти", "t_en": "to come here, to come over",
                  "t_tr": "buraya gelmek", "t_pl": "przyjść tutaj, podejść", "t_it": "venire qui",
                  "t_es": "venir aquí", "t_fr": "venir ici", "t_cs": "přijít sem"}),
    705: (LIST, {"t_ru": "по, через", "t_uk": "по, через", "t_en": "by, via", "t_tr": "ile",
                 "t_pl": "przez, za pomocą", "t_it": "per, via", "t_cs": "přes",
                 "x_ru": "Я отправлю это по почте", "x_uk": "Я надішлю це поштою", "x_en": "I'll send it by post"}),
}

SPLIT_LATER = {
    765: ["der Rock = рок (музыка)"],
    123: ["blau = пьяный (разг.)"],
}
