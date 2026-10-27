"""Шаг 2, cs, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    1327: (T + "в примере zřetelně", {"t_cs": "zřetelný, jasný, zřetelně"}),
    1440: (T + "в примере dobrovolně", {"t_cs": "dobrovolný, dobrovolně"}),
    1530: (T + "в примере Dále!", {"t_cs": "dovnitř, (Herein!) Dále!"}),
    1658: (T + "в примере dovezete", {"t_cs": "doručovat, dodávat, dovézt"}),
    1718: (T + "в примере poblíž", {"t_cs": "blízkost, okolí, (in der Nähe) poblíž"}),
    1769: (T + "в примере levně", {"t_cs": "levný, výhodný, levně"}),
    1867: (T + "в примере v bezpečí", {"t_cs": "bezpečnost, jistota, (in Sicherheit) v bezpečí"}),
    2036: (T + "в примере objednat se, не domluvit", {"x_cs": "Chtěl bych si domluvit termín u zubaře"}),
    2105: (T + "в примере ekonomie", {"t_cs": "ekonomika, hospodářství, ekonomie"}),
    2295: (T + "в примере нет obyvatelstvo", {"x_cs": "Na slavnosti bylo skoro celé obyvatelstvo vesnice"}),
    2494: (T + "в примере hrozně", {"t_cs": "strašný, příšerný, hrozně"}),
}

REPLACE = []
SPLIT_LATER = {}
