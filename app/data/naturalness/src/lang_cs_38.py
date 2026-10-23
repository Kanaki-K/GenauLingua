"""Вычитка чешского, порция p038 (B2–C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    18422: (T + "«můj malý syn» — книжно", {"example_cs": "V restauraci se malý syn zamkl na pánských záchodech a nemůže ven"}),
    18729: (T + "«svého» — лишнее", {"example_cs": "Nedávno jsem náhodou potkal starého kamaráda"}),
    18734: (T + "«příliš» — книжно", {"example_cs": "Jeho styl je na mě moc staromódní"}),
    18770: (T + "«Se svým současným» — тяжело", {"example_cs": "Se současným platem si nemůžu dovolit větší byt"}),
    18771: (T + "«raději» — книжно", {"example_cs": "Na sobotní večer je restaurace plně obsazená, radši půjdeme v pátek"}),
    18897: (T + "«mé» — лишнее", {"example_cs": "S maturitou nejmladší dcery pro nás končí celá jedna epocha"}),
    19005: (T + "«můj syn» — лишнее", {"example_cs": "Po dlouhé přihrávce zezadu dal syn gól"}),
    19021: (T + "«mé sestry» — тяжело", {"example_cs": "Letos rodiče pořádají sestřinu svatbu na zahradě"}),
    19039: (T + "«můj syn» — лишнее", {"example_cs": "Při šipkách syn skoro vždycky trefí střed"}),
}

REPLACE = []

SPLIT_LATER = {}
