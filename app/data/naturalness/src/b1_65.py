"""B1, блок 65: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2384: ("«Ich reiche die Unterlagen ein» — пусто; " + LIST, {
        "t_ru": "подавать (документы)", "t_uk": "подавати (документи)", "t_tr": "teslim etmek, sunmak",
        "t_pl": "składać, wnosić", "t_fr": "déposer, remettre",
        **all_x("Bis Freitag muss ich die Bewerbung einreichen", "До пятницы мне надо подать заявку",
                "До п'ятниці мені треба подати заявку", "I have to hand in my application by Friday",
                "Başvurumu cumaya kadar teslim etmem lazım", "Do piątku muszę złożyć podanie",
                "Devo presentare la domanda entro venerdì", "Tengo que presentar la solicitud antes del viernes",
                "Je dois déposer ma candidature avant vendredi", "Do pátku musím podat přihlášku")}),
    11786: ("«Die Sauce schmeckte köstlich …» — претерит и шаблон köstlich", {**all_x(
        "Kann ich noch etwas Sauce haben?", "Можно мне ещё немного соуса?", "Можна мені ще трохи соусу?",
        "Could I have a bit more sauce?", "Biraz daha sos alabilir miyim?", "Mogę prosić jeszcze trochę sosu?",
        "Posso avere ancora un po' di salsa?", "¿Me pones un poco más de salsa?", "Je peux avoir encore un peu de sauce?",
        "Můžu ještě trochu omáčky?")}),
    14100: ("пример со словом Werbespot, а не Spot; " + LIST, {
        "t_ru": "рекламный ролик, прожектор", "t_uk": "рекламний ролик, прожектор", "t_en": "ad, spotlight",
        "t_tr": "reklam filmi, spot lamba", "t_pl": "reklamówka, reflektor", "t_cs": "reklamní spot, reflektor",
        **all_x("Der Spot läuft jeden Abend vor den Nachrichten", "Этот ролик крутят каждый вечер перед новостями",
                "Цей ролик крутять щовечора перед новинами", "The ad runs every evening before the news",
                "Bu reklam filmi her akşam haberlerden önce yayınlanıyor", "Ta reklamówka leci co wieczór przed wiadomościami",
                "Lo spot va in onda ogni sera prima del telegiornale", "El anuncio sale todas las noches antes de las noticias",
                "Le spot passe tous les soirs avant le journal", "Ten spot běží každý večer před zprávami")}),
    2412: ("«Das muss den Regeln entsprechen» — устав, ru «должно» калька; " + LIST, {
        "t_ru": "соответствовать, отвечать (требованиям)", "t_uk": "відповідати", "t_en": "to correspond to, to match",
        "t_tr": "uymak, karşılık gelmek", "t_pl": "odpowiadać, być zgodnym z", "t_it": "corrispondere, rispettare",
        "t_es": "corresponder, ajustarse a", "t_fr": "correspondre, répondre à",
        **all_x("Das Hotel entspricht genau den Fotos", "Отель точно соответствует фотографиям",
                "Готель точно відповідає фотографіям", "The hotel matches the photos exactly",
                "Otel fotoğraflara tam olarak uyuyor", "Hotel dokładnie odpowiada zdjęciom",
                "L'hotel corrisponde esattamente alle foto", "El hotel corresponde exactamente a las fotos",
                "L'hôtel correspond exactement aux photos", "Hotel přesně odpovídá fotkám")}),
    17592: ("«сетевой дневник», «weblog» — словарное, так не говорят", {
        "t_ru": "блог", "t_uk": "блог", "t_en": "blog", "t_tr": "blog", "t_pl": "blog"}),
    1970: ("«Das Treppenhaus ist sauber» — пусто", {
        "t_tr": "merdiven boşluğu", "t_it": "il vano scale", "t_es": "la escalera",
        **all_x("Im Treppenhaus ist schon wieder das Licht kaputt", "В подъезде опять не работает свет",
                "У під'їзді знову не працює світло", "The light in the stairwell is broken again",
                "Merdiven boşluğunda ışık yine bozuk", "Na klatce schodowej znowu nie działa światło",
                "Nel vano scale la luce è di nuovo rotta", "En la escalera vuelve a estar rota la luz",
                "La lumière de la cage d'escalier est encore en panne", "Na schodišti zase nesvítí světlo")}),
    12228: ("«Die Kinder spielen auf dem Spielplatz» — тавтология", {
        "t_ru": "детская площадка", "t_uk": "дитячий майданчик", "t_en": "playground", "t_tr": "çocuk parkı, oyun alanı",
        "t_pl": "plac zabaw", "t_es": "el parque infantil",
        **all_x("Nachmittags gehe ich mit den Kindern auf den Spielplatz", "Днём я хожу с детьми на детскую площадку",
                "Після обіду я ходжу з дітьми на дитячий майданчик", "In the afternoons I take the kids to the playground",
                "Öğleden sonraları çocuklarla çocuk parkına gidiyorum", "Po południu chodzę z dziećmi na plac zabaw",
                "Il pomeriggio porto i bambini al parco giochi", "Por la tarde llevo a los niños al parque infantil",
                "L'après-midi, j'emmène les enfants à l'aire de jeux", "Odpoledne chodím s dětmi na hřiště")}),
    12727: (LIST + "; en «caregiver» — американское", {
        "t_ru": "медбрат, сиделка", "t_uk": "медбрат, доглядальник", "t_en": "carer, male nurse",
        "t_tr": "hasta bakıcı, erkek hemşire", "t_pl": "pielęgniarz, opiekun", "t_it": "l'infermiere, il badante",
        "x_en": "The carer helps the old man wash"}),
    1833: ("«Du bist sehr schlank» — пусто", {
        "t_ru": "стройный, худой", **all_x(
            "Seit ich Sport mache, bin ich viel schlanker geworden", "С тех пор как занимаюсь спортом, я стал гораздо стройнее",
            "Відколи займаюся спортом, я став набагато стрункішим", "Since I started exercising I've got much slimmer",
            "Spora başladığımdan beri çok inceldim", "Odkąd ćwiczę, jestem dużo szczuplejszy",
            "Da quando faccio sport sono molto più snello", "Desde que hago deporte estoy mucho más delgado",
            "Depuis que je fais du sport, je suis beaucoup plus mince", "Od té doby, co sportuju, jsem mnohem štíhlejší")}),
    15118: ("«Viele Ehen scheitern …» — статистика из новостей", {
        "t_ru": "брак", "t_uk": "шлюб", "t_en": "marriage", "t_tr": "evlilik", "t_pl": "małżeństwo",
        **all_x("Nach zwanzig Jahren Ehe sind sie immer noch verliebt", "После двадцати лет брака они всё ещё влюблены",
                "Після двадцяти років шлюбу вони досі закохані", "After twenty years of marriage they're still in love",
                "Yirmi yıllık evliliğin ardından hâlâ birbirlerine aşıklar", "Po dwudziestu latach małżeństwa wciąż są zakochani",
                "Dopo vent'anni di matrimonio sono ancora innamorati", "Después de veinte años de matrimonio siguen enamorados",
                "Après vingt ans de mariage, ils sont toujours amoureux", "Po dvaceti letech manželství jsou pořád zamilovaní")}),
    15586: ("«Der Pinguin ist niedlich» — пусто", {**all_x(
        "Im Zoo schauen wir den Pinguinen beim Füttern zu", "В зоопарке мы смотрим, как кормят пингвинов",
        "У зоопарку ми дивимося, як годують пінгвінів", "At the zoo we watch the penguins being fed",
        "Hayvanat bahçesinde penguenlerin beslenmesini izliyoruz", "W zoo oglądamy karmienie pingwinów",
        "Allo zoo guardiamo i pinguini mentre mangiano", "En el zoo vemos cómo dan de comer a los pingüinos",
        "Au zoo, on regarde le repas des pingouins", "V zoo se díváme na krmení tučňáků")}),
    11789: ("«Die Austern waren sehr teuer, aber lecker» — претерит", {**all_x(
        "Hast du schon mal Austern probiert?", "Ты когда-нибудь пробовал устрицы?", "Ти колись пробував устриці?",
        "Have you ever tried oysters?", "Hiç istiridye denedin mi?", "Jadłeś kiedyś ostrygi?",
        "Hai mai assaggiato le ostriche?", "¿Alguna vez has probado las ostras?", "Tu as déjà goûté des huîtres?",
        "Už jsi někdy ochutnal ústřice?")}),
    15587: ("«Das Kalb folgt seiner Mutter über die Wiese» — книжно; второе значение — телятина", {
        "t_es": "el ternero, la ternera", "t_cs": "tele, telecí maso",
        **all_x("Ein echtes Wiener Schnitzel ist vom Kalb", "Настоящий венский шницель — из телятины",
                "Справжній віденський шніцель — з телятини", "A real Wiener schnitzel is made from veal",
                "Gerçek Viyana şnitzeli dana etinden yapılır", "Prawdziwy sznycel wiedeński robi się z cielęciny",
                "La vera cotoletta viennese è di vitello", "El auténtico escalope vienés es de ternera",
                "La vraie escalope viennoise est en veau", "Pravý vídeňský řízek je z telecího")}),
    2935: (LIST + "; " + EN, {
        "t_ru": "договариваться (о встрече)", "t_uk": "домовлятися (про зустріч)", "t_en": "to arrange to meet",
        "t_tr": "sözleşmek, buluşmak", "t_pl": "umawiać się", "t_it": "darsi appuntamento", "t_es": "quedar, citarse",
        "t_fr": "se donner rendez-vous", "x_en": "We're arranging to meet next week"}),
    14106: ("пометка (coloq.); en «7 in the evening» — так не говорят", {
        "t_ru": "встреча, место встречи", "t_en": "meet-up, meeting place", "t_es": "el encuentro, la quedada",
        **all_x("Treff ist um sieben am Brunnen", "Встреча в семь у фонтана", "Зустріч о сьомій біля фонтана",
                "Meet-up's at seven by the fountain", "Buluşma saat yedide çeşmenin yanında", "Spotkanie o siódmej przy fontannie",
                "Il ritrovo è alle sette alla fontana", "La quedada es a las siete en la fuente",
                "Rendez-vous à sept heures à la fontaine", "Sraz je v sedm u kašny")}),
    2473: ("«Regelmäßiger Sport fördert die Gesundheit» — лозунг; " + LIST, {
        "t_ru": "способствовать, поддерживать", "t_uk": "сприяти, підтримувати", "t_en": "to promote, to support",
        "t_pl": "wspierać, sprzyjać", "t_it": "favorire, sostenere", "t_es": "favorecer, apoyar", "t_fr": "favoriser, soutenir",
        "t_cs": "podporovat",
        **all_x("Seine Eltern fördern ihn, wo sie können", "Родители поддерживают его, как только могут",
                "Батьки підтримують його, як тільки можуть", "His parents support him however they can",
                "Ailesi onu elinden geldiğince destekliyor", "Rodzice wspierają go, jak tylko mogą",
                "I suoi genitori lo sostengono come possono", "Sus padres lo apoyan en todo lo que pueden",
                "Ses parents le soutiennent comme ils peuvent", "Rodiče ho podporují, jak můžou")}),
    17209: ("«Die Reservierung ist bestätigt» — письмо из системы", {
        "t_ru": "бронирование, бронь", "t_uk": "бронювання", "t_tr": "rezervasyon", "t_pl": "rezerwacja",
        **all_x("Ich habe eine Reservierung auf den Namen Müller", "У меня бронь на фамилию Мюллер",
                "У мене бронювання на прізвище Мюллер", "I have a reservation under the name Müller",
                "Müller adına rezervasyonum var", "Mam rezerwację na nazwisko Müller", "Ho una prenotazione a nome Müller",
                "Tengo una reserva a nombre de Müller", "J'ai une réservation au nom de Müller",
                "Mám rezervaci na jméno Müller")}),
    16365: ("«Die Forderung war ganz ungerecht» — шаблон ungerecht; " + LIST, {
        "t_ru": "требование, претензия", "t_uk": "вимога, претензія", "t_en": "demand, claim", "t_tr": "talep, alacak",
        "t_pl": "żądanie, roszczenie", "t_it": "la richiesta, la pretesa", "t_es": "la exigencia, la demanda",
        **all_x("Er stellt immer nur Forderungen", "Он только и делает, что выдвигает требования",
                "Він тільки й робить, що висуває вимоги", "All he ever does is make demands",
                "Sürekli talepte bulunuyor", "Ciągle tylko stawia żądania", "Non fa che avanzare pretese",
                "No hace más que poner exigencias", "Il ne fait que poser des exigences", "Pořád jen klade požadavky")}),
    2819: ("«Das ist ein sinnvoller Plan» — пусто; " + LIST, {
        "t_ru": "разумный, имеющий смысл", "t_uk": "розумний, що має сенс", "t_en": "sensible, meaningful",
        "t_tr": "mantıklı, anlamlı", "t_pl": "sensowny, rozsądny", "t_it": "sensato, utile", "t_es": "sensato, razonable",
        "t_fr": "judicieux, sensé", "t_cs": "smysluplný, rozumný",
        **all_x("Es ist sinnvoll, vorher zu reservieren", "Имеет смысл забронировать заранее", "Має сенс забронювати заздалегідь",
                "It's sensible to book in advance", "Önceden rezervasyon yapmak mantıklı", "Rozsądnie jest zarezerwować wcześniej",
                "È sensato prenotare prima", "Es sensato reservar con antelación", "Il est judicieux de réserver à l'avance",
                "Je rozumné rezervovat si předem")}),
    1241: (LIST + " (было пять значений)", {
        "t_ru": "записываться (на курс), подтверждать", "t_uk": "записуватися (на курс), підтверджувати",
        "t_en": "to take (a course), to prove", "t_tr": "kursa kaydolmak, kanıtlamak",
        "t_pl": "zapisać się (na kurs), udokumentować", "t_it": "iscriversi, documentare", "t_es": "inscribirse, acreditar",
        "t_fr": "suivre, justifier", "t_cs": "zapsat si, doložit"}),
    1866: ("«Ich trage Shorts» — шаблон одежды; пометка (hovor.)", {
        "t_cs": "šortky, kraťasy",
        **all_x("Bei dieser Hitze gehe ich nur in Shorts raus", "В такую жару я выхожу только в шортах",
                "У таку спеку я виходжу тільки в шортах", "In this heat I only go out in shorts",
                "Bu sıcakta sadece şortla dışarı çıkıyorum", "W taki upał wychodzę tylko w szortach",
                "Con questo caldo esco solo in pantaloncini", "Con este calor solo salgo en pantalones cortos",
                "Avec cette chaleur, je sors seulement en short", "V tomhle vedru chodím ven jen v šortkách")}),
    11792: ("«Die Kinder essen gerne Eiscreme im Sommer» — шаблон «gerne … im Sommer»", {**all_x(
        "Zum Nachtisch gibt es Eiscreme mit Erdbeeren", "На десерт мороженое с клубникой", "На десерт морозиво з полуницею",
        "There's ice cream with strawberries for dessert", "Tatlı olarak çilekli dondurma var", "Na deser są lody z truskawkami",
        "Per dolce c'è gelato con le fragole", "De postre hay helado con fresas", "En dessert, il y a de la glace aux fraises",
        "Ke dezertu je zmrzlina s jahodami")}),
    2272: (LIST, {
        "t_ru": "обоснованный, имеющий право", "t_uk": "обґрунтований, що має право", "t_en": "justified, entitled",
        "t_tr": "haklı, hak sahibi", "t_pl": "uzasadniony, uprawniony", "t_it": "giustificato, autorizzato",
        "t_es": "justificado, autorizado", "t_fr": "justifié, habilité"}),
    2524: ("«Getreide wächst auf dem Feld» — учебник", {
        "t_ru": "зерно, зерновые", "t_uk": "зерно, зернові", "t_en": "grain, cereals",
        **all_x("Müsli besteht vor allem aus Getreide", "Мюсли в основном состоят из зерновых",
                "Мюслі здебільшого складаються із зернових", "Muesli is mostly made of cereals",
                "Müsli çoğunlukla tahıldan oluşur", "Musli to głównie zboże", "Il muesli è fatto soprattutto di cereali",
                "El muesli es sobre todo cereales", "Le muesli, c'est surtout des céréales", "Müsli je hlavně z obilí")}),
    8981: (EN + " («real estate agent» — американское); " + LIST, {
        "t_ru": "риэлтор, маклер", "t_uk": "ріелтор, маклер", "t_en": "estate agent, broker", "t_tr": "emlakçı, komisyoncu",
        "t_pl": "pośrednik nieruchomości, makler",
        "x_en": "The estate agent helped us find a lovely house",
        "x_tr": "Emlakçı güzel bir ev bulmamıza yardım etti"}),
    1715: ("«Ich schaue die Telefonnummer … nach» — громоздко; " + LIST, {
        "t_ru": "посмотреть, проверить", "t_uk": "подивитися, перевірити", "t_en": "to have a look, to look up",
        "t_tr": "bakmak, kontrol etmek", "t_pl": "sprawdzić, zajrzeć", "t_it": "controllare, cercare",
        "t_es": "mirar, consultar", "t_fr": "vérifier, regarder", "t_cs": "podívat se, vyhledat",
        **all_x("Moment, ich schau mal nach", "Секунду, сейчас посмотрю", "Секунду, зараз подивлюся",
                "Hang on, I'll have a look", "Bir saniye, bir bakayım", "Chwila, zaraz sprawdzę", "Un attimo, controllo",
                "Un momento, ahora lo miro", "Attends, je vais vérifier", "Moment, podívám se")}),
    7501: ("«Der Salat ist gemischt» — пусто; " + LIST, {
        "t_ru": "смешанный, разный", "t_uk": "змішаний, різний", "t_en": "mixed, assorted", "t_tr": "karışık, çeşitli",
        "t_pl": "mieszany, różny", "t_fr": "mixte, mélangé",
        **all_x("Einen gemischten Salat, bitte", "Смешанный салат, пожалуйста", "Змішаний салат, будь ласка",
                "A mixed salad, please", "Karışık salata lütfen", "Poproszę mieszaną sałatkę",
                "Un'insalata mista, per favore", "Una ensalada mixta, por favor", "Une salade mixte, s'il vous plaît",
                "Míchaný salát, prosím")}),
    2947: ("«Ich verlängere den Vertrag» — пусто; " + LIST, {
        "t_ru": "продлевать, удлинять", "t_uk": "продовжувати, подовжувати", "t_en": "to extend, to renew",
        "t_tr": "uzatmak, yenilemek", "t_pl": "przedłużyć, wydłużyć", "t_it": "prolungare, rinnovare",
        "t_es": "renovar, alargar", "t_fr": "prolonger, rallonger",
        **all_x("Kann ich das Buch noch eine Woche verlängern?", "Можно продлить книгу ещё на неделю?",
                "Можна продовжити книжку ще на тиждень?", "Can I renew the book for another week?",
                "Kitabın süresini bir hafta daha uzatabilir miyim?", "Mogę przedłużyć książkę o tydzień?",
                "Posso rinnovare il prestito del libro per un'altra settimana?", "¿Puedo renovar el libro una semana más?",
                "Je peux prolonger l'emprunt du livre d'une semaine?", "Můžu si knížku prodloužit o týden?")}),
    14109: ("en «criticize» — американское написание", {
        "t_ru": "критиковать", "t_uk": "критикувати", "t_en": "to criticise", "t_pl": "krytykować",
        "x_en": "You always criticise my work"}),
    1244: ("«Ich brauche eine Beratung» — пусто; " + LIST, {
        "t_ru": "консультация, совет", "t_uk": "консультація, порада", "t_en": "advice, consultation",
        "t_tr": "danışmanlık, tavsiye", "t_pl": "porada, doradztwo", "t_it": "la consulenza, il consiglio",
        "t_es": "el asesoramiento, la consulta", "t_fr": "le conseil, la consultation", "t_cs": "poradenství, konzultace",
        **all_x("Die Beratung bei der Bank ist kostenlos", "Консультация в банке бесплатная", "Консультація в банку безкоштовна",
                "The consultation at the bank is free", "Bankadaki danışmanlık ücretsiz", "Porada w banku jest bezpłatna",
                "La consulenza in banca è gratuita", "El asesoramiento en el banco es gratuito", "Le conseil à la banque est gratuit",
                "Poradenství v bance je zdarma")}),
    3033: ("«Die Zahlung kommt morgen» — пусто, en «The payment is tomorrow» — неверно", {
        "t_ru": "платёж, оплата", "t_uk": "платіж, оплата", "t_en": "payment", "t_tr": "ödeme", "t_pl": "płatność, wpłata",
        **all_x("Die Zahlung ist noch nicht auf meinem Konto angekommen", "Платёж ещё не пришёл на мой счёт",
                "Платіж ще не надійшов на мій рахунок", "The payment hasn't reached my account yet",
                "Ödeme henüz hesabıma geçmedi", "Płatność jeszcze nie wpłynęła na moje konto",
                "Il pagamento non è ancora arrivato sul mio conto", "El pago todavía no ha llegado a mi cuenta",
                "Le paiement n'est pas encore arrivé sur mon compte", "Platba mi ještě nepřišla na účet")}),
    15589: ("«Die Blumen blühen im Frühling» — учебник", {
        "t_en": "to bloom, to flourish",
        **all_x("Bei uns blühen schon die Kirschbäume", "У нас уже цветут вишни", "У нас уже цвітуть вишні",
                "The cherry trees are already in bloom here", "Bizde kiraz ağaçları çiçek açtı bile", "U nas już kwitną wiśnie",
                "Da noi i ciliegi sono già fioriti", "Aquí ya florecen los cerezos", "Chez nous, les cerisiers fleurissent déjà",
                "U nás už kvetou třešně")}),
    480: ("«Das Kinderzimmer ist hell» — пусто", {
        "t_ru": "детская, детская комната",
        **all_x("Aus dem Arbeitszimmer machen wir ein Kinderzimmer", "Из кабинета мы сделаем детскую",
                "Із кабінету ми зробимо дитячу кімнату", "We're turning the study into a nursery",
                "Çalışma odasını çocuk odasına çeviriyoruz", "Z gabinetu robimy pokój dziecięcy",
                "Trasformiamo lo studio in una cameretta", "Vamos a convertir el despacho en habitación infantil",
                "On transforme le bureau en chambre d'enfant", "Z pracovny uděláme dětský pokoj")}),
    1614: ("«Ich höre Musik mit Kopfhörern» — пусто; es «audífonos» — Латинская Америка", {
        "t_es": "los auriculares, los cascos",
        **all_x("Nimm mal die Kopfhörer raus, ich rede mit dir!", "Вынь наушники, я с тобой разговариваю!",
                "Вийми навушники, я з тобою розмовляю!", "Take your headphones out, I'm talking to you!",
                "Kulaklığını çıkar, seninle konuşuyorum!", "Wyjmij słuchawki, mówię do ciebie!",
                "Togliti le cuffie, ti sto parlando!", "¡Quítate los auriculares, que te estoy hablando!",
                "Enlève ton casque, je te parle!", "Sundej si sluchátka, mluvím s tebou!")}),
    12233: ("«Puzzles lösen» — так не говорят (machen); en «on weekends» — американское", {
        "x_de": "Am Wochenende mache ich gern Puzzles", "x_ru": "По выходным я люблю собирать пазлы",
        "x_uk": "На вихідних я люблю збирати пазли", "x_en": "I like doing jigsaw puzzles at the weekend",
        "x_tr": "Hafta sonları yapboz yapmayı severim", "x_pl": "W weekendy chętnie układam puzzle",
        "x_it": "Il fine settimana mi piace fare i puzzle", "x_es": "Los fines de semana me gusta hacer puzles",
        "x_fr": "Le week-end, j'aime faire des puzzles", "x_cs": "O víkendu rád skládám puzzle"}),
    7505: ("«eine scharfe, spitze Klinge» — тавтология; " + LIST, {
        "t_ru": "острый, остроконечный", "t_uk": "гострий, загострений", "t_en": "pointed, sharp", "t_tr": "sivri, keskin",
        "t_pl": "ostry, spiczasty", "t_it": "appuntito, pungente", "t_es": "puntiagudo, afilado", "t_fr": "pointu, acéré",
        "t_cs": "špičatý, ostrý",
        **all_x("Mein Bleistift ist nicht mehr spitz", "Мой карандаш уже не острый", "Мій олівець уже не гострий",
                "My pencil isn't sharp any more", "Kalemim artık sivri değil", "Mój ołówek nie jest już ostry",
                "La mia matita non è più appuntita", "Mi lápiz ya no está afilado", "Mon crayon n'est plus pointu",
                "Tužka už není ostrá")}),
    2739: ("«Ich esse gern Quark» — шаблон «Ich esse gern …»; ru «кварк» — физика", {
        "t_ru": "творог", "t_en": "quark, curd cheese",
        **all_x("Zum Frühstück esse ich Quark mit Obst", "На завтрак я ем творог с фруктами", "На сніданок я їм сир із фруктами",
                "For breakfast I have quark with fruit", "Kahvaltıda meyveli lor peyniri yiyorum",
                "Na śniadanie jem twaróg z owocami", "A colazione mangio il quark con la frutta",
                "Para desayunar tomo quark con fruta", "Au petit-déjeuner, je mange du fromage blanc avec des fruits",
                "K snídani jím tvaroh s ovocem")}),
    1757: ("«Ein Pfennig ist eine alte Münze» — учебник; в речи живёт в выражениях", {
        "t_ru": "пфенниг, копейка", "t_uk": "пфеніг, копійка",
        **all_x("Er dreht jeden Pfennig zweimal um", "Он каждую копейку считает", "Він кожну копійку рахує",
                "He counts every penny", "Her kuruşun hesabını yapıyor", "Liczy każdy grosz", "Conta ogni centesimo",
                "Mira cada céntimo", "Il compte chaque centime", "Šetří každý halíř")}),
    1236: ("«Die Begrüßung war herzlich» — пусто", {
        "t_es": "la bienvenida, el saludo",
        **all_x("Zur Begrüßung bekommt jeder Gast ein Glas Sekt", "В знак приветствия каждый гость получает бокал игристого",
                "На привітання кожен гість отримує келих ігристого", "Every guest gets a glass of bubbly as a welcome",
                "Karşılama olarak her misafire bir kadeh köpüklü şarap veriliyor",
                "Na powitanie każdy gość dostaje kieliszek wina musującego",
                "All'accoglienza ogni ospite riceve un calice di spumante",
                "De bienvenida, cada invitado recibe una copa de cava",
                "En guise d'accueil, chaque invité reçoit une coupe de mousseux",
                "Na přivítanou dostane každý host skleničku sektu")}),
}

SPLIT_LATER = {}
