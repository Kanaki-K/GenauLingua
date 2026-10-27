"""Шаг 2, es, порция 16: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    8380: (T + "word in example", {"t_es": "agradecido, (sich erkenntlich zeigen) demostrar lo agradecido que uno está"}),
    8789: (T + "word in example", {"t_es": "configurar, ajustar, contratar"}),
}

REPLACE = []
SPLIT_LATER = {}
