"""Вычитка чешского, порция p011 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    2149: (T + "«Domluvme se» — книжно", {"example_cs": "Rychle se domluvíme, kdo co přinese"}),
    2152: (T + "«svou» — лишнее", {"example_cs": "Továrna léta vypouštěla odpadní vodu do řeky"}),
    2182: (T + "«svou návštěvu» — калька", {"example_cs": "Návštěvu předem neohlásila a najednou stála před dveřmi"}),
    2188: (T + "«Mohu» — книжно", {"example_cs": "Můžu si ty šaty vyzkoušet?"}),
    2192: (T + "«raději hraji» — книжно", {"example_cs": "Místo abych se učil, radši hraju videohry"}),
    2196: (T + "«natíráme» — не тот вид", {"example_cs": "V sobotu natřeme starý plot na zahradě nabílo"}),
    2203: (T + "«Moje pracovní doba je» — калька", {"example_cs": "Pracovní dobu mám od osmi do pěti"}),
    2218: (T + "«K čemu» — не то слово", {"example_cs": "Proč takové rozrušení?"}),
    2219: (T + "«výzva k letu» — калька", {"example_cs": "Pozor, poslední výzva k nástupu na let do Říma"}),
    2250: (T + "«shledal znepokojivými» — канцелярит", {"example_cs": "Lékařovi se vysoké krevní hodnoty zdály znepokojivé, a tak mě poslal ke specialistovi"}),
    2289: (T + "порядок слов", {"example_cs": "Částku prosím převeďte do pátku"}),
    2312: (T + "«náhle» — книжно", {"example_cs": "Musel jsem prudce zabrzdit"}),
    2314: (T + "«Projev běžel» — калька", {"example_cs": "Projev kancléřky dávali včera večer na všech stanicích"}),
    2353: (T + "вид: zaplatím", {"example_cs": "Zaplatím dvojnásobnou cenu"}),
    2378: (T + "без подлежащего", {"example_cs": "Od příštího roku zavede škola informatiku jako předmět"}),
    2380: (T + "«svůj slib» — калька", {"example_cs": "Slib dodržím"}),
    2381: (T + "«Můj příjem vzrostl» — калька", {"example_cs": "Letos se mi zvýšil příjem"}),
    2394: (T + "«Deset let po přistěhovalectví» — коряво", {"example_cs": "Od přistěhování před deseti lety mluví německy líp než já"}),
    2434: (T + "вид: usnadní", {"example_cs": "To mi usnadní práci"}),
    2445: (T + "«v tomto» — книжно", {"example_cs": "Je odbornice v tomhle oboru"}),
}

REPLACE = []

SPLIT_LATER = {}
