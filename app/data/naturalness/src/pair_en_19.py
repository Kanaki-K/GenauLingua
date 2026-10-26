"""Шаг 2, en, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    10448: (T + "word in example", {"t_en": "pity, misery, shame"}),
    11594: (T + "word in example", {"t_en": "guilt, feeling of guilt, (Schuldgefühle haben) to feel guilty"}),
    11705: (T + "word in example", {"t_en": "feed, lining, food (for animals)"}),
}

REPLACE = []
SPLIT_LATER = {}
