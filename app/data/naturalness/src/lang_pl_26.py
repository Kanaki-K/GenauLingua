"""Вычитка польского, порция p026 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    18342: (T + "«jest napisane … są zabronione» — коряво", {"example_pl": "W umowie najmu jest zapis, że nie wolno trzymać zwierząt"}),
    18378: (T + "«Gdzie jest Pana» — калька, «pan» строчной", {"example_pl": "Gdzie ma pan stałe miejsce zamieszkania?"}),
    18398: (T + "«Nasza … swój» — лишнее", {"example_pl": "Sąsiadka z miłością dba o ogródek przed domem"}),
    18405: (T + "«znajduje się» — книжно", {"example_pl": "Warsztat jest w suterenie"}),
    18436: (T + "«jest pełne» — калька", {"example_pl": "W centrum miasta jest pełno sklepów i restauracji"}),
    18446: (T + "«za swoim pulpitem» — калька", {"example_pl": "Nauczyciel stoi za katedrą"}),
    18460: (T + "порядок «proszę»", {"example_pl": "Możesz, proszę, wytrzeć talerze?"}),
    18473: (T + "«swoje» — лишнее", {"example_pl": "Pies ma miejsce do spania pod stołem"}),
    18486: (T + "«prowadzi domowe życie» — калька", {"example_pl": "Jest bardzo domowa i rzadko gdzieś wychodzi"}),
    18487: (T + "порядок слов", {"example_pl": "Dzieci odrabiają lekcje przy kuchennym stole"}),
    18489: (T + "«nasz» — лишнее", {"example_pl": "Przebudowujemy stary dom, żeby mieć więcej miejsca"}),
    18492: (T + "«już jest zajęte» — коряво", {"example_pl": "Pośrednik dwa razy przekładał termin oglądania, a teraz mieszkania już nie ma"}),
    18498: (T + "«Jako kaucję … chce trzy» — коряво", {"example_pl": "Właściciel chce kaucji w wysokości trzech czynszów miesięcznych, to prawie trzy tysiące euro"}),
    18702: (T + "«Pana» → «pana»", {"example_pl": "Wkrótce się do pana odezwę"}),
    18707: (T + "«Twój paszport jest» — калька", {"example_pl": "Masz nieważny paszport"}),
    18723: (T + "«Twój czynsz jest» — калька", {"example_pl": "Czynsz masz zaległy już od dawna"}),
    18751: (T + "«spóźniony» → «opóźniony» о поезде", {"example_pl": "Pociąg jest opóźniony"}),
    18871: (T + "«stołówka jest pełna» — калька", {"example_pl": "W porze obiadowej w stołówce jest tłum"}),
    18890: (T + "«swój» — лишнее", {"example_pl": "W soboty koszę trawnik"}),
    18894: (T + "«Ona … włosy» — лишнее", {"example_pl": "Czesze się codziennie rano"}),
    18936: (T + "«swoją» — лишнее", {"example_pl": "Wypłatę dostaniesz na koniec miesiąca"}),
    18972: (T + "«moja» — лишнее", {"example_pl": "W wakacje córka pracuje jako kelnerka w lodziarni"}),
    18991: (T + "«moi» — лишнее", {"example_pl": "Na balu dziadkowie zawsze tańczą pierwszego walca"}),
    18993: (T + "«Mój» — лишнее", {"example_pl": "Tata w samochodzie słucha tylko rocka z lat osiemdziesiątych"}),
    18998: (T + "«mój» — лишнее", {"example_pl": "Od operacji dziadek chodzi o lasce"}),
    19007: (T + "«Mój» — лишнее", {"example_pl": "Kolega to prawdziwy hamburczyk i co piątek je bułkę z rybą"}),
    19040: (T + "порядок слов", {"example_pl": "Z powodu wysypki lekarz rodzinny skierował mnie do dermatologa"}),
    19045: (T + "«Następnego lata» → «Przyszłego lata»", {"example_pl": "Przyszłego lata przeprowadzamy się do Hamburga, mąż znalazł tam pracę"}),
    2043: (T + "«Dla uniknięcia» — книжно", {"example_pl": "Żeby uniknąć kłótni, każde dziecko ma u nas własnego pilota"}),
    6754: (T + "«moja praca jest pewna» — калька", {"example_pl": "Na szczęście mam pewną pracę"}),
}

REPLACE = []

SPLIT_LATER = {}
