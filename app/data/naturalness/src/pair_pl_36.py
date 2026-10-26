"""Шаг 2, pl, порция 36: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    16272: (T + "word in example", {"t_pl": "komisja, odpad, (Ausschussware) wybrakowany towar"}),
    16305: (T + "word in example", {"t_pl": "miejsce dla świadka, (in den Zeugenstand treten) zeznawać w sądzie"}),
    16324: (T + "word in example", {"t_pl": "wcześniejsza karalność, (keine Vorstrafen) niekarany"}),
    16471: (T + "word in example", {"t_pl": "nadejście, zbliżanie się, (im Anmarsch sein) zbliżać się"}),
    16731: (T + "word in example", {"t_pl": "bezprawny, bezprawie"}),
    16919: (T + "word in example", {"t_pl": "rozstawić, ustawić, postawić"}),
}

REPLACE = []
SPLIT_LATER = {}
