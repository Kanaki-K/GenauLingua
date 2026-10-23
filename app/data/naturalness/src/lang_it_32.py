"""Вычитка итальянского, порция p032 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    11748: (T + 'повтор «la nonna prepara … per Natale»', {"example_it": 'I bambini hanno decorato i biscotti di Natale'}),
    11752: (T + 'нет слова карточки «causare»', {"example_it": 'Il cane ha causato un bel caos in soggiorno'}),
    11762: (T + '«troppo dura da mangiare» — книжно', {"example_it": 'La carne era dura, impossibile da tagliare'}),
    12188: (T + 'повтор 7336 «salita in seconda …»', {"example_it": 'La domenica gioca in una lega amatoriale'}),
    12209: (T + '«vogliamo solo oziare» — калька', {"example_it": 'Oggi oziamo a casa e basta'}),
    12235: (T + 'повтор 12282 «andare a giocare a bowling»', {"example_it": 'Il lunedì il bowling è chiuso'}),
    12282: (T + '«vogliamo andare» — калька', {"example_it": 'Venerdì andiamo a giocare a bowling con gli amici'}),
    12644: (T + '«Non si deve sputare» — калька', {"example_it": 'Non sputare per terra!'}),
    12653: (T + '«Devo riprendere fiato» — калька', {"example_it": 'Lasciami riprendere fiato un attimo'}),
    12686: (T + '«non ha spina dorsale, non ha coraggio» — калька', {"example_it": 'Si è fatto male alla spina dorsale cadendo'}),
    12825: (T + 'повтор 13067 «andiamo a trovarlo la domenica»', {"example_it": 'Da quando il nonno non riesce più ad alzarsi da solo, vive in una casa di cura'}),
}

REPLACE = []

SPLIT_LATER = {}
