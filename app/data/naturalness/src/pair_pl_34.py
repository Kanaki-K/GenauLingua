"""Шаг 2, pl, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    14539: (T + "word in example", {"t_pl": "rękopis, maszynopis, (ohne Manuskript) bez kartki"}),
    14542: (T + "word in example", {"t_pl": "urok, zaklęcie, (in seinen Bann ziehen) zauroczyć"}),
}

REPLACE = []
SPLIT_LATER = {}
