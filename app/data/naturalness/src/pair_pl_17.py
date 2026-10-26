"""Шаг 2, pl, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    9770: (T + "word in example", {"t_pl": "za darmo, bezpłatnie, gratis"}),
    9771: (T + "word in example", {"t_pl": "kupujący, nabywca, kupiec"}),
    9833: (T + "word in example", {"t_pl": "w pełni zarezerwowany, zarezerwowany, brak wolnych miejsc"}),
}

REPLACE = []
SPLIT_LATER = {}
