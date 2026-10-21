"""B1, блок 96: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    13767: ("ru «носит свои волосы, собранные в хвост» — калька", {
        "x_ru": "Она собирает длинные волосы в хвост", "x_uk": "Вона збирає довге волосся у хвіст",
        "x_tr": "Uzun saçlarını at kuyruğu yapıyor"}),
    17373: ("pl — другой смысл; tr — на «Вы» во множественном; " + LIST, {
        "t_uk": "ремінь безпеки", "t_en": "seat belt",
        "x_pl": "Nie zapomnij zapiąć pasa bezpieczeństwa, zanim samochód ruszy",
        "x_tr": "Araba hareket etmeden önce emniyet kemerini takmayı unutma"}),
    2848: ("en «advisor» — американское; " + LIST, {
        "t_ru": "налоговый консультант", "t_uk": "податковий консультант", "t_en": "tax adviser", "t_tr": "mali müşavir",
        "t_it": "il commercialista", "x_en": "I need a tax adviser for my tax return"}),
    11977: ("«… schmeckte nach nichts» — претерит; " + LIST, {
        "t_ru": "пресный, безвкусный", "t_uk": "прісний, несмачний", "t_en": "bland, dull", "t_tr": "tatsız, yavan",
        "t_pl": "mdły, nudny", "t_it": "insipido, scialbo", "t_es": "soso, insípido", "t_fr": "fade, insipide", "t_cs": "mdlý, nudný",
        **all_x("Die Suppe ist mir zu fade, gib mir mal das Salz", "Суп для меня пресноват, дай-ка соль",
                "Суп для мене прісний, дай-но сіль", "The soup's too bland for me, pass me the salt",
                "Çorba bana fazla tatsız geldi, tuzu verir misin", "Zupa jest dla mnie za mdła, podaj mi sól",
                "La zuppa per me è troppo insipida, passami il sale", "La sopa está demasiado sosa para mí, pásame la sal",
                "La soupe est trop fade pour moi, passe-moi le sel", "Polévka je mi moc mdlá, podej mi sůl")}),
    9242: ("en «garbage collector» — американское; " + LIST, {
        "t_ru": "мусорщик", "t_en": "bin man, dustman", "t_tr": "çöpçü", "x_en": "The bin men come every Monday morning"}),
    14780: ("«… klang wunderbar im Konzertsaal» — претерит", {**all_x(
        "Auf der Hochzeit spielt eine Gruppe Streichmusik", "На свадьбе группа играет струнную музыку",
        "На весіллі гурт грає струнну музику", "At the wedding a group is playing string music",
        "Düğünde bir grup yaylı çalgı müziği çalıyor", "Na weselu zespół gra muzykę smyczkową",
        "Al matrimonio un gruppo suona musica per archi", "En la boda un grupo toca música de cuerda",
        "Au mariage, un groupe joue de la musique pour cordes", "Na svatbě hraje skupina smyčcovou hudbu")}),
    14781: ("en «favorite» — американское; «legendär» — громко", {**all_x(
        "Das neue Album von der Band kommt im Mai raus", "Новый альбом этой группы выходит в мае",
        "Новий альбом цього гурту виходить у травні", "The band's new album comes out in May",
        "Grubun yeni albümü mayısta çıkıyor", "Nowy album tego zespołu wychodzi w maju",
        "Il nuovo album della band esce a maggio", "El nuevo álbum del grupo sale en mayo",
        "Le nouvel album du groupe sort en mai", "Nové album té kapely vychází v květnu")}),
    9243: ("«… fuhr er in den Urlaub» — претерит; en «vacation» — американское; " + LIST, {
        "t_ru": "выход на пенсию", "t_uk": "вихід на пенсію", "t_tr": "emeklilik", "t_pl": "przejście na emeryturę",
        "t_fr": "le départ à la retraite",
        **all_x("Nach der Pensionierung will mein Vater endlich reisen", "После выхода на пенсию мой отец хочет наконец путешествовать",
                "Після виходу на пенсію мій батько хоче нарешті подорожувати",
                "After his retirement my dad finally wants to travel",
                "Emeklilikten sonra babam nihayet seyahat etmek istiyor", "Po przejściu na emeryturę tata chce wreszcie podróżować",
                "Dopo il pensionamento mio padre vuole finalmente viaggiare",
                "Después de la jubilación mi padre quiere por fin viajar",
                "Après son départ à la retraite, mon père veut enfin voyager", "Po odchodu do důchodu chce táta konečně cestovat")}),
    18918: (LIST, {
        "t_ru": "чистить щёткой, расчёсывать", "t_uk": "чистити щіткою, розчісувати", "t_en": "to brush", "t_tr": "fırçalamak",
        "t_pl": "szczotkować", "t_cs": "kartáčovat",
        **all_x("Im Frühling muss ich den Hund jeden Tag bürsten", "Весной мне приходится каждый день вычёсывать собаку щёткой",
                "Навесні мені доводиться щодня вичісувати собаку щіткою", "In spring I have to brush the dog every day",
                "İlkbaharda köpeği her gün fırçalamam gerekiyor", "Wiosną muszę codziennie szczotkować psa",
                "In primavera devo spazzolare il cane tutti i giorni", "En primavera tengo que cepillar al perro todos los días",
                "Au printemps, je dois brosser le chien tous les jours", "Na jaře musím psa každý den kartáčovat")}),
    1106: ("пример повторяет Zähler; " + LIST, {
        "t_ru": "снимать показания, читать по бумажке", "t_uk": "знімати показники, читати з папірця",
        "t_en": "to read off, to read a meter", "t_tr": "okumak", "t_pl": "odczytywać, czytać z kartki", "t_fr": "lire, relever",
        "t_cs": "přečíst, odečíst",
        **all_x("Er liest seine Rede einfach vom Zettel ab", "Он просто читает свою речь по бумажке",
                "Він просто читає свою промову з папірця", "He just reads his speech off a piece of paper",
                "Konuşmasını düpedüz kâğıttan okuyor", "Po prostu czyta swoje przemówienie z kartki",
                "Legge semplicemente il suo discorso da un foglietto", "Simplemente lee su discurso de un papel",
                "Il lit simplement son discours sur une feuille", "Svůj projev prostě čte z papíru")}),
    11978: ("«kostet fünf Euro die Dose» — пусто; en «per can» — американское; " + LIST, {
        "t_ru": "кошачий корм", "t_uk": "корм для котів", "t_pl": "karma dla kota",
        **all_x("Vergiss nicht, Katzenfutter zu kaufen, die Dose ist leer", "Не забудь купить кошачий корм, банка пустая",
                "Не забудь купити корм для котів, банка порожня", "Don't forget to buy cat food, the tin's empty",
                "Kedi maması almayı unutma, kutu boş", "Nie zapomnij kupić karmy dla kota, puszka jest pusta",
                "Non dimenticare di comprare il cibo per gatti, la scatoletta è vuota",
                "No te olvides de comprar comida para gatos, la lata está vacía",
                "N'oublie pas d'acheter de la nourriture pour chats, la boîte est vide",
                "Nezapomeň koupit krmivo pro kočky, plechovka je prázdná")}),
    17375: (LIST, {"t_ru": "автомойка", "t_tr": "oto yıkama", "t_pl": "myjnia samochodowa, myjnia", "t_es": "el lavadero de coches"}),
    15828: ("pl потерял слово; " + LIST, {
        "t_ru": "скармливать", "t_uk": "згодовувати", "t_en": "to feed", "t_tr": "yem olarak vermek", "t_pl": "skarmiać",
        "t_it": "dare da mangiare, dare in pasto", "t_es": "dar de comer", "t_fr": "nourrir avec, donner à manger",
        "x_pl": "Resztki jedzenia skarmiamy kurom"}),
    2119: ("«Es regnet zeitweise» — пусто; " + LIST, {
        "t_ru": "временами", "t_uk": "час від часу", "t_en": "at times", "t_tr": "zaman zaman", "t_pl": "chwilami, okresowo",
        "t_it": "a tratti", "t_es": "a ratos", "t_fr": "par moments", "t_cs": "chvílemi, občas",
        **all_x("Zeitweise war die Straße wegen Schnee gesperrt", "Временами дорогу перекрывали из-за снега",
                "Час від часу дорогу перекривали через сніг", "At times the road was closed because of snow",
                "Yol kar yüzünden zaman zaman kapalıydı", "Chwilami droga była zamknięta z powodu śniegu",
                "A tratti la strada era chiusa per la neve", "A ratos la carretera estaba cortada por la nieve",
                "Par moments, la route était fermée à cause de la neige", "Silnice byla kvůli sněhu chvílemi uzavřená")}),
    8486: ("«Er wälzte sich …» — претерит; " + LIST, {
        "t_ru": "ворочаться, катать", "t_uk": "вертітися, котити", "t_en": "to toss and turn, to roll",
        "t_tr": "dönüp durmak, yuvarlamak", "t_pl": "przewracać się z boku na bok, tarzać się", "t_it": "rigirarsi, rotolare",
        "t_es": "dar vueltas, revolcarse", "t_fr": "se retourner, rouler", "t_cs": "převalovat se, válet",
        **all_x("Ich wälze mich jede Nacht stundenlang im Bett herum", "Я каждую ночь часами ворочаюсь в постели",
                "Я щоночі годинами вертюся в ліжку", "Every night I toss and turn in bed for hours",
                "Her gece saatlerce yatakta dönüp duruyorum", "Co noc godzinami przewracam się w łóżku z boku na bok",
                "Ogni notte mi rigiro nel letto per ore", "Cada noche me paso horas dando vueltas en la cama",
                "Chaque nuit, je me retourne pendant des heures dans mon lit", "Každou noc se hodiny převaluju v posteli")}),
    15829: ("tr «bahar aylarında» — книжно", {"x_tr": "İlkbaharda çocuklar çayırda papatya topluyor"}),
    14782: ("«… leitete das Orchester mit großer Eleganz» — претерит, книжно", {**all_x(
        "Der Dirigent hebt den Stab, und das Konzert beginnt", "Дирижёр поднимает палочку, и концерт начинается",
        "Диригент піднімає паличку, і концерт починається", "The conductor raises his baton and the concert begins",
        "Şef çubuğunu kaldırıyor ve konser başlıyor", "Dyrygent unosi batutę i koncert się zaczyna",
        "Il direttore d'orchestra alza la bacchetta e il concerto comincia",
        "El director de orquesta levanta la batuta y empieza el concierto",
        "Le chef d'orchestre lève sa baguette et le concert commence", "Dirigent zvedne taktovku a koncert začíná")}),
    18921: ("en «check off» — американское; " + LIST, {
        "t_ru": "отмечать галочкой, считать законченным", "t_en": "to tick off, to put behind one", "t_tr": "işaretlemek, tik atmak",
        "t_pl": "odhaczać, zaznaczać", "t_es": "tachar, marcar", "t_fr": "cocher, rayer",
        "x_en": "I tick off the points when I've finished them"}),
    11466: ("«… gaben mir neue Kraft» — претерит; " + LIST, {
        "t_ru": "ободряющий, обнадёживающий", "t_uk": "підбадьорливий, обнадійливий", "t_en": "encouraging",
        "t_tr": "cesaret verici, umut verici", "t_pl": "zachęcający, pokrzepiający", "t_es": "alentador",
        **all_x("Das Gespräch mit der Ärztin war sehr ermutigend", "Разговор с врачом был очень обнадёживающим",
                "Розмова з лікаркою була дуже обнадійливою", "The conversation with the doctor was very encouraging",
                "Doktorla konuşma çok umut vericiydi", "Rozmowa z lekarką była bardzo pokrzepiająca",
                "Il colloquio con la dottoressa è stato molto incoraggiante", "La conversación con la doctora fue muy alentadora",
                "La discussion avec la médecin a été très encourageante", "Rozhovor s doktorkou byl velmi povzbudivý")}),
    9617: ("«… hielt eine Rede» — претерит; en «principal» — американское; " + LIST, {
        "t_ru": "директор школы", "t_en": "head teacher, headmaster", "t_it": "il preside", "t_es": "el director",
        "t_fr": "le directeur, le proviseur",
        **all_x("Wegen der Prügelei muss ich morgen zum Schulleiter", "Из-за драки мне завтра надо к директору школы",
                "Через бійку мені завтра треба до директора школи", "Because of the fight I've got to see the head teacher tomorrow",
                "Kavga yüzünden yarın okul müdürüne gitmem lazım", "Przez bójkę muszę jutro iść do dyrektora szkoły",
                "Per la rissa domani devo andare dal preside", "Por la pelea mañana tengo que ir al director",
                "À cause de la bagarre, je dois aller chez le directeur demain", "Kvůli rvačce musím zítra k řediteli školy")}),
    12380: ("«Die Piraten legten …» — претерит", {**all_x(
        "Für den Kindergeburtstag male ich eine Schatzkarte", "Для детского дня рождения я рисую карту сокровищ",
        "Для дитячого дня народження я малюю карту скарбів", "I'm drawing a treasure map for the children's party",
        "Çocuk doğum günü partisi için bir hazine haritası çiziyorum", "Na urodziny dziecka rysuję mapę skarbów",
        "Per la festa di compleanno dei bambini disegno una mappa del tesoro",
        "Para el cumpleaños infantil dibujo un mapa del tesoro",
        "Pour l'anniversaire des enfants, je dessine une carte au trésor", "Na dětskou oslavu kreslím mapu pokladu")}),
    12381: ("«Die beiden machten …» — претерит", {
        "t_it": "il ballo, il balletto",
        **all_x("Darf ich um ein Tänzchen bitten?", "Разрешите пригласить вас на танец?", "Дозвольте запросити вас на танець?",
                "May I have this dance?", "Benimle bir dans eder misiniz?", "Czy mogę prosić do tańca?",
                "Posso invitarla a fare un ballo?", "¿Me concede este baile?", "Vous m'accordez cette danse?",
                "Smím prosit o tanec?")}),
    9245: ("«… kümmerte sich …» — претерит; " + LIST, {
        "t_ru": "фермерша, крестьянка", "t_uk": "фермерка, селянка", "t_en": "farmer's wife, farmer", "t_tr": "çiftçi kadın",
        "t_pl": "rolniczka, gospodyni", "t_it": "la contadina", "t_es": "la granjera, la campesina", "t_fr": "la fermière",
        "t_cs": "farmářka, selka",
        **all_x("Die Bäuerin verkauft samstags Käse auf dem Markt", "По субботам фермерша продаёт на рынке сыр",
                "Щосуботи фермерка продає на ринку сир", "On Saturdays the farmer's wife sells cheese at the market",
                "Çiftçi kadın cumartesileri pazarda peynir satıyor", "Rolniczka w soboty sprzedaje ser na targu",
                "La contadina il sabato vende formaggio al mercato", "La granjera vende queso en el mercado los sábados",
                "Le samedi, la fermière vend du fromage au marché", "Farmářka v sobotu prodává na trhu sýr")}),
    9618: (LIST, {"t_ru": "введение, вступление", "t_uk": "вступ", "t_en": "introduction", "t_tr": "giriş",
                  "t_pl": "wstęp, wprowadzenie", "t_it": "l'introduzione", "t_es": "la introducción", "t_fr": "l'introduction",
                  "t_cs": "úvod"}),
    18922: ("«… brauchte er …» — претерит; пометки (colloq./hovor.); " + LIST, {
        "t_ru": "дневной сон", "t_uk": "денний сон", "t_en": "afternoon nap", "t_tr": "öğle uykusu",
        "t_pl": "popołudniowa drzemka, drzemka po obiedzie", "t_it": "il riposino, la pennichella", "t_cs": "polední spánek, šlofík",
        **all_x("Opa macht jeden Tag nach dem Essen einen Mittagsschlaf", "У дедушки каждый день после обеда дневной сон",
                "У дідуся щодня після обіду денний сон", "Grandad has an afternoon nap every day after lunch",
                "Dedem her gün yemekten sonra öğle uykusu çekiyor",
                "Dziadek codziennie po obiedzie ucina sobie popołudniową drzemkę",
                "Il nonno ogni giorno dopo pranzo fa il riposino", "El abuelo duerme la siesta todos los días después de comer",
                "Papi fait la sieste tous les jours après le déjeuner", "Děda si každý den po obědě dá šlofíka")}),
    11468: ("«Er war ein echter Optimist, egal wie …» — книжно", {
        "t_tr": "iyimser",
        **all_x("Mein Vater ist ein unverbesserlicher Optimist", "Мой отец — неисправимый оптимист", "Мій батько — невиправний оптиміст",
                "My dad is an incurable optimist", "Babam iflah olmaz bir iyimser", "Mój tata jest niepoprawnym optymistą",
                "Mio padre è un ottimista incorreggibile", "Mi padre es un optimista incorregible",
                "Mon père est un optimiste incorrigible", "Můj táta je nenapravitelný optimista")}),
    8494: (LIST, {"t_ru": "вставить, вписаться", "t_uk": "вставити, вписатися", "t_en": "to insert, to fit in",
                  "t_tr": "eklemek, uyum sağlamak", "t_pl": "wstawić, wpasować się", "t_it": "inserire", "t_es": "insertar",
                  "t_fr": "insérer", "t_cs": "vložit"}),
    18923: ("pl «przy okazji» — другой смысл; " + LIST, {
        "t_ru": "параллельно, заодно", "t_uk": "паралельно, заодно", "t_en": "on the side", "t_tr": "bir yandan da",
        "t_pl": "dodatkowo, przy okazji", "t_it": "parallelamente", "t_es": "al mismo tiempo, aparte", "t_fr": "à côté, en parallèle",
        "t_cs": "vedle toho, souběžně", "x_pl": "Dodatkowo studiuje jeszcze angielski",
        "x_en": "He's also studying English on the side"}),
    891: ("«Die Strümpfe sind schwarz» — пусто; " + LIST, {
        "t_ru": "чулок, носок", "t_uk": "панчоха, шкарпетка", "t_en": "stocking, sock", "t_tr": "çorap", "t_pl": "pończocha, skarpeta",
        "t_it": "la calza", "t_es": "la media, el calcetín", "t_fr": "le bas, la chaussette", "t_cs": "punčocha, ponožka",
        **all_x("Zu Weihnachten hängen wir einen Strumpf an den Kamin", "На Рождество мы вешаем чулок у камина",
                "На Різдво ми вішаємо панчоху біля каміна", "At Christmas we hang a stocking by the fireplace",
                "Noel'de şöminenin yanına bir çorap asıyoruz", "Na Boże Narodzenie wieszamy skarpetę przy kominku",
                "A Natale appendiamo una calza al camino", "En Navidad colgamos un calcetín junto a la chimenea",
                "À Noël, on accroche une chaussette à la cheminée", "O Vánocích věšíme punčochu ke krbu")}),
    18459: (LIST, {"t_ru": "швабра", "t_uk": "швабра", "t_tr": "paspas", "t_it": "il mocio", "t_es": "la fregona",
                   "t_fr": "le balai-serpillière"}),
    2146: ("en «mail» — американское; " + LIST, {
        "t_ru": "отправить", "t_uk": "відправити", "t_en": "to send off, to post", "t_tr": "göndermek", "t_pl": "wysłać",
        "t_it": "spedire", "t_es": "enviar", "t_fr": "envoyer", "t_cs": "odeslat", "x_en": "I'll post the letter straight away"}),
    868: ("«… ist immer montags» — врач принимает не раз в неделю; " + LIST, {
        "t_ru": "часы приёма, приём", "t_uk": "години прийому", "t_en": "office hours, surgery hours",
        "t_tr": "görüşme saati, muayene saati", "t_pl": "godziny przyjęć", "t_it": "l'orario di ricevimento",
        "t_es": "el horario de consulta", "t_fr": "les heures de consultation", "t_cs": "konzultační hodiny, ordinační hodiny",
        **all_x("Die Lehrerin hat dienstags Sprechstunde für die Eltern", "У учительницы по вторникам часы приёма для родителей",
                "Учителька по вівторках має години прийому для батьків", "The teacher has office hours for parents on Tuesdays",
                "Öğretmenin salı günleri veliler için görüşme saati var", "Nauczycielka ma we wtorki godziny przyjęć dla rodziców",
                "La maestra ha l'orario di ricevimento per i genitori il martedì",
                "La profesora tiene horario de consulta para los padres los martes",
                "La maîtresse a ses heures de consultation pour les parents le mardi",
                "Paní učitelka má v úterý konzultační hodiny pro rodiče")}),
    2737: ("«Meine Qualifikationen sind sehr gut» — пусто; " + LIST, {
        "t_ru": "квалификация", "t_uk": "кваліфікація", "t_en": "qualification", "t_tr": "nitelik, yeterlilik",
        "t_pl": "kwalifikacje, kwalifikacja", "t_it": "la qualifica", "t_es": "la cualificación", "t_fr": "la qualification",
        "t_cs": "kvalifikace",
        **all_x("Für den Job fehlt mir leider die nötige Qualifikation",
                "Для этой работы мне, к сожалению, не хватает нужной квалификации",
                "Для цієї роботи мені, на жаль, бракує потрібної кваліфікації",
                "Unfortunately I don't have the right qualification for the job",
                "Ne yazık ki bu iş için gerekli niteliğe sahip değilim", "Niestety brakuje mi kwalifikacji do tej pracy",
                "Purtroppo mi manca la qualifica necessaria per il lavoro",
                "Por desgracia, me falta la cualificación necesaria para el trabajo",
                "Malheureusement, il me manque la qualification nécessaire pour le poste",
                "Bohužel mi na tu práci chybí potřebná kvalifikace")}),
    16860: ("«Die Regierung führte … durch» — претерит, язык новостей; " + LIST, {
        "t_ru": "реформа", "t_uk": "реформа", "t_tr": "reform",
        **all_x("Über die neue Reform vom Schulsystem streiten alle", "О новой реформе школьной системы все спорят",
                "Про нову реформу шкільної системи всі сперечаються", "Everyone's arguing about the new school reform",
                "Okul sistemindeki yeni reform herkesi tartıştırıyor", "O nową reformę szkolnictwa wszyscy się kłócą",
                "Tutti discutono della nuova riforma della scuola", "Todo el mundo discute sobre la nueva reforma escolar",
                "Tout le monde se dispute au sujet de la nouvelle réforme scolaire",
                "O nové školské reformě se všichni hádají")}),
    9622: ("«… ist wichtig für die Zukunft» — лозунг; " + LIST + " (было четыре значения)", {
        "t_ru": "поддержка, содействие", "t_uk": "підтримка, сприяння", "t_en": "support, funding", "t_tr": "destek, teşvik",
        "t_pl": "wsparcie, dofinansowanie", "t_it": "il sostegno, il finanziamento", "t_es": "el apoyo, la ayuda",
        "t_fr": "le soutien, le financement", "t_cs": "podpora, financování",
        **all_x("Für das Studium bekomme ich eine Förderung vom Staat", "На учёбу я получаю поддержку от государства",
                "На навчання я отримую підтримку від держави", "I get funding from the state for my studies",
                "Üniversite için devletten destek alıyorum", "Na studia dostaję dofinansowanie od państwa",
                "Per gli studi ricevo un finanziamento dallo Stato", "Para los estudios recibo una ayuda del Estado",
                "Pour mes études, je reçois un financement de l'État", "Na studium dostávám od státu podporu")}),
    11981: ("en «oatmeal» — американское; " + LIST, {
        "t_ru": "овсяные хлопья", "t_uk": "вівсяні пластівці", "t_en": "porridge oats, oats", "t_tr": "yulaf ezmesi",
        "t_pl": "płatki owsiane", "t_es": "los copos de avena",
        "x_en": "For breakfast I always have porridge oats with milk"}),
}

REPLACE = [
    {"id": 15306, "by": 15827, "lang": "de", "why": "Turteltäubchen — уменьшительное от Turteltaube"},
    {"id": 15837, "by": 2962, "lang": "de", "why": "verschmutzt — форма слова verschmutzen"},
]

SPLIT_LATER = {}
