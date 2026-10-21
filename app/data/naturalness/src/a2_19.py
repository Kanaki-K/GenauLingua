"""A2, блок 19: слова 721–760 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Heute ist es windig/sonnig», «Die Orange ist saftig») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    12877: (LIST, {"t_ru": "ядовитый, токсичный", "t_uk": "отруйний, токсичний", "t_en": "poisonous, toxic",
                   "t_tr": "zehirli", "t_pl": "trujący, toksyczny"}),
    1430: ("«иду на блошиный рынок поблизости» — шаблон «gehe zum X»", {**all_x(
        "Das Sofa habe ich auf dem Flohmarkt gekauft", "Этот диван я купил на барахолке", "Цей диван я купив на барахолці",
        "I bought this sofa at the flea market", "Bu kanepeyi bit pazarından aldım", "Tę kanapę kupiłem na pchlim targu",
        "Questo divano l'ho comprato al mercatino delle pulci", "Este sofá lo compré en el mercadillo",
        "J'ai acheté ce canapé au marché aux puces", "Ten gauč jsem koupil na bleším trhu")}),
    1301: ("«bunt und farbenfroh» — масло масляное, снова Kleid; " + LIST, {
        "t_ru": "разноцветный, пёстрый", "t_uk": "різнобарвний, барвистий", "t_en": "colourful", "t_tr": "rengârenk, renkli",
        "t_pl": "kolorowy", "t_it": "colorato", "t_es": "colorido, de colores", "t_fr": "coloré", "t_cs": "barevný, pestrý",
        **all_x("Im Frühling ist der Garten schön bunt", "Весной сад такой разноцветный", "Навесні сад такий барвистий",
                "In spring the garden is so colourful", "İlkbaharda bahçe rengârenk oluyor", "Wiosną ogród jest taki kolorowy",
                "In primavera il giardino è tutto colorato", "En primavera el jardín es muy colorido",
                "Au printemps, le jardin est tout coloré", "Na jaře je zahrada krásně barevná")}),
    18851: ("дни недели — шаблон «… gehe ich immer ins Fitnessstudio»", {**all_x(
        "Mittwochs haben die Kinder früher Schluss", "По средам у детей уроки заканчиваются раньше",
        "По середах у дітей уроки закінчуються раніше", "On Wednesdays the kids finish school early",
        "Çarşambaları çocukların okulu erken bitiyor", "W środy dzieci wcześniej kończą lekcje",
        "Il mercoledì i bambini escono prima da scuola", "Los miércoles los niños salen antes del colegio",
        "Le mercredi, les enfants finissent plus tôt", "Ve středu končí děti ve škole dřív")}),
    18369: ("«требует арендную плату вовремя» — канцелярски; " + LIST, {
        "t_ru": "хозяйка квартиры, арендодательница", "t_uk": "господиня квартири, орендодавиця", "t_en": "landlady",
        "t_tr": "ev sahibesi", "t_pl": "właścicielka mieszkania", "t_it": "la padrona di casa", "t_es": "la casera, la dueña",
        "t_fr": "la propriétaire, la logeuse", "t_cs": "majitelka bytu, bytná",
        **all_x("Unsere Vermieterin wohnt im Erdgeschoss", "Наша хозяйка квартиры живёт на первом этаже",
                "Наша господиня квартири живе на першому поверсі", "Our landlady lives on the ground floor",
                "Ev sahibemiz zemin katta oturuyor", "Nasza właścicielka mieszkania mieszka na parterze",
                "La nostra padrona di casa abita al piano terra", "Nuestra casera vive en la planta baja",
                "Notre propriétaire habite au rez-de-chaussée", "Naše majitelka bytu bydlí v přízemí")}),
    1042: (SKEL + "; шаблон sonnig", {**all_x(
        "Am Meer ist es oft windig", "На море часто бывает ветрено", "На морі часто вітряно", "It's often windy by the sea",
        "Deniz kenarında hava sık sık rüzgârlı", "Nad morzem często jest wietrznie", "Al mare è spesso ventoso",
        "En la costa suele estar ventoso", "Au bord de la mer, c'est souvent venteux", "U moře je často větrno")}),
    15754: (SKEL + "; шаблон windig", {**all_x(
        "Wir haben einen sonnigen Platz auf der Terrasse gefunden", "Мы нашли солнечное место на террасе",
        "Ми знайшли сонячне місце на терасі", "We found a sunny spot on the terrace", "Terasta güneşli bir yer bulduk",
        "Znaleźliśmy słoneczne miejsce na tarasie", "Abbiamo trovato un posto soleggiato in terrazza",
        "Hemos encontrado un sitio soleado en la terraza", "On a trouvé une place ensoleillée sur la terrasse",
        "Našli jsme slunečné místo na terase")}),
    9591: (LIST + "; «готовы помочь» — канцелярски", {
        "t_ru": "одноклассник", "t_uk": "однокласник", "t_en": "classmate", "t_tr": "sınıf arkadaşı",
        "t_pl": "kolega z klasy", "x_ru": "Мои одноклассники очень милые и всегда помогают",
        "x_uk": "Мої однокласники дуже милі й завжди допомагають"}),
    12334: ("снова Museum; " + LIST, {
        "t_ru": "экскурсия, прогулка", "t_uk": "екскурсія, прогулянка", "t_en": "tour, walk round", "t_tr": "tur, gezi",
        "t_pl": "zwiedzanie, spacer", "t_it": "la visita, il giro", "t_es": "el recorrido, la visita",
        "t_fr": "la visite, le tour", "t_cs": "prohlídka, okruh",
        **all_x("Nach dem Essen machen wir einen kleinen Rundgang durch die Altstadt",
                "После обеда устроим небольшую прогулку по старому городу",
                "Після обіду влаштуємо невелику прогулянку старим містом",
                "After lunch we'll take a little walk round the old town",
                "Yemekten sonra eski şehirde küçük bir tur atacağız", "Po obiedzie zrobimy mały spacer po starym mieście",
                "Dopo pranzo facciamo un giretto per il centro storico",
                "Después de comer haremos un pequeño recorrido por el casco antiguo",
                "Après le repas, on fera un petit tour dans la vieille ville", "Po jídle uděláme malý okruh starým městem")}),
    17864: ("«стадо на ферме» — не A2; в жизни Rind — это говядина в меню", {
        "t_ru": "говядина, корова", "t_uk": "яловичина, корова", "t_en": "beef, cattle", "t_tr": "dana eti, sığır",
        "t_pl": "wołowina, bydło", "t_it": "il manzo, il bovino", "t_es": "la ternera, la vaca",
        "t_fr": "le bœuf, la vache", "t_cs": "hovězí, skot",
        **all_x("Ist das Rind oder Schwein?", "Это говядина или свинина?", "Це яловичина чи свинина?",
                "Is that beef or pork?", "Bu dana eti mi, domuz mu?", "To wołowina czy wieprzowina?",
                "È manzo o maiale?", "¿Es ternera o cerdo?", "C'est du bœuf ou du porc?", "Je to hovězí, nebo vepřové?")}),
    2790: ("«Rauchen ist schädlich» — надпись на пачке", {
        "t_ru": "вредный", "t_uk": "шкідливий", "t_en": "harmful, bad for you", "t_tr": "zararlı", "t_pl": "szkodliwy",
        "t_it": "dannoso", "t_es": "perjudicial, dañino", "t_fr": "nocif, mauvais pour la santé", "t_cs": "škodlivý",
        **all_x("Zu viel Zucker ist schädlich für die Zähne", "Слишком много сахара вредно для зубов",
                "Забагато цукру шкідливо для зубів", "Too much sugar is bad for your teeth", "Fazla şeker dişlere zararlı",
                "Za dużo cukru jest szkodliwe dla zębów", "Troppo zucchero è dannoso per i denti",
                "Demasiado azúcar es perjudicial para los dientes", "Trop de sucre, c'est mauvais pour les dents",
                "Příliš mnoho cukru je škodlivé pro zuby")}),
    1995: ("«Du musst hier umsteigen» — где «здесь»? пусто; " + LIST, {
        "t_ru": "пересаживаться, переходить на другое", "t_uk": "пересідати, переходити на інше",
        "t_en": "to change (trains), to switch", "t_tr": "aktarma yapmak", "t_pl": "przesiadać się",
        "t_it": "cambiare, passare a", "t_es": "hacer transbordo, pasarse a", "t_fr": "changer, passer à",
        "t_cs": "přestoupit, přejít",
        **all_x("In Köln musst du umsteigen", "В Кёльне тебе надо сделать пересадку", "У Кельні тобі треба пересісти",
                "You have to change in Cologne", "Köln'de aktarma yapman lazım", "W Kolonii musisz się przesiąść",
                "A Colonia devi cambiare", "En Colonia tienes que hacer transbordo", "À Cologne, tu dois changer",
                "V Kolíně musíš přestoupit")}),
    2632: ("«Ich schaue einen Krimi» — скелет; " + LIST, {
        "t_ru": "детектив", "t_uk": "детектив", "t_en": "crime story, crime drama", "t_tr": "polisiye", "t_pl": "kryminał",
        **all_x("Sonntagabends schauen wir immer Krimi", "В воскресенье вечером мы всегда смотрим детектив",
                "У неділю ввечері ми завжди дивимося детектив", "On Sunday evenings we always watch a crime drama",
                "Pazar akşamları hep polisiye izleriz", "W niedzielę wieczorem zawsze oglądamy kryminał",
                "La domenica sera guardiamo sempre un giallo", "Los domingos por la noche siempre vemos una película policíaca",
                "Le dimanche soir, on regarde toujours un polar", "V neděli večer se vždycky díváme na detektivku")}),
    1235: (LIST, {"t_ru": "обосновать, объяснить", "t_uk": "обґрунтувати, пояснити", "t_en": "to justify, to give reasons",
                  "t_tr": "gerekçelendirmek", "t_pl": "uzasadnić", "t_it": "giustificare, motivare", "t_es": "justificar",
                  "t_fr": "justifier, motiver", "t_cs": "zdůvodnit", "x_ru": "Вы можете это обосновать?"}),
    1408: (LIST, {"t_ru": "расписание", "t_uk": "розклад руху"}),
    662: (EN, {"x_en": "I'm cooking noodles for lunch"}),
    8503: ("«Котёнок такой милый со своими большими глазами» — длинно", {**all_x(
        "Guck mal, wie niedlich der Hund ist!", "Смотри, какая милая собачка!", "Подивись, який милий песик!",
        "Look how cute that dog is!", "Bak, köpek ne kadar sevimli!", "Zobacz, jaki słodki piesek!",
        "Guarda com'è carino il cane!", "¡Mira qué mono es el perro!", "Regarde comme le chien est mignon!",
        "Podívej, jak je ten pes roztomilý!")}),
    18933: ("«По утрам» — это morgens; vormittags — «до обеда»; " + LIST, {
        "t_ru": "до обеда, утром", "t_uk": "до обіду, вранці", "t_en": "in the morning", "t_tr": "öğleden önce",
        "t_pl": "przed południem", "x_ru": "До обеда мы работаем в офисе", "x_uk": "До обіду ми працюємо в офісі"}),
    17730: ("«очень практичный в дороге» — шаблон praktisch, реклама", {**all_x(
        "Die Kinder spielen zu viel auf dem Tablet", "Дети слишком много играют в планшете",
        "Діти забагато граються в планшеті", "The kids play on the tablet too much", "Çocuklar tablette çok fazla oyun oynuyor",
        "Dzieci za dużo grają na tablecie", "I bambini giocano troppo con il tablet", "Los niños juegan demasiado con la tableta",
        "Les enfants jouent trop sur la tablette", "Děti moc hrají na tabletu")}),
    2064: ("«Ich spiele gerne …» — шаблон Basketball; " + LIST, {
        "t_ru": "волейбол", "t_uk": "волейбол", "t_en": "volleyball", "t_tr": "voleybol", "t_pl": "siatkówka",
        **all_x("Am Strand spielen wir oft Volleyball", "На пляже мы часто играем в волейбол", "На пляжі ми часто граємо у волейбол",
                "We often play volleyball on the beach", "Plajda sık sık voleybol oynarız", "Na plaży często gramy w siatkówkę",
                "In spiaggia giochiamo spesso a pallavolo", "En la playa jugamos a menudo al voleibol",
                "À la plage, on joue souvent au volley", "Na pláži často hrajeme volejbal")}),
    13149: ("«kümmerte sich liebevoll» — претерит, книжно", {**all_x(
        "Mein Bruder arbeitet als Krankenpfleger", "Мой брат работает медбратом", "Мій брат працює медбратом",
        "My brother works as a nurse", "Ağabeyim hemşire olarak çalışıyor", "Mój brat pracuje jako pielęgniarz",
        "Mio fratello fa l'infermiere", "Mi hermano trabaja de enfermero", "Mon frère est infirmier",
        "Můj bratr pracuje jako ošetřovatel")}),
    17747: (EN, {"x_en": "My old camera still works perfectly"}),
    552: ("пример «mein lieber Freund» — так не говорят; живёт слово в обращении «Liebe …»", {**all_x(
        "Liebe Oma, vielen Dank für das Geschenk!", "Дорогая бабушка, большое спасибо за подарок!",
        "Дорога бабусю, щиро дякую за подарунок!", "Dear Gran, thank you so much for the present!",
        "Sevgili babaanne, hediye için çok teşekkürler!", "Kochana babciu, bardzo dziękuję za prezent!",
        "Cara nonna, grazie mille per il regalo!", "Querida abuela, ¡muchas gracias por el regalo!",
        "Chère mamie, merci beaucoup pour le cadeau!", "Milá babičko, moc děkuju za dárek!")}),
    678: (SKEL, {**all_x(
        "Möchtest du eine Orange?", "Хочешь апельсин?", "Хочеш апельсин?", "Would you like an orange?",
        "Portakal ister misin?", "Chcesz pomarańczę?", "Vuoi un'arancia?", "¿Quieres una naranja?",
        "Tu veux une orange?", "Chceš pomeranč?")}),
    757: ("«Er ist Rentner» — пусто", {**all_x(
        "Seit letztem Jahr ist mein Vater Rentner", "С прошлого года мой отец на пенсии", "З минулого року мій батько на пенсії",
        "My father has been retired since last year", "Babam geçen yıldan beri emekli",
        "Od zeszłego roku mój tata jest na emeryturze", "Dall'anno scorso mio padre è in pensione",
        "Mi padre está jubilado desde el año pasado", "Mon père est à la retraite depuis l'année dernière",
        "Táta je od loňska v důchodu")}),
    854: (LIST, {"t_ru": "иначе, а то, ещё (что-нибудь)", "t_uk": "інакше, бо інакше, ще (щось)",
                 "t_en": "otherwise, or else, anything else", "t_tr": "yoksa, başka", "t_pl": "inaczej, bo inaczej, poza tym",
                 "t_it": "altrimenti, per il resto", "t_es": "si no, por lo demás", "t_fr": "sinon, à part ça",
                 "t_cs": "jinak, kromě toho"}),
    876: ("«Ich brauche einen Stadtplan» — пусто", {**all_x(
        "Kannst du mir den Weg auf dem Stadtplan zeigen?", "Можешь показать мне дорогу на карте города?",
        "Можеш показати мені дорогу на карті міста?", "Can you show me the way on the street map?",
        "Bana yolu şehir haritasında gösterebilir misin?", "Możesz mi pokazać drogę na planie miasta?",
        "Mi puoi mostrare la strada sulla cartina della città?", "¿Me puedes enseñar el camino en el plano de la ciudad?",
        "Tu peux me montrer le chemin sur le plan de la ville?", "Můžeš mi ukázat cestu na mapě města?")}),
    898: ("«Wie ist dein Stundenplan?» — так не спрашивают", {**all_x(
        "Laut Stundenplan haben wir jetzt Englisch", "По расписанию у нас сейчас английский",
        "За розкладом у нас зараз англійська", "According to the timetable we've got English now",
        "Ders programına göre şimdi İngilizce var", "Według planu lekcji mamy teraz angielski",
        "Secondo l'orario adesso abbiamo inglese", "Según el horario, ahora tenemos inglés",
        "D'après l'emploi du temps, on a anglais maintenant", "Podle rozvrhu máme teď angličtinu")}),
    917: ("ru «приходит завтра» — о будущем «придёт»", {"x_ru": "Техник придёт завтра"}),
    1079: ("«Ich bin zu Hause» — пусто", {**all_x(
        "Bleib heute lieber zu Hause", "Лучше останься сегодня дома", "Краще залишся сьогодні вдома",
        "You'd better stay at home today", "Bugün evde kalsan iyi olur", "Lepiej zostań dziś w domu",
        "Oggi è meglio che resti a casa", "Mejor quédate hoy en casa", "Reste plutôt à la maison aujourd'hui",
        "Zůstaň dnes radši doma")}),
    1103: ("перевод — пояснение, а не слово; ru пример длинный", {
        "t_ru": "выпускные экзамены, аттестат зрелости", "t_uk": "випускні іспити, атестат зрілості",
        "x_ru": "В следующем году у меня выпускные экзамены", "x_uk": "Наступного року в мене випускні іспити",
        "x_en": "Next year I'm taking my school-leaving exams"}),
    1207: ("«Babysitterin» прячет слово", {**all_x(
        "Für Samstagabend brauchen wir einen Babysitter", "На субботний вечер нам нужна няня",
        "На суботній вечір нам потрібна няня", "We need a babysitter for Saturday night",
        "Cumartesi akşamı için bir bebek bakıcısına ihtiyacımız var",
        "Na sobotni wieczór potrzebujemy opiekunki do dzieci", "Sabato sera ci serve una babysitter",
        "Para el sábado por la noche necesitamos una canguro", "Il nous faut une baby-sitter pour samedi soir",
        "Na sobotní večer potřebujeme chůvu")}),
    1247: ("«In diesem Bereich arbeite ich» — в каком? пусто; " + LIST, {
        "t_ru": "сфера, область", "t_uk": "сфера, галузь", "t_en": "area, field", "t_tr": "alan, sektör",
        "t_pl": "dziedzina, branża", "t_it": "il settore, l'area", "t_es": "el sector, el área",
        "t_fr": "le domaine, le secteur", "t_cs": "oblast, obor",
        **all_x("Ich arbeite im Bereich Marketing", "Я работаю в сфере маркетинга", "Я працюю у сфері маркетингу",
                "I work in the field of marketing", "Pazarlama alanında çalışıyorum", "Pracuję w branży marketingowej",
                "Lavoro nel settore del marketing", "Trabajo en el sector del marketing",
                "Je travaille dans le domaine du marketing", "Pracuji v oblasti marketingu")}),
}

SPLIT_LATER = {}
