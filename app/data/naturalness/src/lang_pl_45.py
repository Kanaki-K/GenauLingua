"""Вычитка польского, порция p045 (C1–C2), 23.10: лишние местоимения, «Czy», кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    18800: (T + "«moja trójka» — калька", {"example_pl": "U pediatry cała trójka wchodzi po kolei i każde płacze przy zastrzyku"}),
    18838: (T + "«Nasz samochód jest» — калька", {"example_pl": "Samochód mamy prastary, ale co rano odpala"}),
    18845: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez remont pociągi przejeżdżają dziś przez tunel w zwolnionym tempie"}),
    19013: (T + "«Moja» — лишнее", {"example_pl": "Ciocia wstąpiła w wieku dwudziestu lat do zakonu i od tego czasu żyje w klasztorze"}),
    19043: (T + "«mój chłopak z randki» — коряво", {"example_pl": "Wczoraj chłopak po prostu wystawił mnie do wiatru, czekałam godzinę w kawiarni"}),
    8092: (T + "«Mój PIN ma … i zawsze» — коряво", {"example_pl": "PIN ma cztery cyfry, a ja zawsze zapominam akurat ostatnią"}),
    8136: (T + "«naszym» — лишнее", {"example_pl": "Jesienią w ogrodzie leży masa jabłek"}),
    8153: (T + "«biegając» — коряво", {"example_pl": "Najlepiej redukuję stres bieganiem"}),
    8201: (T + "«Czy» — лишнее", {"example_pl": "Możesz odebrać paczkę?"}),
    8210: (T + "«Czy» — лишнее", {"example_pl": "Możemy skrócić to spotkanie? Mam potem jeszcze jedno"}),
    8234: (T + "«naszymi» — лишнее", {"example_pl": "Zimą świeży śnieg chrzęści pod butami"}),
    8268: (T + "«Moi» — лишнее", {"example_pl": "Rodzice odnoszą się do mojego nowego chłopaka jeszcze trochę sceptycznie"}),
    8276: (T + "«Na moim rachunku» — калька", {"example_pl": "Na rachunku za telefon są wszystkie połączenia wychodzące z zeszłego miesiąca"}),
    8294: (T + "«Czy» — лишнее", {"example_pl": "Może pan wydać z pięćdziesięciu euro?"}),
    8296: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez nieobecność dwóch nauczycieli lekcja matematyki dziś się nie odbędzie"}),
    8302: (T + "«naszym» — лишнее", {"example_pl": "Wiśnia w ogrodzie kwitnie w tym roku wspaniale"}),
    8322: (T + "«Czy» — лишнее", {"example_pl": "Może mi pani odłożyć te buty do jutra? Przyjdę jeszcze z mężem"}),
    8362: (T + "«Nasza» — лишнее", {"example_pl": "Córka przyszła na świat w noworoczny poranek"}),
    8376: (T + "«Nasz» — лишнее", {"example_pl": "Kocur jest całkowicie przewidywalny: o piątej rano chce jeść"}),
    8406: (T + "«Mój» — лишнее", {"example_pl": "Zły humor na pewno wiąże się z szarą pogodą"}),
    8449: (T + "«Moja» — лишнее", {"example_pl": "Koleżanka z pracy ma stwardnienie rozsiane, a mimo to pracuje na cały etat"}),
    8504: (T + "«mojego» — лишнее", {"example_pl": "Akcesoria do auta kosztują więcej niż samo auto"}),
    8514: (T + "«moim» — лишнее", {"example_pl": "Dziesięć lat w Japonii mocno odcisnęło piętno na tacie, wciąż się kłania"}),
    8537: (T + "«Moja» — лишнее", {"example_pl": "Mama ma nosa do okazji"}),
    8546: (T + "«Z powodu niedostatecznej znajomości» — книжно", {"example_pl": "Przez niedostateczne wyniki z matematyki syn bierze teraz korepetycje"}),
    8563: (T + "«Mój» — лишнее", {"example_pl": "Telefon przetrwał upadek z balkonu bez szwanku"}),
    8564: (T + "«Mój» — лишнее", {"example_pl": "Kot bezgłośnie się skrada i wskakuje mi na kolana"}),
    8598: (T + "«Pan» → «pan»", {"example_pl": "Naprawdę gustownie urządził pan swoje mieszkanie"}),
    8609: (T + "«Mój» — лишнее", {"example_pl": "Tata jest ateistą, ale w Boże Narodzenie śpiewa w kościele najgłośniej"}),
}

REPLACE = []

SPLIT_LATER = {}
