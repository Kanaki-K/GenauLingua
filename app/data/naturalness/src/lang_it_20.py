"""Вычитка итальянского, порция p020 (B1), 23.10: досуг и здоровье — «volentieri», кальки, повторы"""

T = "вычитка итальянского: "

FIXES = {
    12117: (T + "«va volentieri a caccia» — калька gern", {"example_it": "Mio suocero in autunno va a caccia"}),
    12163: (T + "«Prendiamo i remi e remiamo» — тавтология", {"example_it": "Ho perso un remo, giriamo in tondo!"}),
    12485: (T + "«mi fanno male tutte le ossa» — без ситуации", {"example_it": "Con quest'umidità mi fanno male le ossa"}),
    12501: (T + "учебниково", {"example_it": "In ufficio gira un virus"}),
    12518: (T + "«non è più così buona» — калька", {"example_it": "Con l'età la memoria non è più quella di una volta"}),
    12545: (T + "«Ho bisogno di una visita medica» — без ситуации", {"example_it": "Per la squadra di calcio serve un certificato medico"}),
    12559: (T + "«Devi prendere la medicina» — без ситуации", {"example_it": "Questa medicina va presa prima dei pasti"}),
    12588: (T + "«odiare come la peste» — не та идиома", {"example_it": "Quel tipo di persone lo evito come la peste"}),
    12602: (T + "учебниково", {"example_it": "All'ecografia si sente il battito cardiaco del bambino"}),
    12630: (T + "«sudo e mi bagno tutto» — громоздко", {"example_it": "Quando fa caldo sudo tantissimo"}),
    12727: (T + "повтор 12967 «viene da mia nonna / aiuta l'anziano»", {"example_it": "L'infermiere di notte è gentilissimo con i pazienti"}),
}

REPLACE = []

SPLIT_LATER = {}
