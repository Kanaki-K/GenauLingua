"""Шаг 2, en, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    12600: (T + "tense", {"x_en": "The old man is smoking a cigar"}),
    12607: (T + "tense", {"x_en": "The dog is scratching at the door"}),
    12713: (T + "word in example", {"t_en": "drunkenness, high, (den Rausch ausschlafen) to sleep it off"}),
}

REPLACE = []
SPLIT_LATER = {}
