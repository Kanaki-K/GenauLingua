"""Шаг 2, en, порция 37: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    17732: (T + "word in example", {"x_en": "The recovery of the deleted holiday photos cost me a whole weekend"}),
    17814: (T + "word in example", {"t_en": "to contribute, to bring in, to make use of (experience)"}),
    17857: (T + "word in example", {"x_en": "My business partner and I run the business together"}),
    17868: (T + "word in example", {"x_en": "Since the founding of our choir twenty years ago my mum hasn't missed a single rehearsal"}),
}

REPLACE = []
SPLIT_LATER = {}
