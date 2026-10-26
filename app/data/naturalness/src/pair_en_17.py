"""Шаг 2, en, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    9050: (T + "word in example", {"t_en": "activity, work, job", "x_en": "Giving guitar lessons is a nice little side activity for him"}),
    9731: (T + "word in example", {"x_en": "The house has been in the family's possession for a hundred years"}),
    9801: (T + "word in example", {"x_en": "He finances his studies with a job in a café"}),
    9833: (T + "word in example", {"t_en": "fully booked, sold out, booked up"}),
}

REPLACE = []
SPLIT_LATER = {}
