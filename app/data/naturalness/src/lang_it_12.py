"""Вычитка итальянского, порция p012 (B1), 23.10: повторы («Esigo una spiegazione», «in fondo al corridoio», «meno plastica»), голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    1996: (T + "повтор 2722 «meno plastica»", {"example_it": "Per proteggere l'ambiente, spegni la luce!"}),
    2430: (T + "повтор 2472 «Esigo una spiegazione»", {"example_it": "Mi devi una spiegazione"}),
    2448: (T + "«Non è giusto» — оборвано", {"example_it": "Non è giusto, tocca a me!"}),
    2490: (T + "нет слова карточки «la frustrazione»", {"example_it": "Per la frustrazione ha mangiato tutta la cioccolata"}),
    2497: (T + "повтор 1011 «in fondo al corridoio»", {"example_it": "In aereo preferisco il posto sul corridoio"}),
    2508: (T + "«L'avversario è forte» — учебниково", {"example_it": "Domani giochiamo contro un avversario fortissimo"}),
    2586: (T + "повтор 13392 «Qualcuno … alla porta»", {"example_it": "C'è qualcuno che parla inglese?"}),
    2618: (T + "«Mi piace guardare le commedie» — учебниково", {"example_it": "Stasera guardiamo una commedia?"}),
    2620: (T + "«Dobbiamo risolvere il conflitto» — книжно", {"example_it": "Tra i due fratelli c'è sempre conflitto"}),
    2626: (T + "«È corretto» — оборвано", {"example_it": "La risposta è corretta"}),
    2658: (T + "«Guido la macchina per la città» — учебниково", {"example_it": "Lui guida, io leggo la mappa"}),
}

REPLACE = []

SPLIT_LATER = {}
