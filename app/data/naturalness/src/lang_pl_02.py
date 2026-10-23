"""Вычитка польского, порция p002 (A1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    548: (T + "«Czy możesz» — книжно", {"example_pl": "Możesz to przeczytać na głos?"}),
    551: (T + "«Ona» — лишнее", {"example_pl": "Kocha swoją rodzinę"}),
    587: (T + "«On jest» — тяжело", {"example_pl": "To dobry człowiek"}),
    608: (T + "«Jeden moment» — калька", {"example_pl": "Moment, proszę"}),
    620: (T + "«Moja» — лишнее", {"example_pl": "Mama jest w domu"}),
    631: (T + "«na zewnątrz» — книжно", {"example_pl": "Po jedzeniu wychodzimy na dwór"}),
    718: (T + "«Ona» — лишнее", {"example_pl": "Dzwoni na policję"}),
    745: (T + "«On» — лишнее", {"example_pl": "Nie pali"}),
    798: (T + "«swojego» — лишнее", {"example_pl": "Szukam klucza"}),
    800: (T + "«dobrze smakuje» — калька", {"example_pl": "Bardzo mi to smakuje"}),
    805: (T + "«jestem szybciej» — грамматика", {"example_pl": "Rowerem szybciej dojadę niż autobusem"}),
    812: (T + "«Ona idzie» — смысл", {"example_pl": "Chodzi do szkoły"}),
    817: (T + "«Moja» — лишнее", {"example_pl": "Siostra jest dwa lata starsza ode mnie"}),
    822: (T + "«To jest» — тяжело", {"example_pl": "To piękny pomysł"}),
    836: (T + "«Ona» — лишнее", {"example_pl": "Myje się"}),
    845: (T + "«Ona» — лишнее", {"example_pl": "Siedzi na kanapie"}),
    847: (T + "«Mój» — лишнее", {"example_pl": "Syn chodzi do pierwszej klasy"}),
    892: (T + "«Mój» — лишнее", {"example_pl": "Brat jest studentem w Monachium"}),
    931: (T + "«Moja» — лишнее", {"example_pl": "Córka chodzi już do szkoły"}),
    965: (T + "«sprawiają mi przyjemność» — книжно", {"example_pl": "Lubię te lekcje"}),
    971: (T + "«Mój» — лишнее", {"example_pl": "Tata pracuje w biurze"}),
    978: (T + "«Ona» — лишнее", {"example_pl": "Jest zamężna"}),
    1007: (T + "«Co Pan sobie życzy» — книжно", {"example_pl": "Co dla pana?"}),
    1010: (T + "«prosić szklankę» — предлог", {"example_pl": "Mogę prosić o szklankę wody?"}),
    1022: (T + "«Ona» — лишнее", {"example_pl": "Pije kieliszek wina"}),
    1045: (T + "«My idziemy» — коряво", {"example_pl": "My już idziemy do domu"}),
    1060: (T + "«brzmi po niemiecku» — калька", {"example_pl": "Jak jest to słowo po niemiecku?"}),
    1138: (T + "«na ten link» — предлог", {"example_pl": "Kliknij, proszę, w ten link"}),
    1160: (T + "«Moje miejsce pracy jest» — калька", {"example_pl": "Mam miejsce pracy przy oknie"}),
    1200: (T + "«swój» — лишнее", {"example_pl": "Pokaż mi, proszę, dowód osobisty"}),
    1217: (T + "«Czy mogę» — книжно", {"example_pl": "Mogę zapłacić gotówką?"}),
}

REPLACE = []

SPLIT_LATER = {}
