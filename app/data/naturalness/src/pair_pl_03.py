"""Шаг 2, pl, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    1673: (T + "word in example", {"t_pl": "męski, (o zwierzęciu) samiec"}),
    1909: (T + "word in example", {"t_pl": "miejsce, posada, praca"}),
    2372: (T + "word in example", {"t_pl": "pilny, (es eilig haben) spieszyć się"}),
    8334: (T + "word in example", {"t_pl": "uzupełnić, dopisać"}),
    10061: (T + "word in example", {"t_pl": "zły, (böse sein) gniewać się"}),
    10420: (T + "word in example", {"t_pl": "obcy, cudzy, (ich bin fremd hier) nie jestem stąd"}),
    13354: (T + "word in example", {"t_pl": "cztery, czworo"}),
}

REPLACE = []
SPLIT_LATER = {}
