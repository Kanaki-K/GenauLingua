"""Вычитка польского, порция p048 (C2), 23.10: лишние местоимения, «Czy», кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    14283: (T + "«Czy» — лишнее", {"example_pl": "Może mnie pan połączyć z sekretarką?"}),
    14288: (T + "«swój» — лишнее", {"example_pl": "Koniec z wymówkami, dziś sprzątasz pokój!"}),
    14298: (T + "«moja» — лишнее", {"example_pl": "Powiedzieć, że siostra lubi gadać, to mało powiedziane"}),
    14702: (T + "«mój» — лишнее", {"example_pl": "Przy strojeniu gitary nauczyciel od razu słyszy, czy kwinta jest czysta"}),
    14715: (T + "«moja» — лишнее", {"example_pl": "Na szkolnym koncercie siostrzenica po raz pierwszy gra pierwsze skrzypce"}),
    14721: (T + "«Nasz» — лишнее", {"example_pl": "Pies umie nową sztuczkę: daje łapę, a potem przewraca się na plecy"}),
    14766: (T + "«mojej» — лишнее", {"example_pl": "Na ślubie koleżanki imam wygłosił krótką przemowę także po niemiecku"}),
    14767: (T + "«Moi … swojego» — лишнее", {"example_pl": "Rodzice co wieczór oglądają odcinek ulubionego tureckiego serialu"}),
    14768: (T + "«swoje» — лишнее", {"example_pl": "Po trzech dniach grypy mąż świętuje zmartwychwstanie dużą pizzą"}),
    14777: (T + "«swoją» — лишнее", {"example_pl": "Wciąż chętnie puszcza starą płytę winylową Beatlesów"}),
    14778: (T + "«Mój … do naszego» — лишнее", {"example_pl": "Wujek jest rzeźbiarzem i zrobił nam do ogrodu jeża z kamienia"}),
    14801: (T + "«mojej» — лишнее", {"example_pl": "Spóźnić się na niedzielny obiad u babci to grzech śmiertelny"}),
    14809: (T + "«mój» — лишнее", {"example_pl": "Do jednej sceny w „Tatorcie” wujek siedział jako statysta w kawiarni"}),
    15028: (T + "«na zewnątrz» → «przez okno»", {"example_pl": "Kicia siedzi na parapecie i patrzy przez okno"}),
    15216: (T + "«Mój» — лишнее", {"example_pl": "Brat bliźniak zawsze dzwoni, kiedy jestem chory, jakby to czuł"}),
    15223: (T + "«Nasz» — лишнее", {"example_pl": "Kocur siada tyłkiem prosto na mojej klawiaturze"}),
    15230: (T + "«swojego» — лишнее", {"example_pl": "Syn to wierna kopia ojca"}),
    15251: (T + "«mój» — лишнее", {"example_pl": "Z trzydziestoma latami w firmie kolega to prawdziwy weteran, zna każdą sztuczkę"}),
    15259: (T + "«Nasza» — лишнее", {"example_pl": "Sąsiadka uparcie twierdzi, że jest potomkiem Goethego"}),
    15261: (T + "«Nasi» — лишнее", {"example_pl": "Sąsiedzi od dwóch lat są rodziną zastępczą dla małego rodzeństwa"}),
    15267: (T + "«Moja przyjaciółka i ja» — калька", {"example_pl": "Z najlepszą przyjaciółką jesteśmy bratnimi duszami, często dzwonimy do siebie w tej samej chwili"}),
    15287: (T + "«Nasza» — лишнее", {"example_pl": "Sąsiadka jest samotną matką trojga dzieci, a mimo to zawsze ma dobry humor"}),
    15290: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn w wieku trzydziestu lat wciąż daje mamie pranie, prawdziwy maminsynek"}),
    15329: (T + "«Mój» — лишнее", {"example_pl": "Syn zrobił się prawdziwą tyczką, odkąd tak szybko rośnie"}),
    15330: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek w wieku dziewięćdziesięciu lat nie jest zniedołężniałym starcem, wciąż codziennie jeździ na rowerze"}),
    15747: (T + "«moja skrzynka jest zalana» — калька", {"example_pl": "Od czasu ogłoszenia na portalu z używanymi rzeczami skrzynkę mam zalaną mailami"}),
    15785: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek jako dziecko przeżył klęskę głodu i do dziś nie wyrzuca ani kawałka chleba"}),
    15788: (T + "«nasza» — лишнее", {"example_pl": "Po trzech tygodniach nad morzem sąsiadka wygląda kwitnąco"}),
    15794: (T + "«nasz» — лишнее", {"example_pl": "Gdy tylko ktoś ćwiczy na skrzypcach, pies głośno wyje do wtóru"}),
    15820: (T + "«naszym» — лишнее", {"example_pl": "Bambus w ogrodzie rośnie szybciej, niż zdążymy go przycinać"}),
    15830: (T + "«moja» — лишнее", {"example_pl": "Kiedy chodzi o jej dzieci, zwykle łagodna siostra zmienia się w lwicę"}),
    15854: (T + "«moja» — лишнее", {"example_pl": "Odkąd śpiewa w chórze, mama naprawdę rozkwitła"}),
    15872: (T + "«nasza» — лишнее", {"example_pl": "Kiedy się ją głaszcze, kotka chowa pazury"}),
    15879: (T + "«nasz» — лишнее", {"example_pl": "W maju cały ogród pachnie bzem"}),
    16622: (T + "«naszej» — лишнее", {"example_pl": "Dostawa nowej kanapy opóźnia się o dwa tygodnie"}),
    16626: (T + "«Moi» — лишнее", {"example_pl": "Dziadkowie do dziś niechętnie mówią o czasach starego reżimu"}),
    16635: (T + "«Nasz» — лишнее", {"example_pl": "Dozorca zna na pamięć każdy paragraf regulaminu domu"}),
    16638: (T + "«naszym» — лишнее", {"example_pl": "Kameleon w terrarium tak dobrze się maskuje, że czasem muszę go szukać"}),
    16675: (T + "«swojej» — лишнее", {"example_pl": "Nasza burmistrz w czasie kadencji zbudowała trzy nowe place zabaw"}),
    16676: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek był w czasie wojny partyzantem w górach, nigdy nie lubił o tym mówić"}),
    16684: (T + "«Moi» — лишнее", {"example_pl": "Rodzice dorastali w socjalizmie i wciąż pamiętają kolejki przed sklepami"}),
    16694: (T + "запятая перед деепричастием", {"example_pl": "Zabijamy czas, grając w karty"}),
}

REPLACE = []

SPLIT_LATER = {}
