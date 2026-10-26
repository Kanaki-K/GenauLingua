"""Шаг 2, en, порция 16: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    7869: (T + "word in example", {"t_en": "to hum, to grumble, to buzz"}),
    8679: (T + "word in example", {"t_en": "to want to go, to be off to"}),
    8838: (T + "word in example", {"t_en": "board, management, committee"}),
}

REPLACE = []
SPLIT_LATER = {}
