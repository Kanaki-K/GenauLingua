"""Шаг 2, es, порция 44: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    17240: (T + "в примере caer al vacío", {"t_es": "colgarse, estrellarse, caer al vacío"}),
}

REPLACE = []
SPLIT_LATER = {}
