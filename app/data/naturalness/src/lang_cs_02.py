"""Вычитка чешского, порция p002 (A1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    540: (T + "«příliš hlasitá» — книжно", {"example_cs": "Ta hudba hraje strašně nahlas"}),
    734: (T + "«prospekt» — в чешском скорее «leták»", {"example_cs": "Vezmi si s sebou leták"}),
    780: (T + "«Polévka potřebuje» — калька", {"example_cs": "Do polévky to chce ještě trochu soli"}),
    800: (T + "«chutná dobře» — калька", {"example_cs": "To mi chutná"}),
    871: (T + "«příliš pozdě» — книжно", {"example_cs": "Už je moc pozdě"}),
    986: (T + "«hodně na práci» — коряво", {"example_cs": "Je toho hodně k udělání"}),
    1041: (T + "«vítáme» → «vítejte», как в переводе", {"example_cs": "Srdečně vítejte!"}),
}

REPLACE = []

SPLIT_LATER = {}
