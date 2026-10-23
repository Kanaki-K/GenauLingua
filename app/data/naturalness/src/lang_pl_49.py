"""Вычитка польского, порция p049 (C2), 23.10: лишние местоимения и кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    16724: (T + "«mojej» — лишнее", {"example_pl": "W miejscu pamięci klasa córki zobaczyła też komorę gazową, potem długo nikt się nie odzywał"}),
    16741: (T + "«moja» — лишнее", {"example_pl": "Dopóki szef jest na urlopie, władzę dowodzenia w biurze ma koleżanka"}),
    16751: (T + "«swoich» — лишнее", {"example_pl": "Syn zbudował z kartonu i rolek po papierze toaletowym wyrzutnię rakiet dla ludzików lego"}),
    16752: (T + "«Moja» — лишнее", {"example_pl": "Koleżanka z Polski opowiada, jak jej rodzice żyli w czasie stanu wojennego w 1981 roku"}),
    16753: (T + "«moimi» — лишнее", {"example_pl": "Między dziećmi od śniadania panuje rozejm"}),
    16765: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez deszcz przekładamy grilla na przyszłą sobotę"}),
    16771: (T + "«moim» — лишнее", {"example_pl": "Bez nakazu przeszukania komisarz w ulubionym serialu nigdy nie może wejść do domu"}),
    16777: (T + "«Moja» — лишнее", {"example_pl": "Ciocia zasiada w radzie miasta, a jej frakcja na każdym posiedzeniu kłóci się o ścieżki rowerowe"}),
    16784: (T + "«Mój» — лишнее", {"example_pl": "Siostrzeniec studiuje informatykę kryminalistyczną i odzyskuje każdy usunięty plik"}),
    16800: (T + "«Mój» — лишнее", {"example_pl": "Ulubiony komisarz z serialu kryminalnego w nowym sezonie przechodzi do wydziału narkotykowego"}),
    16840: (T + "«Mój» — лишнее", {"example_pl": "Brat jest przedstawicielem firmy winiarskiej i jeździ po całej Europie"}),
    16862: (T + "«Mój» — лишнее", {"example_pl": "Doradca podatkowy zawsze znajduje jakąś lukę, żeby wyszło mi mniej do zapłaty"}),
    16863: (T + "«Mój» — лишнее", {"example_pl": "Kolega dorastał w getcie w Chicago, a dziś jest pediatrą"}),
    16873: (T + "«Mój» — лишнее", {"example_pl": "Kocur jest na głodówce, odkąd zmieniliśmy karmę"}),
    16879: (T + "«Moja» — лишнее", {"example_pl": "Sąsiadka pracuje w ministerstwie finansów i jesienią często wraca do domu dopiero późno"}),
    16883: (T + "«Mój» — лишнее", {"example_pl": "Wujek jako fotograf był w wielu strefach wojny, a dziś fotografuje już tylko wesela"}),
    16885: (T + "«moją» — лишнее", {"example_pl": "Między mamą a sąsiadką od lat trwa waśń o żywopłot"}),
    16886: (T + "«płacić swoje raty» — коряво", {"example_pl": "Dłużnik przestał spłacać raty"}),
    16901: (T + "«Moi» — лишнее", {"example_pl": "Dziadkowie poznali się w 1946 roku w obozie dla uchodźców"}),
    16904: (T + "«mojego» — лишнее", {"example_pl": "U wujka nawet grillowanie staje się ideologią: tylko węgiel, nigdy gaz"}),
    16908: (T + "«Mój» — лишнее", {"example_pl": "Brat jest wykonawcą testamentu dziadka i wszystkim się zajmuje"}),
    16947: (T + "«Mój amerykański szwagier» — коряво", {"example_pl": "Szwagier z Ameryki głosuje na republikanów, a siostra na demokratów"}),
    16950: (T + "«mój» — лишнее", {"example_pl": "W swoim pokoju syn jest małym anarchistą: tam nie obowiązują żadne zasady"}),
    16958: (T + "«mój» — лишнее", {"example_pl": "Po ośmiu latach w Niemczech kolega składa wniosek o niemieckie obywatelstwo"}),
    16967: (T + "«Mój» — лишнее", {"example_pl": "Wujek jest obrońcą w sprawach karnych i przy obiedzie nigdy nie opowiada o swoich sprawach"}),
    16975: (T + "«moja» — лишнее", {"example_pl": "Na wywiadówce żona kruszy kopie za młodą nauczycielką"}),
    17363: (T + "«swoim» — лишнее", {"example_pl": "W niedzielę dziadek lubi zrobić przejażdżkę zabytkowym autem po wsiach"}),
    17660: (T + "«Mój» — лишнее", {"example_pl": "Nauczyciel fizyki zbudował ze starego radia mały nadajnik"}),
    17667: (T + "«z powodu konserwacji» — книжно", {"example_pl": "Winda jest dziś nieczynna, bo trwa konserwacja, musimy iść schodami"}),
    17670: (T + "«Mój» — лишнее", {"example_pl": "Telefon automatycznie szyfruje wszystkie zdjęcia"}),
    17689: (T + "«mój … moje» — лишнее", {"example_pl": "Trojan zainfekował mi komputer i ukradł wszystkie dane"}),
    17736: (T + "«w mojej» — лишнее", {"example_pl": "Pager w kieszeni zawsze piszczy w nieodpowiednim momencie"}),
    17865: (T + "«moja» — лишнее", {"example_pl": "Przez inflację ulubiona bułka w piekarni kosztuje teraz prawie euro"}),
    17877: (T + "«moich» — лишнее", {"example_pl": "Dla dzieci koszenie trawnika za dwa euro na godzinę to czysty wyzysk"}),
    17879: (T + "«Nasz» — лишнее", {"example_pl": "Szczeniak pochodzi z małej hodowli na wsi, widzieliśmy też jego rodziców"}),
    17882: (T + "«Nasza» — лишнее", {"example_pl": "Ulubiona piekarnia ogłosiła bankructwo, teraz kupujemy chleb w supermarkecie"}),
    17885: (T + "«moja kondycja to» — калька", {"example_pl": "Po trzech piętrach brakuje mi tchu, kondycję mam katastrofalną"}),
}

REPLACE = []

SPLIT_LATER = {}
