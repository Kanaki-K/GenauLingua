"""Шаг 2, cs, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    6364: (T + "в примере přesně v", {"t_cs": "bod, tečka, (Punkt acht) přesně v osm"}),
    6382: (T + "в примере dát si napůl, не dělit se", {"x_cs": "Rozdělíme se o jednu pizzu?"}),
    6465: (T + "в примере držet se dál", {"t_cs": "daleko, (sich fernhalten) držet se dál"}),
    7464: (T + "в примере Na zdraví", {"t_cs": "dobro, blaho, (Zum Wohl!) Na zdraví!"}),
    10129: (T + "в примере глагол nezajímá", {"x_cs": "O fotbal nemám zájem"}),
    10266: (T + "в примере drama", {"t_cs": "dramatický, (dramatisch machen) dělat drama"}),
    12334: (T + "в примере kolečko", {"t_cs": "prohlídka, okruh, kolečko"}),
    13931: (T + "в примере pohovor", {"t_cs": "rozhovor, interview, pohovor"}),
    15518: (T + "в примере do chladu", {"t_cs": "chladný, odměřený, (kühl stellen) dát do chladu"}),
}

REPLACE = []
SPLIT_LATER = {}
