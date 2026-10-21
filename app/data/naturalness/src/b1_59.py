"""B1, блок 59: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    14046: (LIST + " (было шесть значений)", {
        "t_ru": "заговорить, затронуть тему", "t_uk": "заговорити, порушити тему", "t_en": "to speak to, to bring up",
        "t_tr": "biriyle konuşmak, konuyu açmak", "t_pl": "zagadnąć, poruszyć temat", "t_it": "rivolgersi a, affrontare",
        "t_es": "dirigirse a, abordar", "t_fr": "aborder, évoquer", "t_cs": "oslovit, zmínit"}),
    2867: ("«Ich brauche eine Taschenlampe» — пусто; en «flashlight» — американское", {"t_en": "torch, flashlight", **all_x(
        "Ohne Taschenlampe sieht man im Keller nichts", "Без фонарика в подвале ничего не видно",
        "Без ліхтарика в підвалі нічого не видно", "You can't see anything in the cellar without a torch",
        "El feneri olmadan bodrumda hiçbir şey görünmüyor", "Bez latarki w piwnicy nic nie widać",
        "Senza torcia in cantina non si vede niente", "Sin linterna no se ve nada en el sótano",
        "Sans lampe de poche, on ne voit rien à la cave", "Bez baterky ve sklepě nic nevidíš")}),
    2688: ("«Das Niveau der Schulen ist hoch» — газета", {**all_x(
        "Das Restaurant hat echt Niveau", "У этого ресторана действительно есть класс", "Цей ресторан справді має клас",
        "The restaurant really has a high standard", "Restoranın kalitesi gerçekten yüksek",
        "Restauracja ma naprawdę wysoki poziom", "Il ristorante ha davvero un buon livello",
        "El restaurante tiene muy buen nivel", "Le restaurant a vraiment du niveau", "Ta restaurace má fakt úroveň")}),
    8905: ("«Die Künstlerin hat ein neues Gemälde gemalt» — шаблон Maler", {"t_en": "artist", **all_x(
        "Sie ist eine echte Künstlerin in der Küche", "На кухне она настоящая художница", "На кухні вона справжня художниця",
        "She's a real artist in the kitchen", "Mutfakta gerçek bir sanatçı", "W kuchni jest prawdziwą artystką",
        "In cucina è una vera artista", "En la cocina es una verdadera artista", "En cuisine, c'est une vraie artiste",
        "V kuchyni je to opravdová umělkyně")}),
    17549: ("«Der Monitor zeigt meine Arbeit» — пусто", {**all_x(
        "Ich arbeite mit zwei Monitoren", "Я работаю с двумя мониторами", "Я працюю з двома моніторами",
        "I work with two monitors", "İki monitörle çalışıyorum", "Pracuję na dwóch monitorach", "Lavoro con due monitor",
        "Trabajo con dos monitores", "Je travaille avec deux écrans", "Pracuji se dvěma monitory")}),
    14500: ("«Die Zeichnung des Künstlers ist wunderbar» — пусто; " + LIST, {
        "t_ru": "рисунок, чертёж", "t_uk": "малюнок, креслення", "t_en": "drawing, sketch", "t_tr": "çizim, resim",
        "t_pl": "rysunek, szkic",
        **all_x("Mein Sohn hat mir eine Zeichnung geschenkt", "Сын подарил мне рисунок", "Син подарував мені малюнок",
                "My son gave me a drawing", "Oğlum bana bir resim hediye etti", "Syn dał mi w prezencie rysunek",
                "Mio figlio mi ha regalato un disegno", "Mi hijo me ha regalado un dibujo", "Mon fils m'a offert un dessin",
                "Syn mi daroval kresbu")}),
    7238: ("«Schreib die nächste Zeile in dein Heft» — школа", {**all_x(
        "Schreib mir ein paar Zeilen, wenn du angekommen bist", "Черкни мне пару строк, когда доедешь",
        "Напиши мені кілька рядків, коли доїдеш", "Drop me a few lines when you get there",
        "Varınca bana birkaç satır yaz", "Napisz mi kilka linijek, jak dojedziesz", "Scrivimi due righe quando arrivi",
        "Escríbeme unas líneas cuando llegues", "Écris-moi quelques lignes quand tu seras arrivé",
        "Napiš mi pár řádků, až dorazíš")}),
    12646: (LIST, {"t_ru": "ухаживать, поддерживать", "t_uk": "доглядати, підтримувати", "t_en": "to look after, to maintain",
                   "t_tr": "bakmak, sürdürmek", "t_pl": "opiekować się, pielęgnować"}),
    2334: ("«Der Deckel passt nicht» — пусто", {**all_x(
        "Mach den Deckel auf den Topf", "Накрой кастрюлю крышкой", "Накрий каструлю кришкою", "Put the lid on the pot",
        "Tencerenin kapağını kapat", "Przykryj garnek pokrywką", "Metti il coperchio sulla pentola", "Pon la tapa a la olla",
        "Mets le couvercle sur la casserole", "Dej na hrnec poklici")}),
    1238: ("«Ich muss zur Behörde gehen» — шаблон Amt («Ich muss morgen aufs Amt»)", {**all_x(
        "Mit den Behörden hatte ich nur Ärger", "С госорганами у меня одни проблемы", "З державними органами в мене одні проблеми",
        "I've had nothing but trouble with the authorities", "Resmi kurumlarla başım hep dertteydi",
        "Z urzędami miałem same kłopoty", "Con gli uffici pubblici ho avuto solo problemi",
        "Con los organismos públicos solo he tenido problemas", "Avec l'administration, je n'ai eu que des ennuis",
        "S úřady jsem měl jen trable")}),
    3070: ("«Es gibt zusätzliche Kosten» — шаблон «Es gibt …»", {**all_x(
        "Für das Gepäck zahlt man zusätzlich", "За багаж платят дополнительно", "За багаж платять додатково",
        "You pay extra for luggage", "Bagaj için ayrıca ödeme yapılıyor", "Za bagaż płaci się dodatkowo",
        "Il bagaglio si paga extra", "El equipaje se paga extra", "Les bagages se paient en plus", "Za zavazadla se platí navíc")}),
    7249: ("ru «Я должен создать отчёт» — калька", {"x_ru": "Мне надо составить отчёт", "x_uk": "Мені треба скласти звіт"}),
    2965: ("«Ich habe das versehentlich gemacht» — пусто", {**all_x(
        "Ich habe versehentlich deine Nachricht gelöscht", "Я нечаянно удалил твоё сообщение", "Я ненавмисно видалив твоє повідомлення",
        "I accidentally deleted your message", "Yanlışlıkla mesajını sildim", "Przypadkiem usunąłem twoją wiadomość",
        "Ho cancellato per sbaglio il tuo messaggio", "Borré sin querer tu mensaje", "J'ai supprimé ton message par erreur",
        "Omylem jsem ti smazal zprávu")}),
    8910: ("«Der Ober bringt uns die Rechnung» — слово живёт в обращении «Herr Ober!»", {**all_x(
        "Herr Ober, die Rechnung bitte!", "Официант, счёт, пожалуйста!", "Офіціанте, рахунок, будь ласка!",
        "Waiter, the bill please!", "Garson, hesap lütfen!", "Kelner, rachunek proszę!", "Cameriere, il conto per favore!",
        "¡Camarero, la cuenta, por favor!", "Garçon, l'addition s'il vous plaît!", "Pane vrchní, platím!")}),
    2475: ("«Das war sehr förmlich» — пусто", {**all_x(
        "Sie müssen nicht so förmlich sein, sagen wir einfach du", "Не нужно так официально, давайте на «ты»",
        "Не треба так офіційно, давайте на «ти»", "You don't need to be so formal, call me by my first name",
        "Bu kadar resmî olmanıza gerek yok, bana sen deyin", "Nie musi Pan być taki formalny, mówmy sobie po imieniu",
        "Non c'è bisogno di essere così formale, diamoci del tu", "No hace falta ser tan formal, tutéame",
        "Pas besoin d'être si formel, on peut se tutoyer", "Nemusíte být tak formální, klidně si tykejme")}),
    18744: ("убрать пометку (fam.)", {"t_fr": "rester assis, glander"}),
    834: ("«Er sitzt im Sessel» — пусто", {**all_x(
        "Opa schläft immer im Sessel ein", "Дедушка всегда засыпает в кресле", "Дідусь завжди засинає в кріслі",
        "Grandad always falls asleep in his armchair", "Dedem hep koltukta uyuyakalıyor", "Dziadek zawsze zasypia w fotelu",
        "Il nonno si addormenta sempre in poltrona", "El abuelo siempre se duerme en el sillón",
        "Papi s'endort toujours dans le fauteuil", "Děda vždycky usne v křesle")}),
    8913: ("«Der Streik … dauerte drei Wochen» — претерит", {**all_x(
        "Wegen des Streiks fahren heute keine Busse", "Из-за забастовки сегодня не ходят автобусы",
        "Через страйк сьогодні не ходять автобуси", "Because of the strike there are no buses today",
        "Grev yüzünden bugün otobüs çalışmıyor", "Z powodu strajku dziś nie jeżdżą autobusy",
        "A causa dello sciopero oggi non passano autobus", "Por la huelga hoy no hay autobuses",
        "À cause de la grève, il n'y a pas de bus aujourd'hui", "Kvůli stávce dnes nejezdí autobusy")}),
}

SPLIT_LATER = {
    16249: ["beim Bund sein (разг.) = служить в армии"],
}
