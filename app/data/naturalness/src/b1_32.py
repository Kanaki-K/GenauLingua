"""B1, блок 32: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17779: (LIST, {"t_ru": "скот, скотина", "t_uk": "худоба, скотина", "t_en": "livestock, cattle",
                   "t_tr": "davar, çiftlik hayvanları", "t_pl": "bydło, inwentarz żywy"}),
    6825: (LIST, {"t_ru": "обнаружить, открыть", "t_uk": "виявити, відкрити", "t_en": "to discover, to spot",
                  "t_tr": "keşfetmek, fark etmek", "t_pl": "odkryć, zauważyć", "t_cs": "objevit, odhalit",
                  "x_en": "I'd love to discover new countries"}),
    6827: (LIST, {"t_ru": "блестящий, гениальный", "t_uk": "блискучий, геніальний", "t_en": "brilliant, superb",
                  "t_tr": "parlak, dâhice", "t_pl": "błyskotliwy, genialny", "t_cs": "skvělý, brilantní"}),
    10330: (LIST + "; ru «Прислушайся к разуму» — калька", {
        "t_ru": "разум, здравый смысл", "t_uk": "розум, здоровий глузд", "t_en": "reason, common sense",
        "t_tr": "akıl, sağduyu", "t_pl": "rozsądek, rozum", "t_es": "la razón, el sentido común",
        "x_ru": "Прислушайся к голосу разума и не покупай эту машину", "x_en": "Listen to reason and don't buy the car"}),
    16045: ("«Das steht so in unserer Verfassung» — учебник права; живое — «в форме»", {
        "t_ru": "состояние, конституция", "t_uk": "стан, конституція", "t_en": "shape, constitution",
        "t_tr": "form, anayasa", "t_pl": "kondycja, konstytucja", "t_it": "la condizione, la costituzione",
        "t_es": "el estado, la constitución", "t_fr": "la forme, la constitution", "t_cs": "kondice, ústava",
        **all_x("Er ist heute in schlechter Verfassung", "Он сегодня в плохом состоянии", "Він сьогодні в поганому стані",
                "He's in bad shape today", "Bugün formu kötü", "Jest dziś w kiepskiej kondycji",
                "Oggi è in cattive condizioni", "Hoy está en mal estado", "Il n'est pas en forme aujourd'hui",
                "Dneska je ve špatné kondici")}),
    6828: ("«Das Konzert war echt krass» — шаблон «Das Konzert war …»; убрать пометки; " + LIST, {
        "t_ru": "крутой, жёсткий", "t_uk": "крутий, жорсткий", "t_en": "awesome, extreme", "t_tr": "müthiş, aşırı",
        "t_pl": "niesamowity, drastyczny", "t_it": "pazzesco, estremo", "t_es": "increíble, tremendo",
        "t_fr": "dingue, extrême", "t_cs": "šílený, drsný",
        **all_x("Krass, hast du das gesehen?", "Круто, ты это видел?", "Круто, ти це бачив?", "Awesome, did you see that?",
                "Müthiş, gördün mü bunu?", "Niesamowite, widziałeś to?", "Pazzesco, hai visto?",
                "¡Increíble! ¿Lo has visto?", "Dingue, tu as vu ça?", "Šílený, viděl jsi to?")}),
    6829: ("ru «совершенно преувеличено» — калька; " + LIST, {
        "t_ru": "преувеличенный, слишком", "t_uk": "перебільшений, занадто", "t_en": "exaggerated, over the top",
        "t_tr": "abartılı, aşırı", "t_pl": "przesadzony, przesadny",
        "x_ru": "50 евро за пиццу? Это уж слишком", "x_uk": "50 євро за піцу? Це вже занадто",
        "x_en": "50 euros for a pizza? That's way over the top"}),
    6830: (LIST, {"t_ru": "окончательный, окончательно", "t_uk": "остаточний, остаточно", "t_en": "final, once and for all",
                  "t_tr": "kesin, nihai", "t_pl": "ostateczny, ostatecznie"}),
    6831: (LIST, {"t_ru": "бесполезный, никуда не годный", "t_uk": "марний, непридатний", "t_en": "useless, pointless",
                  "t_tr": "işe yaramaz, faydasız", "t_pl": "bezużyteczny, daremny", "t_cs": "zbytečný, k ničemu"}),
    17923: ("«Ohne Sauerstoff können wir nicht leben» — учебник", {**all_x(
        "Mach mal das Fenster auf, wir brauchen Sauerstoff!", "Открой окно, нам нужен кислород!",
        "Відчини вікно, нам потрібен кисень!", "Open the window, we need some oxygen!",
        "Pencereyi aç, oksijene ihtiyacımız var!", "Otwórz okno, potrzebujemy tlenu!", "Apri la finestra, ci serve ossigeno!",
        "Abre la ventana, ¡necesitamos oxígeno!", "Ouvre la fenêtre, on a besoin d'oxygène!",
        "Otevři okno, potřebujeme kyslík!")}),
    6833: (LIST + "; ru «Давайте» — к одному человеку", {
        "t_ru": "просмотреть, пройти", "t_uk": "переглянути, пройти", "t_en": "to go through, to be approved",
        "t_tr": "gözden geçirmek, kabul edilmek", "t_pl": "przejrzeć, zostać przyjętym", "t_it": "rivedere, passare",
        "t_es": "repasar, ser aprobado", "t_fr": "revoir, être adopté", "x_ru": "Давай ещё раз просмотрим список"}),
    17103: (LIST, {"t_en": "carriage, coach", "t_pl": "powóz, bryczka"}),
    17512: (LIST, {"t_ru": "чип, жетон", "t_uk": "чіп, жетон", "t_en": "chip, token", "t_tr": "çip, fiş",
                   "t_pl": "czip, żeton"}),
    17924: ("«Gib mir die Koordinaten für das Restaurant» — так не говорят", {**all_x(
        "Schick mir die Koordinaten, dann finde ich dich", "Скинь мне координаты, и я тебя найду",
        "Скинь мені координати, і я тебе знайду", "Send me the coordinates and I'll find you",
        "Koordinatları gönder, seni bulurum", "Wyślij mi współrzędne, to cię znajdę", "Mandami le coordinate e ti trovo",
        "Mándame las coordenadas y te encuentro", "Envoie-moi les coordonnées, je te trouverai",
        "Pošli mi souřadnice a najdu tě")}),
    2133: (LIST + " (было «занимающийся этим вопросом»)", {
        "t_ru": "ответственный, компетентный", "t_uk": "відповідальний, компетентний", "t_en": "responsible, in charge",
        "t_tr": "sorumlu, yetkili", "t_pl": "odpowiedzialny, właściwy"}),
    15452: (LIST, {"t_ru": "гром", "t_uk": "грім", "t_en": "thunder", "t_tr": "gök gürültüsü", "t_pl": "grzmot"}),
    11677: (LIST, {"t_ru": "шнапс, водка", "t_uk": "горілка, шнапс", "t_en": "schnapps, spirits",
                   "t_tr": "sert içki, şnaps", "t_pl": "wódka, nalewka", "x_en": "After dinner we'll have a schnapps"}),
    14997: (LIST, {"t_ru": "товарищ, соратник", "t_uk": "товариш, побратим", "t_en": "comrade", "t_tr": "yoldaş",
                   "t_pl": "towarzysz"}),
    6836: (LIST + "; ru «действовать с этой проблемой» — так не говорят", {
        "t_ru": "действовать, спешить (о часах)", "t_uk": "діяти, спішити (про годинник)",
        "t_en": "to proceed, to be fast (clock)", "t_tr": "hareket etmek, ileri gitmek", "t_pl": "postępować, spieszyć się",
        "t_it": "procedere, agire", "t_es": "proceder, actuar", "t_fr": "procéder, agir", "t_cs": "postupovat, jednat",
        "x_ru": "Как нам действовать в этой ситуации?"}),
    15453: (LIST, {"t_ru": "территория, местность", "t_uk": "територія, місцевість", "t_en": "grounds, terrain",
                   "t_tr": "arazi, alan", "t_pl": "teren, obszar"}),
    3077: (LIST, {"t_ru": "согласиться, одобрить", "t_uk": "погодитися, схвалити", "t_en": "to agree, to approve",
                  "t_tr": "katılmak, onaylamak", "t_pl": "zgodzić się, przyznać rację"}),
    10332: ("«Seine Freunde haben ihm Trost gespendet» — книжно; " + LIST, {
        "t_ru": "утешение", "t_uk": "втіха, розрада", "t_en": "comfort, consolation", "t_tr": "teselli",
        "t_pl": "pocieszenie, otucha",
        **all_x("Das ist ein schwacher Trost", "Это слабое утешение", "Це слабка втіха", "That's small consolation",
                "Bu zayıf bir teselli", "To marne pocieszenie", "È una magra consolazione", "Es un pobre consuelo",
                "C'est une maigre consolation", "To je slabá útěcha")}),
    6838: ("снова пицца (у übertrieben); " + LIST, {
        "t_ru": "восьмой", "t_uk": "восьмий", "t_pl": "ósmy",
        **all_x("Wir wohnen im achten Stock", "Мы живём на восьмом этаже", "Ми живемо на восьмому поверсі",
                "We live on the eighth floor", "Sekizinci katta oturuyoruz", "Mieszkamy na ósmym piętrze",
                "Abitiamo all'ottavo piano", "Vivimos en el octavo piso", "On habite au huitième étage",
                "Bydlíme v osmém patře")}),
    16046: ("«Der Fürst lebte in einem großen Schloss» — претерит, сказка; " + LIST, {
        "t_ru": "князь, правитель", "t_uk": "князь, володар", "t_en": "prince, ruler", "t_tr": "prens, hükümdar",
        "t_pl": "książę, władca",
        **all_x("Monaco wird von einem Fürsten regiert", "Монако правит князь", "Монако править князь",
                "Monaco is ruled by a prince", "Monako'yu bir prens yönetiyor", "Monako rządzi książę",
                "Monaco è governato da un principe", "Mónaco está gobernado por un príncipe",
                "Monaco est gouverné par un prince", "Monaku vládne kníže")}),
    14998: (LIST, {"t_pl": "rasa"}),
    18167: ("«Die Kaution … beträgt 500 Euro» — договор; en «apartment» — американское", {
        "t_en": "deposit, bail",
        **all_x("Die Kaution kriegst du zurück, wenn du ausziehst", "Залог тебе вернут, когда съедешь",
                "Заставу тобі повернуть, коли з'їдеш", "You get the deposit back when you move out",
                "Taşınınca depozitoyu geri alırsın", "Kaucję dostaniesz z powrotem, jak się wyprowadzisz",
                "La cauzione te la ridanno quando te ne vai", "La fianza te la devuelven cuando te mudes",
                "Tu récupères la caution quand tu déménages", "Kauci dostaneš zpátky, až se odstěhuješ")}),
    1090: (LIST, {"t_ru": "общественный, публичный", "t_uk": "громадський, публічний", "t_en": "public",
                  "t_tr": "umumi, herkese açık", "t_pl": "publiczny, dostępny dla wszystkich",
                  "x_en": "They use public transport"}),
    493: ("«Es klingelt an der Tür» — шаблон irgendwer («Irgendwer klingelt an der Tür»); " + LIST, {
        "t_ru": "звонить, звенеть", "t_uk": "дзвонити, дзеленчати", "t_en": "to ring", "t_tr": "zil çalmak, çınlamak",
        "t_pl": "dzwonić", "t_es": "sonar, tocar el timbre",
        **all_x("Bei wem soll ich klingeln?", "В какую квартиру мне звонить?", "У кого мені дзвонити?",
                "Whose bell should I ring?", "Kimin zilini çalayım?", "Do kogo mam dzwonić?", "A chi devo suonare?",
                "¿A quién le toco el timbre?", "Je sonne chez qui?", "Kam mám zazvonit?")}),
    17513: (LIST, {"t_ru": "доступ, захват", "t_tr": "erişim, el koyma"}),
    12544: (EN + " («grandpa» — американское)", {"x_en": "Unfortunately my grandad had a heart attack"}),
    10333: (LIST + "; смысл примера — «изменить»", {
        "t_ru": "обманывать, изменять", "t_uk": "обманювати, зраджувати", "t_en": "to cheat on, to deceive",
        "t_tr": "aldatmak, dolandırmak", "t_it": "tradire, ingannare",
        "x_ru": "Я бы никогда тебе не изменил", "x_uk": "Я б ніколи тобі не зрадив"}),
    6841: ("«Das Essen war einfach fabelhaft» — снова Essen; " + LIST, {
        "t_ru": "потрясающий, сказочный", "t_uk": "чудовий, казковий", "t_en": "fabulous, fantastic",
        "t_tr": "harika, muhteşem", "t_pl": "wspaniały, bajeczny",
        **all_x("Du siehst fabelhaft aus!", "Ты выглядишь потрясающе!", "Ти виглядаєш чудово!", "You look fabulous!",
                "Harika görünüyorsun!", "Wyglądasz wspaniale!", "Hai un aspetto favoloso!",
                "¡Tienes un aspecto fabuloso!", "Tu as l'air formidable!", "Vypadáš báječně!")}),
    13496: (EN + " («movie» — американское)", {"x_en": "Not this film, that one over there"}),
    1218: (LIST, {"t_tr": "nakit"}),
}

REPLACE = [
    {"id": 13495, "by": 13484, "lang": "de", "why": "zweites — форма слова zweiter"},
    {"id": 6835, "by": 657, "lang": "de", "why": "nochmals — книжный вариант nochmal"},
    {"id": 13494, "by": 13496, "lang": "de", "why": "jene — форма слова jener"},
    {"id": 6843, "by": 1473, "lang": "de", "why": "genügend — книжный вариант genug; пример тот же"},
]

SPLIT_LATER = {
    6838: ["achte — форма; леммы «achter» в базе нет, есть только acht (A1)"],
}
