"""Шаг 2, it, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    11737: (T + "word in example", {"t_it": "la bibita, la gazzosa"}),
    12181: (T + "word in example", {"t_it": "il cambiamento, il diversivo, (zur Abwechslung) per cambiare"}),
    12662: (T + "word in example", {"t_it": "lo svenimento, l'impotenza, (in Ohnmacht fallen) svenire"}),
    12674: (T + "word in example", {"t_it": "il respiro, (in einem Atemzug) d'un fiato"}),
}

REPLACE = []
SPLIT_LATER = {}
