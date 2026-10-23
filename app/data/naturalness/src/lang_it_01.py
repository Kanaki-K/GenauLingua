"""Вычитка итальянского, порция p001 (A1), 23.10: голые учебниковые фразы → живые, повторы, «volentieri», «Müller» → «Rossi»"""

T = "вычитка итальянского: "

FIXES = {
    41: (T + "повтор «va al lavoro» (62, 72)", {"example_it": "Il lavoro mi piace molto"}),
    62: (T + "повтор «va al lavoro in…» (72)", {"example_it": "Ho lasciato la macchina davanti a casa"}),
    103: (T + "«Viene sicuramente» — порядок слов", {"example_it": "Sicuramente arriva in ritardo"}),
    113: (T + "«Beve una birra» — без ситуации", {"example_it": "Ci beviamo una birra?"}),
    117: (T + "«La pera è dolce» — учебниково", {"example_it": "Questa pera è dolcissima"}),
    127: (T + "«Compra un fiore rosso» — учебниково", {"example_it": "Che bel fiore!"}),
    137: (T + "без ситуации", {"example_it": "Mi porti un bicchiere d'acqua?"}),
    141: (T + "повтор «a colazione» (138)", {"example_it": "Mi fai un panino?"}),
    144: (T + "«Vado in autobus» — оборвано", {"example_it": "Vado a scuola in autobus"}),
    160: (T + "повтор 402 «Sono qui / È qui»", {"example_it": "Il tuo telefono è lì, sul tavolo"}),
    163: (T + "нет слова карточки «il ringraziamento»", {"example_it": "Un piccolo regalo come ringraziamento"}),
    167: (T + "повтор 305 «Questo va bene»", {"example_it": "Questo è il mio posto"}),
    189: (T + "«La scuola è lì» — учебниково", {"example_it": "La farmacia è lì, a destra"}),
    211: (T + "«Ti invito» — оборвано", {"example_it": "Stasera ti invito io!"}),
    238: (T + "«Mangiamo a mezzogiorno» — учебниково", {"example_it": "A che ora mangiamo?"}),
    244: (T + "«Andiamo a Berlino» — без ситуации", {"example_it": "Domani andiamo al mare in macchina"}),
    248: (T + "повтор «va in…» (62, 72)", {"example_it": "Mia figlia va a scuola in bicicletta"}),
    267: (T + "«Il cibo è pronto» — калька", {"example_it": "La cena è pronta!"}),
    274: (T + "«Mi piace mangiare il pesce» — учебниково", {"example_it": "Il venerdì mangiamo pesce"}),
    278: (T + "«Andiamo all'aeroporto» — учебниково", {"example_it": "Ti accompagno all'aeroporto"}),
    286: (T + "нет слова карточки «la donna / la moglie»", {"example_it": "Mia moglie lavora in ospedale"}),
    305: (T + "повтор 167 «Questo va bene»", {"example_it": "Sono abbastanza stanco"}),
    307: (T + "«Lavora in giardino» — учебниково", {"example_it": "Il nonno lavora in giardino tutto il giorno"}),
    315: (T + "«Müller» — не итальянская фамилия", {"example_it": "Gentile signora Rossi"}),
    323: (T + "«Compra verdura fresca» — учебниково", {"example_it": "Al mercato la verdura è più fresca"}),
    328: (T + "«Sono occupato proprio ora» — калька", {"example_it": "Sto proprio uscendo"}),
    330: (T + "«Bevo volentieri il tè» — калька gern", {"example_it": "Vieni con noi? – Con piacere!"}),
    348: (T + "«È molto felice» — без ситуации", {"example_it": "Sono felice per te!"}),
    374: (T + "«L'autobus si ferma alla fermata» — тавтология", {"example_it": "Tieni un attimo la borsa, per favore"}),
    376: (T + "«Mi dà la mano» — без ситуации", {"example_it": "Dammi la mano, attraversiamo"}),
    400: (T + "«Müller» — не итальянская фамилия", {"example_it": "Buongiorno, signor Rossi, prego, entri"}),
    402: (T + "повтор 160 «Sono qui»", {"example_it": "Vieni qui!"}),
    406: (T + "«È seduto dietro» — без ситуации", {"example_it": "In macchina i bambini stanno dietro"}),
    415: (T + "«Il cane è molto carino» — учебниково", {"example_it": "Il nostro cane si chiama Leo"}),
    428: (T + "повтор 426 «Questa è la sua…»", {"example_it": "I bambini giocano con i loro amici"}),
    431: (T + "повтор 338 «in città»", {"example_it": "Abito in Italia da due anni"}),
    456: (T + "повтор 429 «bevo il caffè la mattina»", {"example_it": "Prendiamo un caffè?"}),
    467: (T + "«Compro il pane» — учебниково", {"example_it": "Dove compri il pane?"}),
    481: (T + "«Andiamo al cinema» — повтор 270", {"example_it": "Il cinema è chiuso il lunedì"}),
    500: (T + "повтор 165 «alle tre»", {"example_it": "Da dove vieni?"}),
    509: (T + "«È malata» — без ситуации", {"example_it": "Oggi mia figlia è malata e resta a casa"}),
    531: (T + "«Il frigorifero è vuoto» — книжно", {"example_it": "Il frigo è vuoto, dobbiamo fare la spesa"}),
}

REPLACE = []

SPLIT_LATER = {}
