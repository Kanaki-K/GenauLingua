"""Шаг 2, tr, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    2484: (T + "word in example", {"t_tr": "barış, huzur, (in Frieden lassen) rahat bırakmak"}),
    2608: (T + "word in example", {"t_tr": "iklim, ortam, hava"}),
    2670: (T + "word in example", {"t_tr": "düşünceli, (nachdenklich machen) düşündürmek"}),
}

REPLACE = []
SPLIT_LATER = {}
