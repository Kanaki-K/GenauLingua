"""Вычитка польского, порция p010 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    1774: (T + "«Na zdrowie! Za twoje zdrowie» — повтор", {"example_pl": "Zdrówko! Za twoje zdrowie"}),
    1782: (T + "«on» — лишнее", {"example_pl": "I jak zareagował?"}),
    1784: (T + "«moja» — лишнее", {"example_pl": "W przyszłym roku córka przechodzi ze szkoły realnej do liceum"}),
    1808: (T + "«Mój» — лишнее", {"example_pl": "Brat pracuje jako kelner w hotelu"}),
    1832: (T + "«Moje serce bije» — калька", {"example_pl": "Serce mi szybko bije"}),
    1841: (T + "«swój» — лишнее", {"example_pl": "Oszczędzaj głos"}),
    1872: (T + "«Moja … smartfon» — лишнее, падеж", {"example_pl": "Babcia też ma teraz smartfona i codziennie wysyła nam zdjęcia"}),
    1877: (T + "«Ona» — лишнее", {"example_pl": "Pracuje starannie"}),
    1881: (T + "«mój» — лишнее", {"example_pl": "Na nowy rower syn co tydzień wrzuca pieniądze do skarbonki"}),
    1896: (T + "«Mój» — лишнее", {"example_pl": "Syn ma dwa obywatelstwa, niemieckie i polskie"}),
    1898: (T + "«On» — лишнее", {"example_pl": "Ciągle dzwoni"}),
    1905: (T + "«Czy» — книжно", {"example_pl": "Jest w pociągu gniazdko do telefonu?"}),
    1928: (T + "«Ona» — лишнее", {"example_pl": "Jest dobrą tancerką"}),
    1941: (T + "«Moja» — лишнее", {"example_pl": "Żona pracuje na pół etatu, żeby po południu być z dziećmi"}),
    1942: (T + "«Obok studiów» — калька", {"example_pl": "Oprócz studiów ma pracę na pół etatu w aptece"}),
    1950: (T + "«Właśnie jestem na terapii» — калька", {"example_pl": "Chodzę teraz na terapię"}),
    1966: (T + "«Naszym miejscem spotkania jest» — книжно", {"example_pl": "Miejsce spotkania: dworzec"}),
    1988: (T + "«Moja» — лишнее", {"example_pl": "Mama wciąż wypełnia każdy formularz przelewu ręcznie"}),
    2009: (T + "«swoje» — лишнее", {"example_pl": "Proszę przynieść dokumenty"}),
    2013: (T + "«podczas studiów» — книжно", {"example_pl": "Rodzice wspierają mnie na studiach"}),
    2029: (T + "«Moje polecane wydarzenie» — калька", {"example_pl": "Polecane wydarzenie na weekend: kino plenerowe w parku miejskim"}),
    2030: (T + "«swój» — лишнее", {"example_pl": "Chcę poprawić niemiecki"}),
    2031: (T + "«Połączenie jest złe» — калька", {"example_pl": "Mamy słabe połączenie"}),
    2063: (T + "«słówek … słówek» — повтор", {"example_pl": "Do testu ze słówek syn powtarza je w autobusie na telefonie"}),
    2066: (T + "«Czy» — книжно", {"example_pl": "Lista jest kompletna?"}),
    2069: (T + "«warunkiem do tej pracy» — коряво", {"example_pl": "Prawo jazdy jest warunkiem przyjęcia do tej pracy"}),
    2082: (T + "«referat» — не слово карточки", {"example_pl": "Jutro mam prezentację i strasznie się denerwuję"}),
    2108: (T + "«a to małe dwupokojowe» — коряво", {"example_pl": "Na oglądanie małego mieszkania dwupokojowego przyszło trzydzieści osób"}),
    2134: (T + "«On» — лишнее", {"example_pl": "Jest bardzo solidny"}),
    2142: (T + "«moich» — лишнее", {"example_pl": "Jestem finansowo zależny od rodziców"}),
    2145: (T + "порядок слов", {"example_pl": "Niestety na sobotę muszę ci odmówić"}),
}

REPLACE = []

SPLIT_LATER = {}
