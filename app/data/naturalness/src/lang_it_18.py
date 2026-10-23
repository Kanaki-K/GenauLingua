"""Вычитка итальянского, порция p018 (B1), 23.10: чувства и характер — кальки, повторы, учебниковые фразы"""

T = "вычитка итальянского: "

FIXES = {
    10112: (T + "«Tu ne sei responsabile» — книжно", {"example_it": "Il responsabile sei tu"}),
    10150: (T + "«Vuole vendetta per tutto» — коряво", {"example_it": "Pensa solo alla vendetta"}),
    10152: (T + "без ситуации", {"example_it": "Dopo la festa tutta la casa è sottosopra"}),
    10184: (T + "«Riesco a sentire il vento» — калька", {"example_it": "Senti questa corrente?"}),
    10190: (T + "«Preghiamo ogni sera» — учебниково", {"example_it": "La nonna prega ogni sera"}),
    10215: (T + "«La perdita mi rende triste» — калька", {"example_it": "La perdita del cane l'ha colpita molto"}),
    10218: (T + "«Dovresti comportarti meglio» — калька", {"example_it": "Comportati bene dalla nonna, eh?"}),
    10220: (T + "«il bambino è molto buono» — учебниково", {"example_it": "Oggi il piccolo è stato buonissimo"}),
    10241: (T + "«coraggiosamente» — коряво", {"example_it": "I bambini sono stati coraggiosi dal dentista"}),
    10256: (T + "«Io, scemo» — калька", {"example_it": "E io, come uno scemo, ho lasciato la luce accesa"}),
    10267: (T + "нет слова карточки «il punto debole»", {"example_it": "Il cioccolato è il mio punto debole"}),
    10285: (T + "без ситуации", {"example_it": "La polizia cerca ancora il motivo del delitto"}),
    10288: (T + "повтор 10164 «imbarazzante per me»", {"example_it": "Il rumore del trapano è molto spiacevole"}),
    10296: (T + "повтор 10098 «contro la mia volontà»", {"example_it": "Con un po' di volontà ce la fai"}),
    10298: (T + "«visione chiara della mia vita» — калька", {"example_it": "La nuova direttrice ha una visione chiara per l'azienda"}),
    10321: (T + "«Volevi spaventarmi» — неживо", {"example_it": "Mi hai spaventato!"}),
    10324: (T + "«Qual è il tuo dispiacere?» — калька", {"example_it": "Che dispiacere vederti così triste"}),
    10335: (T + "«ha un odore disgustoso» — калька", {"example_it": "Nel frigo c'è un odore disgustoso"}),
    10338: (T + "повтор 10295 «è disgustoso»", {"example_it": "Questa minestra è schifosa!"}),
    10347: (T + "«Sono proprio feccia» — коряво", {"example_it": "Quei tipi sono feccia"}),
    10356: (T + "«Con il cibo attiri» — коряво", {"example_it": "Con un po' di prosciutto attiri il gatto in casa"}),
    10371: (T + "«difenderti dal bullismo» — книжно", {"example_it": "Difenditi, non lasciarti mettere i piedi in testa"}),
    10372: (T + "«Non mi spaventa niente così facilmente» — коряво", {"example_it": "I temporali spaventano molto il mio cane"}),
    10404: (T + "учебниково", {"example_it": "Senza disciplina non si arriva da nessuna parte"}),
    10405: (T + "«Lavora molto concentrato» — калька", {"example_it": "Non disturbarlo, è molto concentrato"}),
    10406: (T + "«atteggiamento verso il lavoro» — книжно", {"example_it": "Ha sempre un atteggiamento positivo"}),
    10409: (T + "повтор 10179 «gelosa di sua sorella»", {"example_it": "È un po' invidioso della mia macchina nuova"}),
}

REPLACE = []

SPLIT_LATER = {}
