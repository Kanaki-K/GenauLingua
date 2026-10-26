"""Шаг 2, en, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    16846: (T + "word in example", {"t_en": "censorship, (school) mark, grade"}),
    16881: (T + "word in example", {"t_en": "to withhold, to keep from, to embezzle"}),
    16888: (T + "word in example", {"t_en": "applicable, current, in force"}),
    16966: (T + "word in example", {"t_en": "serious criminal, dangerous criminal, felon"}),
    17379: (T + "word in example", {"t_en": "vehicle, contraption, conveyance"}),
}

REPLACE = []
SPLIT_LATER = {}
