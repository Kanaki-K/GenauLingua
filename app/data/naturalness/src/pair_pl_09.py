"""Шаг 2, pl, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    1491: (T + "word in example", {"t_pl": "śliski, gładki, ślisko"}),
    1576: (T + "word in example", {"t_pl": "w kratę, w kratkę"}),
    1594: (T + "word in example", {"x_pl": "Mamy jeszcze kilka drobnych mebli do sprzedania"}),
    1645: (T + "word in example", {"x_pl": "Na swojej drodze życiowej dziadek mieszkał w pięciu krajach"}),
    1667: (T + "word in example", {"t_pl": "mailować, napisać maila"}),
    1679: (T + "word in example", {"t_pl": "mysz, myszka"}),
    1699: (T + "word in example", {"x_pl": "Po szkole średniej poszedł do nauki zawodu"}),
    1734: (T + "word in example", {"t_pl": "potrzebny, konieczny, (nicht nötig) nie trzeba"}),
}

REPLACE = []
SPLIT_LATER = {}
