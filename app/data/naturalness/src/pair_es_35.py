"""Шаг 2, es, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    15297: (T + "word in example", {"t_es": "la punta de los pies, (auf Zehenspitzen) de puntillas"}),
    16190: (T + "word in example", {"t_es": "interrogar, (sich verhören) oír mal"}),
    16213: (T + "word in example", {"t_es": "de por vida, perpetuo, (lebenslänglich bekommen) la cadena perpetua"}),
}

REPLACE = []
SPLIT_LATER = {}
