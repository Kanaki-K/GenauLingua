"""Шаг 2, it, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    16858: (T + "word in example", {"x_it": "Il fisco vuole vedere ancora le ricevute per il mio studio"}),
    17383: (T + "word in example", {"x_it": "Sfreccio al supermercato prima che chiuda"}),
}

REPLACE = []
SPLIT_LATER = {}
