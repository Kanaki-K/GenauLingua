"""Вычитка чешского, порция p024 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    15943: (T + "«velmi» — книжно", {"example_cs": "Anglická královna byla hodně oblíbená"}),
    15947: (T + "«Miluji svou» — книжно", {"example_cs": "Miluju svobodu"}),
    15950: (T + "Knast — разговорное «basa»", {"example_cs": "Byl tři roky v base"}),
    15951: (T + "«Potřebuji pro to» — калька", {"example_cs": "Na to potřebuju důkaz"}),
    16049: (T + "«svou» — лишнее", {"example_cs": "Děda změnil závěť"}),
    16080: (T + "«tento» — книжно", {"example_cs": "Policie ten případ vyšetřuje"}),
    16084: (T + "«uzavírá» — не тот вид", {"example_cs": "Policie kvůli nehodě uzavřela silnici"}),
    16091: (T + "«stále» — книжно", {"example_cs": "Vyšetřování pořád probíhá"}),
    16092: (T + "doch — потеряно", {"example_cs": "Nejsem přece tvůj otrok!"}),
    16099: (T + "«Chtěl bych chránit své» — книжно", {"example_cs": "Chci si chránit soukromí"}),
    16106: (T + "«Můj všední den» — калька", {"example_cs": "Všední dny mám dobře uspořádané"}),
    16111: (T + "«velmi» — книжно", {"example_cs": "Fanoušci fotbalového klubu jsou hodně věrní"}),
    16120: (T + "«velmi» — книжно", {"example_cs": "Vládce Dubaje je strašně bohatý"}),
    16123: (T + "«V mnoha … stále» — книжно", {"example_cs": "Spousta zemí ještě pořád vykonává popravy"}),
    16142: (T + "«mnoho» — книжно", {"example_cs": "V boji bylo hodně raněných"}),
    16169: (T + "«Toto» — книжно", {"example_cs": "Tohle město má asi 50000 obyvatel"}),
    16218: (T + "«zakazuji» — книжно", {"example_cs": "To ti zakazuju"}),
    16469: (T + "«tomto … velmi» — книжно", {"example_cs": "Právní situace je v tomhle případě hodně složitá"}),
    17072: (T + "«velmi» — книжно", {"example_cs": "Tunel je hodně dlouhý a tmavý"}),
    17084: (T + "«Moje kolo je» — калька", {"example_cs": "Mám rozbité kolo, musím jít pěšky"}),
    17103: (T + "«Dříve» — книжно", {"example_cs": "Dřív lidé jezdili kočárem"}),
    17116: (T + "«Nádrž v mém autě» — калька", {"example_cs": "V autě mám skoro prázdnou nádrž"}),
    17131: (T + "«Přecházíme» — не тот вид", {"example_cs": "Přejdeme ulici u semaforu"}),
}

REPLACE = []

SPLIT_LATER = {}
