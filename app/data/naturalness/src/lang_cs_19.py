"""Вычитка чешского, порция p019 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    10432: (T + "«svůj» — лишнее", {"example_cs": "Musím překonat strach"}),
    10450: (T + "«své» — лишнее", {"example_cs": "Je úplně zamilovaný do spolužačky"}),
    10456: (T + "«velmi» — книжно", {"example_cs": "Můj syn je hrozně tvrdohlavý"}),
    10548: (T + "«se svými cíli» — тяжело", {"example_cs": "S cíli musíme být realističtí"}),
    11134: (T + "«Můj klíč» — калька", {"example_cs": "Klíč mi záhadně zmizel"}),
    11136: (T + "«Každodenní život» — книжно", {"example_cs": "Všední dny jsou teď dost hektické"}),
    11273: (T + "«svého» — лишнее", {"example_cs": "Je úplně blázen do nového učitele"}),
    11466: (T + "«velmi» — книжно", {"example_cs": "Rozhovor s doktorkou byl hodně povzbudivý"}),
    11588: (T + "«obava byla správná» — калька", {"example_cs": "Moje obava se potvrdila: vlak zrušili"}),
    11650: (T + "«Připijme» — книжно", {"example_cs": "Pojďme si připít šampaňským!"}),
    11687: (T + "«Míchám» — не тот вид", {"example_cs": "Zamíchám kávu lžičkou"}),
    11704: (T + "«Míchám» — не тот вид", {"example_cs": "Smíchám přísady na koláč"}),
    11705: (T + "«své … velmi» — книжно", {"example_cs": "Pes sežere krmivo hrozně rychle"}),
    11708: (T + "«polyká s vodou» — калька", {"example_cs": "Dítě spolkne tabletu a zapije ji vodou"}),
    11710: (T + "«svého majitele» — калька", {"example_cs": "Pes olizuje páníčkovi ruku"}),
    11786: (T + "без глагола — коряво", {"example_cs": "Můžu si přidat ještě trochu omáčky?"}),
    11792: (T + "«Ke dezertu» — калька", {"example_cs": "Jako dezert je zmrzlina s jahodami"}),
    11837: (T + "man — безлично", {"example_cs": "U pultu se dá koupit i dort s sebou"}),
    11891: (T + "«Pro osvěžení» — калька", {"example_cs": "Na osvěženou skočíme do jezera"}),
    11959: (T + "«loupu» — не тот вид", {"example_cs": "K snídani si oloupu pomeranč"}),
    11960: (T + "«milují při sledování» — калька", {"example_cs": "Děti si u filmu nejradši dávají gumové medvídky"}),
    11963: (T + "«krájím» — не тот вид", {"example_cs": "Do polévky nakrájím celer nadrobno"}),
    11969: (T + "«Raději» — книжно", {"example_cs": "Radši piju neperlivou vodu než minerálku"}),
    11986: (T + "«příliš» — книжно", {"example_cs": "Jídlo v restauraci bylo na mě moc mastné"}),
    11991: (T + "«pijeme» — не тот вид", {"example_cs": "Po jídle si dáme likér"}),
}

REPLACE = []

SPLIT_LATER = {}
