"""Шаг 2, cs, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    324: (T + "в примере udělat si pohodlí", {"t_cs": "útulný, pohodlný, (es sich gemütlich machen) udělat si pohodlí"}),
    381: (T + "в примере hlavně že", {"t_cs": "hlavní věc, to hlavní, (Hauptsache, …) hlavně že"}),
    505: (T + "в примере bolí mě hlava", {"t_cs": "bolest hlavy, (Kopfschmerzen haben) bolí mě hlava"}),
    512: (T + "в примере sestřička", {"t_cs": "ošetřovatel, zdravotní sestra, sestřička"}),
    594: (T + "в примере mínus", {"t_cs": "minus, mínus"}),
    18976: (T + "в примере rovně", {"t_cs": "rovný, rovně"}),
    18978: (T + "в примере pořádná", {"t_cs": "pořádně, opravdu, pořádný"}),
}

REPLACE = []
SPLIT_LATER = {}
