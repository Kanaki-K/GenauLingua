"""Вычитка итальянского, порция p016 (B1), 23.10: кальки, повторы («in autunno le foglie», «la chiave», «ne ha passate tante»), тавтологии"""

T = "вычитка итальянского: "

FIXES = {
    8056: (T + "«impacchetta tutto svelta» — коряво", {"example_it": "Il piccolo è svelto come uno scoiattolo"}),
    8058: (T + "«radicalmente corti» — калька", {"example_it": "Ho fatto un cambiamento radicale: capelli corti!"}),
    8145: (T + "повтор «colazione inclusa» (6819)", {"example_it": "L'abbonamento comprende dieci lezioni di yoga"}),
    8166: (T + "повтор 7017 «ne ha passate tante nella vita»", {"example_it": "In quegli anni ha vissuto momenti molto duri"}),
    8182: (T + "«I libri uno sopra l'altro» — повтор шаблона", {"example_it": "Le scatole sono impilate una sopra l'altra in cantina"}),
    8303: (T + "«con questa falce ho falciato» — тавтология", {"example_it": "Mio nonno taglia ancora l'erba con la falce"}),
    8380: (T + "«mostrarmi riconoscente» — книжно", {"example_it": "Ti sono molto riconoscente per l'aiuto"}),
    8401: (T + "«legare la valigia» — неживо", {"example_it": "Lega bene le bici sul tetto della macchina"}),
    8409: (T + "повтор «in autunno le foglie»", {"example_it": "Mi è caduto un bottone della giacca"}),
    8440: (T + "повтор «la chiave»", {"example_it": "Mi è sparito il caricabatterie"}),
    8595: (T + "«vogliono correre in giro» — калька", {"example_it": "I bambini scorrazzano in giardino"}),
    8660: (T + "повтор «in autunno le foglie»", {"example_it": "Mia figlia vuole una cameretta viola"}),
    8758: (T + "«La mia carriera è importante per me» — калька", {"example_it": "Per lei la carriera viene prima di tutto"}),
    8782: (T + "«vivono molti animali» — учебниково", {"example_it": "I bambini adorano passare le vacanze in fattoria"}),
    8829: (T + "«a Berlino» — без нужды", {"example_it": "Domani sono a Torino per lavoro"}),
}

REPLACE = []

SPLIT_LATER = {}
