"""Шаг 2, en, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    1396: (T + "word in example", {"t_en": "to take care of, to get done, to sort out"}),
    1429: (T + "tense", {"x_en": "He's been flirting with her all evening"}),
    1669: (T + "word in example", {"t_en": "estate agent, agent, broker"}),
    1754: (T + "natural", {"x_en": "The HR manager wants to have a word with me"}),
}

REPLACE = []
SPLIT_LATER = {}
