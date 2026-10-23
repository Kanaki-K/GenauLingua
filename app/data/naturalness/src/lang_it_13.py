"""Вычитка итальянского, порция p013 (B1), 23.10: нет слова карточки, повторы («violare le regole», «buttare via», «domani parto/torno»), голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    2792: (T + "нет слова карточки «cambiare»", {"example_it": "In salita cambia marcia!"}),
    2808: (T + "«Ma è ovvio» — без ситуации", {"example_it": "Ovviamente vengo anch'io!"}),
    2809: (T + "нет слова карточки «inviare»", {"example_it": "Ti invio il file stasera"}),
    2813: (T + "«Guardo una serie» — учебниково", {"example_it": "Stiamo guardando una serie fantastica"}),
    2828: (T + "нет слова карточки «la preoccupazione»", {"example_it": "Le preoccupazioni non lo fanno dormire"}),
    2850: (T + "«Qui puzza» — без ситуации", {"example_it": "Il formaggio puzza, ma è buonissimo"}),
    2884: (T + "повтор 605 «Adesso va di moda»", {"example_it": "C'è la tendenza a lavorare sempre di più da casa"}),
    2887: (T + "повтор 1672 «il rubinetto gocciola»", {"example_it": "Dal soffitto gocciola acqua"}),
    2898: (T + "«Mi sorprendi» — без ситуации", {"example_it": "Mi hai sorpreso con questa notizia"}),
    2906: (T + "«Qui è normale» — оборвано", {"example_it": "Qui è normale lasciare la mancia"}),
    2944: (T + "«di Berlino» — без нужды", {"example_it": "I prezzi qui sono paragonabili a quelli di Milano"}),
    2953: (T + "повтор 18988 «mi manchi»", {"example_it": "Ti manca la tua famiglia?"}),
    2963: (T + "повтор 2041 «non perdere tempo»", {"example_it": "Non sprecare l'acqua!"}),
    2972: (T + "нет слова карточки «la comprensione»", {"example_it": "Grazie per la comprensione"}),
    2975: (T + "повтор 2974 «violazione delle regole»", {"example_it": "Chi viola il divieto paga una multa"}),
    2999: (T + "«Trasmette così tanto calore» — коряво", {"example_it": "Il calore del camino è piacevolissimo"}),
    3003: (T + "повтор 3059 «Domani parto / Torno domani»", {"example_it": "Quando partite per le vacanze?"}),
    3006: (T + "повтор 3005 «buttare via»", {"example_it": "Le scatole vecchie le butto via"}),
    3059: (T + "«Torno domani» — оборвано", {"example_it": "Torniamo in treno o in macchina?"}),
}

REPLACE = []

SPLIT_LATER = {}
