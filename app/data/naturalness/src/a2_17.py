"""A2, блок 17: слова 641–680 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Das Haus ist modern», «Physik ist interessant») — пусто"
EN = "английский пример: так не говорят"
SCHOOL = "школьные предметы: «X ist mein Lieblingsfach/interessant/schwer» — один шаблон на все"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1382: ("«Бутылка содержит один литр» — надпись на этикетке; " + LIST, {
        "t_ru": "содержать, включать", "t_uk": "містити, включати", "t_en": "to contain, to include",
        "t_tr": "içermek", "t_pl": "zawierać",
        **all_x("Enthält das Essen Nüsse? Ich bin allergisch", "Это блюдо содержит орехи? У меня аллергия",
                "Ця страва містить горіхи? У мене алергія", "Does the food contain nuts? I'm allergic",
                "Bu yemek fındık içeriyor mu? Alerjim var", "Czy to danie zawiera orzechy? Mam alergię",
                "Il piatto contiene noci? Sono allergico", "¿La comida contiene frutos secos? Soy alérgico",
                "Est-ce que le plat contient des noix? Je suis allergique", "Obsahuje to jídlo ořechy? Jsem alergický")}),
    7275: (LIST, {"t_ru": "особенно, прежде всего", "t_uk": "особливо, зокрема", "t_en": "especially, in particular",
                  "t_tr": "özellikle", "t_pl": "szczególnie, zwłaszcza", "x_en": "I like the city, especially the old centre"}),
    14506: ("пример повторял Gitarre; " + LIST, {
        "t_ru": "инструмент, прибор", "t_uk": "інструмент, прилад", "t_en": "instrument", "t_tr": "enstrüman, alet",
        "t_pl": "instrument, przyrząd",
        **all_x("Spielst du ein Instrument?", "Ты играешь на каком-нибудь инструменте?",
                "Ти граєш на якомусь інструменті?", "Do you play an instrument?", "Bir enstrüman çalıyor musun?",
                "Grasz na jakimś instrumencie?", "Suoni uno strumento?", "¿Tocas algún instrumento?",
                "Tu joues d'un instrument?", "Hraješ na nějaký nástroj?")}),
    8916: ("uk «Будівельний майданчик перекриває рух» — канцелярски; " + LIST, {
        "t_ru": "стройка", "t_uk": "будівництво", "t_en": "construction site, roadworks", "t_tr": "şantiye",
        "t_pl": "budowa", "x_uk": "Будівництво перекриває весь рух"}),
    392: ("«Die Heizung funktioniert gut» — скелет, шаблон System", {
        "t_ru": "отопление, батарея", "t_uk": "опалення, батарея", "t_en": "heating, radiator", "t_tr": "kalorifer",
        "t_pl": "ogrzewanie, kaloryfer",
        **all_x("Die Heizung geht nicht, in der Wohnung ist es eiskalt", "Отопление не работает, в квартире холодно",
                "Опалення не працює, у квартирі холодно", "The heating's not working, it's freezing in the flat",
                "Kalorifer çalışmıyor, evde buz gibi soğuk", "Ogrzewanie nie działa, w mieszkaniu jest lodowato",
                "Il riscaldamento non funziona, in casa si gela", "La calefacción no funciona, en casa hace un frío horrible",
                "Le chauffage ne marche pas, il fait glacial dans l'appartement", "Topení nefunguje, v bytě je hrozná zima")}),
    607: (SKEL + "; " + LIST, {
        "t_ru": "современный", "t_uk": "сучасний", "t_en": "modern", "t_tr": "modern", "t_pl": "nowoczesny",
        **all_x("Die Küche ist ganz modern eingerichtet", "Кухня обставлена совсем по-современному",
                "Кухня облаштована зовсім по-сучасному", "The kitchen is very modern",
                "Mutfak çok modern döşenmiş", "Kuchnia jest bardzo nowocześnie urządzona",
                "La cucina è arredata in modo molto moderno", "La cocina está decorada de forma muy moderna",
                "La cuisine est aménagée de façon très moderne", "Kuchyň je zařízená velmi moderně")}),
    1686: ("«Das Messer ist scharf» — скелет", {**all_x(
        "Das Messer schneidet nicht mehr gut", "Этот нож уже плохо режет", "Цей ніж уже погано ріже",
        "This knife doesn't cut well any more", "Bu bıçak artık iyi kesmiyor", "Ten nóż już słabo kroi",
        "Questo coltello non taglia più bene", "Este cuchillo ya no corta bien", "Ce couteau ne coupe plus bien",
        "Ten nůž už špatně krájí")}),
    1448: ("«Wo ist denn die Gabel?» — шаблон Löffel («Wo ist der Löffel …?»)", {
        "t_uk": "виделка",
        **all_x("Kinder, esst bitte mit Messer und Gabel!", "Дети, ешьте, пожалуйста, ножом и вилкой!",
                "Діти, їжте, будь ласка, ножем і виделкою!", "Kids, please eat with a knife and fork!",
                "Çocuklar, lütfen bıçak ve çatalla yiyin!", "Dzieci, jedzcie, proszę, nożem i widelcem!",
                "Bambini, mangiate con coltello e forchetta, per favore!", "¡Niños, comed con cuchillo y tenedor, por favor!",
                "Les enfants, mangez avec un couteau et une fourchette, s'il vous plaît!",
                "Děti, jezte prosím nožem a vidličkou!")}),
    7288: (LIST, {"t_ru": "настоящий, фактический", "t_uk": "справжній, фактичний", "t_en": "actual, real",
                  "t_tr": "asıl, gerçek", "t_pl": "właściwy, rzeczywisty", "t_it": "vero, effettivo",
                  "t_es": "verdadero, real", "t_fr": "véritable, réel", "t_cs": "skutečný, vlastní"}),
    18750: (LIST, {"t_ru": "новогодняя ночь, 31 декабря", "t_uk": "новорічна ніч", "t_en": "New Year's Eve",
                   "t_tr": "yılbaşı gecesi", "t_pl": "sylwester"}),
    9503: ("«Студентка сидит на лекции» — пусто; en «female student» — так не говорят", {**all_x(
        "Als Studentin hatte ich wenig Geld", "Когда я была студенткой, у меня было мало денег",
        "Коли я була студенткою, у мене було мало грошей", "When I was a student, I didn't have much money",
        "Öğrenciyken az param vardı", "Jako studentka miałam mało pieniędzy", "Da studentessa avevo pochi soldi",
        "Cuando era estudiante, tenía poco dinero", "Quand j'étais étudiante, j'avais peu d'argent",
        "Jako studentka jsem měla málo peněz")}),
    1759: (SCHOOL, {**all_x(
        "Morgen schreiben wir einen Test in Physik", "Завтра у нас контрольная по физике", "Завтра в нас контрольна з фізики",
        "We've got a physics test tomorrow", "Yarın fizik sınavımız var", "Jutro piszemy sprawdzian z fizyki",
        "Domani abbiamo una verifica di fisica", "Mañana tenemos un examen de física",
        "Demain, on a un contrôle de physique", "Zítra píšeme test z fyziky")}),
    1280: (SCHOOL, {**all_x(
        "In Biologie haben wir heute über Bienen gesprochen", "Сегодня на биологии мы говорили о пчёлах",
        "Сьогодні на біології ми говорили про бджіл", "In biology today we talked about bees",
        "Bugün biyoloji dersinde arılardan bahsettik", "Dziś na biologii rozmawialiśmy o pszczołach",
        "Oggi a biologia abbiamo parlato delle api", "Hoy en biología hemos hablado de las abejas",
        "Aujourd'hui, en biologie, on a parlé des abeilles", "Dnes jsme v biologii mluvili o včelách")}),
    1307: (SCHOOL, {**all_x(
        "Die Chemie zwischen uns stimmt einfach", "Между нами просто есть химия", "Між нами просто є хімія",
        "We just have good chemistry", "Aramızda iyi bir kimya var", "Po prostu jest między nami chemia",
        "Tra noi c'è proprio chimica", "Entre nosotros hay química", "Entre nous, il y a une vraie chimie",
        "Mezi námi prostě funguje chemie")}),
    1570: ("«каждый раз в понедельник» — калька; " + LIST, {
        "t_ru": "по, каждый раз", "t_uk": "по, щоразу", "t_en": "each, every time", "t_tr": "her biri, her defasında",
        "t_pl": "po, za każdym razem", "t_it": "ciascuno, ogni volta", "t_es": "cada uno, cada vez",
        "t_fr": "chacun, à chaque fois", "t_cs": "každý, pokaždé",
        **all_x("Die Kinder bekommen jeweils zwei Euro", "Дети получают по два евро", "Діти отримують по два євро",
                "The children get two euros each", "Çocukların her biri iki euro alıyor", "Dzieci dostają po dwa euro",
                "I bambini ricevono due euro ciascuno", "Los niños reciben dos euros cada uno",
                "Les enfants reçoivent deux euros chacun", "Děti dostanou každé dvě eura")}),
    18752: ("пример длиннее, чем говорят", {**all_x(
        "Sonntags schlafe ich immer lange", "По воскресеньям я всегда долго сплю", "По неділях я завжди довго сплю",
        "On Sundays I always have a lie-in", "Pazarları hep geç saate kadar uyurum", "W niedziele zawsze długo śpię",
        "La domenica dormo sempre fino a tardi", "Los domingos siempre duermo hasta tarde",
        "Le dimanche, je fais toujours la grasse matinée", "V neděli vždycky dlouho spím")}),
    1620: ("«Das ist kostenlos» — пусто; " + LIST, {
        "t_ru": "бесплатный", "t_uk": "безкоштовний", "t_en": "free (of charge)", "t_tr": "ücretsiz, bedava",
        "t_pl": "bezpłatny, darmowy",
        **all_x("Für Kinder ist der Eintritt kostenlos", "Для детей вход бесплатный", "Для дітей вхід безкоштовний",
                "Entry is free for children", "Çocuklar için giriş ücretsiz", "Dla dzieci wstęp jest bezpłatny",
                "Per i bambini l'ingresso è gratuito", "Para los niños la entrada es gratis",
                "L'entrée est gratuite pour les enfants", "Pro děti je vstup zdarma")}),
    1076: ("«Die Zitrone ist sauer» — скелет", {**all_x(
        "Tee mit Zitrone, bitte", "Чай с лимоном, пожалуйста", "Чай з лимоном, будь ласка", "Tea with lemon, please",
        "Limonlu çay lütfen", "Herbatę z cytryną poproszę", "Un tè al limone, per favore", "Un té con limón, por favor",
        "Un thé au citron, s'il vous plaît", "Čaj s citronem, prosím")}),
    11761: ("«Я хочу … пожалуйста» — грубо, в кафе так не просят; " + LIST, {
        "t_en": "portion, helping", "t_tr": "porsiyon", "t_pl": "porcja",
        "x_ru": "Большую порцию макарон, пожалуйста", "x_uk": "Велику порцію макаронів, будь ласка",
        "x_en": "I'd like a large portion of pasta, please", "x_tr": "Büyük bir porsiyon makarna lütfen"}),
    18: ("«Die Ampel steht auf Rot» — шаблон grün («Die Ampel ist grün …»)", {**all_x(
        "Fahr an der zweiten Ampel links", "На втором светофоре поверни налево", "На другому світлофорі поверни ліворуч",
        "Turn left at the second set of lights", "İkinci trafik ışığından sola dön", "Na drugich światłach skręć w lewo",
        "Al secondo semaforo gira a sinistra", "En el segundo semáforo gira a la izquierda",
        "Au deuxième feu, tourne à gauche", "Na druhém semaforu odboč doleva")}),
    11772: (EN, {"x_en": "We have lunch in the cafeteria"}),
    262: (EN + " («On holidays we do not work»); " + LIST, {
        "t_ru": "праздник, нерабочий день", "t_uk": "свято, неробочий день", "t_en": "public holiday",
        "t_tr": "resmi tatil, bayram", "t_pl": "święto, dzień wolny",
        **all_x("An Feiertagen arbeiten wir nicht", "В праздники мы не работаем", "У святкові дні ми не працюємо",
                "We don't work on public holidays", "Resmi tatillerde çalışmıyoruz", "W święta nie pracujemy",
                "Nei giorni festivi non lavoriamo", "Los días festivos no trabajamos",
                "Les jours fériés, nous ne travaillons pas", "O svátcích nepracujeme")}),
    2122: ("перевод — список из шести; «хороший аттестат» — аттестат один на всю школу", {
        "t_ru": "табель, аттестат", "t_uk": "табель, атестат", "t_en": "school report, certificate",
        "t_tr": "karne, belge", "t_pl": "świadectwo", "t_it": "la pagella, il certificato",
        "t_es": "el boletín de notas, el certificado", "t_fr": "le bulletin, le certificat", "t_cs": "vysvědčení, posudek",
        **all_x("Morgen gibt es Zeugnisse", "Завтра выдают табели", "Завтра видають табелі",
                "We get our school reports tomorrow", "Yarın karneler veriliyor", "Jutro rozdają świadectwa",
                "Domani danno le pagelle", "Mañana dan los boletines de notas", "Demain, on reçoit les bulletins",
                "Zítra se rozdává vysvědčení")}),
    8946: ("«Служащий работает в большом офисе» — пусто; " + LIST, {
        "t_ru": "сотрудник, служащий", "t_uk": "працівник, службовець", "t_en": "employee", "t_tr": "çalışan",
        "t_pl": "pracownik",
        **all_x("Die Firma hat dreißig Angestellte", "В фирме тридцать сотрудников", "У фірмі тридцять працівників",
                "The company has thirty employees", "Şirketin otuz çalışanı var", "Firma ma trzydziestu pracowników",
                "L'azienda ha trenta dipendenti", "La empresa tiene treinta empleados", "L'entreprise a trente employés",
                "Firma má třicet zaměstnanců")}),
    842: ("uk «Він катається» — смысл «идёт кататься» потерян", {"x_uk": "Він іде кататися на лижах",
                                                                "x_en": "He's going skiing"}),
    # täglich (блок 11, мой) — шаблон joggen («Ich jogge jeden Morgen …»)
    18651: ("мой пример «Ich jogge täglich» — шаблон joggen", {**all_x(
        "Der Bus fährt täglich außer sonntags", "Автобус ходит ежедневно, кроме воскресенья",
        "Автобус ходить щодня, крім неділі", "The bus runs daily except Sundays", "Otobüs pazar hariç her gün çalışıyor",
        "Autobus jeździ codziennie oprócz niedziel", "L'autobus passa ogni giorno tranne la domenica",
        "El autobús pasa a diario excepto los domingos", "Le bus circule tous les jours sauf le dimanche",
        "Autobus jezdí denně kromě neděle")}),
    12216: ("«бегаю трусцой каждое утро полчаса» — порядок слов; " + LIST, {
        "t_ru": "бегать (трусцой)", "t_uk": "бігати (підтюпцем)", "t_en": "to jog", "t_tr": "koşu yapmak",
        "t_pl": "biegać", "x_ru": "Каждое утро я полчаса бегаю", "x_uk": "Щоранку я пів години бігаю",
        "x_en": "I go jogging for half an hour every morning"}),
    1925: ("«Er ist sehr sympathisch» — пусто", {**all_x(
        "Dein neuer Kollege ist echt sympathisch", "Твой новый коллега очень приятный", "Твій новий колега дуже симпатичний",
        "Your new colleague is really nice", "Yeni iş arkadaşın çok sempatik", "Twój nowy kolega z pracy jest bardzo sympatyczny",
        "Il tuo nuovo collega è davvero simpatico", "Tu nuevo compañero es muy simpático",
        "Ton nouveau collègue est vraiment sympa", "Tvůj nový kolega je fakt sympatický")}),
    26: ("«прописаться, заявить о прибытии» — другие значения; " + LIST, {
        "t_ru": "записаться, зарегистрироваться", "t_uk": "записатися, зареєструватися", "t_en": "to register, to sign up",
        "t_tr": "kaydolmak", "t_pl": "zapisać się, zarejestrować się", "t_it": "iscriversi, registrarsi",
        "t_es": "inscribirse, registrarse", "t_fr": "s'inscrire, s'enregistrer", "t_cs": "přihlásit se, zaregistrovat se",
        "x_uk": "Я хочу записатися на курс", "x_en": "I'd like to sign up for the course"}),
    1297: ("«провести по счёту» — бухгалтерия; " + LIST, {
        "t_ru": "забронировать, заказать", "t_uk": "забронювати, замовити", "t_en": "to book", "t_tr": "rezervasyon yapmak",
        "t_pl": "zarezerwować", "x_ru": "Я хотел бы забронировать отель", "x_en": "I'd like to book a hotel"}),
    1922: (LIST, {"t_ru": "сидеть в интернете, заниматься сёрфингом", "t_uk": "сидіти в інтернеті, займатися серфінгом",
                  "t_en": "to surf", "t_tr": "internette gezinmek, sörf yapmak", "t_pl": "surfować"}),
    690: ("«Ostern ist ein Feiertag» — пусто", {**all_x(
        "Was macht ihr an Ostern?", "Что вы делаете на Пасху?", "Що ви робите на Великдень?",
        "What are you doing at Easter?", "Paskalya'da ne yapıyorsunuz?", "Co robicie na Wielkanoc?",
        "Cosa fate a Pasqua?", "¿Qué hacéis por Pascua?", "Qu'est-ce que vous faites à Pâques?",
        "Co děláte na Velikonoce?")}),
    1733: ("четвёртый пример про «Termin»", {**all_x(
        "Ich notiere mir deine Nummer", "Я запишу себе твой номер", "Я запишу собі твій номер",
        "I'll note down your number", "Numaranı not alıyorum", "Zanotuję sobie twój numer", "Mi segno il tuo numero",
        "Me apunto tu número", "Je note ton numéro", "Zapíšu si tvoje číslo")}),
    2036: (LIST + "; en «We agree on a meeting time» — книжно", {
        "t_ru": "договориться, назначить", "t_uk": "домовитися, призначити", "t_en": "to arrange, to agree on",
        "t_tr": "kararlaştırmak, ayarlamak", "t_pl": "ustalić, umówić się", "t_it": "fissare, concordare",
        "t_es": "concertar, acordar", "t_fr": "fixer, convenir de", "t_cs": "domluvit, dohodnout",
        "x_ru": "Давай договоримся о встрече", "x_uk": "Давай домовимося про зустріч",
        "x_en": "Let's arrange an appointment"}),
    13549: ("шаблон trainieren («dreimal pro Woche im Fitnessstudio»)", {**all_x(
        "Ich musste viermal klingeln, bis jemand aufgemacht hat", "Мне пришлось звонить четыре раза, пока кто-то не открыл",
        "Мені довелося дзвонити чотири рази, поки хтось не відчинив", "I had to ring four times before anyone opened the door",
        "Biri kapıyı açana kadar dört kez zili çalmak zorunda kaldım", "Musiałem dzwonić cztery razy, zanim ktoś otworzył",
        "Ho dovuto suonare quattro volte prima che qualcuno aprisse", "Tuve que llamar cuatro veces hasta que alguien abrió",
        "J'ai dû sonner quatre fois avant qu'on m'ouvre", "Musel jsem zvonit čtyřikrát, než někdo otevřel")}),
    7464: ("«на благо всех людей» — язык лозунгов; " + LIST, {
        "t_ru": "благо, благополучие", "t_uk": "благо, добробут", "t_en": "good, well-being", "t_tr": "iyilik, refah",
        "t_pl": "dobro, pomyślność",
        **all_x("Das mache ich nur zu deinem Wohl", "Я делаю это только ради твоего же блага",
                "Я роблю це лише для твого ж блага", "I'm only doing it for your own good",
                "Bunu sadece senin iyiliğin için yapıyorum", "Robię to tylko dla twojego dobra",
                "Lo faccio solo per il tuo bene", "Lo hago solo por tu bien", "Je le fais seulement pour ton bien",
                "Dělám to jen pro tvoje dobro")}),
    8980: (EN + " («I send my application tomorrow»); " + LIST, {
        "t_ru": "заявка на работу, кандидатура", "t_uk": "заявка на роботу, кандидатура", "t_en": "(job) application",
        "t_tr": "iş başvurusu", "t_pl": "podanie o pracę, aplikacja",
        "x_en": "I'll send off my application tomorrow"}),
    9835: (LIST, {"t_ru": "карманные деньги", "t_uk": "кишенькові гроші", "t_en": "pocket money", "t_tr": "harçlık",
                  "t_pl": "kieszonkowe"}),
    9841: ("«Клиентка хочет купить платье» — пусто; " + LIST, {
        "t_ru": "клиентка, покупательница", "t_uk": "клієнтка, покупниця", "t_en": "customer (female)", "t_tr": "müşteri",
        "t_pl": "klientka",
        **all_x("Die Kundin hat sich über den Preis beschwert", "Покупательница пожаловалась на цену",
                "Покупниця поскаржилася на ціну", "The customer complained about the price", "Müşteri fiyattan şikâyet etti",
                "Klientka skarżyła się na cenę", "La cliente si è lamentata del prezzo", "La clienta se quejó del precio",
                "La cliente s'est plainte du prix", "Zákaznice si stěžovala na cenu")}),
    17213: ("«Двигатель твоей машины очень мощный» — шаблон Motor; " + LIST, {
        "t_ru": "машина, вагон", "t_uk": "машина, вагон", "t_en": "car, carriage", "t_tr": "araba, vagon",
        "t_pl": "samochód, wagon", "t_it": "la macchina, il vagone", "t_es": "el coche, el vagón",
        "t_fr": "la voiture, le wagon", "t_cs": "auto, vagon",
        **all_x("Wo hast du den Wagen geparkt?", "Где ты поставил машину?", "Де ти поставив машину?",
                "Where did you park the car?", "Arabayı nereye park ettin?", "Gdzie zaparkowałeś samochód?",
                "Dove hai parcheggiato la macchina?", "¿Dónde has aparcado el coche?",
                "Où est-ce que tu as garé la voiture?", "Kde jsi zaparkoval auto?")}),
    469: (LIST, {"t_ru": "универмаг", "t_uk": "універмаг"}),
}

# insbesondere — письменное; говорят besonders
REPLACE = [{"id": 7275, "by": 1262, "lang": "de", "why": "insbesondere — письменное, в речи besonders"}]

SPLIT_LATER = {}
