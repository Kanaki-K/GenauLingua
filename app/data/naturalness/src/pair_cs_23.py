"""Шаг 2, cs, порция 23: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    15467: (T + "в примере králíček", {"t_cs": "králík, králíček"}),
    15498: (T + "в примере severně", {"t_cs": "severní, na sever od, severně"}),
    15686: (T + "в примере bouřlivo", {"t_cs": "bouřlivý, vášnivý, (es ist stürmisch) je bouřlivo"}),
}

REPLACE = []
SPLIT_LATER = {}
