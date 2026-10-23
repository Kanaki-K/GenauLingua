"""Вычитка польского, порция p040 (C1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    9093: (T + "«Mój terminarz jest» — калька", {"example_pl": "W tym tygodniu mam tak napięty terminarz, że nie mam czasu nawet na fryzjera"}),
    9103: (T + "«Mój» — лишнее", {"example_pl": "Kolega jest głównym kandydatem na kierownika oddziału"}),
    9105: (T + "«Nasza … z efektywnością … na zewnątrz» — коряво", {"example_pl": "Lekarka rodzinna pracuje tak efektywnie, że po dziesięciu minutach jest się już z powrotem na dworze"}),
    9113: (T + "«Nasza» — лишнее", {"example_pl": "Korepetytorka to emerytowana nauczycielka matematyki z sąsiedniego domu"}),
    9114: (T + "«mojego» — лишнее", {"example_pl": "Naleśniki to konik brata, nic innego nie gotuje"}),
    9130: (T + "«Nasz … swoje potrzeby» — коряво", {"example_pl": "Pies najchętniej załatwia się tuż przed domem sąsiadów"}),
    9217: (T + "«swoją» — лишнее", {"example_pl": "W wyborach przewodniczącego klasy córka odrzuciła nominację, bo nie miała ochoty"}),
    9568: (T + "«naszego» — лишнее", {"example_pl": "Szkoła dla psów szkoli szczeniaka na psa terapeutę"}),
    9848: (T + "«Moje oszczędności» — калька", {"example_pl": "Oszczędności wystarczą mi akurat na wakacje"}),
    9851: (T + "«swoją» — лишнее", {"example_pl": "Syn wymienił kanapkę na dwa ciastka od kolegi"}),
    9866: (T + "«nie kupuje historii» — англицизм", {"example_pl": "Nauczycielka nie wierzy w jego historię o psie, który zjadł zadanie domowe"}),
    10808: (T + "«na zewnątrz» → «na mieście»", {"example_pl": "Z próżności dziadek nosi okulary tylko w domu, a na mieście nikogo nie poznaje"}),
    10811: (T + "«Nasz» — лишнее", {"example_pl": "Pies ma słabość do skarpetek, ale tylko świeżo noszonych"}),
    10830: (T + "«Ponieważ» — книжно", {"example_pl": "Nikt nie zjadł jego ciasta, więc mąż jest trochę urażony"}),
    10868: (T + "«Nasz» — лишнее", {"example_pl": "Stary pies jest chaotyczny i głośny, ale właśnie dlatego taki uroczy"}),
    10886: (T + "«Nasz» — лишнее", {"example_pl": "Kot godzinami czai się przed mysią dziurą za szafą"}),
    10888: (T + "«Nasza» — лишнее", {"example_pl": "Sąsiadka jest tak zaradna, że oprócz trójki dzieci dba jeszcze o ogród całej ulicy"}),
    10909: (T + "«Nasza» — лишнее", {"example_pl": "Kotka wiedzie wspaniałe życie: śpi, je i daje się obsługiwać całemu domowi"}),
    10922: (T + "«Mój» — лишнее", {"example_pl": "Szwagier to prawdziwy fanatyk fitnessu, nawet na weselu robi pompki"}),
    10928: (T + "«Nasza» — лишнее", {"example_pl": "Kotka wskakuje na szafę z takim wdziękiem, że za każdym razem bijemy jej brawo"}),
    10935: (T + "«mojego» — лишнее", {"example_pl": "Do wymówek syna potrzeba sporo wyobraźni"}),
    10937: (T + "«moja» — лишнее", {"example_pl": "Przy trzecim rozlanym soku rano nawet cierpliwa żona traci panowanie nad sobą"}),
    10939: (T + "«Nasz» — лишнее", {"example_pl": "Pies ma pogodne usposobienie, nawet listonosz jest jego przyjacielem"}),
    10940: (T + "«Nasza» — лишнее", {"example_pl": "Opiekunka jest tak godna zaufania, że dajemy jej nawet klucz do domu"}),
    10948: (T + "«moi» — лишнее", {"example_pl": "O ostatni kawałek pizzy synowie niemal za każdym razem urządzają małą bójkę"}),
    10964: (T + "«moja trójka» — калька", {"example_pl": "Tylko przy jedzeniu pizzy cała trójka dzieci jest w pełnej zgodzie"}),
    10968: (T + "«Ponieważ» — книжно", {"example_pl": "Byłem niedbały przy wypełnianiu formularza, więc nowy dowód przyjdzie dopiero za sześć tygodni"}),
    10974: (T + "нет слова карточки «wyśmiewać»", {"example_pl": "Dzieci mnie wyśmiewają, bo nie wiem, jak wrzucić filmik do sieci"}),
    10976: (T + "«nasz» — лишнее", {"example_pl": "Z wielką żądzą pies patrzy na każdy kawałek kiełbasy, który może spaść ze stołu"}),
    10992: (T + "«nasz» — лишнее", {"example_pl": "U babci syn nigdy nie jest niegrzeczny, tylko w domu wspina się na wszystkie meble"}),
    10997: (T + "«Nasz» — лишнее", {"example_pl": "Kot jest zupełnie nieposłuszny: im częściej mówimy „Zejdź ze stołu!”, tym chętniej tam wskakuje"}),
    11010: (T + "«mojego» — лишнее", {"example_pl": "W korku u zwykle spokojnego męża pojawia się agresja, której w ogóle u niego nie znam"}),
    11012: (T + "«Nasz» — лишнее", {"example_pl": "Kot patrzy na nowego szczeniaka bardzo wrogo i syczy, kiedy ten podchodzi za blisko"}),
    11013: (T + "«Nasi» — лишнее", {"example_pl": "Nowi sąsiedzi są bardzo taktowni i po dziesiątej wieczorem już nie piorą"}),
    11026: (T + "«Naszego» — лишнее", {"example_pl": "Psa nie da się przechytrzyć: tabletkę w serze za każdym razem znajduje i wypluwa"}),
    11027: (T + "«swojego» — лишнее", {"example_pl": "Na zaproszeniu jest napisane „mile widziane przebranie”, a mąż od wczoraj szuka pirackiego kapelusza"}),
    11033: (T + "«Nasz» — лишнее", {"example_pl": "Kocur nie ma skrupułów: kradnie psu jedzenie prosto z miski, kiedy ten patrzy"}),
}

REPLACE = []

SPLIT_LATER = {}
