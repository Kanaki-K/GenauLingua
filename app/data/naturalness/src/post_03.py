"""После прохода, блок 3: указания-замены, которые ведут на выключенную строку.
Два круга (unterbringen B2↔C1, bezweifeln B1↔C1 — обе строки пропадали у людей)
и четыре цепочки (anderes→anderer→andere, guck→gucken B1→gucken A2,
leuchtend C2→leuchtend B1→leuchten, Checkpoint→Kontrolle B2→Kontrolle B1). 22.10."""

LIST = "список → главное слово и не больше одной альтернативы"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18268: ("строка снова самостоятельна; пример в пассиве состояния; " + LIST, {
        "t_ru": "разместить, поселить", "t_uk": "розмістити, поселити", "t_en": "to put up, to accommodate", "t_tr": "yerleştirmek, misafir etmek", "t_pl": "przenocować, zakwaterować",
        "t_it": "ospitare, sistemare", "t_es": "alojar, hospedar", "t_fr": "loger, héberger", "t_cs": "ubytovat, umístit",
        **all_x("Zur Hochzeit bringen wir die Verwandten aus Polen bei den Nachbarn unter",
                "На свадьбу мы размещаем родственников из Польши у соседей",
                "На весілля ми розміщуємо родичів із Польщі в сусідів",
                "For the wedding we're putting up the relatives from Poland at the neighbours'",
                "Düğün için Polonya'dan gelen akrabaları komşulara yerleştiriyoruz",
                "Na wesele przenocujemy krewnych z Polski u sąsiadów",
                "Per il matrimonio sistemiamo i parenti dalla Polonia dai vicini",
                "Para la boda alojamos a los parientes de Polonia en casa de los vecinos",
                "Pour le mariage, on loge la famille venue de Pologne chez les voisins",
                "Na svatbu ubytujeme příbuzné z Polska u sousedů")}),
    10259: ("строка снова самостоятельна; " + LIST, {
        "t_ru": "сомневаться", "t_uk": "сумніватися", "t_en": "to doubt", "t_tr": "şüphe etmek", "t_pl": "wątpić",
        "t_it": "dubitare", "t_es": "dudar", "t_fr": "douter", "t_cs": "pochybovat",
        **all_x("Ich bezweifle, dass der Bus bei diesem Schnee pünktlich kommt",
                "Сомневаюсь, что автобус придёт вовремя в такой снег",
                "Сумніваюся, що автобус прийде вчасно в такий сніг",
                "I doubt the bus will be on time in this snow",
                "Bu karda otobüsün zamanında geleceğinden şüpheliyim",
                "Wątpię, żeby autobus przyjechał punktualnie w taki śnieg",
                "Dubito che l'autobus arrivi puntuale con questa neve",
                "Dudo que el autobús llegue puntual con esta nieve",
                "Je doute que le bus arrive à l'heure avec cette neige",
                "Pochybuju, že autobus v tomhle sněhu přijede načas")}),
}

UNREPLACE = [
    {"id": 18268, "why": "старое «untergebracht — форма от unterbringen»: строка давно переименована в unterbringen"},
    {"id": 10259, "why": "старое «bezweifle — форма от bezweifeln»: строка давно переименована в bezweifeln"},
]

REPLACE = [
    {"id": 6256, "by": 21, "lang": "de", "why": "цепочка: anderes → anderer → andere, ведём прямо на andere"},
    {"id": 6388, "by": 8448, "lang": "de", "why": "цепочка: guck → gucken B1 → gucken A2"},
    {"id": 8519, "by": 7134, "lang": "de", "why": "цепочка: leuchtend C2 → leuchtend B1 → leuchten"},
    {"id": 16933, "by": 502, "lang": "de", "why": "цепочка: Checkpoint → Kontrolle B2 → Kontrolle B1"},
]

SPLIT_LATER = {}
