"""Шаг 2, cs, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    8703: (T + "в примере úctyhodných", {"t_cs": "statný, značný, úctyhodný"}),
    8909: (T + "в примере působí", {"t_cs": "činný, působící, (tätig sein) působit"}),
    9059: (T + "в примере vykonstruovaně", {"t_cs": "vykonstruovaný, vykonstruovaně"}),
    9363: (T + "в примере asistentka", {"t_cs": "asistence, (Assistenz der Geschäftsführung) asistentka vedení"}),
}

REPLACE = []
SPLIT_LATER = {}
