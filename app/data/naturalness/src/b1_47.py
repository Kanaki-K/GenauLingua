"""B1, блок 47: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    7004: ("убрать пометку (fam.); " + LIST, {"t_ru": "металлолом, хлам", "t_uk": "металобрухт, мотлох",
                                             "t_fr": "la ferraille, la camelote", "t_it": "il rottame, la robaccia"}),
    10418: (LIST, {"t_en": "distraction, diversion", "t_tr": "dikkat dağıtma, kafa dağıtma",
                   "t_pl": "rozproszenie uwagi, rozrywka"}),
    7005: ("«eine grobe Beleidigung» — книжно; " + LIST, {
        "t_ru": "грубый, приблизительный", "t_uk": "грубий, приблизний", "t_en": "rude, rough", "t_tr": "kaba, kabaca",
        "t_pl": "grubiański, zgrubny", "t_it": "sgarbato, approssimativo", "t_es": "grosero, aproximado",
        "t_fr": "grossier, approximatif", "t_cs": "hrubý, přibližný",
        **all_x("Grob geschätzt kostet das 100 Euro", "Это стоит приблизительно 100 евро", "Це коштує приблизно 100 євро",
                "At a rough guess it costs 100 euros", "Kabaca tahminle 100 euro tutar", "Zgrubnie licząc, to kosztuje 100 euro",
                "A stima approssimativa costa 100 euro", "Cuesta aproximadamente 100 euros",
                "Ça coûte approximativement 100 euros", "Stojí to přibližně 100 eur")}),
    10419: ("убрать пометку (fam.)", {"t_fr": "paranoïaque, parano"}),
    7006: (EN + " («I suspect he'll come soon»)", {"x_en": "I assume he'll be here soon"}),
    8846: ("«Die Konferenz findet nächste Woche statt» — шаблон Kongress", {**all_x(
        "Ich bin die ganze Woche auf einer Konferenz in Wien", "Я всю неделю на конференции в Вене",
        "Я весь тиждень на конференції у Відні", "I'm at a conference in Vienna all week",
        "Bütün hafta Viyana'da bir konferanstayım", "Cały tydzień jestem na konferencji w Wiedniu",
        "Sono a una conferenza a Vienna tutta la settimana", "Estoy toda la semana en una conferencia en Viena",
        "Je suis à une conférence à Vienne toute la semaine", "Celý týden jsem na konferenci ve Vídni")}),
    8847: (LIST, {"t_ru": "занимать, тревожить", "t_uk": "займати, турбувати", "t_en": "to occupy, to concern",
                  "t_tr": "meşgul etmek, düşündürmek", "t_pl": "zajmować, zaprzątać", "t_it": "preoccupare, occupare",
                  "t_es": "preocupar, ocupar", "t_fr": "préoccuper, occuper", "t_cs": "zaměstnávat, trápit"}),
    11698: ("убрать пометку (hovor.)", {"t_cs": "slanina, špek"}),
    12576: (EN + " («sits in a wheelchair»)", {"x_en": "My grandad uses a wheelchair"}),
    9776: ("«Die Bezahlung erfolgt nach Abschluss der Arbeit» — договор", {**all_x(
        "Die Bezahlung ist hier echt schlecht", "Оплата здесь реально плохая", "Оплата тут справді погана",
        "The pay here is really bad", "Burada ücret gerçekten kötü", "Wynagrodzenie jest tu naprawdę kiepskie",
        "La paga qui è davvero bassa", "Aquí la paga es muy mala", "La paie est vraiment nulle ici",
        "Plat je tady fakt mizerný")}),
    2999: ("«Die Wärme der Sonne ist heute angenehm» — снова погода", {**all_x(
        "Sie strahlt so viel Wärme aus", "От неё исходит столько тепла", "Від неї йде стільки тепла",
        "She radiates so much warmth", "Etrafına o kadar çok sıcaklık yayıyor ki", "Emanuje z niej tyle ciepła",
        "Trasmette così tanto calore", "Transmite tanta calidez", "Elle dégage tellement de chaleur",
        "Vyzařuje z ní tolik vřelosti")}),
    2142: ("убрать пометку (fam.)", {"t_fr": "dépendant, accro"}),
    12578: ("«Der Arzt verschreibt eine Dosis von 500 mg» — рецепт", {**all_x(
        "Die Dosis macht das Gift", "Яд делает доза", "Отруту робить доза", "It's the dose that makes the poison",
        "Zehri yapan dozdur", "Dawka czyni truciznę", "È la dose che fa il veleno", "La dosis hace el veneno",
        "C'est la dose qui fait le poison", "Jed dělá dávka")}),
    17128: ("«Ich schiebe die Karre zum Markt» — пусто; убрать пометки (разг.)/(colloq.)/(fam.)/(hovor.)", {
        "t_ru": "развалюха, тачка", "t_uk": "драндулет, тачка", "t_en": "old banger, cart", "t_tr": "külüstür araba, el arabası",
        "t_pl": "gruchot, taczka", "t_it": "il macinino, il carretto", "t_es": "el carro, la carretilla",
        "t_fr": "la bagnole, la brouette", "t_cs": "kraksna, trakař",
        **all_x("Die alte Karre springt nicht an", "Эта старая развалюха не заводится", "Цей старий драндулет не заводиться",
                "The old banger won't start", "Külüstür araba çalışmıyor", "Stary gruchot nie chce zapalić",
                "Il vecchio macinino non parte", "El viejo carro no arranca", "La vieille bagnole ne démarre pas",
                "Ta stará kraksna nechce naskočit")}),
    7010: ("«Nichts hindert uns, unsere Ziele zu erreichen» — лозунг", {**all_x(
        "Der Lärm hindert mich am Schlafen", "Шум мешает мне спать", "Шум заважає мені спати",
        "The noise stops me from sleeping", "Gürültü uyumamı engelliyor", "Hałas przeszkadza mi spać",
        "Il rumore mi impedisce di dormire", "El ruido me impide dormir", "Le bruit m'empêche de dormir",
        "Hluk mi brání spát")}),
    2687: ("«Das war eine Niederlage» — пусто", {**all_x(
        "Nach der Niederlage war die Stimmung im Keller", "После поражения настроение было ниже плинтуса",
        "Після поразки настрій був на нулі", "After the defeat everyone was really down",
        "Yenilgiden sonra moraller bozuktu", "Po porażce nastroje były fatalne", "Dopo la sconfitta l'umore era a terra",
        "Tras la derrota el ánimo estaba por los suelos", "Après la défaite, le moral était au plus bas",
        "Po porážce byla nálada pod psa")}),
    17524: ("«Der Hacker versucht … zu hacken» — масло масляное; " + LIST, {
        "t_ru": "рубить, взламывать", "t_uk": "рубати, зламувати", "t_en": "to chop, to hack",
        "t_tr": "doğramak, bilgisayar korsanlığı yapmak", "t_pl": "siekać, włamywać się", "t_it": "tritare, hackerare",
        "t_es": "picar, hackear", "t_fr": "hacher, pirater", "t_cs": "sekat, hacknout",
        **all_x("Ich hacke die Zwiebeln klein", "Я мелко рублю лук", "Я дрібно січу цибулю", "I'm chopping the onions finely",
                "Soğanları ince ince doğruyorum", "Siekam drobno cebulę", "Trito finemente le cipolle",
                "Pico la cebolla muy fina", "Je hache les oignons finement", "Nasekám cibuli najemno")}),
    7011: ("«Sitz aufrecht und nicht gekrümmt» — так не говорят", {**all_x(
        "Sitz bitte aufrecht!", "Сиди, пожалуйста, прямо!", "Сиди, будь ласка, прямо!", "Sit up straight, please!",
        "Lütfen dik otur!", "Siedź, proszę, prosto!", "Stai seduto dritto, per favore!", "¡Siéntate derecho, por favor!",
        "Tiens-toi droit, s'il te plaît!", "Seď prosím zpříma!")}),
    15023: ("«Die Gestalt des Mannes war groß und schlank» — роман", {**all_x(
        "Im Nebel sehe ich eine dunkle Gestalt", "В тумане я вижу тёмную фигуру", "У тумані я бачу темну постать",
        "I can see a dark figure in the fog", "Siste karanlık bir siluet görüyorum", "We mgle widzę ciemną postać",
        "Nella nebbia vedo una figura scura", "En la niebla veo una figura oscura",
        "Dans le brouillard, je vois une silhouette sombre", "V mlze vidím tmavou postavu")}),
    10422: ("ru «Тебе не нужно так волноваться» — калька", {**all_x(
        "Reg dich doch nicht so auf!", "Не волнуйся ты так!", "Не хвилюйся ти так!", "Don't get so worked up!",
        "Bu kadar sinirlenme!", "Nie denerwuj się tak!", "Non agitarti così!", "¡No te alteres tanto!",
        "Ne t'énerve pas comme ça!", "Nerozčiluj se tak!")}),
    15487: (LIST, {"t_en": "rooster, tap"}),
    16122: ("«Die Armee erobert die Stadt» — учебник истории", {**all_x(
        "Er hat ihr Herz im Sturm erobert", "Он быстро покорил её сердце", "Він швидко підкорив її серце",
        "He won her heart in no time", "Kısa sürede onun gönlünü kazandı", "Szybko zdobył jej serce",
        "Ha conquistato il suo cuore in un attimo", "Conquistó su corazón enseguida",
        "Il a conquis son cœur en un rien de temps", "Hned si získal její srdce")}),
    1826: (LIST + " (было шесть значений)", {
        "t_ru": "купюра, видимость", "t_uk": "купюра, видимість", "t_en": "note, appearance", "t_tr": "banknot, görünüş",
        "t_pl": "banknot, pozór", "t_it": "la banconota, l'apparenza", "t_es": "el billete, la apariencia",
        "t_fr": "le billet, l'apparence", "t_cs": "bankovka, zdání"}),
    7013: ("наречие «точно» — у ряда A2 (325); здесь прилагательное", {
        "t_ru": "точный", "t_uk": "точний", "t_en": "exact, precise", "t_tr": "kesin, tam", "t_pl": "dokładny",
        "t_it": "esatto, preciso", "t_es": "exacto, preciso", "t_fr": "exact, précis", "t_cs": "přesný"}),
    10423: ("«Ihr Lächeln war bezaubernd» — претерит", {**all_x(
        "Was für ein bezauberndes kleines Dorf!", "Какая очаровательная деревушка!", "Яке чарівне селище!",
        "What a charming little village!", "Ne büyüleyici küçük bir köy!", "Co za urocza mała wioska!",
        "Che paesino incantevole!", "¡Qué pueblecito tan encantador!", "Quel charmant petit village!",
        "To je ale kouzelná vesnička!")}),
    10424: ("«Sie zeigte ihre Zuneigung …» — претерит", {**all_x(
        "Kinder brauchen viel Zuneigung", "Детям нужно много нежности", "Дітям потрібно багато ніжності",
        "Children need lots of affection", "Çocukların çok sevgiye ihtiyacı var", "Dzieci potrzebują dużo czułości",
        "I bambini hanno bisogno di tanto affetto", "Los niños necesitan mucho cariño",
        "Les enfants ont besoin de beaucoup d'affection", "Děti potřebují hodně něhy")}),
}

REPLACE = [{"id": 7014, "by": 6382, "lang": "de", "why": "geteilt — причастие от teilen"}]

SPLIT_LATER = {}
