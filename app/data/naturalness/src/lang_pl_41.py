"""Вычитка польского, порция p041 (C1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    11063: (T + "«Nasz» — лишнее", {"example_pl": "Pies i kocur sąsiada są nierozłączne i nawet śpią razem na słońcu"}),
    11092: (T + "«Nasz» — лишнее", {"example_pl": "Dozorca to dziwak, najchętniej kosi trawnik o szóstej rano"}),
    11103: (T + "«Nasz» — лишнее", {"example_pl": "Stary budzik jest bardziej niezawodny niż jakikolwiek telefon"}),
    11110: (T + "«Nasz» — лишнее", {"example_pl": "Hydraulik jest tak niesolidny, że teraz dzwonię do niego co rano"}),
    11114: (T + "«Moja tolerancja … jest zerowa» — калька", {"example_pl": "Po dziesiątej wieczorem mam zerową tolerancję na głośną muzykę"}),
    11115: (T + "«moją» — лишнее", {"example_pl": "Przez niezdolność do mówienia „nie” co weekend dostaję nowe zadania"}),
    11116: (T + "«Nasza» — лишнее", {"example_pl": "Nowa pediatra promieniuje takim spokojem, że nawet dzieci nie boją się zastrzyku"}),
    11123: (T + "«Nasza» — лишнее", {"example_pl": "Dwulatka buntuje się teraz przy wszystkim, co mówimy"}),
    11126: (T + "«Nasz» — лишнее", {"example_pl": "Kot to mały buntownik, śpi tylko tam, gdzie nie wolno"}),
    11132: (T + "«Moja niechęć … jest znana» — калька", {"example_pl": "W całym biurze wiedzą o mojej niechęci do porannych spotkań"}),
    11137: (T + "«Mój» — лишнее", {"example_pl": "Chłopak jest bardzo pomysłowy, jeśli chodzi o wymówki, dlaczego nie może tańczyć"}),
    11145: (T + "«Mój» — лишнее", {"example_pl": "Dawny szef ciągle szykanował mnie bezsensownymi tabelkami w Excelu"}),
    11159: (T + "«mojej» — лишнее", {"example_pl": "Maksyma mamy: nigdy nie chodzić na zakupy z pustym żołądkiem"}),
    11176: (T + "«Nasz» — лишнее", {"example_pl": "Mops w kostiumie dinozaura wygląda raczej słodko niż przerażająco"}),
    11181: (T + "«Nasza» — лишнее", {"example_pl": "Właścicielka mieszkania jest nieco ekscentryczna, na każdą okazję nosi inny kapelusz"}),
    11199: (T + "«Nasza» — лишнее", {"example_pl": "Pierwsza próba samodzielnego tapetowania salonu skończyła się kompletnym fiaskiem"}),
    11241: (T + "«Mój» — лишнее", {"example_pl": "Kocur czuje się ponad tym wszystkim i ignoruje nas, gdy go wołamy"}),
    11461: (T + "«mojej włoskiej szwagierki» — коряво", {"example_pl": "Dla szwagierki Włoszki śmietana w carbonarze to perwersja"}),
    11897: (T + "«Nasz» — лишнее", {"example_pl": "Królik co noc podgryza kable za kanapą"}),
    12249: (T + "«Mój» — лишнее", {"example_pl": "Sąsiad jest zapalonym kolekcjonerem dzbanków do kawy, w kuchni ma ich ponad dwieście"}),
    12284: (T + "«mój tata mojego syna» — коряво", {"example_pl": "„No, kolego, znowu wykopałeś piłkę do ogrodu sąsiada?” – pyta dziadek wnuka"}),
    12757: (T + "«mojego» — лишнее", {"example_pl": "Pierwszym objawem przeziębienia u męża jest zawsze zły humor"}),
    12766: (T + "«Mój» — лишнее", {"example_pl": "Dziadek ma cukrzycę i musi kontrolować dietę"}),
    12789: (T + "«Ponieważ» — книжно", {"example_pl": "Córce ciągle zapalają się migdałki, więc wiosną zostaną usunięte"}),
    12799: (T + "«Moja» — лишнее", {"example_pl": "Siostrzenica studiuje medycynę i koniecznie chce potem pracować w medycynie sądowej, babcia uważa to za upiorne"}),
}

REPLACE = []

SPLIT_LATER = {}
