"""Шаг 2, en, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    11519: (T + "word in example", {"t_en": "brave, (sich wacker halten) to put up a brave show"}),
    12333: (T + "word in example", {"t_en": "Olympics, Olympic Games, olympiad"}),
    12357: (T + "word in example", {"t_en": "firing range, firing line, shooting distance"}),
    12966: (T + "word in example", {"t_en": "suicide, would-be suicide, (ein Selbstmörder sein) to be suicidal"}),
    13029: (T + "word in example", {"t_en": "pathogen, bug, causative agent"}),
    13146: (T + "word in example", {"t_en": "unwell, indisposed, under the weather"}),
}

REPLACE = []
SPLIT_LATER = {}
