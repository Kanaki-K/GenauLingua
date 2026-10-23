"""Вычитка чешского, порция p026 (B1–B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    18284: (T + "«odpadky … odpadky» — повтор", {"example_cs": "Koš na odpadky je plný, vyneseš ho?"}),
    18309: (T + "«Necháváme» — не тот вид", {"example_cs": "Necháme si namontovat novou kuchyň"}),
    18389: (T + "«velmi» — книжно", {"example_cs": "Nastěhování do nového bytu bylo hodně stresující"}),
    18405: (T + "«se nachází» — канцелярит", {"example_cs": "Dílna je v suterénu domu"}),
    18424: (T + "«Uklízím» — не тот вид", {"example_cs": "Uklidím konzervy do spíže"}),
    18429: (T + "«velmi» — книжно", {"example_cs": "Malé městečko na pobřeží bylo hodně idylické"}),
    18446: (T + "«svou» — лишнее", {"example_cs": "Učitel stojí za katedrou"}),
    18465: (T + "«velmi» — книжно", {"example_cs": "Pohovka má hodně měkké čalounění"}),
    18473: (T + "«své» — лишнее", {"example_cs": "Pes má místo na spaní pod stolem"}),
    18483: (T + "«velmi dobře» — книжно", {"example_cs": "Starý šicí stroj pořád funguje skvěle"}),
    18484: (T + "«dávám» — не тот вид", {"example_cs": "Pro hosty dám na gauč čisté povlečení"}),
    18486: (T + "«Vede domácký život» — калька", {"example_cs": "Je hodně domácká a málokdy chodí ven"}),
    18489: (T + "«náš» — лишнее", {"example_cs": "Přestavujeme starý dům, abychom měli víc místa"}),
    18697: (T + "mittlerweile — «уже теперь»", {"example_cs": "Teď už chápu, o co jde"}),
    18705: (T + "«pracuji» — книжно", {"example_cs": "Momentálně pracuju v kavárně"}),
    18712: (T + "«pracuji» — книжно", {"example_cs": "Přes den pracuju v kanceláři, večer doma"}),
    18713: (T + "«Držíme se harmonogramu» — калька", {"example_cs": "Harmonogram zatím dobře dodržujeme"}),
    18717: (T + "«Postupně chápu» — коряво", {"example_cs": "Pomalu začínám chápat, co myslíš"}),
    18723: (T + "«Tvůj nájem je splatný» — калька", {"example_cs": "Nájem je už dávno po splatnosti"}),
    18871: (T + "«V čase oběda» — калька", {"example_cs": "V době oběda je jídelna úplně narvaná"}),
    18880: (T + "«takže nikdo není» — смысл", {"example_cs": "Řídíme střídavě, aby nikdo nebyl unavený"}),
    18886: (T + "«nejdříve» — книжно", {"example_cs": "Balík přijde nejdřív příští týden"}),
    18973: (T + "«zůstáváme» — не тот вид", {"example_cs": "Protože celý den prší, zůstaneme dnes doma"}),
    19032: (T + "«tento» — книжно", {"example_cs": "Kolo si tenhle týden nechám opravit v dílně"}),
    2043: (T + "«Pro předcházení hádkám» — канцелярит", {"example_cs": "Aby se předešlo hádkám, má u nás každé dítě vlastní ovladač"}),
    6754: (T + "«Moje práce je» — калька", {"example_cs": "Práci mám naštěstí jistou"}),
}

REPLACE = []

SPLIT_LATER = {}
