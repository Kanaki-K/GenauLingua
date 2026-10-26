"""Шаг 2, pl, порция 24: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    15936: (T + "word in example", {"t_pl": "majestat, wysokość, (Eure Majestät) Wasza Królewska Mość"}),
    15941: (T + "word in example", {"t_pl": "naród, lud, ludzie"}),
    16025: (T + "word in example", {"t_pl": "nielegalny, nielegalnie, niezgodny z prawem"}),
    16036: (T + "word in example", {"t_pl": "przyznanie się, wyznanie, (ein Geständnis machen) przyznać się"}),
    16063: (T + "word in example", {"t_pl": "zawieszenie wyroku, okres próby, (auf Bewährung) warunkowe zwolnienie"}),
    16077: (T + "word in example", {"t_pl": "przestępczy, kryminalny, (das ist kriminell) to przestępstwo"}),
    16142: (T + "word in example", {"t_pl": "walka, starcie, potyczka"}),
    17055: (T + "word in example", {"t_pl": "łódź, łódka, motorówka"}),
}

REPLACE = []
SPLIT_LATER = {}
