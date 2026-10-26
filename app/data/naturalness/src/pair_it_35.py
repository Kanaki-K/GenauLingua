"""Шаг 2, it, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    15575: (T + "word in example", {"t_it": "il bufalo, (Büffelmilch) il latte di bufala"}),
    16190: (T + "word in example", {"t_it": "interrogare, (sich verhören) capire male"}),
    16213: (T + "word in example", {"t_it": "a vita, (lebenslänglich bekommen) l'ergastolo"}),
}

REPLACE = []
SPLIT_LATER = {}
