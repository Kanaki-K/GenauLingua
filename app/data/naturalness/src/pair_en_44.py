"""Шаг 2, en, порция 44: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    17240: (T + "word in example", {"t_en": "to crash, to fall"}),
    17831: (T + "word in example", {"t_en": "left behind, stayed behind, lagging"}),
    18356: (T + "word in example", {"t_en": "leaky, not watertight, (undicht sein) to leak"}),
    18366: (T + "word in example", {"t_en": "back exit, back door, rear exit"}),
}

REPLACE = []
SPLIT_LATER = {}
