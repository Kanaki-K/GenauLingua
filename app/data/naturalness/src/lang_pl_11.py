"""Вычитка польского, порция p011 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    2152: (T + "«swoje» — лишнее", {"example_pl": "Fabryka latami odprowadzała ścieki do rzeki"}),
    2163: (T + "«Mój» — лишнее", {"example_pl": "Dziadek po wojnie pracował jako tłumacz dla aliantów"}),
    2169: (T + "«Czy» — книжно", {"example_pl": "To już oficjalne, że się przeprowadzacie?"}),
    2180: (T + "«Na home office nabrałem nawyku» — коряво", {"example_pl": "Pracując zdalnie, przyzwyczaiłem się, że w południe wychodzę na krótki spacer"}),
    2183: (T + "«Pan» — регистр", {"example_pl": "Fakturę znajdzie pan w załączniku"}),
    2188: (T + "«Czy» — книжно", {"example_pl": "Mogę przymierzyć tę sukienkę?"}),
    2201: (T + "«Moje … jest dziesięć minut» — калька", {"example_pl": "Do nowej pracy mam tylko dziesięć minut rowerem"}),
    2203: (T + "«Mój czas pracy to» — калька", {"example_pl": "Czas pracy mam od ósmej do piątej"}),
    2236: (T + "«Pan» — регистр", {"example_pl": "Może mi pan wystawić paragon?"}),
    2242: (T + "«Mój» — лишнее", {"example_pl": "Tata od trzydziestu lat kupuje zawsze tę samą markę samochodu"}),
    2243: (T + "«mój» — лишнее", {"example_pl": "Jako dziecko brat koniecznie chciał jeździć w wyścigach samochodowych"}),
    2245: (T + "«Moje ubezpieczenie kosztuje» — калька", {"example_pl": "Ubezpieczenie samochodu kosztuje mnie 80 euro miesięcznie"}),
    2254: (T + "«Mój … jest zachwycony» — калька", {"example_pl": "Syn zachwyca się dinozaurami"}),
    2260: (T + "«On» — лишнее", {"example_pl": "Twierdzi, że ma rację"}),
    2279: (T + "«Moi» — лишнее", {"example_pl": "Dziadkowie mieszkali w amerykańskiej strefie okupacyjnej"}),
    2288: (T + "«Moja» — лишнее", {"example_pl": "Mama nie zamawia przez internet, woli zadzwonić na infolinię zamówień"}),
    2302: (T + "«Czy» — книжно", {"example_pl": "Te warzywa są bio?"}),
    2311: (T + "«On» — лишнее", {"example_pl": "Trenuje boks"}),
    2340: (T + "«Mój» — лишнее", {"example_pl": "Syn przed snem zawsze chce posłuchać opowieści detektywistycznej"}),
    2341: (T + "«Moja» — лишнее", {"example_pl": "Babcia wychowała się w Niemieckiej Republice Demokratycznej"}),
    2342: (T + "«Mój» — лишнее", {"example_pl": "Tata jest cukrzykiem"}),
    2349: (T + "«Chętnie oglądam» — калька gern", {"example_pl": "Lubię oglądać filmy dokumentalne"}),
    2361: (T + "«Moje oceny są» — калька", {"example_pl": "Mam oceny powyżej średniej w klasie, tylko nie z matematyki"}),
    2378: (T + "«wprowadzają» — нет подлежащего", {"example_pl": "Od przyszłego roku szkoła wprowadza informatykę jako przedmiot"}),
    2380: (T + "«swojej» — лишнее", {"example_pl": "Dotrzymam obietnicy"}),
    2381: (T + "«Mój dochód wzrósł» — калька", {"example_pl": "W tym roku mam wyższy dochód"}),
    2396: (T + "«Mój» — лишнее", {"example_pl": "Syn od trzech lat gra w hokeja"}),
    2401: (T + "«jest do odebrania» — канцелярит", {"example_pl": "Klucz odbierze pan w recepcji"}),
    2435: (T + "«w zrównoważony sposób» — книжно", {"example_pl": "Odżywiam się zdrowo i różnorodnie"}),
    2440: (T + "«Mój» — лишнее", {"example_pl": "Siostrzeniec to trudny zjadacz, je tylko makaron i frytki"}),
    2445: (T + "«Ona» — лишнее", {"example_pl": "Jest ekspertką w tej dziedzinie"}),
}

REPLACE = []

SPLIT_LATER = {}
