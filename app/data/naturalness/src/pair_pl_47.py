"""Шаг 2, pl, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    11488: (T + "word in example", {"t_pl": "skandaliczny, oburzający, (das ist skandalös) to skandal"}),
    11507: (T + "word in example", {"t_pl": "wizjonerski, dalekowzroczny, (ein visionärer Mensch) wizjoner"}),
    11511: (T + "word in example", {"t_pl": "wytrwały, uporczywy, wytrwale"}),
    12029: (T + "word in example", {"t_pl": "ugotowany, gotowany, (hart gekocht) na twardo"}),
    12329: (T + "word in example", {"t_pl": "lina, sznur, (Seilspringen) skakanka"}),
    14270: (T + "word in example", {"t_pl": "ucichnąć, zamilknąć, milknąć"}),
}

REPLACE = []
SPLIT_LATER = {}
