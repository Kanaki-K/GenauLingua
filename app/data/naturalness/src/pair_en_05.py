"""Шаг 2, en, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    1326: (T + "word in example", {"x_en": "It's raining, that's why we'll take the car"}),
    1718: (T + "word in example", {"t_en": "vicinity, closeness, (in der Nähe) nearby"}),
    1867: (T + "word in example", {"t_en": "safety, security, (in Sicherheit) safe"}),
    2036: (T + "word in example", {"t_en": "to arrange, to agree on, (einen Termin vereinbaren) to make an appointment"}),
    2800: (T + "word in example", {"t_en": "dirty, filthy"}),
    3015: (T + "word in example", {"t_en": "value, worth", "x_en": "The ring has great sentimental value for me, it was my gran's"}),
    6186: (T + "word in example", {"t_en": "out, outside"}),
    6193: (T + "natural", {"x_en": "That's not difficult at all"}),
}

REPLACE = []
SPLIT_LATER = {}
