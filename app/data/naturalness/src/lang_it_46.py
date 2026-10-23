"""Вычитка итальянского, порция p046 (C2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    8656: (T + 'повтор «portare un ombrello»', {"example_it": 'Per sicurezza ho fatto una copia del passaporto'}),
    11487: (T + '«Nella scelta del colore» — книжно', {"example_it": 'Davanti al menù è sempre indeciso'}),
}

REPLACE = []

SPLIT_LATER = {}
