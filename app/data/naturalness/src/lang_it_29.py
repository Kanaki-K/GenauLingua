"""Вычитка итальянского, порция p029 (B2), 23.10: нет слова карточки, повторы, книжное"""

T = "вычитка итальянского: "

FIXES = {
    8886: (T + "«ha fatto le nuove canzoni» — коряво", {"example_it": "Il produttore della band è anche il loro manager"}),
    8909: (T + "нет слова карточки «attivo»", {"example_it": "A ottant'anni è ancora attivissima"}),
    8951: (T + "повтор 8877 «viene ogni …dì»", {"example_it": "Con i vicini dividiamo una donna delle pulizie"}),
    8954: (T + "«Devo fare di nuovo» — калька", {"example_it": "Il lavoro sporco tocca sempre a me"}),
    10391: (T + "«Io e il mio amato andiamo» — книжно", {"example_it": "Aspetta il ritorno del suo amato"}),
}

REPLACE = []

SPLIT_LATER = {}
