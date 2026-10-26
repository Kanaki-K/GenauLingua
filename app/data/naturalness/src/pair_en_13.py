"""Шаг 2, en, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    2828: (T + "word in example", {"t_en": "worry, care, (keine Sorge) don't worry"}),
    2909: (T + "word in example", {"t_en": "dealing with, interaction, handling", "x_en": "Handling the new app is easier than I thought"}),
    2926: (T + "word in example", {"t_en": "injustice, wrong, (im Unrecht sein) to be wrong"}),
    2927: (T + "word in example", {"t_en": "conversation, entertainment, chat"}),
    3003: (T + "word in example", {"t_en": "to leave, to drive away, to go away"}),
    3039: (T + "word in example", {"t_en": "moment, point in time, timing"}),
}

REPLACE = []
SPLIT_LATER = {}
