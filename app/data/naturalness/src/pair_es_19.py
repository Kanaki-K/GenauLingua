"""Шаг 2, es, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    10607: (T + "word in example", {"t_es": "el reproche, la acusación, (Vorwürfe machen) reprochar"}),
    11854: (T + "word in example", {"x_es": "En el huerto de la abuela crece col"}),
    11891: (T + "word in example", {"t_es": "el refresco, el refrigerio, (zur Erfrischung) para refrescarse"}),
}

REPLACE = []
SPLIT_LATER = {}
