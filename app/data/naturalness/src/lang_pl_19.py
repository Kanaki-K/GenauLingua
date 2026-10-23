"""Вычитка польского, порция p019 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    10432: (T + "«swój» — лишнее", {"example_pl": "Muszę przezwyciężyć strach"}),
    10448: (T + "«został odwołany» — пассив", {"example_pl": "Wielka szkoda, że odwołali mecz"}),
    10450: (T + "«swojej» — лишнее", {"example_pl": "Jest totalnie zakochany w koleżance z klasy"}),
    10456: (T + "«Mój» — лишнее", {"example_pl": "Syn jest bardzo uparty"}),
    10457: (T + "«Czuję tęsknotę za moją» — калька", {"example_pl": "Dopada mnie tęsknota za ojczyzną"}),
    10459: (T + "«Wątpię, że» — грамматика", {"example_pl": "Wątpię, żeby to się udało"}),
    10463: (T + "«on» — лишнее", {"example_pl": "Obawiam się, że nie przyjdzie"}),
    10547: (T + "«Dziś jest dla mnie» — калька", {"example_pl": "Dziś mam szczęśliwy dzień"}),
    10674: (T + "«każdego ranka» — книжно", {"example_pl": "Codzienny dojazd do pracy to prawdziwy koszmar"}),
    11134: (T + "«Mój» — лишнее", {"example_pl": "Klucz zniknął mi w tajemniczy sposób"}),
    11273: (T + "«Ona» — лишнее", {"example_pl": "Zachwyca się nowym nauczycielem"}),
    11352: (T + "нет «bei allen»", {"example_pl": "Nowy szef jest u wszystkich raczej nielubiany"}),
    11378: (T + "«on … z tym» — лишнее", {"example_pl": "Wierzę, że sobie poradzi"}),
    11468: (T + "«Mój» — лишнее", {"example_pl": "Tata jest niepoprawnym optymistą"}),
    11481: (T + "«Jest tak przytulnie leżeć» — грамматика", {"example_pl": "Tak przytulnie jest leżeć pod ciepłym kocem z dobrą książką"}),
    11494: (T + "«Moi» — лишнее", {"example_pl": "Rodzice są dość tolerancyjni, mogę wracać o północy"}),
    11698: (T + "«chętnie jem» — калька gern", {"example_pl": "Na śniadanie lubię boczek z jajkami"}),
    11705: (T + "«swoją» — лишнее", {"example_pl": "Pies bardzo szybko je karmę"}),
    11710: (T + "«swojego» — лишнее", {"example_pl": "Pies liże rękę właściciela"}),
    11822: (T + "«Czy» — книжно", {"example_pl": "Tę rybę można jeść na surowo?"}),
    11846: (T + "«Jakie jest twoje» — калька", {"example_pl": "Jakie masz ulubione jedzenie?"}),
    11859: (T + "«Moja» — лишнее", {"example_pl": "Babcia piecze najlepszą szarlotkę"}),
    11906: (T + "«moich» — лишнее", {"example_pl": "W czasie ramadanu wielu kolegów pości"}),
    11928: (T + "«Mój» — лишнее", {"example_pl": "Syn najbardziej lubi surową marchewkę"}),
    11943: (T + "«ich» — лишнее", {"example_pl": "Dzieci pochłonęły wszystkie słodycze, które przyniosła babcia"}),
    11946: (T + "«w zimie» → «zimą»", {"example_pl": "Ciepła owsianka smakuje szczególnie dobrze zimą"}),
    11947: (T + "«Mój» — лишнее", {"example_pl": "Syn je brokuły tylko z dużą ilością sera"}),
    11971: (T + "«Mój» — лишнее", {"example_pl": "Syn najbardziej lubi paluszki rybne z puree ziemniaczanym"}),
    12004: (T + "«Moja» — лишнее", {"example_pl": "Córka ma alergię na orzeszki ziemne"}),
    12007: (T + "«czyni ciekawszym» — книжно", {"example_pl": "Odrobina przyprawy sprawia, że jedzenie jest dużo ciekawsze"}),
}

REPLACE = []

SPLIT_LATER = {}
