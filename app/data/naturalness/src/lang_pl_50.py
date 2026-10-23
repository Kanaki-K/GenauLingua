"""Вычитка польского, порция p050 (C2), 23.10: лишние местоимения и кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    18060: (T + "«On» — лишнее", {"example_pl": "Obraca się w najwyższych sferach społeczeństwa"}),
    18063: (T + "«W mojej firmie» — калька", {"example_pl": "U nas w firmie godziny pracy są elastyczne, mogę zaczynać o siódmej albo o dziesiątej"}),
    18077: (T + "«mój» — лишнее", {"example_pl": "W okresie dojrzewania młodszy brat zmutował w porannego marudę"}),
    18098: (T + "«Mój» — лишнее", {"example_pl": "Brat lubi gotować eksperymentalnie, wczoraj były truskawki z pieprzem"}),
    18388: (T + "«nasza» — лишнее", {"example_pl": "Po imprezie kuchnia wygląda jak chlew"}),
    18399: (T + "«Nasz» — лишнее", {"example_pl": "Jamnik uważa się za psa obronnego i szczeka na każdego listonosza"}),
    18408: (T + "«Każdy sierpień … w naszym» — калька", {"example_pl": "Co roku w sierpniu jesteśmy w domku letniskowym nad jeziorem"}),
    18452: (T + "«Mój» — лишнее", {"example_pl": "Podnajemca zawsze płaci czynsz punktualnie pierwszego dnia miesiąca"}),
    18458: (T + "«Nasza» — лишнее", {"example_pl": "Kotka ciągle próbuje zajrzeć do łazienki przez dziurkę od klucza"}),
    18477: (T + "«Z powodu … nie będzie zaopatrzenia» — коряво", {"example_pl": "Przez roboty na naszej ulicy zaopatrzenie w wodę jest dziś do południa wstrzymane"}),
    18911: (T + "«były to» — книжно", {"example_pl": "Kiedy spoglądam wstecz, to były szczęśliwe lata"}),
}

REPLACE = []

SPLIT_LATER = {}
