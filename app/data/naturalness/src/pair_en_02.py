"""Шаг 2, en, порция 2: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    551: (T + "word in example", {"t_en": "to love, to adore"}),
    649: (T + "word in example", {"t_en": "to take, (in a restaurant) to have"}),
    654: (T + "word in example", {"t_en": "nothing, not anything"}),
    706: (T + "word in example", {"t_en": "person, people", "x_en": "How many people are there in your group?"}),
    836: (T + "word in example", {"t_en": "oneself, itself, himself, herself"}),
    1028: (T + "word in example", {"t_en": "to become, to get, to be going to be"}),
    1072: (T + "word in example", {"t_en": "newspaper, paper"}),
    1153: (T + "word in example", {"t_en": "appetite, (Guten Appetit!) enjoy your meal"}),
    1160: (T + "word in example", {"t_en": "workplace, job, desk"}),
    1284: (T + "word in example", {"t_en": "look, view, glance"}),
    1316: (T + "natural", {"x_en": "I study so that I'll pass the exam"}),
}

REPLACE = []
SPLIT_LATER = {}
