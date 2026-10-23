"""Вычитка чешского, порция p029 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    8707: (T + "«své» — лишнее", {"example_cs": "Syn zdokonalil auto z lega, teď má dokonce dálkové ovládání"}),
    8869: (T + "«dělá koktejl» — калька", {"example_cs": "Barman mi namíchá koktejl"}),
    8871: (T + "«mé» — книжно", {"example_cs": "Medicína je moje poslání"}),
    8942: (T + "«od svého otce» — книжно", {"example_cs": "Učí se řemeslu od táty"}),
    8945: (T + "«Můj otec … našich» — книжно", {"example_cs": "Táta je přísný strážce rodinných tradic"}),
    8955: (T + "«naléhavě» — книжно", {"example_cs": "Moje klientka se chce rozvést a nutně potřebuje termín"}),
    8963: (T + "«Tento» — книжно", {"example_cs": "Tenhle týden musím zase dělat noční směnu"}),
    8979: (T + "«svou» — лишнее", {"example_cs": "Můj synovec chce za každou cenu být hasičem a každý den nosí červenou helmu"}),
    8985: (T + "«svou» — лишнее", {"example_cs": "Děda má pořád starou diplomatku z osmdesátých let s číselným zámkem"}),
    8998: (T + "«velmi» — книжно", {"example_cs": "Pisatel toho anonymního dopisu zřejmě naši rodinu hodně dobře zná"}),
    9039: (T + "«S touto» — книжно", {"example_cs": "S touhle kartou můžu provést nákup do padesáti eur bez PINu"}),
    9169: (T + "«tento» — книжно", {"example_cs": "Moje jméno ještě není na výplatní listině, proto jsem tenhle měsíc nedostal peníze"}),
    9206: (T + "«tento» — книжно", {"example_cs": "Kvůli stavebním pracím tenhle týden nejezdí tramvaj a všichni se mačkají v autobuse"}),
    9210: (T + "«tento» — книжно", {"example_cs": "Manžel je tenhle týden služebně v Hamburku, takže děti do školy vozím sama"}),
    9486: (T + "«Moji rodiče» — книжно", {"example_cs": "Rodiče neměli šanci na vzdělání, a proto pro ně naše studium tolik znamenalo"}),
    9511: (T + "«příliš» — книжно", {"example_cs": "Na promoci měl rektor strašně dlouhý projev"}),
    9538: (T + "«vyvozuji» — книжно", {"example_cs": "Z jeho mlčení vyvozuju závěr, že je pořád uražený"}),
    9787: (T + "«svůj … své» — лишнее", {"example_cs": "Uděláme výměnu, ty mi dáš sendvič a já ti dám brambůrky"}),
    9821: (T + "«daroval» — книжно", {"example_cs": "K zásnubám jí dal prsten s malým diamantem"}),
    10097: (T + "«velmi» — книжно", {"example_cs": "Jeho laskavost mě hodně dojala"}),
    10391: (T + "«Můj milý a já» — калька", {"example_cs": "S mým milým jedeme spolu na dovolenou"}),
}

REPLACE = []

SPLIT_LATER = {}
