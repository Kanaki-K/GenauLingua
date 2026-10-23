"""Вычитка итальянского, порция p037 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    17557: (T + '«Devo spingere» — калька', {"example_it": 'Spingi la leva a sinistra'}),
    17958: (T + 'повтор 17956 «gli scienziati»', {"example_it": 'Mi piace esplorare le stradine delle città che visito'}),
    18183: (T + '«un buco tutto in disordine» — не тот смысл', {"example_it": "Affitta una stanzetta vicino all'università"}),
    18217: (T + 'повтор 18385 «cambiare le lenzuola»', {"example_it": 'Le lenzuola si stanno asciugando sul balcone'}),
    18235: (T + 'повтор 6519 «riparo dalla pioggia»', {"example_it": 'La capanna in fondo al giardino è il nostro nascondiglio'}),
}

REPLACE = []

SPLIT_LATER = {}
