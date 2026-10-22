"""После прохода, блок 1: одно слово в двух-трёх рядах на разных уровнях.
Значение одно — остаётся нижний уровень, верхний выключается в его пользу.
Разные значения (erhaben C1 «выше чего-то» / C2 «величественный») — оба остаются. 22.10."""

LIST = "список → главное слово и не больше одной альтернативы"
DUP = "дубль слова на другом уровне"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    10384: ("пример-пустышка; C2-двойник 11525 выключается; " + LIST, {
        "t_ru": "искренний, честный", "t_uk": "щирий, чесний", "t_en": "sincere, genuine", "t_tr": "samimi, içten", "t_pl": "szczery, uczciwy",
        **all_x("Ich habe mich über seine aufrichtige Entschuldigung wirklich gefreut",
                "Я по-настоящему обрадовался его искреннему извинению",
                "Я справді зрадів його щирому вибаченню",
                "I was really pleased by his sincere apology",
                "Samimi özrüne gerçekten sevindim",
                "Naprawdę ucieszyły mnie jego szczere przeprosiny",
                "Le sue scuse sincere mi hanno fatto davvero piacere",
                "Su disculpa sincera me alegró de verdad",
                "Ses excuses sincères m'ont vraiment fait plaisir",
                "Jeho upřímná omluva mě opravdu potěšila")}),
    6657: ("пример-пустышка; C1-двойник 7991 выключается", {
        **all_x("Mein Onkel ist im ganzen Dorf berühmt für seinen Apfelkuchen",
                "Мой дядя знаменит на всю деревню своим яблочным пирогом",
                "Мій дядько славиться на все село своїм яблучним пирогом",
                "My uncle is famous in the whole village for his apple cake",
                "Amcam elmalı pastasıyla bütün köyde ünlü",
                "Mój wujek słynie w całej wsi ze swojej szarlotki",
                "Mio zio è famoso in tutto il paese per la sua torta di mele",
                "Mi tío es famoso en todo el pueblo por su tarta de manzana",
                "Mon oncle est célèbre dans tout le village pour sa tarte aux pommes",
                "Strýc je v celé vesnici slavný svým jablečným koláčem")}),
    502: ("«Die Kontrolle ist wichtig» — пусто; B2-двойник 16546 выключается; " + LIST, {
        "t_ru": "проверка, контроль", "t_uk": "перевірка, контроль", "t_en": "check, control", "t_pl": "kontrola",
        "t_es": "el control, la revisión", "t_fr": "le contrôle",
        **all_x("Bei der Kontrolle im Bus habe ich zum Glück meine Monatskarte dabei",
                "При проверке в автобусе у меня, к счастью, с собой проездной",
                "Під час перевірки в автобусі в мене, на щастя, з собою проїзний",
                "Luckily I've got my monthly pass on me when they check tickets on the bus",
                "Otobüsteki kontrolde neyse ki aylık kartım yanımda",
                "Przy kontroli w autobusie mam na szczęście bilet miesięczny",
                "Al controllo sull'autobus per fortuna ho con me l'abbonamento",
                "En el control del autobús por suerte llevo el abono mensual",
                "Au contrôle dans le bus, j'ai heureusement mon abonnement sur moi",
                "Při kontrole v autobuse mám naštěstí u sebe měsíční jízdenku")}),
    1870: ("«Die Preise sinken» — пусто; C1-двойник 7922 выключается; " + LIST, {
        "t_ru": "падать, снижаться, тонуть", "t_uk": "падати, знижуватися, тонути", "t_en": "to fall, to sink", "t_tr": "düşmek, batmak", "t_pl": "spadać, tonąć",
        "t_it": "calare, affondare", "t_es": "bajar, hundirse", "t_fr": "baisser, couler", "t_cs": "klesat, potápět se",
        **all_x("Im Oktober sinken die Temperaturen nachts schon unter null",
                "В октябре ночью температура уже опускается ниже нуля",
                "У жовтні вночі температура вже опускається нижче нуля",
                "In October the temperature already falls below zero at night",
                "Ekimde geceleri sıcaklık şimdiden sıfırın altına düşüyor",
                "W październiku temperatura w nocy spada już poniżej zera",
                "A ottobre di notte le temperature calano già sotto lo zero",
                "En octubre las temperaturas bajan ya de cero por la noche",
                "En octobre, les températures baissent déjà sous zéro la nuit",
                "V říjnu teploty v noci klesají už pod nulu")}),
    8321: ("в примере «das Erhabene» (сущ.); значение отлично от erhaben 11241 C1 — оба остаются; " + LIST, {
        "t_ru": "величественный, возвышенный", "t_uk": "величний, піднесений", "t_en": "majestic, sublime", "t_tr": "görkemli, yüce", "t_pl": "majestatyczny, wzniosły",
        "t_it": "maestoso, sublime", "t_es": "majestuoso, sublime", "t_fr": "majestueux, sublime", "t_cs": "majestátní, vznešený",
        **all_x("Der Blick vom Gipfel auf die verschneiten Alpen ist einfach erhaben",
                "Вид с вершины на заснеженные Альпы просто величественный",
                "Краєвид з вершини на засніжені Альпи просто величний",
                "The view from the summit over the snowy Alps is simply majestic",
                "Zirveden karlı Alplerin manzarası tek kelimeyle görkemli",
                "Widok ze szczytu na zaśnieżone Alpy jest po prostu majestatyczny",
                "La vista dalla cima sulle Alpi innevate è semplicemente maestosa",
                "La vista desde la cumbre sobre los Alpes nevados es sencillamente majestuosa",
                "La vue du sommet sur les Alpes enneigées est tout simplement majestueuse",
                "Výhled z vrcholu na zasněžené Alpy je prostě majestátní")}),
}

