"""Шаг 2, en, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    98: (T + "word in example", {"t_en": "notice, answer, (Bescheid sagen) to let someone know"}),
    214: (T + "word in example", {"t_en": "agreed, okay, (einverstanden sein) to agree"}),
    268: (T + "word in example", {"t_en": "party, celebration, festival"}),
    757: (T + "word in example", {"t_en": "pensioner, retiree, (Rentner sein) to be retired"}),
    801: (T + "natural", {"x_en": "I've got a pain in my knee"}),
    941: (T + "word in example", {"t_en": "to meet, to bump into"}),
    1064: (T + "word in example", {"t_en": "to wish, to want, (sich wünschen) would like"}),
    1074: (T + "word in example", {"t_en": "note, slip of paper, piece of paper"}),
    1136: (T + "word in example", {"t_en": "fear, (Angst haben) to be afraid"}),
}

REPLACE = []
SPLIT_LATER = {}
