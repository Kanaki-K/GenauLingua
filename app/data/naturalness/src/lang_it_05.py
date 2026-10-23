"""Вычитка итальянского, порция p005 (A2), 23.10: повторы («mi sono dimenticato», «licenziato», «ringraziarti», «prenotare»), нет слова карточки, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    1222: (T + "«Mi piace giocare» — учебниково", {"example_it": "Mio figlio gioca a basket nella squadra della scuola"}),
    1228: (T + "повтор 1317 «ringraziarti»", {"example_it": "Ci tengo a ringraziare tutti"}),
    1235: (T + "«Può giustificarlo?» — без ситуации", {"example_it": "Come giustifichi questa spesa?"}),
    1297: (T + "повтор 1805 «Vorrei prenotare»", {"example_it": "Ho prenotato le vacanze online"}),
    1312: (T + "«Io sono contro» — коряво", {"example_it": "Chi è contro?"}),
    1319: (T + "повтор «Per questo sono…» (161)", {"example_it": "È proprio per questo che ti chiamo"}),
    1342: (T + "нет слова карточки «sottile»", {"example_it": "Il ghiaccio è ancora troppo sottile"}),
    1432: (T + "повтор «fare il bagno» (69)", {"example_it": "Il fiume attraversa tutta la città"}),
    1479: (T + "«Devo lavare i piatti» — учебниково", {"example_it": "Stasera i piatti li lavi tu!"}),
    1505: (T + "повтор 1634 «ti sei licenziato»", {"example_it": "Non c'è motivo di preoccuparsi"}),
    1665: (T + "«Non ho voglia» — оборвано", {"example_it": "Hai voglia di un gelato?"}),
    1683: (T + "повтор 584 «Di solito…»", {"example_it": "Il martedì per lo più lavoro da casa"}),
    1685: (T + "нет слова карточки «la folla»", {"example_it": "C'era una folla enorme al concerto"}),
    1691: (T + "нет слова карточки «il dipendente»", {"example_it": "L'azienda ha cinquanta dipendenti"}),
    1720: (T + "повтор 2093 «perché sono malato»", {"example_it": "Domani non lavoro, perché è festa"}),
    1793: (T + "«È molto ricco» — без ситуации", {"example_it": "Ha sposato un uomo molto ricco"}),
    1813: (T + "«non gioca alcun ruolo» — калька", {"example_it": "Nel film ha un piccolo ruolo"}),
    1819: (T + "повтор 1834 «ce l'ho fatta»", {"example_it": "Ce la fai a venire alle otto?"}),
    1843: (T + "повтор «Il tempo è …» (1032)", {"example_it": "Ho fatto un sogno terribile"}),
    1865: (T + "нет слова карточки «mettere»", {"example_it": "Mettiti qui accanto a me"}),
    1903: (T + "повтор 10027 «tè invece del caffè»", {"example_it": "Invece di guardare la tv, leggi un libro"}),
    1922: (T + "«Navigo su internet» — учебниково", {"example_it": "Ho passato la sera a navigare su internet"}),
    1989: (T + "«A proposito, domani vengo» — коряво", {"example_it": "A proposito, hai sentito Marco?"}),
    1995: (T + "«A Colonia» — без нужды", {"example_it": "A Bologna devi cambiare"}),
    2040: (T + "«Mi sono innamorato» — оборвано", {"example_it": "Si è innamorato della sua vicina di casa"}),
    2041: (T + "повтор «la chiave»", {"example_it": "Non perdere tempo!"}),
    2071: (T + "«Preparo la cena» — учебниково", {"example_it": "Mi preparo per l'esame"}),
    2089: (T + "нет слова карточки «a causa di»", {"example_it": "A causa dello sciopero non ci sono treni"}),
    2095: (T + "«Lavoro ancora qui» — не то значение", {"example_it": "Continuerò a lavorare qui anche in futuro"}),
    2216: (T + "повтор 6355 «aprire la porta»", {"example_it": "Apri tu il vino?"}),
    2295: (T + "нет слова карточки «la popolazione»", {"example_it": "La popolazione della città è in aumento"}),
    2458: (T + "«Questo cibo» — калька", {"example_it": "Il formaggio è troppo grasso per me"}),
    2603: (T + "нет слова карточки «a malapena»", {"example_it": "Senza occhiali ci vedo a malapena"}),
    2668: (T + "повтор 631 «Dopo aver mangiato»", {"example_it": "Dopo che sei partito, ha chiamato tua madre"}),
    2880: (T + "повтор 6284 «me ne sono dimenticato»", {"example_it": "È un disastro totale"}),
    2950: (T + "«Mi sono ferito» — оборвано", {"example_it": "Mi sono ferito alla mano in cucina"}),
    6241: (T + "«È piuttosto buono» — без ситуации", {"example_it": "Oggi fa piuttosto freddo"}),
}

REPLACE = []

SPLIT_LATER = {}
