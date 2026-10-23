"""Вычитка итальянского, порция p028 (B2), 23.10: книжные короткие примеры → разговорные"""

T = "вычитка итальянского: "

FIXES = {
    7476: (T + "«spetta un grande ringraziamento per questo» — книжно", {"example_it": "Il merito spetta tutto a lui"}),
    7509: (T + "«infliggere dolore» — книжно", {"example_it": "Le sue parole mi hanno causato molto dolore"}),
    7818: (T + "«Quello che fai rasenta» — книжно", {"example_it": "La tua idea rasenta la follia!"}),
    8113: (T + "«quando parla con il capo» — странно", {"example_it": "Al telefono ha camuffato la voce per farmi uno scherzo"}),
    8116: (T + "«senza nessuna colpa» — книжно", {"example_it": "Sono finito dentro la loro lite senza volerlo"}),
}

REPLACE = []

SPLIT_LATER = {}
