"""Вычитка чешского, порция p050 (C2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    18063: (T + "«V mé firmě» — калька", {"example_cs": "U nás ve firmě je pracovní doba variabilní, můžu začínat v sedm nebo v deset"}),
    18086: (T + "«svou» — лишнее", {"example_cs": "Na novou mraženou pizzu hledá firma ještě testovací osoby"}),
    18101: (T + "«V mém románu» — смысл", {"example_cs": "V tom sci-fi románu, co čtu, létá vesmírná loď na antihmotu"}),
    18388: (T + "«naše» — лишнее", {"example_cs": "Po večírku vypadá kuchyně jako chlív"}),
    18394: (T + "«mým rodičům» — книжно", {"example_cs": "Příští měsíc se stěhujeme na předměstí, abychom byli blíž k našim"}),
    18408: (T + "«v našem letním domě» — калька", {"example_cs": "Každý srpen trávíme na chatě u jezera"}),
    18421: (T + "«svém … příliš» — книжно", {"example_cs": "Babička má v malém obýváku moc velký lustr"}),
    18434: (T + "«mé» — лишнее", {"example_cs": "Rozhovor s učitelkou rozptýlil všechny pochybnosti"}),
    18452: (T + "«Můj … vždy» — книжно", {"example_cs": "Podnájemník mi platí nájem vždycky včas, prvního v měsíci"}),
    18456: (T + "«našeho domu» — тяжело", {"example_cs": "U nás ve vstupní hale stojí už týdny cizí kolo"}),
    18477: (T + "«dnes» → «dneska»", {"example_cs": "Kvůli stavebním pracím bude dneska v naší ulici do poledne přerušené zásobování vodou"}),
    18859: (T + "«Naše noční procházky» — калька", {"example_cs": "Noční procházky se psem jsou pro nás nejklidnější část dne"}),
    18902: (T + "«své» — лишнее", {"example_cs": "Děda sepisuje vzpomínky pro potomky, plnicím perem"}),
    18908: (T + "«Miminko sousedů» — тяжело", {"example_cs": "Sousedovic miminko už hodiny nepřetržitě křičí"}),
    18911: (T + "«ohlédnu zpět» — плеоназм", {"example_cs": "Když se ohlédnu, byla to šťastná léta"}),
    18929: (T + "«dnes» → «dneska»", {"example_cs": "Tehdy to bylo úplně normální, ale dneska by to nikdo neudělal"}),
    18930: (T + "«právě» → «zrovna»", {"example_cs": "Autobus jezdí jen každou hodinu a zrovna nám ujel"}),
    18943: (T + "«Toto» → «Tohle»", {"example_cs": "Tohle přátelství přetrvalo spoustu krizí"}),
}

REPLACE = []

SPLIT_LATER = {}
