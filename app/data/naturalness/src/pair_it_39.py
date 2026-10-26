"""Шаг 2, it, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    7762: (T + "word in example", {"x_it": "Al cinema mia figlia vuole sempre sedersi nelle file anteriori, e poi le fa male il collo"}),
    7790: (T + "word in example", {"t_it": "la rotazione, il giro, la piroetta"}),
    7851: (T + "word in example", {"t_it": "unanime, all'unanimità"}),
    7926: (T + "word in example", {"t_it": "la circostanza, il disturbo, (Umstände machen) disturbarsi"}),
    7963: (T + "word in example", {"t_it": "la scorta, l'accompagnamento, (das letzte Geleit) accompagnare nell'ultimo viaggio"}),
    7965: (T + "word in example", {"t_it": "costante, stabile, costantemente"}),
}

REPLACE = []
SPLIT_LATER = {}
