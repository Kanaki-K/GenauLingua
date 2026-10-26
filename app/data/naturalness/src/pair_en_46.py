"""Шаг 2, en, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    8633: (T + "word in example", {"t_en": "to devastate, to ravage, to wreck"}),
    8652: (T + "word in example", {"t_en": "frontal, head-on, (frontal unterrichten) to teach from the front"}),
    9926: (T + "word in example", {"t_en": "finder's reward, reward, finder's fee"}),
    11312: (T + "word in example", {"t_en": "disgusting, gross, repulsive"}),
    11383: (T + "word in example", {"x_en": "I'm such a klutz — I've tipped coffee all over my light trousers again"}),
}

REPLACE = []
SPLIT_LATER = {}
