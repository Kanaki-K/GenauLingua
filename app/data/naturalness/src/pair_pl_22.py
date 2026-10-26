"""Шаг 2, pl, порция 22: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    14015: (T + "word in example", {"t_pl": "obraza, zniewaga, obelga"}),
    14945: (T + "word in example", {"t_pl": "osobny, osobno, rozdzielony"}),
    14974: (T + "word in example", {"t_pl": "sylwetka, figura, postać"}),
}

REPLACE = []
SPLIT_LATER = {}
