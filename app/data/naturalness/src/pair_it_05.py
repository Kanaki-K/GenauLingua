"""Шаг 2, it, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    1232: (T + "word in example", {"t_it": "finire, terminare, chiudere"}),
    1327: (T + "word in example", {"t_it": "chiaro, nitido, chiaramente"}),
    1440: (T + "word in example", {"t_it": "volontario, volontariamente"}),
    1530: (T + "word in example", {"t_it": "dentro, (herein!) avanti!"}),
    1537: (T + "word in example", {"t_it": "là, (hin und zurück) andata e ritorno"}),
    1737: (T + "word in example", {"t_it": "usare, sfruttare, approfittare"}),
    1867: (T + "word in example", {"t_it": "la sicurezza, la certezza, (in Sicherheit) al sicuro"}),
    2492: (T + "word in example", {"t_it": "condurre, guidare, portare"}),
    2684: (T + "word in example", {"t_it": "nebbioso, con nebbia, (es ist neblig) c'è nebbia"}),
}

REPLACE = []
SPLIT_LATER = {}
