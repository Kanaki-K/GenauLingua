"""Шаг 2, fr, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    10048: (T + "в примере honnêtement", {"t_fr": "honnête, franc, honnêtement"}),
    10133: (T + "в примере сущ. sourire, глагола нет", {"x_fr": "Tu souris si joliment"}),
    10349: (T + "в примере réuni", {"t_fr": "uni, réuni"}),
}

REPLACE = []
SPLIT_LATER = {}
