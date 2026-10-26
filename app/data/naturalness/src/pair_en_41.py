"""Шаг 2, en, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    11059: (T + "word in example", {"t_en": "gloom, the blues, (Trübsal blasen) to mope"}),
    12792: (T + "word in example", {"x_en": "Three weeks without sun every February really affect my mum's psyche"}),
}

REPLACE = []
SPLIT_LATER = {}
