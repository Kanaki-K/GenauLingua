"""Шаг 2, en, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    15253: (T + "natural", {"x_en": "My maid of honour forgot the rings at the registry office, so we used two jelly bears"}),
    15291: (T + "word in example", {"t_en": "companion, escort, chaperone"}),
    15549: (T + "word in example", {"x_en": "In the forest we saw a big stag"}),
    15878: (T + "word in example", {"t_en": "chestnut, conker"}),
    16262: (T + "word in example", {"x_en": "For the destruction of the old files a company is coming with a big shredder"}),
}

REPLACE = []
SPLIT_LATER = {}
