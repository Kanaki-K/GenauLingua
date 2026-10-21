"""B1, блок 36: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2345: ("«Gestern gab es einen Diebstahl …» — шаблон Überfall", {"t_ru": "кража, воровство", "t_en": "theft", **all_x(
        "Ich will den Diebstahl bei der Polizei anzeigen", "Я хочу заявить в полицию о краже",
        "Я хочу заявити в поліцію про крадіжку", "I want to report the theft to the police",
        "Hırsızlığı polise bildirmek istiyorum", "Chcę zgłosić kradzież na policję",
        "Voglio denunciare il furto alla polizia", "Quiero denunciar el robo a la policía",
        "Je veux porter plainte pour le vol", "Chci nahlásit krádež na policii")}),
    16061: ("ru «Свидетель должен был» — калька", {"x_ru": "Свидетелю пришлось принести присягу"}),
    10356: ("«Das Angebot soll Kunden locken» — реклама; " + LIST, {
        "t_ru": "приманивать, привлекать", "t_uk": "приманювати, приваблювати", "t_en": "to lure, to attract",
        "t_tr": "cezbetmek, kandırıp çekmek", "t_pl": "wabić, zwabiać", "t_it": "attirare, attrarre",
        "t_es": "atraer, tentar", "t_fr": "attirer, appâter", "t_cs": "lákat, přilákat",
        **all_x("Mit Futter lockst du die Katze ins Haus", "Кормом можно приманить кошку в дом",
                "Кормом можна приманити кішку в дім", "You can lure the cat into the house with food",
                "Kediyi mamayla eve çekebilirsin", "Jedzeniem zwabisz kota do domu", "Con il cibo attiri il gatto in casa",
                "Con comida atraes al gato a casa", "Avec de la nourriture, tu attires le chat dans la maison",
                "Žrádlem kočku přilákáš domů")}),
    18177: (EN + " («apartment» — американское)", {"x_en": "My flat is on the third floor"}),
    3014: ("ru «правильный инструмент» — калька", {"x_ru": "Для этой работы мне нужен подходящий инструмент"}),
    6880: ("ru «Мы должны провести» — калька", {"x_ru": "Тест нужно провести завтра",
                                              "x_en": "We need to carry out the test tomorrow"}),
    14438: (LIST, {"t_ru": "выступать, возникать", "t_uk": "виступати, виникати", "t_en": "to perform, to occur",
                   "t_tr": "sahneye çıkmak, ortaya çıkmak", "t_pl": "występować, pojawiać się",
                   "t_it": "esibirsi, comparire", "t_es": "actuar, aparecer", "t_fr": "se produire, survenir",
                   "t_cs": "vystupovat, vyskytnout se"}),
    17516: (LIST, {"t_ru": "переключить, накинуть", "t_uk": "перемкнути, накинути", "t_en": "to flip, to put around",
                   "t_tr": "çevirmek, omuza atmak", "t_pl": "przełączyć, narzucić", "t_it": "girare, mettere addosso",
                   "t_es": "accionar, poner", "t_fr": "basculer, mettre autour", "t_cs": "přepnout, dát kolem"}),
    6881: (EN, {"x_en": "We have lots of interests in common"}),
    16062: ("«Das ist völlig legal» — пусто", {**all_x(
        "Ist das überhaupt legal?", "Это вообще законно?", "Це взагалі законно?", "Is that even legal?",
        "Bu yasal mı ki?", "Czy to w ogóle legalne?", "Ma è legale?", "¿Eso es legal siquiera?", "C'est légal, au moins?",
        "Je to vůbec legální?")}),
    6882: ("ru «в промежутке» — калька; " + LIST, {
        "t_ru": "между, в промежутке", "t_uk": "між, у проміжку", "t_en": "in between", "t_tr": "arasında, o arada",
        "t_pl": "pomiędzy, w międzyczasie", "t_fr": "entre les deux, entre-temps",
        "x_ru": "Между делами у меня ещё есть немного времени"}),
    12552: ("«Der Arzt brauchte eine sterile Nadel» — претерит; " + LIST, {
        "t_ru": "игла, иголка", "t_uk": "голка, спиця", "t_en": "needle, pin", "t_tr": "iğne, şiş", "t_pl": "igła, szpilka",
        **all_x("Hast du Nadel und Faden?", "У тебя есть иголка с ниткой?", "У тебе є голка з ниткою?",
                "Have you got a needle and thread?", "İğnen ipliğin var mı?", "Masz igłę i nitkę?", "Hai ago e filo?",
                "¿Tienes aguja e hilo?", "Tu as du fil et une aiguille?", "Máš jehlu a nit?")}),
    16063: (LIST, {"t_ru": "условный срок, испытательный срок", "t_uk": "умовний термін, випробувальний термін",
                   "t_en": "probation, suspended sentence", "t_tr": "denetimli serbestlik, ertelenmiş ceza",
                   "t_pl": "zawieszenie wyroku, okres próby"}),
    6883: (EN + " (подлежащее сменилось)", {"t_ru": "далёкий, дальний", "x_en": "I dream of travelling to distant countries"}),
    9467: ("«… hat mich das Autofahren gelehrt» — книжно (в речи beibringen)", {**all_x(
        "Das Leben hat mich gelehrt, geduldig zu sein", "Жизнь научила меня терпению", "Життя навчило мене терпінню",
        "Life has taught me to be patient", "Hayat bana sabırlı olmayı öğretti", "Życie nauczyło mnie cierpliwości",
        "La vita mi ha insegnato a essere paziente", "La vida me ha enseñado a ser paciente",
        "La vie m'a appris à être patient", "Život mě naučil být trpělivý")}),
    17109: ("ru «не переезжай кошку» — так не говорят; " + LIST, {
        "t_ru": "задавить, переехать", "t_uk": "задавити, переїхати", "t_en": "to run over", "t_tr": "ezmek, çiğnemek",
        "t_pl": "przejechać, rozjechać", "x_ru": "Смотри не задави кошку"}),
    1460: (EN, {"x_en": "We're learning a poem by heart"}),
    6885: ("порядок слов в ru/en", {"x_ru": "То, что ты рассказываешь, крайне интересно",
                                    "x_en": "What you're telling me is highly interesting"}),
    15008: ("ru «приходит сегодня» — время", {"x_ru": "Моя невеста придёт сегодня на ужин",
                                              "x_en": "My fiancée is coming to dinner tonight"}),
    12157: (LIST, {"t_ru": "бейсбол", "t_uk": "бейсбол", "t_pl": "baseball"}),
    15009: (LIST, {"t_ru": "свадьба, брак", "t_uk": "шлюб, весілля", "t_en": "marriage, wedding", "t_tr": "evlilik, nikâh",
                   "t_pl": "ślub, małżeństwo"}),
    13953: ("«Kannst du mir den Weg … weisen?» — в речи zeigen (шаблон zeigen); " + LIST, {
        "t_ru": "указывать, показывать", "t_uk": "вказувати, показувати", "t_en": "to point, to show",
        "t_tr": "göstermek, işaret etmek", "t_pl": "wskazywać, pokazywać",
        **all_x("Der Pfeil weist nach links", "Стрелка указывает налево", "Стрілка вказує ліворуч", "The arrow points left",
                "Ok sola işaret ediyor", "Strzałka wskazuje w lewo", "La freccia indica a sinistra",
                "La flecha señala a la izquierda", "La flèche indique la gauche", "Šipka ukazuje doleva")}),
    10357: (LIST, {"t_ru": "личность, характер", "t_uk": "особистість, характер", "t_en": "personality, character",
                   "t_tr": "kişilik, karakter", "t_pl": "osobowość, charakter"}),
    16065: (LIST + " (было «объявление, упор»)", {
        "t_ru": "теракт, покушение", "t_uk": "теракт, замах", "t_en": "attack, assassination attempt",
        "t_tr": "saldırı, suikast", "t_pl": "zamach, atak", "t_it": "l'attentato", "t_fr": "l'attentat",
        "t_cs": "atentát, útok"}),
    2059: (EN, {"x_en": "Hand out the sheets"}),
}

REPLACE = [
    {"id": 13499, "by": 1123, "lang": "de", "why": "sämtlich — книжный вариант alle"},
    {"id": 13500, "by": 13496, "lang": "de", "why": "jenem — форма слова jener"},
]

SPLIT_LATER = {
    10356: ["locken = завивать (Haare locken)"],
    17516: ["umlegen (разг.) = убить"],
}
