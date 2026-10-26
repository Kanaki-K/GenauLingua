"""Шаг 2, pl, порция 2: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    763: (T + "natural", {"t_pl": "poprawny, właściwy, (das ist richtig) to się zgadza", "x_pl": "Masz rację, to się zgadza"}),
    846: (T + "word in example", {"t_pl": "natychmiast, od razu, zaraz"}),
    951: (T + "word in example", {"t_pl": "o, wokół, koło"}),
    1128: (T + "word in example", {"t_pl": "oferować, proponować, częstować"}),
    1153: (T + "word in example", {"t_pl": "apetyt, (Guten Appetit) smacznego"}),
    1284: (T + "word in example", {"t_pl": "spojrzenie, widok, (auf den ersten Blick) na pierwszy rzut oka"}),
}

REPLACE = []
SPLIT_LATER = {}
