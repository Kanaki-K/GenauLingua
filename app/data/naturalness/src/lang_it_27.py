"""Вычитка итальянского, порция p027 (B2), 23.10: «volentieri», повторы, учебниковые и оборванные фразы"""

T = "вычитка итальянского: "

FIXES = {
    7109: (T + "«indovinare l'indovinello» — тавтология", {"example_it": "Indovina chi ho visto ieri!"}),
    7129: (T + "повтор 6990 «superare questo periodo difficile»", {"example_it": "Con un solo stipendio è dura cavarsela"}),
    7132: (T + "«Dobbiamo spegnere» — калька", {"example_it": "Spegni le candele prima di andare a letto"}),
    7137: (T + "без ситуации", {"example_it": "Guardiamo il sole tramontare sul mare"}),
    7142: (T + "«La formica è minuscola» — учебниково", {"example_it": "L'appartamento è minuscolo, ma in pieno centro"}),
    7161: (T + "«Volevano cacciarlo» — калька", {"example_it": "L'hanno buttato fuori dal bar"}),
    7180: (T + "«mangio volentieri» — калька; учебниково", {"example_it": "Feste, discorsi e cose del genere non fanno per me"}),
    7206: (T + "«Puoi portarlo fuori?» — без ситуации", {"example_it": "Puoi portare fuori la spazzatura?"}),
    7237: (T + "«perché non sto bene» — учебниково", {"example_it": "Se non passa, rivolgiti a un medico"}),
    7245: (T + "«pronta a partire per il viaggio» — громоздко", {"example_it": "Siete tutti pronti a partire?"}),
    7262: (T + "«potrei addormentarmi» — оборвано", {"example_it": "Sono talmente stanco che dormirei in piedi"}),
    7296: (T + "повтор 15831 «zanzare quest'estate»", {"example_it": "Il traffico è una vera piaga in questa città"}),
    7308: (T + "«Questo rafforza» — книжно", {"example_it": "Così il mio sospetto si rafforza ancora"}),
    7329: (T + "«Il pallone fluttua» — учебниково", {"example_it": "Le foglie fluttuano lente sull'acqua"}),
    7345: (T + "«di Berlino» — без нужды", {"example_it": "Abitiamo una ventina di chilometri a est di Bologna"}),
    7398: (T + "«Devo affilare» — калька", {"example_it": "Questo coltello non taglia più, bisogna affilarlo"}),
}

REPLACE = []

SPLIT_LATER = {}
