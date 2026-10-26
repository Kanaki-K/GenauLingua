"""Шаг 2, it, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    1279: (T + "word in example", {"x_it": "Il mio percorso formativo non è stato lineare: prima l'apprendistato, poi la maturità, poi l'università"}),
    1388: (T + "word in example", {"t_it": "il relax, il rilassamento, (zur Entspannung) per rilassarsi"}),
    1391: (T + "word in example", {"t_it": "venire a sapere, scoprire, sperimentare"}),
}

REPLACE = []
SPLIT_LATER = {}
