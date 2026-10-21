"""A2, блок 11: слова 401–440 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist grün/rund/hässlich») — так о вещи не говорят"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
TIME = "«о 18 годині», «at 6 in the evening» — так время не называют"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    360: (SKEL, {**all_x(
        "Die Ampel ist grün, du kannst fahren", "Светофор зелёный, можешь ехать", "На світлофорі зелений, можеш їхати",
        "The light's green, you can go", "Işık yeşil, gidebilirsin", "Jest zielone światło, możesz jechać",
        "Il semaforo è verde, puoi andare", "El semáforo está en verde, puedes pasar",
        "Le feu est vert, tu peux y aller", "Je zelená, můžeš jet")}),
    2097: (LIST, {"t_ru": "мало, немного", "t_uk": "мало, трохи", "t_en": "little, few", "t_tr": "az, biraz",
                  "t_pl": "mało, niewiele", "x_en": "There are only a few seats left",
                  "x_pl": "Zostało niewiele wolnych miejsc", "x_es": "Solo quedan pocos asientos libres",
                  "x_fr": "Il ne reste que peu de places"}),
    10212: (LIST + "; fr «journée très palpitante» — неживо", {
        "t_ru": "захватывающий, волнующий", "t_tr": "heyecan verici", "t_fr": "palpitant, passionnant",
        "x_fr": "C'était une journée vraiment passionnante"}),
    13908: (LIST, {"t_ru": "подтвердить", "t_uk": "підтвердити", "t_en": "to confirm", "t_tr": "onaylamak, doğrulamak",
                   "t_pl": "potwierdzić"}),
    2753: (LIST, {"t_ru": "шина", "t_uk": "шина", "t_en": "tyre", "t_tr": "lastik", "t_pl": "opona"}),
    1080: ("uk «у свою каву» — калька", {"x_uk": "Скільки цукру тобі покласти в каву?"}),
    584: (LIST + "; «Я чаще всего ем дома» — книжно", {
        "t_ru": "обычно, чаще всего", "t_uk": "зазвичай, найчастіше", "t_en": "mostly, usually", "t_tr": "genellikle",
        "t_pl": "najczęściej, zwykle", "t_es": "casi siempre, normalmente", "t_fr": "la plupart du temps, le plus souvent",
        "x_ru": "Обычно я ем дома", "x_uk": "Зазвичай я їм удома", "x_fr": "La plupart du temps, je mange à la maison"}),
    10217: ("«по-настоящему испугал» — калька; " + LIST, {
        "t_ru": "испугаться, напугать", "t_uk": "злякатися, налякати", "t_en": "to be frightened, to scare",
        "t_tr": "korkmak, korkutmak", "t_pl": "przestraszyć się, przestraszyć", "t_fr": "faire peur, s'effrayer",
        "t_cs": "vyděsit, leknout se", "x_ru": "Ну ты меня и напугал!", "x_uk": "Ну ти мене й налякав!"}),
    18651: (EN + " («I jog daily for an hour»); " + LIST, {
        "t_ru": "ежедневно, каждый день", "t_uk": "щодня", "t_tr": "her gün", "t_pl": "codziennie",
        "x_en": "I go jogging for an hour every day", "x_es": "Corro una hora todos los días"}),
    6623: ("пример повторял wegen («Wegen des Regens bleibe ich zu Hause»); aufgrund — так пишут, а говорят wegen", {
        "t_ru": "из-за, по причине", "t_uk": "через, з причини", "t_en": "due to, because of", "t_tr": "nedeniyle",
        "t_pl": "z powodu", "t_it": "a causa di", "t_es": "debido a, a causa de", "t_fr": "à cause de, en raison de",
        "t_cs": "kvůli",
        **all_x("Aufgrund von Bauarbeiten fällt der Zug aus", "Из-за ремонтных работ поезд отменён",
                "Через ремонтні роботи поїзд скасовано", "The train is cancelled due to engineering works",
                "Yol çalışmaları nedeniyle tren iptal edildi", "Z powodu prac remontowych pociąg jest odwołany",
                "A causa di lavori il treno è soppresso", "Debido a unas obras, el tren está cancelado",
                "En raison de travaux, le train est supprimé", "Kvůli stavebním pracím vlak nejede")}),
    2089: ("четвёртый пример «из-за дождя остаюсь дома» (aufgrund, trotz, daher) — у каждого свой", {**all_x(
        "Wegen dir kommen wir zu spät!", "Из-за тебя мы опоздаем!", "Через тебе ми запізнимося!",
        "We'll be late because of you!", "Senin yüzünden geç kalacağız!", "Przez ciebie się spóźnimy!",
        "Per colpa tua arriveremo in ritardo!", "¡Por tu culpa vamos a llegar tarde!",
        "À cause de toi, on va être en retard!", "Kvůli tobě přijdeme pozdě!")}),
    14395: ("«Der Künstler malt schöne Bilder» — из детской книжки; " + LIST, {
        "t_ru": "художник, артист", "t_uk": "художник, митець", "t_en": "artist", "t_tr": "sanatçı", "t_pl": "artysta",
        **all_x("Auf dem Markt verkaufen Künstler ihre Bilder", "На рынке художники продают свои картины",
                "На ринку художники продають свої картини", "Artists sell their paintings at the market",
                "Pazarda sanatçılar resimlerini satıyor", "Na targu artyści sprzedają swoje obrazy",
                "Al mercato gli artisti vendono i loro quadri", "En el mercado los artistas venden sus cuadros",
                "Au marché, des artistes vendent leurs tableaux", "Na trhu prodávají umělci své obrazy")}),
    526: (TWO + " («ерунда» — разговорное значение); «Ich esse Käse und Brot» — скелет", {
        "t_ru": "сыр", "t_uk": "сир", "t_en": "cheese", "t_tr": "peynir", "t_pl": "ser", "t_it": "il formaggio",
        "t_es": "el queso", "t_fr": "le fromage", "t_cs": "sýr",
        **all_x("Ein Brötchen mit Käse, bitte", "Булочку с сыром, пожалуйста", "Булочку з сиром, будь ласка",
                "A cheese roll, please", "Peynirli bir sandviç lütfen", "Bułkę z serem poproszę",
                "Un panino al formaggio, per favore", "Un panecillo con queso, por favor",
                "Un petit pain au fromage, s'il vous plaît", "Rohlík se sýrem, prosím")}),
    1440: ("«Die Teilnahme ist freiwillig» — язык анкет; " + LIST, {
        "t_ru": "добровольный, по своей воле", "t_uk": "добровільний, з власної волі",
        "t_en": "voluntary, of one's own free will", "t_tr": "gönüllü, kendi isteğiyle", "t_pl": "dobrowolny, dobrowolnie",
        "t_it": "volontario", "t_fr": "volontaire",
        **all_x("Niemand zwingt mich, ich mache das freiwillig", "Меня никто не заставляет, я делаю это по своей воле",
                "Мене ніхто не змушує, я роблю це з власної волі",
                "Nobody's forcing me, I'm doing it of my own free will",
                "Kimse beni zorlamıyor, bunu kendi isteğimle yapıyorum", "Nikt mnie nie zmusza, robię to dobrowolnie",
                "Nessuno mi obbliga, lo faccio volontariamente", "Nadie me obliga, lo hago voluntariamente",
                "Personne ne m'oblige, je le fais volontairement", "Nikdo mě nenutí, dělám to dobrovolně")}),
    95: (LIST + "; «Я рассказываю тебе» — по-русски о будущем «расскажу»", {
        "t_ru": "сообщать, рассказывать", "t_uk": "повідомляти, розповідати", "t_en": "to report, to tell about",
        "t_tr": "anlatmak, bildirmek", "t_pl": "opowiadać, relacjonować", "t_it": "raccontare, riferire",
        "t_es": "contar, informar", "t_fr": "raconter, rapporter", "t_cs": "vyprávět, informovat",
        "x_ru": "Я расскажу тебе о своей поездке", "x_uk": "Я розповім тобі про свою подорож",
        "x_en": "I'll tell you about my trip"}),
    14396: ("«Der Titel des Buchs ist interessant» — пусто; «трек, звание» — другие значения", {
        "t_ru": "название, заголовок", "t_uk": "назва, заголовок", "t_en": "title", "t_tr": "başlık, ad",
        "t_pl": "tytuł",
        **all_x("Ich habe den Titel des Films vergessen", "Я забыл название фильма", "Я забув назву фільму",
                "I've forgotten the title of the film", "Filmin adını unuttum", "Zapomniałem tytułu filmu",
                "Ho dimenticato il titolo del film", "He olvidado el título de la película",
                "J'ai oublié le titre du film", "Zapomněl jsem název filmu")}),
    888: ("«У него много стресса» — калька; " + LIST, {
        "t_ru": "стресс, спешка", "t_uk": "стрес, поспіх", "t_en": "stress", "t_tr": "stres", "t_pl": "stres",
        **all_x("Ich habe gerade viel Stress bei der Arbeit", "У меня сейчас на работе сплошной стресс",
                "У мене зараз на роботі суцільний стрес", "I've got a lot of stress at work right now",
                "Şu an işte çok stresim var", "Mam teraz dużo stresu w pracy",
                "In questo periodo ho tanto stress al lavoro", "Ahora tengo mucho estrés en el trabajo",
                "En ce moment, j'ai beaucoup de stress au travail", "V práci mám teď hodně stresu")}),
    339: ("«Gesundheit ist wichtig» — плакат, а не речь; живёт слово в «Gesundheit!» после чиха", {
        "t_it": "la salute, salute!", "t_es": "la salud, ¡salud!", "t_fr": "la santé, à tes souhaits",
        **all_x("Hatschi! — Gesundheit! — Danke!", "Апчхи! — Будь здоров! — Спасибо!", "Апчхи! — Будь здоровий! — Дякую!",
                "Achoo! — Bless you! — Thanks!", "Hapşu! — Çok yaşa! — Sen de gör!", "Apsik! — Na zdrowie! — Dziękuję!",
                "Etciù! — Salute! — Grazie!", "¡Achís! — ¡Salud! — ¡Gracias!", "Atchoum! — À tes souhaits! — Merci!",
                "Hepčí! — Na zdraví! — Díky!")}),
    789: ("«Ich schenke dir ein Buch» — из учебника; «наливать» — устар.", {
        "t_ru": "дарить", "t_uk": "дарувати", "t_en": "to give (as a present)", "t_tr": "hediye etmek",
        "t_pl": "podarować, dawać w prezencie",
        **all_x("Was schenkst du deiner Mutter zum Geburtstag?", "Что ты подаришь маме на день рождения?",
                "Що ти подаруєш мамі на день народження?", "What are you giving your mum for her birthday?",
                "Annene doğum gününde ne hediye edeceksin?", "Co podarujesz mamie na urodziny?",
                "Cosa regali a tua madre per il compleanno?", "¿Qué le vas a regalar a tu madre por su cumpleaños?",
                "Qu'est-ce que tu offres à ta mère pour son anniversaire?", "Co daruješ mámě k narozeninám?")}),
    6628: (LIST, {"t_ru": "резать, стричь", "t_uk": "різати, стригти", "t_en": "to cut", "t_tr": "kesmek",
                  "t_pl": "kroić, ciąć", "t_cs": "krájet, stříhat"}),
    12513: ("«Mir tut der Magen weh» — тот же пример, что Ohr", {**all_x(
        "Iss nicht so viel, sonst verdirbst du dir den Magen", "Не ешь так много, а то испортишь желудок",
        "Не їж так багато, бо зіпсуєш шлунок", "Don't eat so much or you'll upset your stomach",
        "Bu kadar çok yeme, yoksa miden bozulur", "Nie jedz tyle, bo rozstroisz sobie żołądek",
        "Non mangiare così tanto, se no ti rovini lo stomaco", "No comas tanto, que te va a sentar mal al estómago",
        "Ne mange pas trop, sinon tu vas avoir mal à l'estomac", "Nejez tolik, nebo si zkazíš žaludek")}),
    12515: ("«Der Patient wartet beim Arzt» — из детской книжки", {"t_ru": "пациент", "t_uk": "пацієнт", **all_x(
        "Der Arzt hat heute viele Patienten", "У врача сегодня много пациентов", "У лікаря сьогодні багато пацієнтів",
        "The doctor has a lot of patients today", "Doktorun bugün çok hastası var", "Lekarz ma dziś dużo pacjentów",
        "Il medico oggi ha tanti pazienti", "El médico tiene muchos pacientes hoy",
        "Le médecin a beaucoup de patients aujourd'hui", "Lékař má dnes hodně pacientů")}),
    914: ("«пью кофе из чашки» — смысла нет", {**all_x(
        "Möchtest du eine Tasse Tee?", "Хочешь чашку чая?", "Хочеш чашку чаю?", "Would you like a cup of tea?",
        "Bir fincan çay ister misin?", "Chcesz filiżankę herbaty?", "Vuoi una tazza di tè?", "¿Quieres una taza de té?",
        "Tu veux une tasse de thé?", "Dáš si šálek čaje?")}),
    573: (EN + "; " + LIST, {"t_ru": "рынок", "t_uk": "ринок, базар", "t_en": "market", "t_tr": "pazar",
                             "t_pl": "rynek, targ", "x_ru": "В субботу будет рынок",
                             "x_en": "There's a market on Saturday"}),
    2071: ("третий пример про экзамен (schwierig, bestehen); " + LIST, {
        "t_ru": "готовить, готовиться", "t_uk": "готувати, готуватися", "t_en": "to prepare, to get ready",
        "t_tr": "hazırlamak", "t_pl": "przygotowywać",
        **all_x("Ich bereite das Abendessen vor", "Я готовлю ужин", "Я готую вечерю", "I'm getting dinner ready",
                "Akşam yemeğini hazırlıyorum", "Przygotowuję kolację", "Preparo la cena", "Estoy preparando la cena",
                "Je prépare le dîner", "Připravuji večeři")}),
    1658: ("«Wir liefern Lebensmittel nach Hause» — язык рекламы; " + LIST, {
        "t_ru": "доставлять, поставлять", "t_uk": "доставляти, постачати", "t_en": "to deliver, to supply",
        "t_tr": "teslim etmek", "t_pl": "dostarczać, dowozić", "t_es": "entregar, repartir",
        "t_cs": "doručovat, dodávat",
        **all_x("Wann wird das Sofa geliefert?", "Когда доставят диван?", "Коли доставлять диван?",
                "When will the sofa be delivered?", "Kanepe ne zaman teslim edilecek?", "Kiedy dostarczą kanapę?",
                "Quando consegnano il divano?", "¿Cuándo entregan el sofá?", "Le canapé sera livré quand?",
                "Kdy doručí gauč?")}),
    420: (SKEL + "; " + LIST, {
        "t_ru": "некрасивый, уродливый", "t_uk": "негарний, потворний", "t_en": "ugly, nasty", "t_tr": "çirkin",
        "t_pl": "brzydki, paskudny", "t_it": "brutto", "t_es": "feo", "t_fr": "laid, moche", "t_cs": "ošklivý, škaredý",
        **all_x("Ich finde die Farbe ziemlich hässlich", "По-моему, цвет довольно некрасивый",
                "Як на мене, колір доволі негарний", "I think the colour's pretty ugly", "Bence rengi oldukça çirkin",
                "Moim zdaniem ten kolor jest dość brzydki", "Secondo me il colore è piuttosto brutto",
                "A mí el color me parece bastante feo", "Je trouve la couleur plutôt moche",
                "Ta barva je podle mě docela ošklivá")}),
    1879: (SKEL + " («Ich spare Geld»); " + LIST, {
        "t_ru": "копить, экономить", "t_uk": "заощаджувати, економити", "t_en": "to save",
        "t_tr": "para biriktirmek, tasarruf etmek", "t_pl": "oszczędzać",
        **all_x("Ich spare für ein neues Auto", "Я коплю на новую машину", "Я відкладаю на нову машину",
                "I'm saving up for a new car", "Yeni bir araba için para biriktiriyorum", "Oszczędzam na nowy samochód",
                "Risparmio per una macchina nuova", "Estoy ahorrando para un coche nuevo",
                "J'économise pour une nouvelle voiture", "Šetřím na nové auto")}),
    904: (SKEL, {**all_x(
        "Meine Oma kocht die beste Suppe", "Моя бабушка варит самый вкусный суп", "Моя бабуся варить найсмачніший суп",
        "My gran makes the best soup", "En güzel çorbayı babaannem yapar", "Moja babcia gotuje najlepszą zupę",
        "Mia nonna fa la zuppa più buona", "Mi abuela hace la mejor sopa", "Ma grand-mère fait la meilleure soupe",
        "Moje babička vaří nejlepší polévku")}),
    6641: (LIST + "; «район, округ» — другое значение (Landkreis)", {
        "t_ru": "круг", "t_uk": "коло", "t_en": "circle", "t_tr": "daire, çember", "t_pl": "koło, krąg",
        "t_it": "il cerchio, la cerchia", "t_es": "el círculo", "t_fr": "le cercle", "t_cs": "kruh",
        "x_en": "We're sitting in a circle"}),
    771: (TWO + " («примерно» — наречие, своя строка); " + SKEL, {
        "t_ru": "круглый", "t_uk": "круглий", "t_en": "round", "t_tr": "yuvarlak", "t_pl": "okrągły",
        "t_it": "rotondo", "t_es": "redondo", "t_fr": "rond", "t_cs": "kulatý",
        **all_x("Wir haben einen runden Tisch in der Küche", "У нас на кухне круглый стол", "У нас на кухні круглий стіл",
                "We've got a round table in the kitchen", "Mutfakta yuvarlak bir masamız var",
                "W kuchni mamy okrągły stół", "In cucina abbiamo un tavolo rotondo",
                "En la cocina tenemos una mesa redonda", "On a une table ronde dans la cuisine",
                "V kuchyni máme kulatý stůl")}),
    6646: (LIST + "; «Я должен сдать» — калька с muss", {
        "t_ru": "сдать, состоять", "t_uk": "скласти, складатися", "t_en": "to pass, to consist of",
        "t_tr": "geçmek, oluşmak", "t_pl": "zdać, składać się", "t_it": "superare, consistere",
        "t_es": "aprobar, consistir", "t_fr": "réussir, consister", "t_cs": "složit, skládat se",
        "x_ru": "Мне нужно сдать экзамен", "x_uk": "Мені треба скласти іспит", "x_en": "I have to pass the exam"}),
    735: ("«Du prüfst die Dokumente» — неживо; " + LIST, {
        "t_ru": "проверять", "t_uk": "перевіряти", "t_en": "to check, to test", "t_tr": "kontrol etmek",
        "t_pl": "sprawdzać", "t_it": "controllare, verificare", "t_es": "comprobar, revisar",
        "t_fr": "vérifier, contrôler", "t_cs": "kontrolovat, zkoušet",
        **all_x("Prüf bitte, ob die Tür zu ist", "Проверь, пожалуйста, закрыта ли дверь",
                "Перевір, будь ласка, чи зачинені двері", "Please check the door is shut",
                "Kapının kapalı olup olmadığını kontrol et lütfen", "Sprawdź, proszę, czy drzwi są zamknięte",
                "Controlla, per favore, se la porta è chiusa", "Comprueba, por favor, si la puerta está cerrada",
                "Vérifie, s'il te plaît, que la porte est fermée", "Zkontroluj prosím, jestli jsou dveře zavřené")}),
    222: ("«Die Hose ist zu eng» — снова Hose; " + LIST, {
        "t_ru": "узкий, тесный", "t_uk": "вузький, тісний", "t_en": "narrow, tight", "t_tr": "dar",
        "t_pl": "wąski, ciasny", "t_it": "stretto", "t_es": "estrecho", "t_fr": "étroit, serré", "t_cs": "úzký, těsný",
        **all_x("Die Straße ist hier sehr eng", "Здесь очень узкая улица", "Тут дуже вузька вулиця",
                "The street is very narrow here", "Burada sokak çok dar", "Tutaj ulica jest bardzo wąska",
                "Qui la strada è molto stretta", "Aquí la calle es muy estrecha", "Ici, la rue est très étroite",
                "Tady je ulice hodně úzká")}),
    1963: (TIME + "; " + LIST, {
        "t_ru": "тренировка", "t_uk": "тренування", "t_en": "training, workout", "t_tr": "antrenman", "t_pl": "trening",
        "x_ru": "Тренировка начинается в шесть вечера", "x_uk": "Тренування починається о шостій вечора",
        "x_en": "Training starts at 6 pm", "x_it": "L'allenamento comincia alle sei",
        "x_es": "El entrenamiento empieza a las seis"}),
    18144: ("en/it/es «girlfriend/ragazza/novia» — Freundin здесь «подруга»; " + LIST, {
        "t_ru": "рядом, по соседству", "t_uk": "поруч, по сусідству", "t_en": "next door",
        "t_tr": "yan tarafta, bitişikte", "t_pl": "obok, po sąsiedzku", "t_it": "accanto", "t_es": "al lado",
        "t_fr": "à côté", "t_cs": "vedle",
        "x_ru": "Моя подруга живёт по соседству", "x_en": "My friend lives next door",
        "x_it": "La mia amica abita qui accanto", "x_es": "Mi amiga vive al lado",
        "x_cs": "Moje kamarádka bydlí vedle"}),
    6657: (LIST, {"t_ru": "известный, знаменитый", "t_uk": "відомий, знаменитий", "t_en": "famous",
                  "t_tr": "ünlü, meşhur", "t_pl": "słynny, znany"}),
    17075: (LIST, {"t_ru": "поездка, экскурсия", "t_uk": "поїздка, екскурсія", "t_en": "tour, trip",
                   "t_tr": "tur, gezi", "t_pl": "wycieczka, trasa", "t_it": "il giro, il tour",
                   "t_es": "el recorrido, la excursión", "t_fr": "le tour, l'excursion", "t_cs": "výlet, prohlídka",
                   "x_en": "We're doing a tour of the city"}),
    1976: ("«упражняться на пианино» — так не говорят, говорят «позаниматься»", {
        "t_ru": "упражняться, заниматься", "t_uk": "тренуватися, займатися", "t_en": "to practise, to rehearse",
        "t_tr": "pratik yapmak, çalışmak", "t_pl": "ćwiczyć", "t_it": "esercitarsi, provare",
        "t_es": "practicar, ensayar", "t_fr": "s'entraîner, répéter", "t_cs": "cvičit, trénovat",
        "x_ru": "Мне сегодня ещё надо позаниматься на пианино",
        "x_uk": "Мені сьогодні ще треба позайматися на піаніно",
        "x_en": "I still have to practise the piano today"}),
}

# aufgrund — письменное; говорят wegen
REPLACE = [{"id": 6623, "by": 2089, "lang": "de", "why": "aufgrund — письменное, в речи wegen"}]

SPLIT_LATER = {
    526: ["der Käse = ерунда (разг.)"],
    771: ["rund = примерно (rund 100 Euro)"],
    6641: ["der Kreis = район (Landkreis)"],
}
