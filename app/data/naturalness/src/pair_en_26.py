"""Шаг 2, en, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    7088: (T + "word in example", {"t_en": "to break into, to penetrate, to get into"}),
    18263: (T + "natural", {"x_en": "The washing is drying in the sun"}),
    18389: (T + "word in example", {"t_en": "move-in, entry, moving in"}),
    18641: (T + "natural", {"x_en": "You're constantly disturbing me"}),
    18818: (T + "word in example", {"t_en": "to wipe off, to wipe down, to wipe away"}),
    18820: (T + "word in example", {"t_en": "quick, on the double, (dalli!) hurry up"}),
}

REPLACE = []
SPLIT_LATER = {}
