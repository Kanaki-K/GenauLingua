"""Вычитка польского, порция p020 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    12117: (T + "«Mój» — лишнее", {"example_pl": "Teść jesienią lubi chodzić na polowania"}),
    12129: (T + "«swojego» — лишнее", {"example_pl": "Bez misia nie zaśnie"}),
    12132: (T + "«Moja … swoją» — лишнее", {"example_pl": "Córka lubi bawić się lalką"}),
    12161: (T + "«Mój» — лишнее", {"example_pl": "Siostrzeniec jest gimnastykiem i robi już salto w tył"}),
    12177: (T + "«bardzo piękne» — бледно", {"example_pl": "Fajerwerki w sylwestra były przepiękne"}),
    12233: (T + "«chętnie układam» — калька gern", {"example_pl": "W weekendy lubię układać puzzle"}),
    12247: (T + "«Mój» — лишнее", {"example_pl": "Tata co tydzień gra w lotto"}),
    12255: (T + "«na imprezę» — коряво", {"example_pl": "Kto jest na liście gości?"}),
    12263: (T + "«Mój» — лишнее", {"example_pl": "Syn od dwóch lat gra w hokeja"}),
    12336: (T + "«swojego» — лишнее", {"example_pl": "Na urodziny dostał koszulkę ulubionego klubu"}),
    12345: (T + "«On jest» — тяжело", {"example_pl": "To waga ciężka w swojej branży"}),
    12367: (T + "«każdego ranka» — книжно", {"example_pl": "Co rano robię dwadzieścia pompek"}),
    12385: (T + "«każdego dnia» — книжно", {"example_pl": "Futbolista amerykański codziennie ciężko trenuje"}),
    12408: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn w Ameryce jest baseballistą w drużynie uniwersyteckiej"}),
    12417: (T + "«Mój» — лишнее", {"example_pl": "Kolega z drużyny podał mi wczoraj dobrą piłkę"}),
    12488: (T + "«Mój» — лишнее", {"example_pl": "Dziadek jest niewidomy"}),
    12498: (T + "«Mój» — лишнее", {"example_pl": "Dziadek niestety zachorował na raka"}),
    12501: (T + "«sprawia, że» — книжно", {"example_pl": "Przez ten wirus choruje mnóstwo ludzi"}),
    12511: (T + "«Mój mózg» — калька", {"example_pl": "Mózg mi dziś w ogóle nie działa"}),
    12518: (T + "«Moja pamięć nie jest» — калька", {"example_pl": "Pamięć mi już nie dopisuje"}),
    12540: (T + "«Czy istnieje» — книжно", {"example_pl": "Jest jakieś lekarstwo na tę chorobę?"}),
    12557: (T + "«Mój … w wieku» — книжно", {"example_pl": "Dziadek ma 70 lat i wciąż jest w świetnej formie"}),
    12563: (T + "«będzie operować» — тяжело", {"example_pl": "Chirurg operuje pacjentkę jutro"}),
    12568: (T + "«bardzo poważny» — коряво", {"example_pl": "Uraz nogi nie jest zbyt poważny"}),
    12570: (T + "«na jego czole» — калька", {"example_pl": "Na czole wciąż ma bliznę po wypadku"}),
    12573: (T + "«nie będzie leczona» — пассив", {"example_pl": "Infekcja może być groźna, jeśli się jej nie leczy"}),
    12576: (T + "«Mój» — лишнее", {"example_pl": "Dziadek jeździ na wózku inwalidzkim"}),
    12585: (T + "«Czy są ocalali» — книжно", {"example_pl": "Są jacyś ocalali?"}),
    12602: (T + "«Jego bicie serca jest» — калька", {"example_pl": "Ma bardzo szybkie bicie serca"}),
    12641: (T + "«Moja» — лишнее", {"example_pl": "Babcia potrzebuje opieki"}),
    12646: (T + "«Ona … swoją» — лишнее", {"example_pl": "Codziennie opiekuje się starą matką"}),
    12783: (T + "«Mój» — лишнее", {"example_pl": "Pies powoli się starzeje i dużo więcej śpi"}),
    12807: (T + "«Moja» — лишнее", {"example_pl": "Babcia mieszka teraz w domu starców"}),
    12864: (T + "«Mój» — лишнее", {"example_pl": "Dziadek od wczoraj leży w szpitalu"}),
    12879: (T + "«Ona» — лишнее", {"example_pl": "Nosi soczewki kontaktowe zamiast okularów"}),
    12938: (T + "«Czy twoje» — книжно", {"example_pl": "Dziecko jest zaszczepione przeciw odrze?"}),
    12962: (T + "«Jego bezsenność sprawia» — калька", {"example_pl": "Przez bezsenność jest zmęczony i drażliwy"}),
    12967: (T + "«mojej» — лишнее", {"example_pl": "Do babci codziennie rano przychodzi opiekunka"}),
}

REPLACE = []

SPLIT_LATER = {}
