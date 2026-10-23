"""Вычитка польского, порция p042 (C1), 23.10: лишние местоимения и кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    12822: (T + "«Moja … swoją» — лишнее", {"example_pl": "Przyjaciółka pracuje jako pielęgniarka na oddziale psychiatrycznym i kocha swoją pracę"}),
    12845: (T + "«nasz» — лишнее", {"example_pl": "Po weekendzie na wsi kot ma pchły, a teraz drapie się cała rodzina"}),
    12865: (T + "«moja» — лишнее", {"example_pl": "Odkąd chodzi do przedszkola, mała jest bardzo podatna na przeziębienia"}),
    12873: (T + "«Mój smartwatch» — калька", {"example_pl": "Smartwatch mierzy mi tętno nawet w nocy"}),
    12882: (T + "«Nasz» — лишнее", {"example_pl": "Stary pies ma brzydki zapach z pyska, więc musimy iść z nim do weterynarza"}),
    12891: (T + "«Nasza» — лишнее", {"example_pl": "Kotka ma cukrzycę i dostaje insulinę dwa razy dziennie"}),
    12895: (T + "«naszemu» — лишнее", {"example_pl": "Weterynarz usunął psu mały ropień z ucha"}),
    12898: (T + "«nasza» — лишнее", {"example_pl": "Po znieczuleniu u weterynarza kotka jeszcze zatacza się po mieszkaniu"}),
    12900: (T + "«Nasz» — лишнее", {"example_pl": "Mały po karuzeli zwymiotował w samochodzie"}),
    12904: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez wszy w przedszkolu sanepid wysłał list do wszystkich rodziców"}),
    12907: (T + "«moi» — лишнее", {"example_pl": "O ostatni kawałek pizzy synowie prawie skoczyli sobie do gardeł"}),
    13038: (T + "«Nasz … wciąż nawet robi» — порядок", {"example_pl": "Stary lekarz rodzinny wciąż robi nawet wizyty domowe, kiedy ma się gorączkę"}),
    13735: (T + "«Nasz» — лишнее", {"example_pl": "Mały co rano krzywo zapina kurtkę"}),
    14126: (T + "«Swój» — лишнее", {"example_pl": "Urlop syn tym razem pokrywa w całości z własnego kieszonkowego"}),
    14180: (T + "«Nasza» — лишнее", {"example_pl": "Mała ma takie gadane, że wygrywa każdą kłótnię ze starszym bratem"}),
    14189: (T + "«swojego» — лишнее", {"example_pl": "Córka wkleja do notatnika bilety do kina, liście i zdjęcia i rysuje wokół ramki"}),
    14570: (T + "«Moja rodzina jest katolicka» — калька", {"example_pl": "U nas w rodzinie wszyscy są katolikami i co niedzielę chodzą do kościoła"}),
    14577: (T + "«swoją» — лишнее", {"example_pl": "Co wieczór syn gra mi na flecie prostym nową piosenkę"}),
    14586: (T + "«Moich trzech synów nazywa» — согласование", {"example_pl": "Trzej synowie nazywają siebie trzema muszkieterami i walczą w przedpokoju drewnianymi łyżkami"}),
    14587: (T + "«Nasza» — лишнее", {"example_pl": "Sąsiadka jest Żydówką i co roku zaprasza nas na Chanukę z plackami ziemniaczanymi"}),
    14589: (T + "«mojej» — лишнее", {"example_pl": "Na bierzmowanie siostrzenicy przyjeżdża nawet arcybiskup i cała rodzina się stroi"}),
    14603: (T + "«swój» — лишнее", {"example_pl": "Bardzo uroczyście syn wręcza mi pierwszy własnoręcznie zrobiony prezent, koronę z tektury"}),
    14605: (T + "«naszej» — лишнее", {"example_pl": "Syn uważa, że w piwnicy mieszka coś nadprzyrodzonego, a to tylko ogrzewanie"}),
    14606: (T + "«nasz» — лишнее", {"example_pl": "Mama mówi, że pies jest jej muzą, odkąd maluje, jest na każdym obrazie"}),
    14610: (T + "«nasz» — лишнее", {"example_pl": "Córka co wieczór ćwiczy na wiolonczeli, a pies za każdym razem wyje razem z nią"}),
    14628: (T + "нет слова карточки «historia miłosna»", {"example_pl": "Historia miłosna dziadków zaczyna się od zgubionego parasola na przystanku autobusowym"}),
    14645: (T + "«swojej» — лишнее", {"example_pl": "Dziadek pisze pamiętniki i po roku doszedł dopiero do pierwszej krowy"}),
    14647: (T + "«swoim» — лишнее", {"example_pl": "Siostrzeniec kręci telefonem krótkie filmy z chomikiem i już nazywa siebie filmowcem"}),
    14656: (T + "«Moja» — лишнее", {"example_pl": "Babcia jest bardzo przesądna i unika czarnych kotów"}),
    14671: (T + "«moich» — лишнее", {"example_pl": "Kiedy pada Wi-Fi, dla dzieci to koniec świata"}),
    15139: (T + "«Mój» — лишнее", {"example_pl": "Wujek jest homoseksualny i od trzydziestu lat mieszka z mężem w tej samej wsi"}),
}

REPLACE = []

SPLIT_LATER = {}
