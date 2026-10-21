"""B1, блок 27: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    279: ("«Der Flur ist lang» — пусто", {
        "t_ru": "прихожая, коридор", "t_uk": "передпокій, коридор", "t_en": "hallway, corridor", "t_tr": "antre, koridor",
        **all_x("Lass deine Schuhe im Flur stehen", "Оставь обувь в прихожей", "Залиш взуття в передпокої",
                "Leave your shoes in the hallway", "Ayakkabılarını antrede bırak", "Zostaw buty w przedpokoju",
                "Lascia le scarpe nell'ingresso", "Deja los zapatos en el recibidor", "Laisse tes chaussures dans l'entrée",
                "Nech si boty v předsíni")}),
    12531: ("ru «быстро сходить по-маленькому» — так не говорят; en «real quick» — американское; " + LIST, {
        "t_ru": "писать, сходить по-маленькому", "t_en": "to pee, to take a leak",
        "x_ru": "Мне надо сбегать пописать", "x_en": "I just need a quick pee"}),
    6755: ("убрать пометку (hovor.)", {"t_tr": "leke", "t_cs": "skvrna, flek"}),
    2709: ("«Das ist das Paradies» — пусто", {"t_en": "paradise", **all_x(
        "Hier ist es wie im Paradies", "Здесь как в раю", "Тут як у раю", "It's like paradise here", "Burası cennet gibi",
        "Tu jest jak w raju", "Qui è come in paradiso", "Esto es como el paraíso", "Ici, c'est comme au paradis",
        "Je to tu jako v ráji")}),
    15442: ("«Wir kletterten …» — претерит; uk «бескид» — это горный хребет", {
        "t_uk": "скеля, брила",
        **all_x("Spring nicht von dem Felsen ins Wasser!", "Не прыгай со скалы в воду!", "Не стрибай зі скелі у воду!",
                "Don't jump off the rock into the water!", "Kayadan suya atlama!", "Nie skacz ze skały do wody!",
                "Non saltare dalla roccia in acqua!", "¡No saltes de la roca al agua!", "Ne saute pas du rocher dans l'eau!",
                "Neskákej ze skály do vody!")}),
    6758: (LIST, {"t_ru": "вполне, совершенно", "t_uk": "цілком, безумовно", "t_en": "quite, absolutely",
                  "t_tr": "oldukça, kesinlikle", "t_pl": "całkiem, jak najbardziej", "t_it": "del tutto, senz'altro",
                  "t_es": "perfectamente, sin duda", "t_cs": "naprosto, docela"}),
    6759: ("смысл примера — резервная копия, а uk/en/tr/pl — «защитить»; " + LIST, {
        "t_ru": "сделать резервную копию, обеспечить", "t_uk": "зробити резервну копію, забезпечити",
        "t_en": "to back up, to secure", "t_tr": "yedeklemek, güvence altına almak",
        "t_pl": "zrobić kopię zapasową, zabezpieczyć", "t_it": "salvare, proteggere", "t_es": "guardar, asegurar",
        "t_fr": "sauvegarder, sécuriser", "t_cs": "zálohovat, zabezpečit",
        "x_uk": "Нам треба зробити резервну копію наших даних", "x_en": "We need to back up our data",
        "x_tr": "Verilerimizi yedeklememiz gerek", "x_pl": "Musimy zrobić kopię zapasową naszych danych"}),
    6760: (LIST, {"t_ru": "в остальном, иначе", "t_uk": "в іншому, інакше", "t_en": "otherwise, apart from that",
                  "t_tr": "bunun dışında, aksi halde", "t_pl": "poza tym, w przeciwnym razie", "t_fr": "à part ça, sinon"}),
    14989: ("«Der junge Bursche ist sehr hilfsbereit» — пусто; убрать пометки (coloq.)/(fam.); " + LIST, {
        "t_ru": "парень, малый", "t_uk": "хлопець, парубок", "t_en": "lad, guy", "t_tr": "delikanlı, oğlan",
        "t_pl": "chłopak, facet", "t_it": "il ragazzo, il giovanotto", "t_es": "el chico, el chaval",
        "t_fr": "le gars, le garçon", "t_cs": "chlapík, mladík",
        **all_x("Er ist ein netter Bursche", "Он славный парень", "Він славний хлопець", "He's a nice lad",
                "İyi bir delikanlı", "To miły chłopak", "È un bravo ragazzo", "Es un buen chaval", "C'est un brave gars",
                "Je to fajn chlapík")}),
    18158: ("пример про Wohnblock, а не про Block; " + LIST, {
        "t_ru": "блокнот, квартал", "t_uk": "блокнот, квартал", "t_en": "notepad, block", "t_tr": "bloknot, blok",
        "t_pl": "notatnik, blok", "t_it": "il blocco note, il condominio", "t_es": "el bloc de notas, el bloque",
        "t_fr": "le bloc-notes, l'immeuble",
        **all_x("Gib mir mal einen Block und einen Stift", "Дай-ка мне блокнот и ручку", "Дай-но мені блокнот і ручку",
                "Pass me a notepad and a pen", "Bana bir bloknot ve kalem ver", "Daj mi notatnik i długopis",
                "Passami un blocco note e una penna", "Pásame un bloc de notas y un boli",
                "Passe-moi un bloc-notes et un stylo", "Podej mi blok a propisku")}),
    6761: (LIST, {"t_ru": "замешанный, запутанный", "t_uk": "замішаний, заплутаний", "t_en": "involved, entangled",
                  "t_tr": "karışmış, karmaşık", "t_pl": "zamieszany, zawiły", "t_it": "implicato, intricato",
                  "t_es": "implicado, enredado", "t_fr": "mêlé, compliqué"}),
    17777: (LIST, {"t_en": "advertising, ad", "t_fr": "la publicité, la pub"}),
    6762: ("«Kannst du mal nach rechts blicken?» — так не говорят (schauen); живое — «sich blicken lassen»", {
        "t_ru": "смотреть, показываться", "t_uk": "дивитися, показуватися", "t_en": "to look, to show up",
        "t_tr": "bakmak, görünmek", "t_pl": "spojrzeć, pokazać się", "t_it": "guardare, farsi vedere",
        "t_es": "mirar, dejarse ver", "t_fr": "regarder, se montrer", "t_cs": "podívat se, ukázat se",
        **all_x("Lass dich mal wieder blicken!", "Показывайся к нам почаще!", "Показуйся до нас частіше!",
                "Show up again soon!", "Yine görün bize!", "Pokaż się znowu u nas!", "Fatti vedere ogni tanto!",
                "¡Déjate ver de vez en cuando!", "Montre-toi de temps en temps!", "Zase se u nás ukaž!")}),
    10296: ("«Ich habe den Willen, das zu schaffen» — так не говорят; " + LIST, {
        "t_ru": "воля, желание", "t_tr": "irade, istek", "t_en": "will, willpower",
        **all_x("Das hat er gegen meinen Willen gemacht", "Он сделал это против моей воли", "Він зробив це проти моєї волі",
                "He did it against my will", "Bunu isteğim dışında yaptı", "Zrobił to wbrew mojej woli",
                "L'ha fatto contro la mia volontà", "Lo hizo en contra de mi voluntad", "Il l'a fait contre ma volonté",
                "Udělal to proti mé vůli")}),
    12533: ("«женщина-врач», «female doctor» — лишнее", {
        "t_ru": "врач, доктор", "t_en": "doctor", "t_tr": "doktor, hekim"}),
    1950: (EN + " («I'm doing therapy»); " + LIST, {
        "t_ru": "терапия, лечение", "t_uk": "терапія, лікування", "t_en": "therapy, treatment", "t_tr": "terapi, tedavi",
        "t_pl": "terapia, leczenie", "x_en": "I'm in therapy at the moment"}),
    10297: (LIST, {"t_ru": "полезный, готовый помочь"}),
    10298: (LIST, {"t_ru": "видение, мечта", "t_uk": "бачення, мрія", "t_en": "vision", "t_tr": "vizyon, hayal",
                   "t_pl": "wizja", "t_cs": "vize, představa"}),
    2218: ("«Die Aufregung vor der Prüfung war groß» — пусто; " + LIST, {
        "t_ru": "волнение, переполох", "t_uk": "хвилювання, переполох", "t_en": "excitement, fuss", "t_tr": "heyecan, telaş",
        "t_pl": "zdenerwowanie, zamieszanie", "t_it": "l'agitazione, il trambusto", "t_es": "los nervios, el alboroto",
        "t_fr": "la nervosité, l'agitation", "t_cs": "nervozita, rozrušení",
        **all_x("Wozu die ganze Aufregung?", "К чему весь этот переполох?", "Навіщо весь цей переполох?",
                "What's all the fuss about?", "Bu telaş niye?", "Po co to całe zamieszanie?",
                "Perché tutto questo trambusto?", "¿A qué viene tanto alboroto?", "Pourquoi toute cette agitation?",
                "K čemu takové rozrušení?")}),
    2414: ("«Du darfst mich nicht enttäuschen» — книжно; ru «не должен» — калька", {
        "t_ru": "разочаровывать, подводить", "t_uk": "розчаровувати, підводити",
        **all_x("Enttäusch mich nicht!", "Не подведи меня!", "Не підведи мене!", "Don't let me down!",
                "Beni hayal kırıklığına uğratma!", "Nie zawiedź mnie!", "Non deludermi!", "¡No me decepciones!",
                "Ne me déçois pas!", "Nezklam mě!")}),
    1924: ("«Das ist ein Symbol für Frieden» — пусто; " + LIST, {
        "t_ru": "символ, значок", "t_uk": "символ, значок", "t_en": "symbol, icon", "t_tr": "sembol, simge",
        "t_pl": "symbol, ikona", "t_it": "il simbolo, l'icona", "t_es": "el símbolo, el icono",
        "t_fr": "le symbole, l'icône", "t_cs": "symbol, ikona",
        **all_x("Klick auf das Symbol oben rechts", "Нажми на значок справа вверху", "Натисни на значок угорі праворуч",
                "Click on the icon at the top right", "Sağ üstteki simgeye tıkla", "Kliknij ikonę w prawym górnym rogu",
                "Clicca sull'icona in alto a destra", "Haz clic en el icono de arriba a la derecha",
                "Clique sur l'icône en haut à droite", "Klikni na ikonu vpravo nahoře")}),
    616: ("«Er fährt mit dem Motorrad» — шаблон Fahrrad («Er fährt mit dem Fahrrad»)", {**all_x(
        "Ich hätte so gern ein Motorrad", "Я так хочу мотоцикл", "Я б так хотів мотоцикл", "I'd love to have a motorbike",
        "Bir motosikletim olsun çok isterdim", "Tak bardzo chciałbym mieć motocykl", "Mi piacerebbe tanto avere una moto",
        "Me encantaría tener una moto", "J'aimerais tellement avoir une moto", "Strašně bych chtěl motorku")}),
    6764: ("«Ich kehre das Zimmer» — пусто; " + LIST, {
        "t_ru": "подметать, поворачивать", "t_uk": "підмітати, повертати", "t_tr": "süpürmek, çevirmek",
        "t_pl": "zamiatać, zawracać", "t_it": "spazzare, girare", "t_es": "barrer, girar", "t_fr": "balayer, tourner",
        "t_cs": "zametat, obrátit", "t_en": "to sweep, to turn",
        **all_x("Kannst du mal den Hof kehren?", "Можешь подмести двор?", "Можеш підмести двір?", "Can you sweep the yard?",
                "Avluyu süpürebilir misin?", "Możesz pozamiatać podwórko?", "Puoi spazzare il cortile?",
                "¿Puedes barrer el patio?", "Tu peux balayer la cour?", "Můžeš zamést dvůr?")}),
    17778: ("«Der Gewinn war größer als erwartet» — отчёт фирмы; " + LIST, {
        "t_ru": "выигрыш, прибыль", "t_uk": "виграш, прибуток", "t_en": "winnings, profit", "t_tr": "ikramiye, kâr",
        "t_pl": "wygrana, zysk", "t_it": "la vincita, il guadagno", "t_es": "el premio, el beneficio",
        "t_fr": "le gain, le bénéfice", "t_cs": "výhra, zisk",
        **all_x("Den Gewinn teilen wir uns", "Выигрыш поделим", "Виграш поділимо", "We'll split the winnings",
                "İkramiyeyi paylaşacağız", "Wygraną się podzielimy", "La vincita ce la dividiamo",
                "El premio nos lo repartimos", "On partage les gains", "Výhru si rozdělíme")}),
    10302: ("ru «в глубокой скорби» — книжно; " + LIST, {
        "t_ru": "горе, траур", "t_uk": "горе, жалоба", "t_en": "grief, mourning", "t_tr": "yas, keder",
        "t_pl": "żałoba, smutek", "t_es": "el luto, la tristeza",
        "x_ru": "Семья всё ещё в трауре", "x_uk": "Родина досі в жалобі", "x_en": "The family is still in mourning"}),
    324: ("«Das Café ist gemütlich» — пусто; " + LIST, {
        "t_ru": "уютный, удобный", "t_uk": "затишний, зручний", "t_en": "cosy, comfortable", "t_tr": "rahat, keyifli",
        "t_pl": "przytulny, wygodny", "t_it": "accogliente, comodo", "t_es": "acogedor, cómodo",
        "t_fr": "chaleureux, confortable", "t_cs": "útulný, pohodlný",
        **all_x("Mach es dir gemütlich!", "Располагайся поудобнее!", "Влаштовуйся зручніше!", "Make yourself comfortable!",
                "Rahatına bak!", "Usiądź sobie wygodnie!", "Mettiti comodo!", "¡Ponte cómodo!",
                "Installe-toi confortablement!", "Udělej si pohodlí!")}),
    700: (LIST, {"t_ru": "парковка, стоянка", "t_uk": "парковка, стоянка", "t_en": "parking space, car park",
                 "t_es": "la plaza de aparcamiento, el aparcamiento"}),
    1038: (LIST, {"t_ru": "вернуться, прийти снова", "t_uk": "повернутися, прийти знову", "t_en": "to come back, to return",
                  "t_tr": "geri gelmek, tekrar gelmek", "t_pl": "wracać, przyjść znowu"}),
    13933: (LIST + " (было семь значений)", {
        "t_ru": "передать", "t_uk": "передати", "t_en": "to pass on, to tell", "t_tr": "iletmek, söylemek",
        "t_pl": "przekazać, powiedzieć", "t_it": "riferire, dire", "t_es": "transmitir, decir", "t_fr": "transmettre, dire",
        "t_cs": "vyřídit, předat"}),
    10304: (LIST, {"t_ru": "привлекательный, заманчивый", "t_uk": "привабливий, заманливий", "t_en": "attractive, appealing",
                   "t_tr": "çekici, cazip", "t_pl": "atrakcyjny, ponętny", "t_fr": "attrayant, séduisant"}),
    17095: ("«Die Geschwindigkeit war zu hoch» — протокол", {**all_x(
        "Mit welcher Geschwindigkeit bist du gefahren?", "С какой скоростью ты ехал?", "З якою швидкістю ти їхав?",
        "What speed were you doing?", "Hangi hızla gidiyordun?", "Z jaką prędkością jechałeś?", "A che velocità andavi?",
        "¿A qué velocidad ibas?", "Tu roulais à quelle vitesse?", "Jakou rychlostí jsi jel?")}),
    10306: ("«Der Abschied fiel uns schwer» — претерит", {**all_x(
        "Der Abschied ist mir echt schwergefallen", "Прощание далось мне очень тяжело", "Прощання далося мені дуже важко",
        "Saying goodbye was really hard for me", "Veda etmek bana çok zor geldi", "Pożegnanie było dla mnie naprawdę trudne",
        "L'addio per me è stato davvero difficile", "La despedida me costó muchísimo",
        "Les adieux ont été vraiment durs pour moi", "Loučení mi dalo fakt zabrat")}),
}

REPLACE = [
    {"id": 13490, "by": 13481, "lang": "de", "why": "denselben — форма слова derselbe"},
    {"id": 10301, "by": 10207, "lang": "de", "why": "Zorn — книжный вариант Wut"},
]

SPLIT_LATER = {
    13933: ["ausrichten = устраивать (ein Fest ausrichten), выравнивать"],
    6764: ["kehren = поворачивать (jemandem den Rücken kehren)"],
}
