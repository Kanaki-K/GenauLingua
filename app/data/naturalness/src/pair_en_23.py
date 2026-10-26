"""Шаг 2, en, порция 23: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    15483: (T + "natural", {"x_en": "The frog is sitting on a leaf"}),
    15506: (T + "natural", {"x_en": "The sheep are grazing in the meadow"}),
    15536: (T + "unnatural idiom", {"x_en": "He's as clumsy as an elephant"}),
    15735: (T + "tense", {"x_en": "I've even let my cactus dry out"}),
    15852: (T + "natural", {"x_en": "The birds chirp in the morning"}),
}

REPLACE = []
SPLIT_LATER = {}
