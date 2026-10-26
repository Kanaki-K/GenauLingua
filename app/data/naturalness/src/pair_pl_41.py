"""Шаг 2, pl, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    11895: (T + "word in example", {"t_pl": "nalewać, dolewać, dolać"}),
    12759: (T + "word in example", {"t_pl": "zatrzymanie akcji serca, zatrzymanie serca, (fast Herzstillstand) serce prawie staje"}),
    12778: (T + "word in example", {"t_pl": "załamać się, runąć, zawalić się"}),
    12808: (T + "word in example", {"t_pl": "chrząkanie, odchrząkiwanie, chrząknięcie"}),
}

REPLACE = []
SPLIT_LATER = {}
