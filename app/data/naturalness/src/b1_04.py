"""B1, блок 4: следующие 40 по частоте (после 120). Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Das Gebäude ist alt», «Das Gesetz ist streng») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    9440: (EN, {"x_en": "The professor is explaining the task"}),
    6366: ("«Das ist wunderschön» — пусто", {**all_x(
        "Du siehst heute wunderschön aus", "Ты сегодня прекрасно выглядишь", "Ти сьогодні чудово виглядаєш",
        "You look beautiful today", "Bugün çok güzel görünüyorsun", "Wyglądasz dziś przepięknie", "Oggi sei bellissima",
        "Hoy estás preciosa", "Tu es magnifique aujourd'hui", "Dneska vypadáš nádherně")}),
    1273: (LIST, {"t_ru": "двигать, двигаться", "t_uk": "рухати, рухатися", "t_en": "to move", "t_tr": "hareket ettirmek",
                  "t_pl": "poruszać, ruszać się", "t_it": "muovere, muoversi", "t_es": "mover, moverse",
                  "t_fr": "bouger, déplacer", "t_cs": "hýbat, pohnout"}),
    13407: ("pl — порядок «ани я, ани ты» не тот; ru — «этого» после глагола", {
        "t_en": "neither", "x_ru": "Ни ты, ни я этого не знаем", "x_pl": "Ani ty, ani ja tego nie wiemy",
        "x_en": "Neither you nor I know that"}),
    1396: (EN + "; " + LIST, {
        "t_ru": "сделать, уладить", "t_uk": "зробити, упоратися", "t_en": "to take care of, to get done",
        "t_tr": "halletmek", "t_pl": "załatwić", "t_it": "sbrigare, sistemare", "t_es": "hacer, encargarse de",
        "t_fr": "régler, s'occuper de", "t_cs": "vyřídit, zařídit",
        "x_en": "I've still got to sort something out quickly"}),
    6369: ("«Die Stadt ist weit entfernt» — пусто; " + LIST, {
        "t_ru": "далёкий, на расстоянии", "t_uk": "далекий, на відстані", "t_en": "away, distant",
        "t_tr": "uzak, uzaklıkta", "t_pl": "odległy, oddalony",
        **all_x("Der Bahnhof ist nur zehn Minuten entfernt", "Вокзал всего в десяти минутах отсюда",
                "Вокзал лише за десять хвилин звідси", "The station is only ten minutes away",
                "İstasyon sadece on dakika uzaklıkta", "Dworzec jest tylko dziesięć minut stąd",
                "La stazione è a soli dieci minuti", "La estación está a solo diez minutos",
                "La gare est à dix minutes seulement", "Nádraží je jen deset minut odsud")}),
    6370: (LIST, {"t_ru": "очевидно, явно", "t_uk": "очевидно, явно", "t_en": "obviously, clearly",
                  "t_tr": "belli ki, apaçık", "t_pl": "najwyraźniej, ewidentnie", "t_it": "evidentemente, ovviamente",
                  "t_es": "evidentemente, obviamente", "t_fr": "manifestement, évidemment", "t_cs": "zjevně, očividně"}),
    1906: (LIST, {"t_ru": "вставлять, торчать", "t_uk": "вставляти, застрягти", "t_en": "to put in, to be stuck",
                  "t_tr": "sokmak, takılı kalmak", "t_pl": "wkładać, tkwić", "t_it": "infilare, mettere",
                  "t_es": "meter, estar metido", "t_fr": "mettre, enfoncer", "t_cs": "strčit, vězet"}),
    15942: ("«Er ist schuldig» — пусто; «должен (денег)» — другое значение, своя строка", {
        "t_ru": "виноватый, виновный", "t_uk": "винний", "t_en": "guilty", "t_tr": "suçlu", "t_pl": "winny",
        "t_it": "colpevole", "t_es": "culpable", "t_fr": "coupable", "t_cs": "vinný",
        **all_x("Ich fühle mich schuldig", "Я чувствую себя виноватым", "Я почуваюся винним", "I feel guilty",
                "Kendimi suçlu hissediyorum", "Czuję się winny", "Mi sento colpevole", "Me siento culpable",
                "Je me sens coupable", "Cítím se vinný")}),
    1981: ("«Das ist eine Überraschung» — пусто", {**all_x(
        "Was für eine Überraschung, dass du hier bist!", "Какой сюрприз, что ты здесь!", "Який сюрприз, що ти тут!",
        "What a surprise to see you here!", "Seni burada görmek ne sürpriz!", "Co za niespodzianka, że tu jesteś!",
        "Che sorpresa vederti qui!", "¡Qué sorpresa verte aquí!", "Quelle surprise de te voir ici!",
        "To je překvapení, že jsi tady!")}),
    15943: ("«Die Königin ist sehr elegant» — пусто", {**all_x(
        "Die englische Königin war sehr beliebt", "Английскую королеву очень любили", "Англійську королеву дуже любили",
        "The English queen was very popular", "İngiliz kraliçesi çok sevilirdi", "Angielska królowa była bardzo lubiana",
        "La regina inglese era molto amata", "La reina inglesa era muy querida", "La reine d'Angleterre était très aimée",
        "Anglická královna byla velmi oblíbená")}),
    6377: ("«Wir müssen das überleben» — так не говорят", {**all_x(
        "Nur zwei Leute haben den Unfall überlebt", "В аварии выжили только два человека", "В аварії вижили лише двоє людей",
        "Only two people survived the accident", "Kazada sadece iki kişi hayatta kaldı", "Wypadek przeżyły tylko dwie osoby",
        "Solo due persone sono sopravvissute all'incidente", "Solo dos personas sobrevivieron al accidente",
        "Seules deux personnes ont survécu à l'accident", "Nehodu přežili jen dva lidé")}),
    2573: ("ru «участвую в работе» — канцелярски; en «by participating» — книжно", {
        "x_ru": "Я помогаю тем, что работаю вместе со всеми", "x_en": "I help by joining in"}),
    17057: (LIST, {"t_ru": "борт", "t_uk": "борт", "t_en": "board (ship, plane)", "t_tr": "güverte", "t_pl": "pokład"}),
    2803: ("«Ich schütze die Natur» — лозунг", {**all_x(
        "Zieh eine Mütze an, die schützt vor der Kälte", "Надень шапку, она защитит от холода",
        "Вдягни шапку, вона захистить від холоду", "Put a hat on, it'll protect you from the cold",
        "Bere tak, seni soğuktan korur", "Załóż czapkę, ochroni cię przed zimnem",
        "Mettiti un berretto, ti protegge dal freddo", "Ponte un gorro, te protegerá del frío",
        "Mets un bonnet, ça te protégera du froid", "Vezmi si čepici, ochrání tě před zimou")}),
    15945: (SKEL, {**all_x(
        "Das ist gegen das Gesetz", "Это противозаконно", "Це суперечить закону", "That's against the law",
        "Bu kanuna aykırı", "To jest niezgodne z prawem", "È contro la legge", "Eso va contra la ley",
        "C'est contraire à la loi", "To je proti zákonu")}),
    314: (SKEL, {**all_x(
        "In welchem Gebäude ist das Büro?", "В каком здании офис?", "У якій будівлі офіс?",
        "Which building is the office in?", "Ofis hangi binada?", "W którym budynku jest biuro?",
        "In quale edificio è l'ufficio?", "¿En qué edificio está la oficina?", "Le bureau est dans quel bâtiment?",
        "Ve které budově je kancelář?")}),
    10109: ("«Я за тебя обеспокоен» — книжно", {"x_ru": "Я за тебя беспокоюсь", "x_uk": "Я за тебе хвилююся"}),
}

SPLIT_LATER = {
    15942: ["schuldig sein = быть должным (Ich bin dir zehn Euro schuldig)"],
}
