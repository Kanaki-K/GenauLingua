"""Вычитка итальянского, порция p015 (B1), 23.10: нет слова карточки, кальки, тавтологии, повторы («partiamo domani», «controllo un attimo»)"""

T = "вычитка итальянского: "

FIXES = {
    6833: (T + "«Rivediamo di nuovo» — тавтология", {"example_it": "Rivediamo la lista un'ultima volta"}),
    6851: (T + "нет слова карточки «rompere»", {"example_it": "Riesci a rompere questa noce?"}),
    6872: (T + "«Rimontiamo la tenda» — без ситуации", {"example_it": "Montiamo la tenda qui?"}),
    6889: (T + "«ogni dettaglio» — калька", {"example_it": "Raccontami tutto nei minimi dettagli"}),
    6890: (T + "«mi è del tutto sconosciuta» — книжно", {"example_it": "Il numero è sconosciuto, non rispondo"}),
    6924: (T + "«del tutto improbabile» — калька", {"example_it": "È molto improbabile"}),
    6925: (T + "«praticamente una garanzia» — коряво", {"example_it": "Ho praticamente finito"}),
    6927: (T + "«sostituto del tè» — неживо", {"example_it": "Ho sempre una batteria di ricambio"}),
    6931: (T + "без ситуации", {"example_it": "Il capo l'ha trasferito a Milano"}),
    6950: (T + "повтор 6952 «domani … partiamo»", {"example_it": "Domattina ci mettiamo in viaggio presto"}),
    6952: (T + "повтор 6950", {"example_it": "A che ora partiamo?"}),
    6969: (T + "«Ho constatato che non viene» — коряво", {"example_it": "Ho constatato che mancavano venti euro nel portafoglio"}),
    6994: (T + "«Il nodo della mia corda» — неживо", {"example_it": "Non riesco a sciogliere questo nodo"}),
    7005: (T + "«A stima approssimativa» — коряво", {"example_it": "È solo un calcolo approssimativo"}),
    7032: (T + "«marciato nel bosco» — не то значение", {"example_it": "I soldati marciano per la città"}),
    7061: (T + "«tasse incluse» — канцелярит", {"example_it": "Sono 50 euro, consegna inclusa"}),
    7091: (T + "повтор 6662 «Controllo un attimo»; калька", {"example_it": "Aspetta, guardo un attimo le mail"}),
    7140: (T + "«Scuote solo la testa» — калька", {"example_it": "Scuote la testa senza dire niente"}),
    7190: (T + "«Vogliamo continuare» — калька", {"example_it": "Continuiamo il discorso domani?"}),
    7315: (T + "«È generalmente noto» — канцелярит", {"example_it": "In generale sono contento del mio lavoro"}),
    7715: (T + "«sta seduta insieme e racconta» — калька", {"example_it": "La domenica siamo tutti insieme a tavola"}),
}

REPLACE = []

SPLIT_LATER = {}
