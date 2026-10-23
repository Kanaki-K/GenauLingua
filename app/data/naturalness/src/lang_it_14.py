"""Вычитка итальянского, порция p014 (B1), 23.10: нет слова карточки, кальки, повторы («la tua roba», «bussare alla porta», «la chiave»)"""

T = "вычитка итальянского: "

FIXES = {
    3067: (T + "«è armoniosa» — книжно", {"example_it": "La convivenza con mia suocera non è sempre facile"}),
    13392: (T + "повтор 6505 «bussa alla porta»", {"example_it": "Qualcuno vuole un caffè?"}),
    6369: (T + "нет слова карточки «lontano»", {"example_it": "La stazione non è molto lontana, dieci minuti a piedi"}),
    6415: (T + "«Lo apprezzo molto» — оборвано", {"example_it": "Apprezzo molto il tuo aiuto"}),
    6520: (T + "«Continuiamo e basta» — коряво", {"example_it": "Dai, andiamo avanti!"}),
    6541: (T + "нет слова карточки «filarsela»", {"example_it": "Filiamocela, presto!"}),
    6583: (T + "«si fanno visita a vicenda» — калька", {"example_it": "Tra vicini ci aiutiamo a vicenda"}),
    6610: (T + "«Devo avvertirti» — без ситуации", {"example_it": "Ti avverto, è molto piccante"}),
    6638: (T + "«mi procura molta gioia» — калька", {"example_it": "Questo lavoro mi procura molte soddisfazioni"}),
    6707: (T + "нет слова карточки «enorme»", {"example_it": "Stanotte c'è stato un temporale enorme"}),
    6710: (T + "«Non ho voglia di tutta questa roba» — коряво", {"example_it": "Quanta roba hai in macchina!"}),
    6727: (T + "повтор «la chiave»", {"example_it": "Ho frugato tutto l'appartamento per trovare il passaporto"}),
    6730: (T + "«a Berlino» — без нужды", {"example_it": "Ci stiamo avvicinando a Bologna, tra dieci minuti siamo lì"}),
    6819: (T + "нет слова карточки «incluso»", {"example_it": "La colazione è inclusa nel prezzo"}),
}

REPLACE = []

SPLIT_LATER = {}
