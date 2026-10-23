"""Вычитка польского, порция p005 (A2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    1222: (T + "«Chętnie gram» — калька gern", {"example_pl": "Lubię grać w koszykówkę"}),
    1285: (T + "«Ona» — лишнее", {"example_pl": "Ma blond włosy"}),
    1312: (T + "«przeciw temu» — лишнее", {"example_pl": "Jestem przeciw"}),
    1382: (T + "«Czy» — книжно", {"example_pl": "To danie zawiera orzechy? Mam alergię"}),
    1394: (T + "«Pana» — регистр", {"example_pl": "Otrzymałem pana paczkę"}),
    1473: (T + "«wystarczająco dużo» — тяжело", {"example_pl": "Masz dość pieniędzy?"}),
    1484: (T + "«Mój … w wieku» — книжно", {"example_pl": "Dziadek ma dziewięćdziesiąt lat i jest jeszcze całkiem zdrowy"}),
    1547: (T + "«że on przyjdzie» — тяжело", {"example_pl": "Oby przyszedł"}),
    1580: (T + "«Masz znajomość» — калька", {"example_pl": "Masz jakąś wiedzę z księgowości?"}),
    1670: (T + "«Moja» — лишнее", {"example_pl": "Córka lubi malować zwierzęta"}),
    1671: (T + "«ludzie» — лишнее", {"example_pl": "Niektórzy nie jedzą mięsa"}),
    1682: (T + "«Jakie jest twoje zdanie» — калька", {"example_pl": "A ty jakie masz zdanie?"}),
    1685: (T + "«Mieliśmy mnóstwo zabawy» — калька", {"example_pl": "Na imprezie było mnóstwo zabawy"}),
    1726: (T + "«jutrem» — падеж", {"example_pl": "Denerwujesz się przed jutrem?"}),
    1749: (T + "«wydarzyło» — не слово карточки", {"example_pl": "Co się zdarzyło?"}),
    1771: (T + "«To jest prywatne» — калька", {"example_pl": "To prywatna sprawa"}),
    1793: (T + "«On» — лишнее", {"example_pl": "Jest bardzo bogaty"}),
    1812: (T + "«Czy» — книжно", {"example_pl": "Ten autobus jedzie w kierunku centrum?"}),
    1822: (T + "«Czy» — книжно", {"example_pl": "Zupa jest bardzo ostra?"}),
    1874: (T + "«moja … telefon komórkowy» — книжно", {"example_pl": "Nawet babcia ma komórkę"}),
    2104: (T + "«To jest» — тяжело", {"example_pl": "To naprawdę świetne"}),
    2157: (T + "«Mój … w wieku» — книжно", {"example_pl": "Dziadek ma 80 lat i wciąż jest bardzo aktywny"}),
    2285: (T + "«Skarżę się menedżerowi» — калька", {"example_pl": "Idę się poskarżyć kierownikowi"}),
    2668: (T + "«wychodzę na zewnątrz» — книжно", {"example_pl": "Po tym, jak zjem, wyjdę na dwór"}),
    2714: (T + "«Mój» — лишнее", {"example_pl": "Komputer znowu mi się zawiesił"}),
    2753: (T + "«Opona jest przebita» — калька", {"example_pl": "Mam przebitą oponę"}),
    2760: (T + "«Moja» — лишнее", {"example_pl": "Córka od dwóch lat jeździ konno"}),
    2810: (T + "«o ósmej» — 20 часов", {"example_pl": "Program leci o ósmej wieczorem"}),
    3013: (T + "«do ósmej» — 20 часов", {"example_pl": "Biblioteka jest otwarta w dni powszednie do dwudziestej"}),
    3047: (T + "«Moim celem jest» — книжно", {"example_pl": "Mój cel to zdać B1 do lata"}),
    6241: (T + "«To jest całkiem dobre» — калька", {"example_pl": "To całkiem niezłe"}),
}

REPLACE = []

SPLIT_LATER = {}
