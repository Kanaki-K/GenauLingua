"""Вычитка чешского, порция p013 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    2762: (T + "«běží reportáž» — калька", {"example_cs": "Dnes večer dávají reportáž o zdravotních sestrách"}),
    2768: (T + "«dal pokutu» — разговорно не о суде", {"example_cs": "Soudce mu uložil jen pokutu"}),
    2839: (T + "«Můj sen je» — калька", {"example_cs": "Mým snem je rychlé sportovní auto"}),
    2863: (T + "«příliš» — книжно", {"example_cs": "Podle nové studie spíme moc málo"}),
    2874: (T + "«Můj diář je» — калька", {"example_cs": "Mám hodně plný diář"}),
    2881: (T + "«mnoho» — книжно", {"example_cs": "Bylo hodně mrtvých"}),
    2911: (T + "gut — потеряно", {"example_cs": "Umí dobře zacházet s dětmi"}),
    2930: (T + "«nejedou všechny vlaky» — двусмысленно", {"example_cs": "Kvůli nečasu nejede žádný vlak"}),
    2966: (T + "«rozesíláme» — не тот вид", {"example_cs": "Svatební pozvánky tentokrát rozešleme e-mailem, ušetříme za známky"}),
    2969: (T + "«ověřuji» — не тот вид", {"example_cs": "Před cestou do Thajska si ověřím, jestli moje pojistné krytí platí i v zahraničí"}),
    2970: (T + "«stará» — не тот вид", {"example_cs": "Kdo se postará o vaši kočku, když budete na dovolené?"}),
    2987: (T + "«předpokládaně» — книжно", {"example_cs": "Stavba před naším domem potrvá pravděpodobně do konce března"}),
    3014: (T + "«na tuto práci» — книжно", {"example_cs": "Na tohle potřebuju správné nářadí"}),
    3029: (T + "«s naším karavanem» — калька", {"example_cs": "Jedeme na dovolenou karavanem"}),
    3039: (T + "«Ten okamžik» — калька", {"example_cs": "Tohle je opravdu špatně zvolený okamžik"}),
}

REPLACE = []

SPLIT_LATER = {}
