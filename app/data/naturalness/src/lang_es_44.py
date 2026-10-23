"""Вычитка испанского, порция p044 (C1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    17216: (T + '«en Múnich» — без нужды', {"example_es": 'De paso hacia Francia siempre dormimos en casa de mi primo en Zaragoza'}),
    18362: (T + '«en Múnich» — без нужды', {"example_es": 'Por ese dinero en Madrid consigues como mucho un cuchitril sin calefacción'}),
}

REPLACE = []

SPLIT_LATER = {}
