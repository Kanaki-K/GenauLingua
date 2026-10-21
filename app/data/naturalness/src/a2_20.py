"""A2, блок 20: слова 761–787 по частоте (последние в A2). Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Er ist Pilot», «Mein PC ist schnell», «Die Qualität ist hoch») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1287: ("«Es gab einen Brand» — пусто; " + LIST, {
        "t_ru": "пожар", "t_uk": "пожежа", "t_en": "fire", "t_tr": "yangın", "t_pl": "pożar",
        **all_x("In der Nachbarschaft gab es gestern einen Brand", "Вчера по соседству был пожар", "Учора поблизу була пожежа",
                "There was a fire in the neighbourhood yesterday", "Dün mahallede yangın çıktı", "Wczoraj w okolicy był pożar",
                "Ieri c'è stato un incendio nel quartiere", "Ayer hubo un incendio en el barrio",
                "Hier, il y a eu un incendie dans le quartier", "Včera byl v sousedství požár")}),
    1306: (EN + " («I chat with friends»)", {"x_en": "I'm chatting with friends right now"}),
    1348: ("«Mein Ehepartner arbeitet hier» — пусто; слово — из анкет и приглашений", {
        "t_ru": "супруг, супруга", "t_uk": "чоловік, дружина", "t_en": "spouse", "t_tr": "eş", "t_pl": "małżonek, małżonka",
        "t_it": "il coniuge", "t_es": "el cónyuge", "t_fr": "le conjoint", "t_cs": "manžel, manželka",
        **all_x("Kommt Ihr Ehepartner auch mit?", "Ваш супруг тоже придёт?", "Ваш чоловік теж прийде?",
                "Is your spouse coming too?", "Eşiniz de geliyor mu?", "Czy małżonek też przyjdzie?",
                "Viene anche il Suo coniuge?", "¿Viene también su cónyuge?", "Votre conjoint vient aussi?",
                "Přijde i váš manžel?")}),
    1380: ("пример про Enkelin — слово Enkel не видно, и повтор строки Enkelin", {
        "t_ru": "внук", "t_uk": "онук", "t_en": "grandson, grandchild", "t_tr": "torun", "t_pl": "wnuk",
        "t_it": "il nipote", "t_es": "el nieto", "t_fr": "le petit-fils", "t_cs": "vnuk, vnouče",
        **all_x("Am Wochenende passen wir auf unseren Enkel auf", "На выходных мы присматриваем за внуком",
                "На вихідних ми доглядаємо онука", "We're looking after our grandson at the weekend",
                "Hafta sonu torunumuza bakıyoruz", "W weekend opiekujemy się wnukiem",
                "Nel fine settimana badiamo a nostro nipote", "El fin de semana cuidamos a nuestro nieto",
                "Ce week-end, on garde notre petit-fils", "O víkendu hlídáme vnuka")}),
    1533: (LIST, {"t_ru": "скачивать", "t_uk": "завантажувати, скачувати", "x_uk": "Я саме завантажую застосунок"}),
    1671: ("«Manche Leute mögen das» — что «это»? пусто", {**all_x(
        "Manche Leute essen kein Fleisch", "Некоторые люди не едят мясо", "Деякі люди не їдять м'яса",
        "Some people don't eat meat", "Bazı insanlar et yemiyor", "Niektórzy ludzie nie jedzą mięsa",
        "Alcune persone non mangiano carne", "Algunas personas no comen carne",
        "Certaines personnes ne mangent pas de viande", "Někteří lidé nejedí maso")}),
    1683: ("«Я чаще всего езжу» — книжно", {"x_ru": "Я обычно езжу на автобусе", "x_uk": "Я зазвичай їжджу автобусом"}),
    1761: (SKEL, {**all_x(
        "Als Kind wollte ich Pilot werden", "В детстве я хотел стать пилотом", "У дитинстві я хотів стати пілотом",
        "As a kid I wanted to be a pilot", "Çocukken pilot olmak istiyordum", "Jako dziecko chciałem zostać pilotem",
        "Da bambino volevo fare il pilota", "De pequeño quería ser piloto", "Enfant, je voulais devenir pilote",
        "Jako dítě jsem chtěl být pilotem")}),
    1769: (SKEL + "; " + LIST, {
        "t_ru": "недорогой, выгодный", "t_uk": "недорогий, вигідний", "t_en": "inexpensive, cheap",
        "t_tr": "uygun fiyatlı, ucuz", "t_pl": "tani, niedrogi",
        **all_x("Hier kann man preiswert essen", "Здесь можно недорого поесть", "Тут можна недорого поїсти",
                "You can eat cheaply here", "Burada ucuza yemek yenebilir", "Tu można tanio zjeść",
                "Qui si mangia a prezzi convenienti", "Aquí se come barato", "Ici, on mange pas cher",
                "Tady se dá levně najíst")}),
    1812: ("пример — обрывок; " + LIST, {
        "t_ru": "направление, сторона", "t_uk": "напрямок, сторона", "t_en": "direction", "t_tr": "yön", "t_pl": "kierunek",
        **all_x("Fährt dieser Bus in Richtung Zentrum?", "Этот автобус идёт в сторону центра?", "Цей автобус їде в бік центру?",
                "Does this bus go in the direction of the city centre?", "Bu otobüs merkez yönüne mi gidiyor?",
                "Czy ten autobus jedzie w kierunku centrum?", "Questo autobus va in direzione centro?",
                "¿Este autobús va en dirección al centro?", "Ce bus va en direction du centre?",
                "Jede tenhle autobus směrem do centra?")}),
    1858: (LIST, {"t_ru": "секретариат, приёмная", "t_uk": "секретаріат, приймальня", "t_en": "office, secretariat",
                  "t_tr": "sekreterlik", "t_pl": "sekretariat"}),
    1871: ("«Die Situation ist schwierig» — скелет", {**all_x(
        "Was würdest du in so einer Situation machen?", "Как бы ты поступил в такой ситуации?",
        "Як би ти вчинив у такій ситуації?", "What would you do in that situation?", "Bu durumda ne yapardın?",
        "Co byś zrobił w takiej sytuacji?", "Cosa faresti in questa situazione?", "¿Qué harías en esta situación?",
        "Qu'est-ce que tu ferais dans cette situation?", "Co bys dělal v takové situaci?")}),
    1893: ("«Die Kinder sind auf dem Sportplatz» — пусто; " + LIST, {
        "t_ru": "спортплощадка, стадион", "t_uk": "спортивний майданчик", "t_en": "sports field", "t_tr": "spor sahası",
        "t_pl": "boisko",
        **all_x("Nach der Schule spielen die Jungs auf dem Sportplatz Fußball",
                "После школы мальчишки играют в футбол на спортплощадке",
                "Після школи хлопці грають у футбол на спортивному майданчику",
                "After school the boys play football on the sports field",
                "Okuldan sonra çocuklar spor sahasında futbol oynuyor", "Po szkole chłopcy grają w piłkę na boisku",
                "Dopo la scuola i ragazzi giocano a calcio al campo sportivo",
                "Después del colegio los chicos juegan al fútbol en el campo de deportes",
                "Après l'école, les garçons jouent au foot sur le terrain de sport",
                "Po škole hrají kluci fotbal na hřišti")}),
    2010: (LIST, {"t_ru": "делать, предпринимать", "t_uk": "робити, затівати", "t_en": "to do, to undertake",
                  "t_tr": "bir şey yapmak", "t_pl": "robić coś, przedsiębrać", "x_ru": "Что будем сегодня делать?"}),
    2112: ("«Ich esse eine Wurst» — скелет", {**all_x(
        "Möchtest du Käse oder Wurst aufs Brot?", "Тебе на хлеб сыр или колбасу?", "Тобі на хліб сир чи ковбасу?",
        "Would you like cheese or sausage on your bread?", "Ekmeğine peynir mi salam mı istersin?",
        "Chcesz na chleb ser czy kiełbasę?", "Vuoi il formaggio o il salume sul pane?",
        "¿Quieres queso o embutido en el pan?", "Tu veux du fromage ou de la charcuterie sur ton pain?",
        "Chceš na chleba sýr, nebo salám?")}),
    2120: ("«Ich habe ein Zertifikat bekommen» — пусто", {**all_x(
        "Nach dem Kurs bekommst du ein Zertifikat", "После курса ты получишь сертификат", "Після курсу ти отримаєш сертифікат",
        "You'll get a certificate after the course", "Kurstan sonra bir sertifika alacaksın", "Po kursie dostaniesz certyfikat",
        "Alla fine del corso ricevi un attestato", "Después del curso te dan un certificado",
        "Après le cours, tu reçois un certificat", "Po kurzu dostaneš certifikát")}),
    2550: ("«Berlin ist die Hauptstadt» — пусто, и снова Berlin", {**all_x(
        "Wie heißt die Hauptstadt von Australien?", "Как называется столица Австралии?", "Як називається столиця Австралії?",
        "What's the capital of Australia?", "Avustralya'nın başkenti neresi?", "Jak się nazywa stolica Australii?",
        "Qual è la capitale dell'Australia?", "¿Cuál es la capital de Australia?", "Quelle est la capitale de l'Australie?",
        "Jak se jmenuje hlavní město Austrálie?")}),
    2627: (EN + "; " + LIST, {"t_ru": "косметика", "t_uk": "косметика", "t_en": "cosmetics, make-up",
                              "t_tr": "kozmetik", "t_pl": "kosmetyki", "x_en": "I'm buying myself some new make-up"}),
    2684: ("«Es ist neblig heute» — шаблон windig, sonnig", {
        "t_fr": "brumeux, il y a du brouillard",
        **all_x("Fahr vorsichtig, es ist sehr neblig", "Езжай осторожно, очень туманно", "Їдь обережно, дуже туманно",
                "Drive carefully, it's very foggy", "Dikkatli sür, hava çok sisli", "Jedź ostrożnie, jest bardzo mglisto",
                "Guida con prudenza, c'è molta nebbia", "Conduce con cuidado, que hay mucha niebla",
                "Conduis prudemment, il y a beaucoup de brouillard", "Jeď opatrně, je hrozně mlhavo")}),
    2714: (SKEL, {**all_x(
        "Mein PC ist schon wieder abgestürzt", "Мой компьютер опять завис", "Мій комп'ютер знову завис",
        "My PC has crashed again", "Bilgisayarım yine çöktü", "Mój komputer znowu się zawiesił",
        "Il mio PC si è bloccato di nuovo", "Se me ha vuelto a colgar el PC", "Mon PC a encore planté",
        "Počítač mi zase spadl")}),
    2738: (SKEL + "; «свойство» — другое слово", {
        "t_ru": "качество", "t_uk": "якість", "t_en": "quality", "t_tr": "kalite", "t_pl": "jakość",
        **all_x("Beim Obst achte ich auf die Qualität", "Когда покупаю фрукты, я смотрю на качество",
                "Коли купую фрукти, я дивлюся на якість", "When I buy fruit, I look at the quality",
                "Meyve alırken kaliteye dikkat ederim", "Kiedy kupuję owoce, zwracam uwagę na jakość",
                "Quando compro la frutta, guardo la qualità", "Cuando compro fruta, me fijo en la calidad",
                "Quand j'achète des fruits, je fais attention à la qualité", "Když kupuji ovoce, dívám se na kvalitu")}),
    2782: (LIST, {"t_ru": "собирать, коллекционировать", "t_uk": "збирати, колекціонувати", "t_en": "to collect, to gather",
                  "t_tr": "toplamak, biriktirmek", "t_pl": "zbierać, kolekcjonować", "t_it": "collezionare, raccogliere",
                  "t_es": "coleccionar, recoger", "t_fr": "collectionner, ramasser", "t_cs": "sbírat"}),
    2836: ("«Der Spieler ist gut» — скелет; «азартный игрок» — другое значение", {
        "t_ru": "игрок", "t_uk": "гравець, гравчиня", "t_en": "player", "t_tr": "oyuncu", "t_pl": "gracz, zawodnik",
        **all_x("Dieser Spieler hat heute zwei Tore geschossen", "Этот игрок сегодня забил два гола",
                "Цей гравець сьогодні забив два голи", "That player scored two goals today", "Bu oyuncu bugün iki gol attı",
                "Ten zawodnik strzelił dziś dwa gole", "Quel giocatore oggi ha segnato due gol",
                "Ese jugador ha marcado hoy dos goles", "Ce joueur a marqué deux buts aujourd'hui",
                "Ten hráč dnes dal dva góly")}),
    3013: ("«Montag ist ein Werktag» — из словаря, а не из жизни", {**all_x(
        "Die Bibliothek ist an Werktagen bis 20 Uhr offen", "Библиотека по будним дням открыта до восьми",
        "Бібліотека в будні дні відкрита до восьмої", "The library is open until 8 pm on weekdays",
        "Kütüphane hafta içi saat sekize kadar açık", "Biblioteka jest otwarta w dni powszednie do ósmej",
        "La biblioteca è aperta fino alle otto nei giorni feriali", "La biblioteca abre hasta las ocho los días laborables",
        "La bibliothèque est ouverte jusqu'à 20 heures les jours de semaine", "Knihovna má ve všední dny otevřeno do osmi")}),
    8730: ("«Unter Sonstiges kannst du … eintragen» — инструкция к анкете", {
        "t_ru": "прочий, остальной", "t_uk": "інший, решта", "t_en": "other", "t_tr": "diğer", "t_pl": "inny, pozostały",
        **all_x("Und die sonstigen Kosten, wie Strom und Wasser?", "А прочие расходы, например свет и вода?",
                "А інші витрати, наприклад світло й вода?", "And what about other costs, like electricity and water?",
                "Peki elektrik ve su gibi diğer masraflar?", "A pozostałe koszty, jak prąd i woda?",
                "E le altre spese, come luce e acqua?", "¿Y los otros gastos, como la luz y el agua?",
                "Et les autres frais, comme l'électricité et l'eau?", "A ostatní náklady, jako elektřina a voda?")}),
}

SPLIT_LATER = {}
