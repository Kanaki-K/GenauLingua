"""Вычитка польского, порция p024 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    15938: (T + "«Mój» — лишнее", {"example_pl": "Dziadek służył w wojsku"}),
    15945: (T + "«To jest» — тяжело", {"example_pl": "To niezgodne z prawem"}),
    15958: (T + "«On jest całkowicie» — тяжело", {"example_pl": "Jest zupełnie niewinny"}),
    15994: (T + "«zostało wycofane» — пассив", {"example_pl": "Wycofano oskarżenie"}),
    15996: (T + "«on» — лишнее", {"example_pl": "Mam podejrzenie, że kłamie"}),
    15998: (T + "«On» — лишнее", {"example_pl": "Gra w obronie"}),
    16016: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn jest porucznikiem w Bundeswehrze"}),
    16049: (T + "«swój» — лишнее", {"example_pl": "Dziadek zmienił testament"}),
    16062: (T + "«Czy» — книжно", {"example_pl": "To w ogóle legalne?"}),
    16074: (T + "«daje konferencję» — калька", {"example_pl": "Premier zwołuje dziś konferencję prasową"}),
    16075: (T + "«Mój» — лишнее", {"example_pl": "Wujek mówi, że tutejsi fachowcy to istna mafia"}),
    16087: (T + "«nastąpiło» — канцелярит", {"example_pl": "Do aresztowania podejrzanego doszło rano"}),
    16106: (T + "«Moja codzienność jest» — калька", {"example_pl": "Na co dzień mam wszystko dobrze uporządkowane"}),
    16117: (T + "«To jest … i jest» — тяжело", {"example_pl": "To szantaż, to nielegalne"}),
    16132: (T + "«swojej» — лишнее", {"example_pl": "Odziedziczy dom po babci"}),
    16139: (T + "«To jest» — тяжело", {"example_pl": "To niesprawiedliwa decyzja"}),
    16249: (T + "«Federacja» — не то слово", {"example_pl": "Rząd federalny uchwalił nowe ustawy"}),
    16381: (T + "«Mój urlop został zatwierdzony» — пассив", {"example_pl": "Zatwierdzili mi urlop!"}),
    16680: (T + "«swoim» — лишнее", {"example_pl": "Dostał duży spadek po wujku"}),
    16722: (T + "«Mój» — лишнее", {"example_pl": "Dziadek ma konserwatywne poglądy"}),
    16843: (T + "«Mój» — лишнее", {"example_pl": "Brat pracuje w remizie strażackiej tuż obok naszego domu"}),
    17084: (T + "«Mój rower jest zepsuty» — калька", {"example_pl": "Zepsuł mi się rower, muszę iść piechotą"}),
    17090: (T + "порядок слов", {"example_pl": "Po drodze tutaj kompletnie zabłądziliśmy"}),
    17099: (T + "«Do kogo należy» — книжно", {"example_pl": "Czyj jest ten pojazd z przodu?"}),
    17116: (T + "«Bak w moim samochodzie» — калька", {"example_pl": "Mam prawie pusty bak"}),
}

REPLACE = []

SPLIT_LATER = {}
