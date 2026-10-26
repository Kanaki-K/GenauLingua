"""Шаг 2, en, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    12219: (T + "word in example", {"t_en": "drawn, undecided, a draw"}),
    12471: (T + "word in example", {"t_en": "sore, hurting, (weh tun) to hurt"}),
    12503: (T + "natural", {"x_en": "He fractured his skull"}),
    12558: (T + "word in example", {"x_en": "You need to come on an empty stomach for the blood test"}),
}

REPLACE = []
SPLIT_LATER = {}
