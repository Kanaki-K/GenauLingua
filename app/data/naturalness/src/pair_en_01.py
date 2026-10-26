"""Шаг 2, en, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    45: (T + "natural", {"x_en": "She takes the baby in her arms"}),
    69: (T + "word in example", {"t_en": "to bathe, to take a bath, to swim"}),
    185: (T + "natural", {"x_en": "I'll give you the book"}),
    187: (T + "word in example", {"t_en": "but, after all"}),
    235: (T + "natural", {"x_en": "Adults only"}),
    295: (T + "word in example", {"t_en": "in the past, earlier, used to"}),
    364: (T + "word in example", {"t_en": "cheap, good value, reasonable", "x_en": "The price is very reasonable"}),
    416: (T + "word in example", {"t_en": "hunger, (Hunger haben) to be hungry"}),
}

REPLACE = []
SPLIT_LATER = {}
