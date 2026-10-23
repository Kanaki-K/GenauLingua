"""Вычитка итальянского, порция p038 (B2/C1), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    18663: (T + 'повтор 18922 «riposare dopo mangiato»', {"example_it": 'Lascialo riposare, è malato'}),
    18728: (T + '«mi aiuta a restare organizzato» — калька', {"example_it": 'Al mattino ho la mia piccola routine: caffè, doccia, giornale'}),
    18747: (T + "повтор 18772 «pescare all'alba»", {"example_it": "Siamo partiti all'alba per evitare il traffico"}),
    7668: (T + '«devo affaticare gli occhi» — калька', {"example_it": 'Leggere senza occhiali mi affatica gli occhi'}),
}

REPLACE = []

SPLIT_LATER = {}