REPLACE = [
    {"id": 11525, "by": 10384, "lang": "de", "why": DUP + ": aufrichtig C2 → B1"},
    {"id": 7991, "by": 6657, "lang": "de", "why": DUP + ": berühmt C1 → A2"},
    {"id": 18792, "by": 6449, "lang": "de", "why": DUP + ": dringend C1 → A2"},
    {"id": 13464, "by": 194, "lang": "de", "why": DUP + ": dritte A2 → A1"},
    {"id": 13515, "by": 194, "lang": "de", "why": DUP + ": dritter B1 → dritte A1"},
    {"id": 18782, "by": 2420, "lang": "de", "why": DUP + ": Ereignis B2 → B1"},
    {"id": 16987, "by": 16936, "lang": "de", "why": DUP + ": Gesandte C2 → C1"},
    {"id": 16509, "by": 16890, "lang": "de", "why": DUP + ": Geschworene C1 → B2"},
    {"id": 11097, "by": 10394, "lang": "de", "why": DUP + ": gruselig C1 → B1"},
    {"id": 9273, "by": 9006, "lang": "de", "why": DUP + ": Kaufmann C2 → A2"},
    {"id": 8466, "by": 7965, "lang": "de", "why": DUP + ": konstant C2 → C1"},
    {"id": 16546, "by": 502, "lang": "de", "why": DUP + ": Kontrolle B2 → B1"},
    {"id": 13727, "by": 572, "lang": "de", "why": DUP + ": Mantel C1 → A2"},
    {"id": 8794, "by": 1761, "lang": "de", "why": DUP + ": Pilot B1 → A2"},
    {"id": 16406, "by": 16268, "lang": "de", "why": DUP + ": Privilegien (мн. ч.) C1 → Privileg B2"},
    {"id": 16414, "by": 16318, "lang": "de", "why": DUP + ": Scharfschütze C1 → B2"},
    {"id": 7922, "by": 1870, "lang": "de", "why": DUP + ": sinken C1 → B1"},
    {"id": 8371, "by": 7749, "lang": "de", "why": DUP + ": stolpern C2 → C1"},
    {"id": 11601, "by": 10564, "lang": "de", "why": DUP + ": unverschämt C2 → B2"},
    {"id": 16690, "by": 16594, "lang": "de", "why": DUP + ": zivil C2 → C1"},
]

SPLIT_LATER = {}
