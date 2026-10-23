"""Вычитка польского, порция p023 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    15174: (T + "«Moja» — лишнее", {"example_pl": "Kuzynka wychodzi za mąż w maju"}),
    15209: (T + "«Mój» — лишнее", {"example_pl": "Przyrodni brat mieszka w Berlinie"}),
    15214: (T + "«Moja» — лишнее", {"example_pl": "Najlepsza przyjaciółka zapytała, czy zostanę jej druhną"}),
    15239: (T + "«swoim» — лишнее", {"example_pl": "Bardzo tęskni za domem rodzinnym"}),
    15242: (T + "«Moja» — лишнее", {"example_pl": "Mama opiekuje się dziećmi po szkole"}),
    15292: (T + "«Moja» — лишнее", {"example_pl": "Wnuczka w przyszłym miesiącu skończy pięć lat"}),
    15328: (T + "«Moja» — лишнее", {"example_pl": "Siostra jeszcze karmi, dziecko dostaje tylko mleko matki"}),
    15455: (T + "«Atmosfera jest przytulna» — калька", {"example_pl": "Jest tu bardzo przytulna atmosfera"}),
    15465: (T + "«Zimno … jest nie do zniesienia» — калька", {"example_pl": "Na dworze jest dziś nieznośne zimno"}),
    15467: (T + "«Mój mały … bardzo słodki» — тяжело", {"example_pl": "Mój mały królik jest przesłodki"}),
    15472: (T + "«smakują słodko» — калька", {"example_pl": "Banany są już dojrzałe i słodkie"}),
    15475: (T + "«Mróz był silny» — калька", {"example_pl": "Tej nocy był silny mróz"}),
    15568: (T + "«do mojego» — лишнее", {"example_pl": "Pszczoła wleciała do pokoju"}),
    15638: (T + "«Gałąź drzewa» — тяжело", {"example_pl": "Z drzewa ułamała się gałąź"}),
    15641: (T + "«na moim» — лишнее", {"example_pl": "Mam na balkonie palmę"}),
    15663: (T + "«Mój … swoim» — лишнее", {"example_pl": "Chomik co noc biega w kółku"}),
    15679: (T + "«Mój» — лишнее", {"example_pl": "Pudel uwielbia skakać do wody"}),
    15726: (T + "«na zewnątrz» — книжно", {"example_pl": "W nocy słychać szakale"}),
    15735: (T + "«mój … u mnie» — повтор", {"example_pl": "Nawet kaktus mi usechł"}),
    15750: (T + "«w moim swetrze» — калька", {"example_pl": "Mole wygryzły mi dziurę w swetrze"}),
    15772: (T + "«Mój» — лишнее", {"example_pl": "Dziadek łowił kiedyś w rzece węgorze"}),
    15773: (T + "«swoje» — лишнее", {"example_pl": "Paw w zoo dumnie rozkłada pióra"}),
    15780: (T + "«Moja» — лишнее", {"example_pl": "Sąsiadka trzyma w mieszkaniu dwie fretki"}),
    15811: (T + "«na moim» — лишнее", {"example_pl": "Czerwony storczyk pięknie kwitnie na balkonie"}),
    15814: (T + "«Mój» — лишнее", {"example_pl": "Dziadek ma w ogrodzie trzy ule"}),
    15825: (T + "«Mój» — лишнее", {"example_pl": "Syn wierzy, że sanie Świętego Mikołaja ciągną renifery"}),
    15844: (T + "«Mój» — лишнее", {"example_pl": "Młodszy brat łapie w ogrodzie koniki polne do słoika"}),
    15861: (T + "«każdego ranka» — книжно", {"example_pl": "Pierwsze promienie słońca budzą mnie co rano"}),
    15863: (T + "«Mój» — лишнее", {"example_pl": "Dziadek od czterdziestu lat nosi wąsy"}),
}

REPLACE = []

SPLIT_LATER = {}
