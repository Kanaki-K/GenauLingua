"""Шаг 2, it, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    10565: (T + "natural", {"x_it": "Questa chitarra nuova è proprio figa"}),
    10595: (T + "word in example", {"t_it": "rispondere di, assumersi la responsabilità di"}),
    10610: (T + "word in example", {"x_it": "Mio marito nel fine settimana è di reperibilità e forse deve andare in clinica"}),
    10734: (T + "word in example", {"t_it": "affettuoso, amorevole, affettuosamente"}),
}

REPLACE = []
SPLIT_LATER = {}
