"""Шаг 2, pl, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    8909: (T + "word in example", {"t_pl": "czynny, pracujący, (tätig sein als) pracować jako"}),
    8956: (T + "word in example", {"t_pl": "wlec, zawlec, szlifować"}),
    9514: (T + "word in example", {"t_pl": "uświadamianie, wyjaśnienie, (Aufklärungsunterricht) lekcja uświadamiająca"}),
}

REPLACE = []
SPLIT_LATER = {}
