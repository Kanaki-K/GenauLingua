"""Вычитка испанского, порция p040 (C1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    9569: (T + 'повтор 10885 «con setenta años mi abuelo»', {"example_es": 'Nunca es tarde para aprender un idioma'}),
    9887: (T + 'нет слова карточки «sobornable»', {"example_es": 'Todo el mundo es sobornable, solo hay que encontrar el precio'}),
    10919: (T + '«en Hamburgo» — без нужды', {"example_es": 'Mi padre no puede negar su acento andaluz, ni siquiera después de treinta años en Bilbao'}),
}

REPLACE = []

SPLIT_LATER = {}
