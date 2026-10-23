"""Вычитка чешского, порция p039 (C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    7805: (T + "«mého syna» — лишнее", {"example_cs": "Děti v synově třídě jsou zčásti šestileté, zčásti už osmileté"}),
    7816: (T + "«svým» — лишнее", {"example_cs": "Manžel se pořád nemůže rozloučit se starým ošuntělým svetrem, i když má díry na loktech"}),
    7824: (T + "«mých rodičů» — лишнее", {"example_cs": "U rodičů ve vesnici je znát proměna: kde býval řezník, je teď veganská kavárna"}),
    7886: (T + "«mého tchána» — тяжело", {"example_cs": "Tchánův bramborový salát je prvotřídní, ale recept neprozradí"}),
    7917: (T + "«velmi» — книжно", {"example_cs": "Teta má hodně jemný způsob, jak dát najevo, že jí jídlo nechutná"}),
    7921: (T + "«uskutečňuji» — книжно", {"example_cs": "Novoroční předsevzetí většinou uskutečním jen do poloviny ledna"}),
    7946: (T + "«své ženy» — лишнее", {"example_cs": "Po hádce se bratr snaží květinami získat zpět důvěru manželky"}),
    7953: (T + "«Moje školní latina» — калька", {"example_cs": "Školní latinu mám úplně zarezlou"}),
    7987: (T + "«je můj pracovní den» — калька", {"example_cs": "Kvůli spoustě porad mám pracovní den úplně rozkouskovaný"}),
    7998: (T + "«a hledali» — коряво", {"example_cs": "Kvůli snubnímu prstenu jsme pročesali celý dům, a byl v kapse od kalhot"}),
    8000: (T + "порядок слов", {"example_cs": "Když dcera čte, ponoří se do knihy tak, že mě vůbec neslyší"}),
    8022: (T + "«můj klub» — лишнее", {"example_cs": "Jestli náš klub dneska prohraje, sestoupí do druhé ligy"}),
    8035: (T + "«velmi» — книжно", {"example_cs": "Naše porodní asistentka je hodně zkušená, pomohla na svět už víc než tisíci dětem"}),
    8038: (T + "«tvůj hlas přichází» — калька", {"example_cs": "Je špatné spojení, slyším tě úplně trhaně"}),
    8044: (T + "«o svém koni» — лишнее", {"example_cs": "Když dcera vypráví o koni, oči jí jiskří"}),
    8076: (T + "«získala zpět zrak» — калька", {"example_cs": "Po operaci šedého zákalu se babičce skoro úplně vrátil zrak"}),
    8186: (T + "«dnes» → «dneska»", {"example_cs": "Kafe je dneska strašně silné, dal jsi tři lžičky?"}),
    8941: (T + "«ze svého» — лишнее", {"example_cs": "Na masopust se syn převléká za lovce odměn z oblíbeného seriálu"}),
    8988: (T + "«považuje za» — книжно", {"example_cs": "Ve starých filmech má každá bohatá rodina služebnou a dceři to přijde nespravedlivé"}),
    8992: (T + "«Moje teta» — лишнее", {"example_cs": "Teta je nadporučík u námořnictva a na synovu svatbu přijde v uniformě"}),
    8993: (T + "«Moje desetiletá dcera» — лишнее", {"example_cs": "Desetiletá dcera je teď odbornice na ptáky a opravuje i průvodce v muzeu"}),
    9008: (T + "«své odstoupení» — лишнее", {"example_cs": "Po třiceti letech u dětského fotbalového týmu táta oznámil odstoupení z funkce trenéra"}),
    9012: (T + "«Můj děda» — лишнее", {"example_cs": "Děda byl jen svobodník, ale vypráví historky, jako by velel celé armádě"}),
    9015: (T + "«vytvářela» — книжно", {"example_cs": "V hotelu pokojská každý den poskládala z ručníků jiné zvíře a děti byly nadšené"}),
    9026: (T + "«z mé kanceláře» — лишнее", {"example_cs": "Ve výplatní den chodí kolegové z kanceláře vždycky spolu na kebab"}),
    9046: (T + "«Dědeček mé kamarádky» — тяжело", {"example_cs": "Kamarádčin děda byl bankéř v Curychu a naučil ji zapisovat si každý cent"}),
    9061: (T + "«mnozí» — книжно", {"example_cs": "Demolice starého kina rozesmutnila celou ulici, spousta lidí tam měla první rande"}),
    9072: (T + "«zhotoví … takové» — книжно", {"example_cs": "Truhlář nám vyrobí vyvýšenou postel přesně na míru, protože dětský pokoj má šikmé stěny"}),
    9077: (T + "«svůj» — лишнее", {"example_cs": "Na masopust jde syn za policistu a každému hostovi hrdě ukazuje papírový služební odznak"}),
}

REPLACE = []

SPLIT_LATER = {}
