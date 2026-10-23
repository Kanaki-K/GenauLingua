"""Вычитка испанского, порция p028 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    7476: (T + '«Se merece un gran agradecimiento por ello» — книжно', {"example_es": 'Todo el mérito es suyo'}),
    7509: (T + 'без ситуации', {"example_es": 'Sus palabras me causaron mucho dolor'}),
    7818: (T + '«Lo que estás haciendo raya» — книжно', {"example_es": '¡Tu idea raya en la locura!'}),
    8113: (T + '«cuando habla con el jefe» — странно', {"example_es": 'Al teléfono disfrazó la voz para gastarme una broma'}),
    8116: (T + '«sin tener ninguna culpa» — книжно', {"example_es": 'Acabé metido en su pelea sin querer'}),
}

REPLACE = []

SPLIT_LATER = {}
