"""Вычитка испанского, порция p039 (C1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    8007: (T + '«Cada mañana» — калька', {"example_es": 'Por las mañanas se echa en el bol medio paquete de muesli'}),
    8022: (T + 'повтор 7336 «segunda»', {"example_es": 'Si perdemos hoy, descendemos'}),
}

REPLACE = []

SPLIT_LATER = {}
