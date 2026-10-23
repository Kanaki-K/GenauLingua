"""Вычитка польского, порция p015 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    6844: (T + "«twoją» — лишнее", {"example_pl": "Dziękuję bardzo za pomoc"}),
    6876: (T + "«Schodzimy w dół» — плеоназм", {"example_pl": "Schodzimy po schodach na dół"}),
    6878: (T + "«To jest … całkowicie» — тяжело", {"example_pl": "To przecież zupełnie logiczne"}),
    6890: (T + "«całkiem nieznana» — смысл", {"example_pl": "Ta piosenka jest mi zupełnie nieznana"}),
    6906: (T + "«Mój zegarek źle chodzi» — калька", {"example_pl": "Znasz dokładną godzinę? Zegarek mi źle chodzi"}),
    6914: (T + "«swoją» — лишнее", {"example_pl": "Pies zakopuje kość w ogrodzie"}),
    6918: (T + "«Głębokość wynosi» — книжно", {"example_pl": "Woda ma tu trzy metry głębokości"}),
    6919: (T + "«z zewnątrz» — книжно", {"example_pl": "Przeszkadza mi hałas z ulicy"}),
    6934: (T + "«Czy» — книжно", {"example_pl": "Wszyscy studenci byli obecni na wykładzie?"}),
    6938: (T + "«Czy możesz» — книжно", {"example_pl": "Możesz zorganizować mi z nią spotkanie?"}),
    6944: (T + "«straszliwego» — книжно", {"example_pl": "Mam strasznego kaca"}),
    6969: (T + "«on» — лишнее", {"example_pl": "Stwierdziłem, że nie przyjdzie"}),
    6976: (T + "«do góry na dach» — коряво", {"example_pl": "Schody prowadzą w górę, na dach"}),
    6980: (T + "«To jest sedno» — тяжело", {"example_pl": "W tym sedno problemu"}),
    6994: (T + "«na mojej linie» — лишнее", {"example_pl": "Węzeł na linie jest za mocno zaciągnięty"}),
    7005: (T + "«Zgrubnie licząc» — калька", {"example_pl": "Licząc z grubsza, to kosztuje 100 euro"}),
    7006: (T + "«on» — лишнее", {"example_pl": "Przypuszczam, że zaraz przyjdzie"}),
    7017: (T + "«Ona» — лишнее", {"example_pl": "Dużo przeszła w życiu"}),
    7023: (T + "«silnie pachnie» — книжно", {"example_pl": "Jedzenie mocno pachnie czosnkiem"}),
    7037: (T + "«Oni» — лишнее", {"example_pl": "Trzymają się razem, cokolwiek się stanie"}),
    7077: (T + "«swoimi» — лишнее", {"example_pl": "Artysta formuje glinę rękami"}),
    7078: (T + "«Czy» — книжно", {"example_pl": "Możemy cofnąć ostatnią czynność?"}),
    7292: (T + "«To jest» — тяжело", {"example_pl": "To wyłącznie dla ciebie"}),
    7315: (T + "«To jest powszechnie znane» — книжно", {"example_pl": "To powszechnie wiadomo"}),
    7505: (T + "«Mój» — лишнее", {"example_pl": "Ołówek nie jest już ostry"}),
    7537: (T + "«swoją» — лишнее", {"example_pl": "Chcę podnieść kondycję"}),
    7610: (T + "«Ten ząb się chwieje» — книжно", {"example_pl": "Ząb się rusza, zaraz wypadnie"}),
}

REPLACE = []

SPLIT_LATER = {}
