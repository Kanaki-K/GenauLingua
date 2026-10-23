"""Вычитка польского, порция p043 (C1), 23.10: лишние местоимения и кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    15170: (T + "«Nasz» — лишнее", {"example_pl": "Sąsiad od trzech lat jest wdowcem i teraz zaczął tańczyć tango"}),
    15195: (T + "«Nasza» — лишнее", {"example_pl": "Firmowa wigilia co roku zamienia się w orgię ciastek i grzańca"}),
    15198: (T + "«Nasza» — лишнее", {"example_pl": "Stara suczka przez dwanaście lat była wierną towarzyszką taty"}),
    15203: (T + "«Nasz» — лишнее", {"example_pl": "Pies pierdzi przez sen i wszyscy wychodzą z salonu"}),
    15220: (T + "«mojego» — лишнее", {"example_pl": "Kiedy przyjeżdża cały klan męża, brakuje nam krzeseł"}),
    15308: (T + "«mój» — лишнее", {"example_pl": "Po rozwodzie brat stał się dla syna ważną figurą ojca"}),
    15594: (T + "«naszym» — лишнее", {"example_pl": "W sierpniu wzrostu cukinii w ogrodzie nie da się już zahamować"}),
    15595: (T + "«nasza» — лишнее", {"example_pl": "W niedziele wieś jest jak wymarła, nawet piekarnia nie jest otwarta"}),
    15596: (T + "«nasza» — лишнее", {"example_pl": "Wiosną kotka gubi grube zimowe futro i cała kanapa jest w sierści"}),
    15602: (T + "«swoim» — лишнее", {"example_pl": "Sąsiad hoduje w małym ogródku dwadzieścia odmian pomidorów i rozdaje je całej ulicy"}),
    15643: (T + "«moja» — лишнее", {"example_pl": "Przez huragan na Bahamach koleżanka od trzech dni utknęła na lotnisku"}),
    15644: (T + "«W akwenach» — книжно", {"example_pl": "W zbiornikach wodnych wokół wsi można łowić tylko z kartą wędkarską, dziadek przekonał się o tym boleśnie"}),
    15658: (T + "«nasza» — лишнее", {"example_pl": "Po deszczu polna droga jest pełna kraterów, a dzieci wskakują do każdego"}),
    15685: (T + "«Nasz» — лишнее", {"example_pl": "Szczeniak w pierwszym tygodniu pogryzł trzy buty i nogę od stołu"}),
    15692: (T + "«naszą» — лишнее", {"example_pl": "Syn uważa kotkę za słodką, dopóki nie przyjdzie z myszą w pysku, wtedy jest dla niego drapieżnikiem"}),
    15695: (T + "«Nasz» — лишнее", {"example_pl": "Pies na spacerze najbardziej lubi tarzać się w padlinie, a potem musi do wanny"}),
    15697: (T + "«szukał w naszych śmieciach» — коряво", {"example_pl": "Szop pracz grzebał nam w śmieciach w poszukiwaniu jedzenia"}),
    15700: (T + "«Nasz» — лишнее", {"example_pl": "Kocur w nocy upolował mysz i dumnie położył ją pod drzwiami"}),
    15705: (T + "«naszemu» — лишнее", {"example_pl": "Dziś przychodzi kowal przyciąć kopyta kucykowi"}),
    15707: (T + "«naszą» — лишнее", {"example_pl": "Rano słońce zalewa całą sypialnię"}),
    15712: (T + "«naszego» — лишнее", {"example_pl": "Na urlopie w Kanadzie skunks dopadł psa i samochód wciąż śmierdzi"}),
    15720: (T + "«naszej» — лишнее", {"example_pl": "Co lato do kuchni przychodzą mrówki, bo czują cukier"}),
    16374: (T + "«Nasza» — лишнее", {"example_pl": "Stara kotka dzielnie stawia opór nowemu szczeniakowi"}),
    16379: (T + "«moją … naszych» — лишнее", {"example_pl": "Na wszelki wypadek wyznaczyliśmy siostrę na opiekuna prawnego dzieci"}),
    16394: (T + "«Moje» — лишнее", {"example_pl": "Dzieci chodzą do szkoły państwowej, a pieniądze na czesne odkładam na wycieczki klasowe"}),
    16404: (T + "«mojej» — лишнее", {"example_pl": "Do rodziny zastępczej kuzynki co trzy miesiące przychodzi ktoś z opieki społecznej"}),
    16410: (T + "«Ponieważ» — книжно", {"example_pl": "Kiedy w ogrodzie zapalił się kompostownik, strażacy najpierw myśleli o podpaleniu, a to było słońce"}),
    16412: (T + "«Nasz» — лишнее", {"example_pl": "Kot podporządkował sobie cały dom, nawet pies ustępuje mu miejsca"}),
    16422: (T + "«nasza» — лишнее", {"example_pl": "Od kilku dni lodówka jest w stanie oblężenia, syn rośnie"}),
    16426: (T + "«Moja» — лишнее", {"example_pl": "Kuzynka jest prokuratorką i mimo to ogląda każdy kryminał w telewizji"}),
    16441: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek przyjechał do Ameryki jako imigrant z jedną walizką"}),
    16443: (T + "«naszym» — лишнее", {"example_pl": "Dzięcioł na drzewie przed oknem co rano brzmi jak karabin maszynowy"}),
    16452: (T + "«mojej» — лишнее", {"example_pl": "Podczas powodzi w USA gwardia narodowa zabierała sąsiadów kuzynki łodziami"}),
    16504: (T + "«naszą … nasz» — лишнее", {"example_pl": "Na festyn uliczny zamknęli ulicę na całą sobotę i samochód utknął nam w garażu"}),
    16517: (T + "«Moja» — лишнее", {"example_pl": "Przyjaciółka jest położną i ze względu na tajemnicę zawodową nigdy nie mówi, kto u niej rodził"}),
    16531: (T + "«Naszego» — лишнее", {"example_pl": "Kocura nazywamy tylko „Jaśnie Oświeconym”, bo śpi wyłącznie w najlepszym fotelu"}),
    16532: (T + "«Ponieważ» — книжно", {"example_pl": "Kurtka ma małą plamę na rękawie, więc dostaję dwadzieścia procent rabatu"}),
    16544: (T + "«Ponieważ» — книжно", {"example_pl": "Syn jest jeszcze niepełnoletni, więc umowę na jego pierwszy telefon muszę podpisać ja"}),
}

REPLACE = []

SPLIT_LATER = {}
