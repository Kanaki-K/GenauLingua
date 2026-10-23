"""Вычитка чешского, порция p021 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    13175: (T + "«svého» — лишнее", {"example_cs": "Moje žena je objednaná u gynekologa"}),
    13203: (T + "«mám ztuhlost» — калька", {"example_cs": "Z dlouhého sezení u notebooku mám pořád ztuhlou šíji"}),
    13440: (T + "«pomoci» — книжно", {"example_cs": "S čím ti můžu pomoct?"}),
    13448: (T + "время: будешь лучше", {"example_cs": "Čím víc cvičíš, tím budeš lepší"}),
    13575: (T + "«této» — книжно", {"example_cs": "To je jeho páté vítězství v téhle sezóně"}),
    13599: (T + "«jsou čtyři a půl» — без «roku» коряво", {"example_cs": "Synovi jsou teď čtyři a půl roku"}),
    13631: (T + "«potřebuje oblečení» — калька", {"example_cs": "Miminko je nahé, musíme ho obléct"}),
    13645: (T + "«na mé bundě» — калька", {"example_cs": "Na bundě mi chybí knoflík"}),
    13663: (T + "«velmi» — книжно", {"example_cs": "Ta restaurace je hodně elegantní"}),
    13706: (T + "«beru župan» — калька", {"example_cs": "Po sauně si hned obléknu župan"}),
    13720: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju nové plavky na dovolenou"}),
    13761: (T + "«oblékám» — не тот вид", {"example_cs": "V téhle zimě si pod kalhoty obléknu punčocháče"}),
    13899: (T + "«tohoto» — книжно", {"example_cs": "Jaký význam má tohle slovo?"}),
    13916: (T + "«příliš» — книжно", {"example_cs": "Varování před bouří přišlo moc pozdě"}),
    13951: (T + "«velmi» — книжно", {"example_cs": "Je to drahé, ale na druhou stranu hodně dobré"}),
    13952: (T + "«Mohu» — книжно", {"example_cs": "Můžu navrhnout něco jiného?"}),
    13960: (T + "«své» — лишнее", {"example_cs": "Neumím moc dobře vyjadřovat pocity"}),
    13985: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju písemné potvrzení z banky"}),
    13996: (T + "«velmi» — книжно", {"example_cs": "Jeho příspěvek do diskuse byl hodně cenný"}),
}

REPLACE = []

SPLIT_LATER = {}
