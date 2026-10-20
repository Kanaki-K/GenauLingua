"""A1, блок 11: слова 401–440 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
SAME = "пример совпадал с примером другого слова — у каждого свой"
MARK = "пометка «(hovor.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15949: (LIST, {"t_uk": "поліцейський", "t_en": "police officer, policeman"}),
    6405: (LIST, {"t_ru": "тихо, тихий", "t_uk": "тихо, тихий", "t_en": "quietly, quiet", "t_tr": "sessizce, sessiz",
                  "t_pl": "cicho", "t_it": "piano, sottovoce", "t_fr": "doucement", "t_cs": "potichu, tiše"}),
    1049: (LIST + "; «On the weekend I am free» — так не говорят", {
        "t_ru": "выходные", "t_uk": "вихідні", "x_en": "I'm free at the weekend"}),
    169: (LIST + "; «Это длится час» — калька", {
        "t_ru": "длиться, занимать", "t_uk": "тривати, займати", "t_en": "to last, to take", "t_tr": "sürmek",
        "t_pl": "trwać", "t_it": "durare, volerci", "t_es": "durar, tardar", "t_fr": "durer, prendre",
        "x_ru": "Это займёт час", "x_uk": "Це займе годину", "x_pl": "To potrwa godzinę"}),
    90: ("«Er verletzt sich am Bein» — тот же шаблон, что у Arm, и время не совпадало с переводом", {
        "t_ru": "нога", "t_uk": "нога", "t_tr": "bacak", "t_pl": "noga",
        **all_x("Mir tut das Bein weh", "У меня болит нога", "У мене болить нога", "My leg hurts", "Bacağım ağrıyor",
                "Boli mnie noga", "Mi fa male la gamba", "Me duele la pierna", "J'ai mal à la jambe",
                "Bolí mě noha")}),
    17481: (LIST + "; «самолёт» — другое употребление; uk «станок» — русизм; " + MARK + "; " + SAME
            + " (kaputt)", {
        "t_ru": "машина, станок", "t_uk": "машина, верстат", "t_en": "machine", "t_tr": "makine",
        "t_pl": "maszyna", "t_it": "la macchina", "t_cs": "stroj",
        **all_x("Wie funktioniert diese Maschine?", "Как работает эта машина?", "Як працює ця машина?",
                "How does this machine work?", "Bu makine nasıl çalışıyor?", "Jak działa ta maszyna?",
                "Come funziona questa macchina?", "¿Cómo funciona esta máquina?", "Comment marche cette machine?",
                "Jak funguje tenhle stroj?")}),
    578: (EN + "; uk «до моря» — по-украински «на море»", {"t_en": "sea", "x_en": "We're going to the seaside",
                                                         "x_uk": "Ми їдемо на море"}),
    1345: (LIST + "; «местность» — другое употребление", {
        "t_ru": "угол", "t_uk": "ріг, кут", "t_en": "corner", "t_tr": "köşe", "t_pl": "róg, kąt",
        "t_cs": "roh, kout"}),
    6420: (LIST + "; «Торопись же!» — книжно", {
        "t_en": "to hurry", "t_tr": "acele etmek", "t_pl": "spieszyć się",
        "x_ru": "Поторопись!", "x_uk": "Поспіши!", "x_pl": "Pospiesz się!"}),
    297: ("«Wir essen um acht Frühstück» — по-немецки так не говорят", {
        **all_x("Das Frühstück gibt es von sieben bis zehn", "Завтрак с семи до десяти", "Сніданок із сьомої до десятої",
                "Breakfast is from seven to ten", "Kahvaltı yediden ona kadar", "Śniadanie jest od siódmej do dziesiątej",
                "La colazione è dalle sette alle dieci", "El desayuno es de siete a diez",
                "Le petit-déjeuner est servi de sept à dix heures", "Snídaně je od sedmi do deseti")}),
    337: (LIST + "; «звонок» — другое употребление", {
        "t_ru": "разговор, беседа", "t_uk": "розмова, бесіда", "t_en": "conversation, talk", "t_tr": "konuşma, sohbet",
        "t_pl": "rozmowa", "t_it": "la conversazione, il colloquio", "t_es": "la conversación, la charla",
        "t_fr": "la conversation, l'entretien", "t_cs": "rozhovor, hovor"}),
    365: (LIST, {"t_ru": "волосы, волос", "t_uk": "волосся", "t_tr": "saç", "t_pl": "włosy, włos",
                 "t_it": "i capelli", "t_es": "el pelo", "t_fr": "les cheveux", "t_cs": "vlasy, vlas"}),
    507: (TWO + " («пробовать» — kosten = probieren, своя строка)", {
        "t_ru": "стоить", "t_uk": "коштувати", "t_en": "to cost", "t_tr": "mal olmak", "t_pl": "kosztować",
        "t_it": "costare", "t_es": "costar", "t_fr": "coûter", "t_cs": "stát"}),
    350: (LIST + "; uk «Це двадцять градусів» — калька", {
        "t_ru": "градус", "t_uk": "градус", "t_en": "degree", "t_tr": "derece", "t_pl": "stopień",
        "x_en": "It's twenty degrees", "x_uk": "Двадцять градусів"}),
    1694: (TWO + " («успевать, понимать» — своя строка)", {
        "t_ru": "пойти с, идти вместе", "t_uk": "піти з, йти разом", "t_en": "to come along",
        "t_tr": "birlikte gelmek", "t_pl": "iść razem, pójść z", "t_it": "venire con", "t_es": "venir con",
        "t_fr": "venir avec", "t_cs": "jít s", "x_uk": "Ти підеш з нами?"}),
    563: (TWO + " («раствор» — своя строка)", {
        "t_ru": "решение", "t_uk": "рішення", "t_en": "solution, answer", "t_tr": "çözüm", "t_pl": "rozwiązanie",
        "x_en": "That's the right solution"}),
    6436: (SAME + " (Laden: «Der Laden ist geschlossen»); «единодушный» — другое значение", {
        "t_ru": "закрытый, закрыт", "t_uk": "зачинений, закритий", "t_en": "closed", "t_tr": "kapalı",
        "t_pl": "zamknięty, nieczynny",
        **all_x("Sonntags ist die Bank geschlossen", "По воскресеньям банк закрыт", "По неділях банк зачинений",
                "The bank is closed on Sundays", "Banka pazar günleri kapalı", "W niedziele bank jest zamknięty",
                "La domenica la banca è chiusa", "Los domingos el banco está cerrado",
                "Le dimanche, la banque est fermée", "V neděli je banka zavřená")}),
    704: (LIST + "; «Мы делаем перерыв» — калька", {
        "t_ru": "перерыв, пауза", "t_en": "break", "t_tr": "mola, ara", "t_pl": "przerwa",
        "x_ru": "Сделаем перерыв", "x_uk": "Зробимо перерву", "x_en": "Let's take a break", "x_tr": "Mola verelim",
        "x_pl": "Zróbmy przerwę"}),
    9441: (LIST, {"t_ru": "учитель", "t_uk": "вчитель", "t_en": "teacher", "t_tr": "öğretmen", "t_pl": "nauczyciel",
                  "t_it": "l'insegnante, il maestro", "t_es": "el profesor, el maestro", "t_fr": "le professeur",
                  "t_cs": "učitel"}),
    1948: (LIST, {"t_ru": "тема", "t_uk": "тема", "t_en": "topic, subject", "t_tr": "konu", "t_pl": "temat"}),
    634: ("три описания вместо слова", {"t_ru": "вторая половина дня, после обеда",
                                        "t_uk": "друга половина дня, після обіду", "t_tr": "öğleden sonra",
                                        "t_pl": "popołudnie"}),
    676: (EN, {"t_en": "grandma", "t_tr": "büyükanne", "x_en": "Grandma is baking a cake",
               "x_tr": "Büyükannem kek yapıyor"}),
    68: (LIST + "; «курорт с водами» — другое значение", {
        "t_ru": "ванная", "t_uk": "ванна кімната", "t_en": "bathroom, bath", "t_tr": "banyo",
        "t_pl": "łazienka, kąpiel"}),
    970: (LIST + "; " + EN, {"t_ru": "отпуск", "t_uk": "відпустка", "t_en": "holiday, vacation", "t_tr": "tatil",
                             "t_pl": "urlop, wakacje", "x_en": "We're going on holiday"}),
    274: ("«Я люблю есть рыбу» — калька", {"x_ru": "Я люблю рыбу", "x_uk": "Я люблю рибу"}),
    498: (DULL, {**all_x("Hast du schon den Koffer gepackt?", "Ты уже собрал чемодан?", "Ти вже зібрав валізу?",
                         "Have you packed your suitcase yet?", "Bavulunu hazırladın mı?", "Spakowałeś już walizkę?",
                         "Hai già fatto la valigia?", "¿Ya has hecho la maleta?", "Tu as déjà fait ta valise?",
                         "Už máš sbalený kufr?")}),
    761: (EN, {"x_ru": "Мы поедим в ресторане", "x_en": "We're eating at a restaurant"}),
    865: (LIST + "; «манера говорить» — описание", {
        "t_ru": "язык, речь", "t_uk": "мова", "t_en": "language", "t_tr": "dil", "t_pl": "język",
        "t_it": "la lingua", "t_es": "el idioma, la lengua", "t_fr": "la langue", "t_cs": "jazyk"}),
    256: (LIST, {"t_pl": "kolor, farba"}),
    520: (SAME + " (anfangen: «Der Kurs fängt um acht an»); " + LIST, {
        "t_ru": "курс, занятия", "t_uk": "курс, заняття", "t_en": "course, class", "t_tr": "kurs, ders",
        "t_pl": "kurs, zajęcia", "t_it": "il corso", "t_es": "el curso", "t_fr": "le cours", "t_cs": "kurz",
        **all_x("Ich mache einen Deutschkurs", "Я хожу на курсы немецкого", "Я ходжу на курси німецької",
                "I'm doing a German course", "Almanca kursuna gidiyorum", "Chodzę na kurs niemieckiego",
                "Faccio un corso di tedesco", "Hago un curso de alemán", "Je suis un cours d'allemand",
                "Chodím na kurz němčiny")}),
    307: (LIST + "; «двор» — не Garten; " + EN, {
        "t_ru": "сад, огород", "t_uk": "сад, город", "t_en": "garden", "t_tr": "bahçe", "t_pl": "ogród",
        "t_it": "il giardino", "t_es": "el jardín", "t_fr": "le jardin", "x_en": "She's working in the garden"}),
    517: (LIST, {"t_ru": "пирог, торт", "t_uk": "пиріг, торт", "t_en": "cake", "t_tr": "kek, pasta", "t_pl": "ciasto",
                 "t_it": "la torta, il dolce", "t_es": "el pastel, la tarta", "t_fr": "le gâteau",
                 "t_cs": "koláč, dort"}),
}

SPLIT_LATER = {
    507: ["kosten = пробовать на вкус"],
    1694: ["mitkommen = успевать, понимать (Kommst du mit?)"],
    563: ["die Lösung = раствор (химия)"],
}
