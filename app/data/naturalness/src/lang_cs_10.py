"""Вычитка чешского, порция p010 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    1774: (T + "«Na zdraví! Na tvoje zdraví» — повтор", {"example_cs": "Na zdraví! Ať žiješ!"}),
    1856: (T + "«plachtíme» — коряво", {"example_cs": "O víkendu jedeme plachtit"}),
    1938: (T + "man — безлично", {"example_cs": "Účast v kurzu je zdarma, ale je potřeba se přihlásit"}),
    1966: (T + "«Naše místo setkání» — калька", {"example_cs": "Sraz máme na nádraží"}),
    1967: (T + "«Dělám hodně sportu» — калька", {"example_cs": "Hodně sportuju"}),
    2030: (T + "«zlepšit svou němčinu» — калька", {"example_cs": "Chci se zlepšit v němčině"}),
    2031: (T + "порядок слов", {"example_cs": "Je špatné spojení"}),
    2108: (T + "«kvůli bytu» — коряво", {"example_cs": "Na prohlídku malého dvoupokojového bytu přišlo třicet lidí"}),
}

REPLACE = []

SPLIT_LATER = {}
