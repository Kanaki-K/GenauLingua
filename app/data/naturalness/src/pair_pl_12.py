"""Шаг 2, pl, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    2448: (T + "word in example", {"t_pl": "sprawiedliwy, uczciwy, fair"}),
    2497: (T + "word in example", {"t_pl": "korytarz, przejście, bieg"}),
    2573: (T + "word in example", {"t_pl": "w ten sposób, że; robiąc coś"}),
    2596: (T + "word in example", {"t_pl": "kandydat (kandydatka), uczestnik (teleturnieju)"}),
    2601: (T + "word in example", {"t_pl": "kupujący, nabywca, kupiec"}),
}

REPLACE = []
SPLIT_LATER = {}
