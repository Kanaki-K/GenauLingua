"""Шаг 2, fr, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    10812: (T + "в примере joyeusement", {"t_fr": "joyeux, content, joyeusement"}),
    11667: (T + "ça sent délicieux — неестественно", {"x_fr": "Ça sent délicieusement bon !"}),
    11719: (T + "в примере tuer, нет abattre", {"x_fr": "Autrefois, au village, on abattait une oie pour Noël"}),
    11891: (T + "в примере se rafraîchir", {"t_fr": "le rafraîchissement, (zur Erfrischung) pour se rafraîchir"}),
}

REPLACE = []
SPLIT_LATER = {}
