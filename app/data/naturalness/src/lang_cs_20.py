"""Вычитка чешского, порция p020 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    12122: (T + "«Můj … velmi» — книжно", {"example_cs": "Soupeř je hodně silný"}),
    12132: (T + "«se svou» — лишнее", {"example_cs": "Moje dcera si ráda hraje s panenkou"}),
    12139: (T + "«velmi» — книжно", {"example_cs": "Náš trenér je hodně přísný"}),
    12177: (T + "«super schön» → «nádherný»", {"example_cs": "Ohňostroj na Silvestra byl nádherný"}),
    12243: (T + "«velmi» — книжно", {"example_cs": "Je to zatím amatér, ale hodně talentovaný"}),
    12245: (T + "«stanujeme» — коряво", {"example_cs": "Příští víkend jedeme stanovat do hor"}),
    12247: (T + "«Můj otec» — книжно", {"example_cs": "Táta každý týden hraje loto"}),
    12363: (T + "«protahuji» — не тот вид", {"example_cs": "Před tréninkem si protáhnu svaly"}),
    12380: (T + "«kreslím» — не тот вид", {"example_cs": "Na dětskou oslavu nakreslím mapu pokladu"}),
    12501: (T + "«mnoho» — книжно", {"example_cs": "Kvůli tomu viru onemocní spousta lidí"}),
    12518: (T + "«Moje paměť» — калька", {"example_cs": "Paměť už mi tolik neslouží"}),
    12532: (T + "«velmi» — книжно", {"example_cs": "Po běhu mám hodně vysoký tep"}),
    12540: (T + "«tuto» — книжно", {"example_cs": "Existuje lék na tuhle nemoc?"}),
    12543: (T + "«velmi» — книжно", {"example_cs": "Heroin je hodně nebezpečná droga"}),
    12544: (T + "«Můj děda měl» — коряво", {"example_cs": "Děda bohužel dostal infarkt"}),
    12545: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju lékařské vyšetření"}),
    12547: (T + "«příliš» — книжно", {"example_cs": "Mám moc vysoký krevní tlak"}),
    12570: (T + "«na jeho čele» — калька", {"example_cs": "Jizvu po nehodě má na čele pořád vidět"}),
    12578: (T + "чешская поговорка — «Dávka dělá jed»", {"example_cs": "Dávka dělá jed"}),
    12583: (T + "«velmi» — книжно", {"example_cs": "Dlouhá nemoc ho hodně oslabila"}),
    12584: (T + "пассив — книжно", {"example_cs": "Nádor se musí odstranit operací"}),
    12602: (T + "«Tlukot jeho srdce» — калька", {"example_cs": "Má hodně rychlý tlukot srdce"}),
    12609: (T + "«Ovíjím» — не тот вид", {"example_cs": "Ovážu si ruku obvazem"}),
    12646: (T + "«svou starou matku» — книжно", {"example_cs": "Každý den pečuje o starou mámu"}),
    12896: (T + "«předepisuje» — не тот вид", {"example_cs": "Lékař jí předepsal antibiotikum"}),
    12953: (T + "«lépe» — книжно", {"example_cs": "Nová zubní protéza sedí mnohem líp"}),
    12962: (T + "«své» — лишнее", {"example_cs": "Kvůli nespavosti je unavený a podrážděný"}),
    12975: (T + "«Pro svou pohodu» — калька", {"example_cs": "Abych se cítil dobře, potřebuju každý den čerstvý vzduch"}),
}

REPLACE = []

SPLIT_LATER = {}
