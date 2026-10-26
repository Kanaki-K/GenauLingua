"""Шаг 2, pl, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    14058: (T + "word in example", {"t_pl": "dostępny, osiągalny, (nicht erreichbar) nieosiągalny"}),
    14221: (T + "word in example", {"t_pl": "rozmowa z samym sobą, (Selbstgespräche führen) rozmawiać ze sobą"}),
}

REPLACE = []
SPLIT_LATER = {}
