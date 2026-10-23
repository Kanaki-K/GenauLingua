"""Вычитка итальянского, порция p040 (C1), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    9569: (T + "повтор 10885 «a settant'anni il nonno…»", {"example_it": 'Non è mai troppo tardi per imparare una lingua'}),
    9887: (T + 'нет слова карточки «corruttibile»', {"example_it": 'Tutti sono corruttibili, basta trovare il prezzo giusto'}),
}

REPLACE = []

SPLIT_LATER = {}
