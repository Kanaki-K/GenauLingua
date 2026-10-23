"""Вычитка чешского, порция p016 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    7718: (T + "«velmi» — книжно", {"example_cs": "Času je strašně málo, musíme si pospíšit"}),
    7864: (T + "«velmi» — книжно", {"example_cs": "Cesta je hodně strmá, musíme jít nahoru pomalu"}),
    7889: (T + "man — безлично", {"example_cs": "Katalog se dá objednat zdarma"}),
    7951: (T + "«své» — лишнее", {"example_cs": "Chtěl bych dát pryč staré kolo"}),
    8102: (T + "«Tento … velmi» — книжно", {"example_cs": "Tenhle nový seriál je mezi mladými hodně populární"}),
    8135: (T + "«příliš» — книжно", {"example_cs": "Řidič zmáčkl brzdu moc pozdě"}),
    8166: (T + "«Ve svém životě … mnoho» — книжно", {"example_cs": "V životě prožila hodně těžkých chvil"}),
    8227: (T + "«Toto … příliš mnoho» — книжно", {"example_cs": "Tohle auto spotřebuje moc benzínu"}),
    8303: (T + "«Touto» — книжно", {"example_cs": "Tou kosou jsem posekal trávu"}),
    8612: (T + "без подлежащего «to»", {"example_cs": "Někdy to trvá tři týdny, než dopis dojde"}),
    8653: (T + "«blikat» — не то слово", {"example_cs": "Než odbočíš, nezapomeň zablikat"}),
    8660: (T + "«listy» — не о листве", {"example_cs": "Na podzim je listí fialové a červené"}),
    8671: (T + "«velmi rušné» — книжно", {"example_cs": "Večer je na náměstí hodně rušno"}),
    8746: (T + "«velmi zaneprázdněný» — книжно", {"example_cs": "Dneska jsem hodně vytížený"}),
    8758: (T + "«Moje kariéra je pro mě» — калька", {"example_cs": "Na kariéře mi hodně záleží"}),
    8765: (T + "«Tato» — книжно", {"example_cs": "Tahle místnost slouží jako kancelář"}),
    8766: (T + "падеж: «vůdcem»", {"example_cs": "Je vůdcem naší skupiny"}),
    8778: (T + "«Můj počítač stojí» — калька", {"example_cs": "Počítač mám na psacím stole"}),
    8782: (T + "«mnoho» — книжно", {"example_cs": "Na farmě žije spousta zvířat"}),
    8808: (T + "«vždy» — книжно", {"example_cs": "Výplata mi chodí vždycky na konci měsíce"}),
    8814: (T + "«Moje směna» — калька", {"example_cs": "Směna mi začíná v šest"}),
    8816: (T + "«tuto» — книжно", {"example_cs": "Poradce mi doporučil tuhle investici"}),
}

REPLACE = []

SPLIT_LATER = {}
