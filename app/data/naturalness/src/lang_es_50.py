"""Вычитка испанского, порция p050 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    18058: (T + '«lee por gusto» — коряво', {"example_es": 'La novela negra es el único género literario que lee mi padre'}),
    18386: (T + '«Todavía tengo que» — калька', {"example_es": 'Todavía hay que preparar la habitación de invitados'}),
    18388: (T + 'повтор 16143 «después de la fiesta la cocina parece»', {"example_es": '¡Tu habitación es una auténtica pocilga!'}),
    18908: (T + '«llorando de forma incesante» — книжно', {"example_es": 'El ruido incesante de las obras me vuelve loco'}),
    18474: (T + '«en Hamburgo» — без нужды', {"example_es": 'Es residente en Valencia'}),
}

REPLACE = []

SPLIT_LATER = {}
