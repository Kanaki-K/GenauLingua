"""Шаг 2, en, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    10035: (T + "word in example", {"t_en": "devil, demon, (zum Teufel) the hell"}),
    10294: (T + "word in example", {"t_en": "mistake, error, (im Irrtum sein) to be mistaken"}),
    10311: (T + "word in example", {"t_en": "to deceive, to be mistaken, to fool"}),
    10324: (T + "word in example", {"t_en": "sorrow, trouble, worry"}),
    10339: (T + "word in example", {"x_en": "That's just cowardly of you"}),
    10349: (T + "word in example", {"x_en": "At Christmas the whole family is united"}),
    10387: (T + "word in example", {"t_en": "unsure, unsafe, uncertain"}),
}

REPLACE = []
SPLIT_LATER = {}
