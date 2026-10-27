"""Шаг 2, fr, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    10764: (T + "в примере moralement", {"t_fr": "moral, moralement"}),
    11263: (T + "в примере avec délicatesse", {"t_fr": "délicat, avec tact, avec délicatesse"}),
    11465: (T + "в примере impatient de", {"t_fr": "avide de, friand de, impatient de"}),
    11564: (T + "в примере prudemment", {"t_fr": "prudent, avisé, prudemment"}),
    11725: (T + "в примере gicler", {"t_fr": "asperger, injecter, gicler"}),
}

REPLACE = []
SPLIT_LATER = {}
