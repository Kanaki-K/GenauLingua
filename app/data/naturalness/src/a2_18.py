"""A2, блок 18: слова 681–720 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Ich schreibe ins Heft», «Der Beruf ist stressig») — пусто"
EN = "английский пример: так не говорят"
DAYS = "дни недели: «Xtags gehe ich immer …» — один шаблон на все; у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1805: ("«Я хочу забронировать» — в ресторане так грубо; " + LIST, {
        "t_ru": "бронировать, заказывать", "t_uk": "бронювати, резервувати", "t_en": "to reserve, to book",
        "t_tr": "rezervasyon yapmak", "t_pl": "rezerwować",
        "x_ru": "Я хотел бы забронировать столик", "x_uk": "Я хотів би забронювати столик",
        "x_en": "I'd like to book a table"}),
    7556: ("«наношу хороший крем каждое утро» — реклама; " + LIST, {
        "t_ru": "крем, мазь",
        **all_x("Diese Creme ist gut für trockene Haut", "Этот крем хорош для сухой кожи", "Цей крем добрий для сухої шкіри",
                "This cream is good for dry skin", "Bu krem kuru cilt için iyi", "Ten krem jest dobry do suchej skóry",
                "Questa crema va bene per la pelle secca", "Esta crema es buena para la piel seca",
                "Cette crème est bonne pour la peau sèche", "Tenhle krém je dobrý na suchou pleť")}),
    8994: (LIST, {"t_ru": "подавать заявку (на работу), рекламировать", "t_uk": "подавати заяву, рекламувати",
                  "t_en": "to apply, to advertise", "t_tr": "başvurmak, reklamını yapmak", "t_pl": "ubiegać się, reklamować",
                  "t_it": "candidarsi, pubblicizzare", "t_es": "solicitar, promocionar", "t_fr": "postuler, promouvoir",
                  "t_cs": "ucházet se, propagovat", "x_en": "I'd like to apply for a new job"}),
    8996: ("«Пекарь каждое утро печёт свежий хлеб» — из детской книжки; Brötchen/Bäcker — у frisch", {
        "t_ru": "пекарь, булочная", "t_es": "el panadero, la panadería",
        **all_x("Unser Bäcker hat sonntags auch auf", "Наша булочная открыта и по воскресеньям",
                "Наша пекарня працює й у неділю", "Our baker's is open on Sundays too", "Bizim fırın pazar günleri de açık",
                "Nasza piekarnia jest otwarta też w niedziele", "Il nostro fornaio è aperto anche la domenica",
                "Nuestra panadería abre también los domingos", "Notre boulanger est ouvert aussi le dimanche",
                "Náš pekař má otevřeno i v neděli")}),
    389: (SKEL + "; " + LIST, {
        "t_ru": "тетрадь, выпуск", "t_uk": "зошит, випуск", "t_en": "exercise book, issue", "t_tr": "defter",
        "t_pl": "zeszyt",
        **all_x("Schreibt die Wörter in euer Heft", "Запишите слова в тетрадь", "Запишіть слова в зошит",
                "Write the words in your exercise books", "Kelimeleri defterinize yazın", "Zapiszcie słówka w zeszycie",
                "Scrivete le parole sul quaderno", "Escribid las palabras en el cuaderno",
                "Écrivez les mots dans votre cahier", "Napište si slovíčka do sešitu")}),
    18300: ("«Мы ремонтируем дом летом» — порядок слов; " + LIST, {
        "t_ru": "делать ремонт, ремонтировать", "t_uk": "робити ремонт, ремонтувати", "t_en": "to renovate, to do up",
        "t_tr": "tadilat yapmak, yenilemek", "t_pl": "remontować",
        "x_ru": "Летом мы делаем ремонт в доме", "x_uk": "Улітку ми робимо ремонт у будинку"}),
    722: ("«Она отправляет мне открытку» — о прошлом/просьбе, не о «сейчас»", {**all_x(
        "Schick mir eine Postkarte aus dem Urlaub!", "Пришли мне открытку из отпуска!", "Надішли мені листівку з відпустки!",
        "Send me a postcard from your holiday!", "Tatilden bana kartpostal gönder!", "Wyślij mi pocztówkę z wakacji!",
        "Mandami una cartolina dalle vacanze!", "¡Mándame una postal de las vacaciones!",
        "Envoie-moi une carte postale de tes vacances!", "Pošli mi pohlednici z dovolené!")}),
    10863: ("пример о «гнилых яблоках», а слово на A2 — «ленивый»", {
        "t_ru": "ленивый, гнилой", "t_uk": "ледачий, гнилий", "t_en": "lazy, rotten", "t_tr": "tembel, çürük",
        "t_pl": "leniwy, zgniły", "t_it": "pigro, marcio", "t_es": "perezoso, podrido", "t_fr": "paresseux, pourri",
        "t_cs": "líný, shnilý",
        **all_x("Sei nicht so faul, hilf mir mal!", "Не ленись, помоги мне!", "Не лінуйся, допоможи мені!",
                "Don't be so lazy, give me a hand!", "Bu kadar tembel olma, bana yardım et!",
                "Nie bądź taki leniwy, pomóż mi!", "Non essere così pigro, aiutami!", "¡No seas tan perezoso, ayúdame!",
                "Ne sois pas si paresseux, aide-moi!", "Nebuď tak líný, pomoz mi!")}),
    9006: ("«Купец успешно вёл своё дело 30 лет» — из романа", {
        "t_ru": "коммерсант, торговец", "t_uk": "комерсант, торговець", "t_en": "businessman, salesman",
        "t_tr": "tüccar, esnaf", "t_pl": "handlowiec, kupiec", "t_it": "il commerciante", "t_es": "el comerciante",
        "t_fr": "le commerçant", "t_cs": "obchodník",
        **all_x("Mein Vater ist Kaufmann", "Мой отец — коммерсант", "Мій батько — комерсант", "My father is a businessman",
                "Babam tüccar", "Mój ojciec jest handlowcem", "Mio padre è commerciante", "Mi padre es comerciante",
                "Mon père est commerçant", "Můj táta je obchodník")}),
    14588: ("«Musikfestival» прячет слово; пример длинный", {**all_x(
        "Im Sommer fahren wir auf ein Festival", "Летом мы едем на фестиваль", "Улітку ми їдемо на фестиваль",
        "We're going to a festival in the summer", "Yazın bir festivale gidiyoruz", "Latem jedziemy na festiwal",
        "In estate andiamo a un festival", "En verano vamos a un festival", "Cet été, on va à un festival",
        "V létě jedeme na festival")}),
    228: (LIST, {"t_en": "ground floor", "x_en": "The flat is on the ground floor"}),
    14608: (LIST, {"t_ru": "карнавал", "t_uk": "карнавал"}),
    1567: ("«Das Fest findet jährlich statt» — книжно; " + LIST, {
        "t_ru": "ежегодно, ежегодный", "t_uk": "щороку, щорічний", "t_en": "annually, yearly", "t_tr": "her yıl, yıllık",
        "t_pl": "co roku, coroczny", "t_it": "ogni anno, annuale", "t_es": "cada año, anual",
        "t_fr": "chaque année, annuel", "t_cs": "každý rok, ročně",
        **all_x("Die Miete steigt jährlich", "Аренда дорожает ежегодно", "Оренда дорожчає щороку",
                "The rent goes up annually", "Kira her yıl artıyor", "Czynsz rośnie co roku", "L'affitto aumenta ogni anno",
                "El alquiler sube cada año", "Le loyer augmente chaque année", "Nájem každý rok stoupá")}),
    14613: ("пример — пресс-релиз; " + LIST, {
        "t_ru": "издательство", "t_uk": "видавництво", "t_en": "publisher, publishing house", "t_tr": "yayınevi",
        "t_pl": "wydawnictwo",
        **all_x("Sie arbeitet bei einem Verlag", "Она работает в издательстве", "Вона працює у видавництві",
                "She works for a publisher", "Bir yayınevinde çalışıyor", "Pracuje w wydawnictwie",
                "Lavora in una casa editrice", "Trabaja en una editorial", "Elle travaille dans une maison d'édition",
                "Pracuje v nakladatelství")}),
    9094: ("«Издатель опубликовал книгу» — пусто и шаблон Verlag", {**all_x(
        "Wer ist der Herausgeber der Zeitschrift?", "Кто издатель этого журнала?", "Хто видавець цього журналу?",
        "Who's the publisher of the magazine?", "Derginin yayıncısı kim?", "Kto jest wydawcą tego czasopisma?",
        "Chi è l'editore della rivista?", "¿Quién es el editor de la revista?", "Qui est l'éditeur du magazine?",
        "Kdo je vydavatelem toho časopisu?")}),
    9033: ("«начинается в девять» — шаблон Training, Sendung", {**all_x(
        "Das war ein langer Arbeitstag", "Это был длинный рабочий день", "Це був довгий робочий день",
        "That was a long working day", "Uzun bir iş günüydü", "To był długi dzień pracy",
        "È stata una lunga giornata lavorativa", "Ha sido una jornada laboral larga",
        "C'était une longue journée de travail", "Byl to dlouhý pracovní den")}),
    18316: ("шаблон renovieren («… das Haus …»)", {**all_x(
        "Die Wohnung ist frisch renoviert", "Квартира недавно отремонтирована", "Квартира щойно відремонтована",
        "The flat has just been renovated", "Daire yeni tadilattan geçti", "Mieszkanie jest świeżo wyremontowane",
        "L'appartamento è appena stato ristrutturato", "El piso está recién reformado",
        "L'appartement vient d'être rénové", "Byt je čerstvě zrekonstruovaný")}),
    1580: ("«Englischkenntnisse» прячет слово; «хорошие знания английского» — калька", {**all_x(
        "Hast du Kenntnisse in Buchhaltung?", "У тебя есть знания в бухгалтерии?", "У тебе є знання з бухгалтерії?",
        "Do you have any knowledge of bookkeeping?", "Muhasebe bilgin var mı?", "Masz znajomość księgowości?",
        "Hai conoscenze di contabilità?", "¿Tienes conocimientos de contabilidad?",
        "Tu as des connaissances en comptabilité?", "Máš znalosti z účetnictví?")}),
    7711: ("«Ты должен вписать своё имя» — калька с musst; " + LIST, {
        "t_ru": "вписать, внести", "t_uk": "вписати, внести", "t_en": "to enter, to write in", "t_tr": "kaydetmek, yazmak",
        "t_pl": "wpisać", "t_it": "inserire, scrivere", "t_es": "anotar, apuntar", "t_fr": "inscrire, noter",
        "t_cs": "zapsat",
        **all_x("Trag dich bitte in die Liste ein", "Впиши, пожалуйста, себя в список", "Впиши себе, будь ласка, у список",
                "Please put your name on the list", "Lütfen adını listeye yaz", "Wpisz się, proszę, na listę",
                "Iscriviti alla lista, per favore", "Apúntate en la lista, por favor",
                "Inscris-toi sur la liste, s'il te plaît", "Zapiš se prosím do seznamu")}),
    17239: ("«Туристы осматривают город» — пусто; " + LIST, {
        "t_ru": "турист", "t_uk": "турист", "t_en": "tourist", "t_tr": "turist", "t_pl": "turysta",
        **all_x("Im Sommer ist die Stadt voller Touristen", "Летом город полон туристов", "Улітку місто повне туристів",
                "In summer the town is full of tourists", "Yazın şehir turist dolu", "Latem miasto jest pełne turystów",
                "D'estate la città è piena di turisti", "En verano la ciudad está llena de turistas",
                "En été, la ville est pleine de touristes", "V létě je město plné turistů")}),
    2087: ("«Besuchen Sie unsere Webseite» — реклама; " + LIST, {
        "t_ru": "сайт", "t_uk": "сайт", "t_en": "website", "t_tr": "web sitesi", "t_pl": "strona internetowa",
        **all_x("Die Öffnungszeiten stehen auf der Webseite", "Часы работы указаны на сайте", "Години роботи вказані на сайті",
                "The opening hours are on the website", "Çalışma saatleri internet sitesinde yazıyor",
                "Godziny otwarcia są na stronie internetowej", "Gli orari sono sul sito web",
                "El horario está en la página web", "Les horaires sont sur le site web", "Otevírací doba je na webové stránce")}),
    18812: ("«актуальная версия» — калька; " + LIST, {
        "t_ru": "актуальный, последний", "t_uk": "актуальний, найновіший", "t_en": "current, latest", "t_tr": "güncel",
        "t_pl": "aktualny, najnowszy", "t_it": "attuale, aggiornato", "t_es": "actual, actualizado",
        "t_fr": "actuel, à jour", "t_cs": "aktuální",
        "x_ru": "Это последняя версия приложения", "x_uk": "Це найновіша версія застосунку"}),
    14625: ("«Плакат на стене очень большой» — пусто", {**all_x(
        "Hängen wir das Plakat in der Küche auf?", "Повесим плакат на кухне?", "Повісимо плакат на кухні?",
        "Shall we put the poster up in the kitchen?", "Posteri mutfağa asalım mı?", "Powiesimy plakat w kuchni?",
        "Appendiamo il poster in cucina?", "¿Colgamos el póster en la cocina?", "On accroche l'affiche dans la cuisine?",
        "Pověsíme ten plakát v kuchyni?")}),
    18813: ("«Partys und Feuerwerk» — шаблон Silvester", {**all_x(
        "An Neujahr sind alle Geschäfte zu", "Первого января все магазины закрыты", "Першого січня всі магазини зачинені",
        "All the shops are shut on New Year's Day", "Yılbaşında bütün dükkanlar kapalı",
        "W Nowy Rok wszystkie sklepy są zamknięte", "A Capodanno tutti i negozi sono chiusi",
        "En Año Nuevo todas las tiendas están cerradas", "Le jour de l'An, tous les magasins sont fermés",
        "Na Nový rok jsou všechny obchody zavřené")}),
    782: (DAYS + "; «Samstags schlafen wir länger» — шаблон sonntags", {**all_x(
        "Samstags gehe ich auf den Markt", "По субботам я хожу на рынок", "По суботах я ходжу на ринок",
        "On Saturdays I go to the market", "Cumartesileri pazara gidiyorum", "W soboty chodzę na targ",
        "Il sabato vado al mercato", "Los sábados voy al mercado", "Le samedi, je vais au marché",
        "V sobotu chodím na trh")}),
    18825: (DAYS, {**all_x(
        "Freitags arbeite ich nur bis mittags", "По пятницам я работаю только до обеда",
        "По п'ятницях я працюю лише до обіду", "On Fridays I only work until lunchtime",
        "Cuma günleri sadece öğlene kadar çalışıyorum", "W piątki pracuję tylko do południa",
        "Il venerdì lavoro solo fino a mezzogiorno", "Los viernes solo trabajo hasta mediodía",
        "Le vendredi, je ne travaille que jusqu'à midi", "V pátek pracuji jen do poledne")}),
    18829: (DAYS, {**all_x(
        "Dienstags kommt immer die Putzfrau", "По вторникам всегда приходит уборщица",
        "По вівторках завжди приходить прибиральниця", "The cleaner always comes on Tuesdays",
        "Salıları hep temizlikçi geliyor", "We wtorki zawsze przychodzi sprzątaczka",
        "Il martedì viene sempre la donna delle pulizie", "Los martes siempre viene la señora de la limpieza",
        "Le mardi, la femme de ménage vient toujours", "V úterý vždycky chodí uklízečka")}),
    18840: (DAYS, {**all_x(
        "Montags ist im Büro immer viel los", "По понедельникам в офисе всегда много дел",
        "По понеділках в офісі завжди багато роботи", "It's always busy at the office on Mondays",
        "Pazartesileri ofiste hep çok iş oluyor", "W poniedziałki w biurze zawsze jest dużo roboty",
        "Il lunedì in ufficio c'è sempre tanto da fare", "Los lunes siempre hay mucho jaleo en la oficina",
        "Le lundi, il y a toujours beaucoup de travail au bureau", "V pondělí je v kanceláři vždycky hodně práce")}),
    1063: ("«Ich benutze ein Wörterbuch» — пусто", {**all_x(
        "Schau doch im Wörterbuch nach!", "Посмотри в словаре!", "Подивися в словнику!", "Look it up in the dictionary!",
        "Sözlüğe bak!", "Sprawdź w słowniku!", "Guarda sul dizionario!", "¡Búscalo en el diccionario!",
        "Regarde dans le dictionnaire!", "Podívej se do slovníku!")}),
    2880: ("в речи total — наречие («total vergessen»); " + LIST, {
        "t_ru": "полный, совершенно", "t_uk": "повний, зовсім", "t_en": "total, totally", "t_tr": "tam, tamamen",
        "t_pl": "całkowity, kompletnie", "t_it": "totale, totalmente", "t_es": "total, totalmente",
        "t_fr": "total, complètement", "t_cs": "úplný, naprosto",
        **all_x("Das habe ich total vergessen!", "Я совершенно об этом забыл!", "Я зовсім про це забув!",
                "I totally forgot!", "Bunu tamamen unuttum!", "Kompletnie o tym zapomniałem!",
                "Me ne sono totalmente dimenticato!", "¡Se me ha olvidado totalmente!", "J'ai complètement oublié!",
                "Naprosto jsem na to zapomněl!")}),
    1223: (LIST, {"t_ru": "мастерить, делать поделки", "t_uk": "майструвати", "t_en": "to do crafts, to tinker",
                  "t_tr": "el işi yapmak", "t_pl": "majsterkować", "t_it": "fare lavoretti", "t_es": "hacer manualidades",
                  "t_fr": "bricoler", "t_cs": "vyrábět, kutit"}),
    1884: ("«Speichere die Datei» — снова Datei; " + LIST, {
        "t_ru": "сохранять, хранить", "t_uk": "зберігати", "t_en": "to save, to store", "t_tr": "kaydetmek, saklamak",
        "t_pl": "zapisywać, przechowywać",
        **all_x("Vergiss nicht, das Dokument zu speichern!", "Не забудь сохранить документ!", "Не забудь зберегти документ!",
                "Don't forget to save the document!", "Belgeyi kaydetmeyi unutma!", "Nie zapomnij zapisać dokumentu!",
                "Non dimenticare di salvare il documento!", "¡No te olvides de guardar el documento!",
                "N'oublie pas d'enregistrer le document!", "Nezapomeň dokument uložit!")}),
    7837: ("«вынашивать ребёнка» — другое значение; пример — язык спортивных новостей", {
        "t_ru": "проводить (соревнование), разносить", "t_uk": "проводити, розносити", "t_en": "to hold (a match), to deliver",
        "t_tr": "düzenlemek, dağıtmak", "t_pl": "rozgrywać, roznosić", "t_it": "disputare, consegnare",
        "t_es": "disputar, repartir", "t_fr": "disputer, distribuer", "t_cs": "konat, roznášet",
        **all_x("Er trägt morgens Zeitungen aus", "По утрам он разносит газеты", "Зранку він розносить газети",
                "He delivers newspapers in the mornings", "Sabahları gazete dağıtıyor", "Rano roznosi gazety",
                "La mattina consegna i giornali", "Por las mañanas reparte periódicos", "Le matin, il distribue des journaux",
                "Ráno roznáší noviny")}),
    130: ("снова «в супе»; " + LIST, {
        "t_ru": "фасоль, боб", "t_uk": "квасоля, біб", "t_en": "bean", "t_tr": "fasulye", "t_pl": "fasola",
        **all_x("Möchtest du grüne Bohnen zum Fleisch?", "Хочешь зелёную фасоль к мясу?", "Хочеш зелену квасолю до м'яса?",
                "Would you like green beans with the meat?", "Etin yanında taze fasulye ister misin?",
                "Chcesz zieloną fasolkę do mięsa?", "Vuoi dei fagiolini con la carne?",
                "¿Quieres judías verdes con la carne?", "Tu veux des haricots verts avec la viande?",
                "Dáš si k masu zelené fazolky?")}),
    11039: (SKEL, {**all_x(
        "Mein Job ist manchmal ziemlich stressig", "Моя работа иногда довольно напряжённая",
        "Моя робота іноді досить напружена", "My job is pretty stressful sometimes", "İşim bazen oldukça stresli",
        "Moja praca bywa dość stresująca", "Il mio lavoro a volte è piuttosto stressante",
        "Mi trabajo a veces es bastante estresante", "Mon travail est parfois assez stressant",
        "Moje práce je někdy dost stresující")}),
    14196: ("«schimpfte» — претерит, книжно; " + LIST, {
        "t_ru": "ругаться, ругать", "t_uk": "лаятися, сварити", "t_en": "to tell off, to grumble",
        "t_tr": "azarlamak, söylenmek", "t_pl": "besztać, narzekać",
        **all_x("Meine Mutter schimpft immer, wenn ich zu spät komme", "Мама всегда ругается, когда я прихожу поздно",
                "Мама завжди сварить, коли я пізно приходжу", "My mum always tells me off when I'm late",
                "Geç kaldığımda annem hep kızıyor", "Mama zawsze na mnie narzeka, kiedy się spóźniam",
                "Mia madre mi sgrida sempre quando arrivo tardi", "Mi madre siempre me regaña cuando llego tarde",
                "Ma mère me gronde toujours quand je rentre tard", "Máma vždycky nadává, když přijdu pozdě")}),
    9562: ("«Мне нужно письменное подтверждение от тебя» — канцелярски", {**all_x(
        "Können Sie mir das bitte schriftlich geben?", "Не могли бы вы дать мне это в письменном виде?",
        "Чи не могли б ви дати мені це в письмовій формі?", "Could you give me that in writing, please?",
        "Bunu bana yazılı olarak verebilir misiniz?", "Czy mogę to dostać na piśmie?",
        "Me lo può dare per iscritto?", "¿Me lo puede dar por escrito?", "Vous pouvez me le donner par écrit?",
        "Můžete mi to dát písemně?")}),
}

SPLIT_LATER = {}
