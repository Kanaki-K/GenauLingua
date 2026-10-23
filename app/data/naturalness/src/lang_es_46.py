"""Вычитка испанского, порция p046 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    8656: (T + 'повтор «llevarse un paraguas»', {"example_es": 'Por si acaso he hecho una copia del pasaporte'}),
    9224: (T + '«de Hamburgo» — без нужды', {"example_es": 'Mi tío fue durante cuarenta años ingeniero jefe en un astillero de Cádiz'}),
    11487: (T + '«al elegir el color» — книжно', {"example_es": 'Delante de la carta siempre está indeciso'}),
}

REPLACE = []

SPLIT_LATER = {}
