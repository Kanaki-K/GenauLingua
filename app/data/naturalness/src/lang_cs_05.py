"""Вычитка чешского, порция p005 (A2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    1184: (T + "«příliš mnoho» — книжно", {"example_cs": "Utrácím moc peněz"}),
    1223: (T + "«se svými dětmi vyrábím» — тяжело", {"example_cs": "Rád s dětmi něco vyrábím"}),
    1232: (T + "«Ukončeme» — книжно", {"example_cs": "Pojďme ten rozhovor tady ukončit, musím běžet"}),
    1306: (T + "«chatuji s přáteli» — книжно", {"example_cs": "Zrovna si píšu s kamarády"}),
    1570: (T + "«Děti dostanou každé» — коряво", {"example_cs": "Každé dítě dostane dvě eura"}),
    1658: (T + "Sie — обращение к продавцу", {"example_cs": "Kdy nám dovezete ten gauč?"}),
    1682: (T + "«Jaký je tvůj názor» — калька", {"example_cs": "Jaký na to máš názor?"}),
    1718: (T + "«V okolí» — не то слово", {"example_cs": "Poblíž je supermarket"}),
    2087: (T + "«na webové stránce» — книжно", {"example_cs": "Otevírací doba je na webových stránkách"}),
    2285: (T + "«Stěžuji si u» — калька", {"example_cs": "Půjdu si stěžovat vedoucímu"}),
    2810: (T + "«Pořad běží» — калька", {"example_cs": "Ten pořad dávají ve 20 hodin"}),
}

REPLACE = []

SPLIT_LATER = {}
