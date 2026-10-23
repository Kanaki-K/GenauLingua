"""Вычитка чешского, порция p001 (A1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    61: (T + "«výrokem» — не то слово, что в переводе", {"example_cs": "Co tím tvrzením myslíš?"}),
    117: (T + "«chutná sladce» — калька", {"example_cs": "Ta hruška je sladká"}),
    155: (T + "«běží pomalu» — калька", {"example_cs": "Počítač je nějaký pomalý"}),
    173: (T + "«Zůstávám» — не тот вид", {"example_cs": "Zůstanu doma, protože prší"}),
    195: (T + "«A ty» — лишнее", {"example_cs": "Půjdeš dnes večer s námi?"}),
    223: (T + "«toaleta» — книжно", {"example_cs": "Promiňte, kde je tady záchod?"}),
    310: (T + "«dát vodu» — калька", {"example_cs": "Podáš mi vodu?"}),
    328: (T + "«zaneprázdněný» — книжно", {"example_cs": "Zrovna mám práci"}),
    358: (T + "«Mnoho pozdravů» — калька", {"example_cs": "Vyřiď pozdrav celé rodině"}),
    517: (T + "«chutná skvěle» — калька", {"example_cs": "Ten koláč je výborný"}),
    527: (T + "«jíst spolu» — коряво", {"example_cs": "Zítra můžeme jít spolu na oběd"}),
}

REPLACE = []

SPLIT_LATER = {}
