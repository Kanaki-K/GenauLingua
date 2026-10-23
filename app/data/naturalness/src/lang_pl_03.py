"""Вычитка польского, порция p003 (A1–A2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    1606: (T + "«Do wypłaty» — предлог", {"example_pl": "Na wypłatę potrzebuję konta w Niemczech"}),
    1738: (T + "«on» — лишнее", {"example_pl": "Nie wiem, czy przyjdzie"}),
    1739: (T + "«na górze na regale» — коряво", {"example_pl": "Książka leży na samej górze regału"}),
    1776: (T + "«Czy» — книжно", {"example_pl": "Egzamin jest jutro?"}),
    2079: (T + "«Ten stopień jest» — тяжело", {"example_pl": "Uwaga, wysoki stopień!"}),
    6222: (T + "«To niemożliwe, to nieprawda» — повтор", {"example_pl": "To przecież nieprawda!"}),
    6228: (T + "«To jest» — тяжело", {"example_pl": "To bardzo daleko stąd"}),
    6268: (T + "«Czy to jest» — тяжело", {"example_pl": "Czy to możliwe?"}),
    6339: (T + "«absolutnie słuszne» — книжно", {"example_pl": "Masz absolutnie rację"}),
    6396: (T + "порядок слов", {"example_pl": "To mi ciebie przypomina"}),
    8735: (T + "«sprawia mi przyjemność» — книжно", {"example_pl": "Lubię swoją pracę"}),
    8742: (T + "«Mój» — лишнее", {"example_pl": "Szef jest bardzo miły"}),
    8788: (T + "«Czy dziś jest» — книжно", {"example_pl": "Jest dziś oprowadzanie po zamku?"}),
    8797: (T + "«Mój» — лишнее", {"example_pl": "Kolega z pracy mi pomaga"}),
    9043: (T + "«Moja … wkrótce» — книжно", {"example_pl": "Córka jest już samodzielna i niedługo się wyprowadza"}),
    9441: (T + "«Mój nauczyciel jest» — калька", {"example_pl": "Mam miłego nauczyciela"}),
    9522: (T + "«W lecie robię praktykę» — калька", {"example_pl": "Latem mam praktyki w banku"}),
    9712: (T + "«swój» — лишнее", {"example_pl": "Chcę sprzedać samochód"}),
    10438: (T + "«twojego» — лишнее", {"example_pl": "Gratuluję ci sukcesu"}),
    11668: (T + "«naprawdę wielkie» — коряво", {"example_pl": "Mam straszne pragnienie"}),
    11696: (T + "«chętnie jem» — калька gern", {"example_pl": "Na śniadanie lubię jeść szynkę"}),
    12253: (T + "«w nocy na dyskotekę» — коряво", {"example_pl": "Idziemy dziś wieczorem potańczyć na dyskotece"}),
    12459: (T + "«Czy ta» — книжно", {"example_pl": "Mysz jest martwa?"}),
    13358: (T + "«Czy» — книжно", {"example_pl": "To wasz samochód?"}),
    13388: (T + "«Moja» — лишнее", {"example_pl": "Córka ma siedem lat"}),
    13526: (T + "«Mój» — лишнее", {"example_pl": "Syn ma piętnaście lat"}),
    13556: (T + "«Mój … skończy» — порядок", {"example_pl": "Tata w przyszłym miesiącu kończy czterdzieści lat"}),
    13593: (T + "«Mój» — лишнее", {"example_pl": "Dziadek ma już sześćdziesiąt lat"}),
    14941: (T + "«Mój» — лишнее", {"example_pl": "Dziadek opowiada świetne historie"}),
    15019: (T + "«Moi krewni» — порядок", {"example_pl": "Odwiedzają mnie krewni"}),
    15029: (T + "«Moja partnerka i ja» — калька", {"example_pl": "Z partnerką mamy wielkie plany na przyszłość"}),
    15084: (T + "«Moja» — лишнее", {"example_pl": "Mama jest gospodynią domową i zajmuje się domem"}),
    15383: (T + "«w małej wsi» — коряво", {"example_pl": "Mieszkam w małej wiosce"}),
    15384: (T + "«Wiatr jest silny» — калька", {"example_pl": "Wieje silny wiatr"}),
    16032: (T + "«swój» — лишнее", {"example_pl": "Proszę złożyć podpis"}),
    17163: (T + "«na tę podróż» — книжно", {"example_pl": "Potrzebujemy paszportów na wyjazd"}),
    17476: (T + "«Moja komórka jest zepsuta» — калька", {"example_pl": "Zepsuła mi się komórka"}),
    17489: (T + "«On» — лишнее", {"example_pl": "Naprawia samochód"}),
}

REPLACE = []

SPLIT_LATER = {}
