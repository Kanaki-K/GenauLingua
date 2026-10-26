"""Шаг 2, pl, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    10909: (T + "word in example", {"t_pl": "istnienie, egzystencja, życie"}),
    10971: (T + "word in example", {"t_pl": "paniczny, w panice"}),
    10975: (T + "word in example", {"t_pl": "nieustraszony, bez strachu"}),
}

REPLACE = []
SPLIT_LATER = {}
