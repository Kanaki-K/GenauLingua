"""Вычитка чешского, порция p047 (C2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    11489: (T + "«své» — лишнее", {"example_cs": "Je fakt zodpovědná a stará se o kolegy"}),
    11493: (T + "«Moje» — лишнее", {"example_cs": "Sestra je pokrytkyně: káže o zdravé stravě a potají jí chipsy"}),
    11513: (T + "«velmi» — книжно", {"example_cs": "Hrnčířství je hodně smyslná práce, cítíš hlínu pod rukama"}),
    11519: (T + "«můj» — лишнее", {"example_cs": "Při očkování se malý syn statečně drží a vůbec nepláče"}),
    11520: (T + "«moje … zůstává» — порядок", {"example_cs": "Imponuje mi, jak sestra zůstává klidná se třemi malými dětmi"}),
    11531: (T + "«přináší překvapení» — калька", {"example_cs": "Vyúčtování služeb nás letos nepříjemně překvapilo"}),
    11582: (T + "«Moje» — лишнее", {"example_cs": "Rozvážná sestra zůstane klidná, i když se auto porouchá na dálnici"}),
    11595: (T + "«až příliš» — книжно", {"example_cs": "Je až moc důvěřivý a naletí na každý trik"}),
    11603: (T + "«Můj strýc» — лишнее", {"example_cs": "Strejda je trochu neomalený, ale má velké srdce"}),
    11907: (T + "«tohoto» → «tohohle»", {"example_cs": "Nejdůležitější přísadou do tohohle receptu je čerstvé máslo"}),
    11973: (T + "«Miluji … můj» — книжно", {"example_cs": "Miluju mořské plody, ale manžel ne"}),
    11983: (T + "«Moje» — лишнее", {"example_cs": "Babička dělá výborné masové kuličky s bramborovou kaší"}),
    11998: (T + "«Můj» — лишнее", {"example_cs": "Prastrýc bohužel brzy propadl pití, v rodině se o tom nerado mluví"}),
    12010: (T + "«dochucuji» → «dochucuju»", {"example_cs": "Jídlo dochucuju čerstvými bylinkami"}),
    12017: (T + "«skutečná» — книжно", {"example_cs": "Pro tátu je nakládaný sleď pravá lahůdka"}),
    12369: (T + "«Můj … své školy» — тяжело", {"example_cs": "Syn je nejlepší nadhazovač ve školním baseballovém týmu"}),
    12379: (T + "«Můj» — лишнее", {"example_cs": "Nejlepší kamarád mi v desáté třídě přebral přítelkyni"}),
    12396: (T + "«mého» — лишнее", {"example_cs": "Rozlučková párty pro kolegu byla fakt pěkná"}),
    12961: (T + "«musel být odstraněn» — пассив", {"example_cs": "Nádor byl zhoubný a museli ho odstranit"}),
    12963: (T + "«by nemohl s námi» — порядок", {"example_cs": "Náš pes je očkovaný proti vzteklině, jinak by s námi nesměl do Chorvatska"}),
    12964: (T + "«Můj» — лишнее", {"example_cs": "Synovec je sekundář a pořád má noční služby"}),
    12991: (T + "«Jak velká je moje závislost» — калька", {"example_cs": "Jakou mám závislost na mobilu, poznám, až když se vybije baterka"}),
    13004: (T + "«moje» — лишнее", {"example_cs": "V plném výtahu dostává kamarádka občas záchvat paniky"}),
    13014: (T + "«Moje» — лишнее", {"example_cs": "Sestra darovala kostní dřeň cizímu dítěti"}),
    13015: (T + "«Můj muž» — лишнее", {"example_cs": "Manžel je nevyléčitelný optimista, i v zácpě vidí jen to dobré"}),
    13033: (T + "«Moje» — лишнее", {"example_cs": "Prababička byla jako mladá žena kvůli tuberkulóze rok v sanatoriu"}),
    13051: (T + "«Moje … o svém dni» — калька", {"example_cs": "Kamarádka pracuje na patologii a u večeře radši nevypráví, jaký měla den"}),
    13070: (T + "«svém» — лишнее", {"example_cs": "Ve svépomocné skupině teď strýc úplně otevřeně mluví o problému s alkoholem"}),
    13073: (T + "«velmi» — книжно", {"example_cs": "Po ozařování je teta hodně unavená, ale nevzdává se"}),
    13082: (T + "«pochybuji o jeho» — тяжело", {"example_cs": "Kdo se v listopadu koupe v jezeře, o jeho duševním stavu pochybuju"}),
    13083: (T + "«dnes» → «dneska»", {"example_cs": "Dřív se o duševní nemoci skoro nemluvilo, dneska o tom lidi mluví otevřeněji"}),
    13090: (T + "«této» → «téhle»", {"example_cs": "Průměrná délka života v téhle zemi v posledních letech vzrostla"}),
    13092: (T + "«své vlastní» — лишнее", {"example_cs": "Od padesátých narozenin častěji přemýšlím o vlastní smrtelnosti"}),
    13099: (T + "«Můj … v mých» — калька", {"example_cs": "Masér mi v zádech najde každý uzel"}),
    13125: (T + "«dnes velmi» — книжно", {"example_cs": "Lepra je dneska hodně vzácná"}),
    13146: (T + "«dnes» → «dneska»", {"example_cs": "Teta je dneska bohužel indisponovaná a nemůže přijít na oslavu"}),
    13595: (T + "«dnes» → «dneska»", {"example_cs": "V důsledku stávky dneska nejede skoro žádný autobus"}),
    13605: (T + "«Můj … raději hraji» — книжно", {"example_cs": "Brácha má rád fotbal, kdežto já radši hraju šachy"}),
    13607: (T + "«Moje nové kolo» — калька", {"example_cs": "Nové kolo mě stálo skoro dva tisíce eur"}),
    13773: (T + "«Moje» — калька", {"example_cs": "Staré večerní šaty mi po dvaceti letech pořád padnou"}),
    14223: (T + "«tónu hlasu mámy» — тяжело", {"example_cs": "Podle tónu máminého hlasu v telefonu hned poznám, jestli se něco stalo"}),
    14240: (T + "«v mém kurzu» — лишнее", {"example_cs": "„Rozumím jen nádraží“ je rčení, které u nás v kurzu němčiny milují všichni"}),
    14247: (T + "«slabé slovo roku» — коряво", {"example_cs": "„Není to špatné“ je fakt slabé slovo, ten film byl fantastický!"}),
}

REPLACE = []

SPLIT_LATER = {}
