"""Шаг 2, en, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    6364: (T + "word in example", {"t_en": "point, full stop, (Punkt acht) on the dot"}),
    6401: (T + "word in example", {"t_en": "to resemble, to be like, to be the spitting image of"}),
    6499: (T + "word in example", {"t_en": "operation, use, call-out"}),
    7464: (T + "word in example", {"t_en": "good, well-being, (zum Wohl!) cheers"}),
    13384: (T + "word in example", {"t_en": "(passive auxiliary) been, was"}),
    13446: (T + "word in example", {"t_en": "because of that, that way, from that"}),
    14035: (T + "word in example", {"t_en": "here you are, you're welcome, there you go"}),
    15929: (T + "word in example", {"t_en": "victim, sacrifice, casualty"}),
}

REPLACE = []
SPLIT_LATER = {}
