"""B1, блок 87: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18881: ("«Die Wartezeit beim Zahnarzt war lang» — пусто; " + LIST, {
        "t_ru": "время ожидания", "t_uk": "час очікування", "t_en": "waiting time", "t_tr": "bekleme süresi", "t_pl": "czas oczekiwania",
        "t_it": "il tempo d'attesa", "t_es": "el tiempo de espera", "t_fr": "le temps d'attente", "t_cs": "čekací doba",
        **all_x("Wie lange ist die Wartezeit für einen Termin beim Facharzt?", "Какое время ожидания записи к специалисту?",
                "Який час очікування на прийом до фахівця?", "What's the waiting time for an appointment with a specialist?",
                "Uzman randevusu için bekleme süresi ne kadar?", "Jaki jest czas oczekiwania na wizytę u specjalisty?",
                "Quanto è il tempo d'attesa per una visita specialistica?", "¿Cuál es el tiempo de espera para una cita con el especialista?",
                "Quel est le temps d'attente pour un rendez-vous chez le spécialiste?", "Jaká je čekací doba na termín u specialisty?")}),
    15245: ("«Der Säugling schläft nach dem Füttern» — пусто; " + LIST, {
        "t_ru": "младенец, грудной ребёнок", "t_uk": "немовля", "t_en": "infant, baby", "t_tr": "bebek, süt çocuğu", "t_pl": "niemowlę",
        "t_it": "il neonato, il lattante", "t_es": "el bebé, el lactante", "t_fr": "le nourrisson", "t_cs": "kojenec",
        **all_x("Für Säuglinge ist Honig nicht geeignet", "Младенцам мёд не подходит", "Немовлятам мед не підходить",
                "Honey isn't suitable for infants", "Bal bebekler için uygun değil", "Miód nie jest odpowiedni dla niemowląt",
                "Il miele non è adatto ai neonati", "La miel no es adecuada para bebés", "Le miel ne convient pas aux nourrissons",
                "Med není vhodný pro kojence")}),
    14876: ("«Die ungeraden Zahlen sind 1, 3, 5» — учебник; " + LIST, {
        "t_ru": "нечётный", "t_uk": "непарний", "t_en": "odd", "t_tr": "tek", "t_pl": "nieparzysty", "t_cs": "lichý",
        **all_x("Wir wohnen auf der ungeraden Straßenseite", "Мы живём на нечётной стороне улицы", "Ми живемо на непарному боці вулиці",
                "We live on the odd-numbered side of the street", "Sokağın tek numaralı tarafında oturuyoruz",
                "Mieszkamy po nieparzystej stronie ulicy", "Abitiamo sul lato dei numeri dispari",
                "Vivimos en la acera de los números impares", "On habite du côté impair de la rue", "Bydlíme na liché straně ulice")}),
    8189: ("«Die ägyptische Kultur ist faszinierend» — путеводитель", {
        "t_tr": "Mısırlı, Mısır",
        **all_x("Mein Kollege hat ägyptische Wurzeln", "У моего коллеги египетские корни", "У мого колеги єгипетське коріння",
                "My colleague has Egyptian roots", "İş arkadaşımın Mısırlı kökleri var", "Mój kolega ma egipskie korzenie",
                "Il mio collega ha origini egiziane", "Mi compañero tiene raíces egipcias", "Mon collègue a des racines égyptiennes",
                "Můj kolega má egyptské kořeny")}),
    227: ("«Die Erdbeeren sind süß» — пусто; " + LIST, {
        "t_ru": "клубника", "t_uk": "полуниця", "t_pl": "truskawka", "t_es": "la fresa",
        **all_x("Erdbeeren mit Sahne, mehr brauche ich im Sommer nicht", "Клубника со сливками — больше мне летом ничего не надо",
                "Полуниця з вершками — більше мені влітку нічого не треба", "Strawberries and cream, that's all I need in summer",
                "Kremalı çilek, yazın başka bir şeye ihtiyacım yok", "Truskawki z bitą śmietaną, latem nic więcej mi nie trzeba",
                "Fragole con la panna: d'estate non mi serve altro", "Fresas con nata: en verano no necesito nada más",
                "Des fraises à la crème, l'été il ne m'en faut pas plus", "Jahody se šlehačkou, nic víc v létě nepotřebuju")}),
    14246: ("en «mailbox» — американское; в речи Postfach — и ящик почты; " + LIST, {
        "t_ru": "почтовый ящик, абонентский ящик", "t_uk": "поштова скринька, абонентська скринька", "t_en": "PO box, inbox",
        "t_tr": "posta kutusu", "t_pl": "skrzynka pocztowa, skrytka pocztowa", "t_it": "la casella postale, la casella di posta",
        "t_es": "el apartado de correos, la bandeja de entrada", "t_fr": "la boîte postale, la boîte de réception",
        "t_cs": "poštovní přihrádka, schránka",
        **all_x("Die Mail ist nicht in meinem Postfach angekommen", "Письмо не пришло в мой почтовый ящик",
                "Лист не прийшов у мою поштову скриньку", "The email didn't arrive in my inbox", "E-posta posta kutuma gelmedi",
                "Mail nie dotarł do mojej skrzynki pocztowej", "La mail non è arrivata nella mia casella di posta",
                "El correo no ha llegado a mi bandeja de entrada", "Le mail n'est pas arrivé dans ma boîte de réception",
                "E-mail mi nepřišel do schránky")}),
    18404: ("«Wir gingen über den Steg …» — претерит; " + LIST, {
        "t_ru": "мостик, причал", "t_uk": "місток, помост", "t_en": "jetty, footbridge", "t_tr": "iskele", "t_pl": "pomost, kładka",
        "t_it": "il pontile, la passerella", "t_es": "el embarcadero, la pasarela", "t_fr": "le ponton, la passerelle", "t_cs": "molo, lávka",
        **all_x("Abends sitzen wir am Steg und halten die Füße ins Wasser", "По вечерам мы сидим на мостике и опускаем ноги в воду",
                "Увечері ми сидимо на помості й опускаємо ноги у воду", "In the evenings we sit on the jetty with our feet in the water",
                "Akşamları iskelede oturup ayaklarımızı suya sokuyoruz", "Wieczorami siedzimy na pomoście z nogami w wodzie",
                "La sera ci sediamo sul pontile con i piedi nell'acqua", "Por las tardes nos sentamos en el embarcadero con los pies en el agua",
                "Le soir, on s'assoit sur le ponton, les pieds dans l'eau", "Večer sedíme na molu a máme nohy ve vodě")}),
    11930: ("пример повторяет erfrischend; " + LIST, {
        "t_ru": "мята, мятная конфета", "t_uk": "м'ята, м'ятна цукерка", "t_en": "peppermint, mint", "t_tr": "nane, nane şekeri",
        "t_pl": "mięta, miętówka", "t_it": "la menta, la mentina", "t_es": "la menta", "t_fr": "la menthe", "t_cs": "máta, mátový bonbon",
        **all_x("Möchtest du ein Pfefferminz?", "Хочешь мятную конфету?", "Хочеш м'ятну цукерку?", "Would you like a peppermint?",
                "Nane şekeri ister misin?", "Chcesz miętówkę?", "Vuoi una mentina?", "¿Quieres un caramelo de menta?",
                "Tu veux un bonbon à la menthe?", "Dáš si mátový bonbon?")}),
    9904: ("«Das ist ein Sonderangebot» — пусто; " + LIST, {
        "t_ru": "акция, спецпредложение", "t_uk": "акція, спецпропозиція", "t_en": "special offer", "t_tr": "indirim, kampanya",
        "t_pl": "promocja, oferta specjalna", "t_it": "l'offerta speciale", "t_es": "la oferta", "t_fr": "la promotion, l'offre spéciale",
        "t_cs": "akce, akční nabídka",
        **all_x("Das Öl war im Sonderangebot, da habe ich gleich drei gekauft", "Масло было по акции, так что я сразу купил три",
                "Олія була за акцією, тож я одразу купив три", "The oil was on special offer, so I bought three straight away",
                "Yağ indirimdeydi, hemen üç tane aldım", "Olej był w promocji, więc od razu kupiłem trzy",
                "L'olio era in offerta speciale, così ne ho comprati subito tre", "El aceite estaba de oferta, así que compré tres",
                "L'huile était en promotion, alors j'en ai acheté trois", "Olej byl v akci, tak jsem hned koupil tři")}),
    12340: ("en «favorite» — американское", {"t_en": "favourite film", "x_en": "My favourite film is a classic from the 80s"}),
    11931: ("«… nicht mehr zu essen» — тавтология; " + LIST, {
        "t_ru": "гнилой", "t_uk": "гнилий", "t_en": "rotten", "t_tr": "çürümüş", "t_pl": "zgniły", "t_cs": "shnilý",
        **all_x("Im Kühlschrank liegt noch eine verfaulte Tomate", "В холодильнике ещё лежит гнилой помидор",
                "У холодильнику ще лежить гнилий помідор", "There's still a rotten tomato in the fridge",
                "Buzdolabında hâlâ çürümüş bir domates var", "W lodówce leży jeszcze zgniły pomidor",
                "In frigo c'è ancora un pomodoro marcio", "En la nevera todavía hay un tomate podrido",
                "Il y a encore une tomate pourrie dans le frigo", "V lednici je ještě shnilé rajče")}),
    12975: ("«Das Wohlbefinden der Kinder ist uns sehr wichtig» — проспект; " + LIST, {
        "t_ru": "самочувствие, благополучие", "t_uk": "самопочуття, благополуччя", "t_en": "well-being", "t_tr": "iyilik hali, esenlik",
        "t_pl": "samopoczucie", "t_cs": "pohoda, blaho",
        **all_x("Für mein Wohlbefinden brauche ich jeden Tag frische Luft", "Для хорошего самочувствия мне каждый день нужен свежий воздух",
                "Для доброго самопочуття мені щодня потрібне свіже повітря", "For my well-being I need fresh air every day",
                "İyilik halim için her gün temiz havaya ihtiyacım var", "Dla dobrego samopoczucia potrzebuję codziennie świeżego powietrza",
                "Per il mio benessere ho bisogno di aria fresca ogni giorno", "Para mi bienestar necesito aire fresco todos los días",
                "Pour mon bien-être, j'ai besoin d'air frais tous les jours", "Pro svou pohodu potřebuju každý den čerstvý vzduch")}),
    8193: ("en «sweater» — американское; " + LIST, {
        "t_ru": "садиться (при стирке), уменьшаться", "t_uk": "сідати (після прання), зменшуватися", "t_en": "to shrink",
        "t_tr": "çekmek, küçülmek", "t_pl": "kurczyć się, zmniejszać się", "t_it": "restringersi, ridursi", "t_es": "encogerse, reducirse",
        "t_fr": "rétrécir, diminuer", "t_cs": "srazit se, zmenšovat se", "x_en": "The jumper has shrunk in the wash"}),
    18405: (LIST, {"t_ru": "подвальный этаж, цокольный этаж", "t_uk": "цокольний поверх, підвал", "t_en": "basement, lower floor",
                   "t_tr": "bodrum kat", "t_pl": "suterena, piwnica", "t_it": "il seminterrato", "t_es": "el sótano", "t_fr": "le sous-sol",
                   "t_cs": "suterén"}),
    11315: (LIST, {"t_en": "unforgettable"}),
    9597: ("ru «Я должен» — калька; шаблон Freitag; " + LIST, {
        "t_ru": "доклад, реферат", "t_uk": "доповідь, реферат", "t_en": "presentation, talk", "t_tr": "sunum", "t_pl": "referat, prezentacja",
        "t_it": "la relazione", "t_es": "la exposición, el trabajo", "t_fr": "l'exposé", "t_cs": "referát",
        **all_x("Mein Referat war viel zu lang, ich musste es kürzen", "Мой доклад был слишком длинным, пришлось его сокращать",
                "Моя доповідь була задовга, довелося її скорочувати", "My presentation was much too long, I had to cut it down",
                "Sunumum çok uzundu, kısaltmam gerekti", "Mój referat był za długi, musiałem go skrócić",
                "La mia relazione era troppo lunga, ho dovuto accorciarla", "Mi exposición era demasiado larga, tuve que acortarla",
                "Mon exposé était beaucoup trop long, j'ai dû le raccourcir", "Můj referát byl moc dlouhý, musel jsem ho zkrátit")}),
    8194: ("пометка (hovor.); " + LIST, {
        "t_ru": "болтаться, свисать", "t_uk": "бовтатися, звисати", "t_en": "to dangle", "t_tr": "sallanmak, sarkmak",
        "t_pl": "dyndać, zwisać", "t_it": "penzolare, dondolare", "t_es": "balancearse, colgar", "t_fr": "se balancer, pendre",
        "t_cs": "houpat se, viset"}),
    675: ("шаблон «gerne»", {**all_x(
        "In jeden Salat gehört ein Schuss Olivenöl", "В любой салат нужно немного оливкового масла", "У будь-який салат треба трохи оливкової олії",
        "Every salad needs a splash of olive oil", "Her salataya biraz zeytinyağı lazım", "Do każdej sałatki trzeba trochę oliwy z oliwek",
        "In ogni insalata ci vuole un filo d'olio d'oliva", "Cualquier ensalada necesita un chorrito de aceite de oliva",
        "Il faut un filet d'huile d'olive dans chaque salade", "Do každého salátu patří trochu olivového oleje")}),
    1815: ("«Die Rückfahrt dauert zwei Stunden» — справка; " + LIST, {
        "t_ru": "обратный путь", "t_uk": "зворотний шлях", "t_en": "return journey, way back", "t_tr": "dönüş yolu",
        "t_pl": "droga powrotna", "t_it": "il viaggio di ritorno, il ritorno", "t_es": "el viaje de vuelta", "t_fr": "le retour",
        "t_cs": "cesta zpět, zpáteční cesta",
        **all_x("Auf der Rückfahrt haben wir im Stau gestanden", "На обратном пути мы стояли в пробке", "На зворотному шляху ми стояли в заторі",
                "We were stuck in traffic on the way back", "Dönüş yolunda trafikte kaldık", "W drodze powrotnej staliśmy w korku",
                "Durante il viaggio di ritorno siamo rimasti in coda", "En el viaje de vuelta estuvimos en un atasco",
                "Au retour, on était dans les bouchons", "Cestou zpět jsme stáli v zácpě")}),
    15755: (LIST, {"t_ru": "ручной, прирученный", "t_uk": "ручний, приручений", "t_en": "tame", "t_tr": "evcil, uysal",
                   "t_pl": "oswojony", "t_it": "addomesticato, docile", "t_es": "manso", "t_fr": "apprivoisé", "t_cs": "krotký"}),
    11933: ("«Stell deine Kaffeetasse auf die Untertasse» — пусто", {**all_x(
        "Vorsicht, auf die Untertasse ist Kaffee übergeschwappt", "Осторожно, кофе пролился на блюдце", "Обережно, кава пролилася на блюдце",
        "Careful, some coffee has spilt into the saucer", "Dikkat, kahve fincan tabağına taştı", "Uważaj, kawa wylała się na spodek",
        "Attento, il caffè è traboccato nel piattino", "Cuidado, se ha derramado café en el platillo",
        "Attention, du café a débordé dans la soucoupe", "Pozor, kafe vyteklo na podšálek")}),
    13753: ("«… sieht wirklich cool aus» — пусто", {**all_x(
        "Bei dem Regen ziehe ich lieber nicht die Lederjacke an", "В такой дождь кожаную куртку я лучше не надену",
        "У такий дощ шкіряну куртку я краще не вдягатиму", "In this rain I'd rather not wear my leather jacket",
        "Bu yağmurda deri ceketimi giymesem iyi olur", "W taki deszcz wolę nie zakładać skórzanej kurtki",
        "Con questa pioggia preferisco non mettere la giacca di pelle", "Con esta lluvia prefiero no ponerme la chaqueta de cuero",
        "Avec cette pluie, je préfère ne pas mettre mon blouson en cuir", "V tomhle dešti si koženou bundu radši nevezmu")}),
    16702: ("«Die Ministerin gab eine Pressekonferenz» — претерит, новости", {**all_x(
        "Die Ministerin besucht morgen unsere Schule", "Министр завтра посетит нашу школу", "Міністерка завтра відвідає нашу школу",
        "The minister is visiting our school tomorrow", "Bakan yarın okulumuzu ziyaret ediyor", "Pani minister jutro odwiedzi naszą szkołę",
        "La ministra domani visita la nostra scuola", "La ministra visita mañana nuestro colegio",
        "La ministre vient visiter notre école demain", "Ministryně zítra navštíví naši školu")}),
    2648: ("«Das ist ein langfristiger Plan für die Zukunft» — тавтология; " + LIST, {
        "t_ru": "долгосрочный, в долгосрочной перспективе", "t_uk": "довгостроковий, у довгостроковій перспективі",
        "t_en": "long-term, in the long run", "t_tr": "uzun vadeli, uzun vadede", "t_pl": "długoterminowy, na dłuższą metę",
        "t_cs": "dlouhodobý, dlouhodobě",
        **all_x("Langfristig wollen wir ein Haus auf dem Land kaufen", "В долгосрочной перспективе мы хотим купить дом за городом",
                "У довгостроковій перспективі ми хочемо купити будинок за містом", "In the long run we want to buy a house in the country",
                "Uzun vadede köyde bir ev almak istiyoruz", "Na dłuższą metę chcemy kupić dom na wsi",
                "A lungo termine vogliamo comprare una casa in campagna", "A largo plazo queremos comprar una casa en el campo",
                "À long terme, on veut acheter une maison à la campagne", "Dlouhodobě chceme koupit dům na venkově")}),
    15757: ("«Die Tannen wachsen in den Bergen» — учебник", {**all_x(
        "Zu Weihnachten kaufen wir immer eine echte Tanne", "На Рождество мы всегда покупаем настоящую ель",
        "На Різдво ми завжди купуємо справжню ялицю", "We always buy a real fir tree for Christmas",
        "Noel için hep gerçek bir köknar alıyoruz", "Na święta zawsze kupujemy prawdziwą jodłę",
        "A Natale compriamo sempre un abete vero", "En Navidad siempre compramos un abeto de verdad",
        "À Noël, on achète toujours un vrai sapin", "Na Vánoce vždycky kupujeme opravdovou jedli")}),
    409: ("пример — пусто; " + LIST, {
        "t_ru": "высотка, многоэтажка", "t_uk": "багатоповерхівка, висотний будинок", "t_en": "tower block, high-rise",
        "t_tr": "yüksek bina, gökdelen", "t_pl": "wieżowiec", "t_it": "il grattacielo, il palazzone", "t_es": "el rascacielos, la torre",
        "t_fr": "la tour", "t_cs": "výšková budova",
        **all_x("Vom zwanzigsten Stock im Hochhaus sieht man die ganze Stadt", "С двадцатого этажа высотки видно весь город",
                "З двадцятого поверху багатоповерхівки видно все місто", "From the twentieth floor of the tower block you can see the whole city",
                "Yüksek binanın yirminci katından bütün şehir görünüyor", "Z dwudziestego piętra wieżowca widać całe miasto",
                "Dal ventesimo piano del grattacielo si vede tutta la città", "Desde el piso veinte del rascacielos se ve toda la ciudad",
                "Du vingtième étage de la tour, on voit toute la ville", "Z dvacátého patra výškové budovy je vidět celé město")}),
    15247: ("«Ich zeige mit dem Zeigefinger» — тавтология", {**all_x(
        "Man zeigt nicht mit dem Zeigefinger auf Leute!", "На людей указательным пальцем не показывают!",
        "На людей вказівним пальцем не показують!", "You don't point at people with your index finger!",
        "İnsanlara işaret parmağıyla işaret edilmez!", "Nie pokazuje się ludzi palcem wskazującym!",
        "Non si indicano le persone con l'indice!", "¡No se señala a la gente con el dedo índice!",
        "On ne montre pas les gens avec l'index!", "Na lidi se ukazováčkem neukazuje!")}),
    9905: (LIST, {"t_ru": "рассчитываться, сводить счёты", "t_uk": "розраховуватися, зводити рахунки", "t_en": "to settle up, to get even",
                  "t_tr": "hesaplaşmak, hesabı kapatmak", "t_pl": "rozliczać się", "t_it": "fare i conti, regolare i conti",
                  "t_es": "hacer cuentas, ajustar cuentas", "t_fr": "faire les comptes, régler ses comptes", "t_cs": "vyúčtovat, vyřídit si účty"}),
    8203: ("«Er ist gerade hereingekommen» — пусто", {
        "t_cs": "vejít, jít dál",
        **all_x("Darf ich hereinkommen?", "Можно войти?", "Можна увійти?", "May I come in?", "İçeri girebilir miyim?",
                "Mogę wejść?", "Posso entrare?", "¿Puedo entrar?", "Je peux entrer?", "Můžu jít dál?")}),
    3023: ("uk «Об'єднання» — не то слово; " + LIST, {
        "t_ru": "воссоединение", "t_uk": "возз'єднання", "t_en": "reunification", "t_tr": "yeniden birleşme", "t_pl": "zjednoczenie",
        "t_cs": "znovusjednocení", "x_uk": "Возз'єднання Німеччини відбулося у 1990 році"}),
    9906: ("«Er verschloss alle Wertsachen …» — претерит; " + LIST, {
        "t_ru": "ценные вещи", "t_uk": "цінні речі", "t_en": "valuables", "t_tr": "değerli eşyalar", "t_pl": "kosztowności",
        "t_cs": "cennosti",
        **all_x("Lass deine Wertsachen lieber im Hotel", "Ценные вещи лучше оставь в отеле", "Цінні речі краще залиш у готелі",
                "You'd better leave your valuables at the hotel", "Değerli eşyalarını otelde bıraksan iyi olur",
                "Kosztowności lepiej zostaw w hotelu", "Gli oggetti di valore lasciali in albergo",
                "Mejor deja los objetos de valor en el hotel", "Laisse plutôt tes objets de valeur à l'hôtel",
                "Cennosti si radši nech v hotelu")}),
    3000: ("пример длинный; " + LIST, {
        "t_ru": "умывальня", "t_uk": "умивальня", "t_en": "washroom", "t_tr": "lavabo odası", "t_pl": "umywalnia", "t_it": "il bagno",
        "t_es": "el aseo", "t_fr": "les sanitaires, la salle d'eau", "t_cs": "umývárna",
        **all_x("Der Waschraum auf dem Campingplatz ist sehr sauber", "Умывальня в кемпинге очень чистая", "Умивальня в кемпінгу дуже чиста",
                "The washroom at the campsite is very clean", "Kamp alanındaki lavabo odası çok temiz", "Umywalnia na kempingu jest bardzo czysta",
                "Il bagno del campeggio è molto pulito", "El aseo del camping está muy limpio",
                "Les sanitaires du camping sont très propres", "Umývárna v kempu je velmi čistá")}),
    8206: ("«Die Längen der Bretter …» — так не говорят; " + LIST, {
        "t_ru": "длина", "t_uk": "довжина", "t_en": "length", "t_tr": "uzunluk", "t_pl": "długość", "t_it": "la lunghezza",
        "t_es": "el largo, la longitud", "t_fr": "la longueur", "t_cs": "délka",
        **all_x("Welche Länge soll der Rock haben?", "Какой длины должна быть юбка?", "Якої довжини має бути спідниця?",
                "What length should the skirt be?", "Etek ne uzunlukta olsun?", "Jakiej długości ma być spódnica?",
                "Di che lunghezza deve essere la gonna?", "¿De qué largo tiene que ser la falda?",
                "La jupe doit faire quelle longueur?", "Jakou délku má mít sukně?")}),
    12984: ("«Nach der schweren Mahlzeit hatte ich …» — книжно; " + LIST, {
        "t_ru": "изжога", "t_uk": "печія", "t_en": "heartburn", "t_tr": "mide yanması", "t_pl": "zgaga", "t_es": "la acidez",
        **all_x("Von Kaffee bekomme ich oft Sodbrennen", "От кофе у меня часто изжога", "Від кави в мене часто печія",
                "Coffee often gives me heartburn", "Kahve yüzünden sık sık mide yanması oluyor", "Po kawie często mam zgagę",
                "Il caffè mi dà spesso bruciore di stomaco", "El café me da a menudo acidez",
                "Le café me donne souvent des brûlures d'estomac", "Z kávy mám často pálení žáhy")}),
    2306: ("«Der Blinker funktioniert nicht» — шаблон; пометка (hovor.); en «turn signal» — американское; " + LIST, {
        "t_ru": "поворотник", "t_uk": "поворотник", "t_en": "indicator", "t_tr": "sinyal", "t_pl": "kierunkowskaz", "t_it": "la freccia",
        "t_es": "el intermitente", "t_fr": "le clignotant", "t_cs": "směrovka, blinkr",
        **all_x("Mach den Blinker an, bevor du abbiegst!", "Включи поворотник, прежде чем поворачивать!", "Увімкни поворотник, перш ніж повертати!",
                "Put your indicator on before you turn!", "Dönmeden önce sinyal ver!", "Włącz kierunkowskaz, zanim skręcisz!",
                "Metti la freccia prima di girare!", "¡Pon el intermitente antes de girar!", "Mets ton clignotant avant de tourner!",
                "Než odbočíš, zapni blinkr!")}),
    14251: ("«… kam zur richtigen Zeit» — претерит; пометка (fam.); " + LIST, {
        "t_ru": "телефонный звонок", "t_uk": "телефонний дзвінок", "t_en": "phone call", "t_tr": "telefon görüşmesi", "t_pl": "telefon",
        "t_it": "la telefonata", "t_es": "la llamada telefónica", "t_fr": "l'appel téléphonique, le coup de fil", "t_cs": "telefonát",
        **all_x("Ich warte noch auf einen Telefonanruf vom Arzt", "Я ещё жду телефонного звонка от врача",
                "Я ще чекаю телефонного дзвінка від лікаря", "I'm still waiting for a phone call from the doctor",
                "Hâlâ doktordan bir telefon görüşmesi bekliyorum", "Wciąż czekam na telefon od lekarza",
                "Aspetto ancora una telefonata dal medico", "Todavía espero una llamada telefónica del médico",
                "J'attends encore un appel téléphonique du médecin", "Pořád čekám na telefonát od doktora")}),
}

REPLACE = [
    {"id": 8197, "by": 6289, "lang": "de", "why": "verschwunden — причастие глагола verschwinden"},
    {"id": 1992, "by": 12339, "lang": "de", "why": "Umkleide — краткий вариант слова Umkleideraum"},
]

SPLIT_LATER = {}
