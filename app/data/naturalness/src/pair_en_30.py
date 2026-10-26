"""Шаг 2, en, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    10471: (T + "tense", {"x_en": "The girls are shrieking with joy"}),
    10512: (T + "tense", {"x_en": "The girls are giggling behind me"}),
    10534: (T + "natural", {"x_en": "The family is mourning their late grandfather"}),
    10573: (T + "tense", {"x_en": "He's grinning at me"}),
    10610: (T + "word in example", {"t_en": "willingness, on-call duty, (Bereitschaft haben) to be on call"}),
    10614: (T + "word in example", {"t_en": "disaster, harm, misfortune"}),
    10700: (T + "word in example", {"x_en": "Only after the test did we have certainty: we're having a baby"}),
}

REPLACE = []
SPLIT_LATER = {}
