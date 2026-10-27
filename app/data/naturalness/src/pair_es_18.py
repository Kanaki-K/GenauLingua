"""Шаг 2, es, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    10022: (T + "word in example", {"t_es": "lo siento, (es tut mir leid, dass) siento"}),
    10048: (T + "word in example", {"t_es": "honesto, sincero, sinceramente"}),
    10220: (T + "word in example", {"t_es": "bueno, obediente, (brav sein) portarse bien"}),
    10281: (T + "word in example", {"t_es": "llorar, lloriquear, aullar"}),
    10302: (T + "word in example", {"t_es": "el luto, el duelo, la tristeza"}),
    10337: (T + "word in example", {"t_es": "curioso, tenso, (gespannt sein) tener curiosidad"}),
    10387: (T + "word in example", {"t_es": "inseguro, dudoso, (unsicher sein) no estar seguro"}),
    10409: (T + "word in example", {"t_es": "envidioso, celoso, (neidisch sein) tener envidia"}),
}

REPLACE = []
SPLIT_LATER = {}
