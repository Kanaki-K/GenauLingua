"""Шаг 2, pl, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    98: (T + "word in example", {"t_pl": "odpowiedź, decyzja, (Bescheid sagen) dać znać"}),
    161: (T + "word in example", {"t_pl": "za to, po to"}),
    202: (T + "word in example", {"t_pl": "właśnie, (dann eben) no to"}),
    268: (T + "word in example", {"t_pl": "święto, impreza, festyn"}),
    459: (T + "word in example", {"t_pl": "zimny, (kalt werden) stygnąć"}),
    943: (T + "word in example", {"t_pl": "suchy, (trocken werden) wyschnąć"}),
    1136: (T + "word in example", {"t_pl": "strach, lęk, (Angst haben) bać się"}),
}

REPLACE = []
SPLIT_LATER = {}
