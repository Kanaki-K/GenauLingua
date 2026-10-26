"""Шаг 2, pl, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    16765: (T + "word in example", {"t_pl": "przełożyć, przekładać, odroczyć"}),
    16811: (T + "word in example", {"t_pl": "powracający do nałogu, recydywista, (rückfällig werden) wrócić do przestępstwa"}),
    17876: (T + "word in example", {"t_pl": "do negocjacji, (nicht verhandelbar) nie podlega negocjacjom"}),
}

REPLACE = []
SPLIT_LATER = {}
