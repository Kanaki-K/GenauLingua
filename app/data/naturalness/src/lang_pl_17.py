"""Вычитка польского, порция p017 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    8861: (T + "«z powodu żywopłotu» — коряво", {"example_pl": "Prezes ogródków działkowych zwrócił nam uwagę w sprawie żywopłotu"}),
    8879: (T + "«pracownica pracuje» — повтор", {"example_pl": "Ta pracownica jest w tej firmie już dziesięć lat"}),
    8910: (T + "«Kelner, rachunek» — грубо", {"example_pl": "Panie kelnerze, poproszę rachunek!"}),
    8932: (T + "«organizuje terminy spotkań» — книжно", {"example_pl": "Sekretarz pracuje w biurze i ustala szefowi terminy spotkań"}),
    8947: (T + "«na zlecenie» — неточно", {"example_pl": "Pracuje jako niezależna dziennikarka"}),
    9010: (T + "«Mój» — лишнее", {"example_pl": "Dziadek był kiedyś marynarzem"}),
    9032: (T + "«Mój» — лишнее", {"example_pl": "Brat uczy się na cieślę"}),
    9054: (T + "«Mój» — лишнее", {"example_pl": "Wujek jest przedsiębiorcą i nigdy nie ma czasu"}),
    9118: (T + "«On nie jest dyplomatą» — тяжело", {"example_pl": "Żaden z niego dyplomata, zawsze mówi wprost, co myśli"}),
    9124: (T + "«Moja» — лишнее", {"example_pl": "Ciocia jest pisarką i mieszka w Wiedniu"}),
    9138: (T + "«mój» — лишнее", {"example_pl": "Zimą wujek pracuje jako drwal"}),
    9155: (T + "«Moja» — лишнее", {"example_pl": "Siostra pracuje jako chirurg w szpitalu"}),
    9164: (T + "«Pan» — регистр", {"example_pl": "Z wnioskiem musi pan iść do właściwego urzędu"}),
    9173: (T + "«Karczmarka … swoich» — архаично", {"example_pl": "Gospodyni zna osobiście wszystkich stałych gości"}),
    9186: (T + "«Mój» — лишнее", {"example_pl": "Mąż piłuje w piwnicy drewno do kominka"}),
    9267: (T + "«Moi» — лишнее", {"example_pl": "Koledzy z pracy są naprawdę mili i pomocni"}),
    9294: (T + "«Moja» — лишнее", {"example_pl": "Kuzynka jest pilotką i co tydzień lata do Nowego Jorku"}),
    9446: (T + "«Ona» — лишнее", {"example_pl": "Mówi bardzo dobrze po francusku"}),
    9451: (T + "«moje» — лишнее", {"example_pl": "Uczę dziecko pływać"}),
    9468: (T + "«Moja» — лишнее", {"example_pl": "Mama od trzydziestu lat uczy w szkole podstawowej"}),
    9474: (T + "«Mój» — лишнее", {"example_pl": "Syn potrafi wymyślać świetne historie"}),
    9481: (T + "«Moja» — лишнее", {"example_pl": "Siostra pracuje w instytucie badań morskich"}),
    9532: (T + "«mojego» — лишнее", {"example_pl": "Prowadzę poszukiwania do artykułu"}),
    9553: (T + "«Mój» — лишнее", {"example_pl": "Syn pilnie potrzebuje korepetycji z angielskiego"}),
    9592: (T + "«Moje pióro jest puste» — калька", {"example_pl": "W wiecznym piórze skończył mi się atrament, potrzebuję nowego"}),
    9598: (T + "«Mój» — лишнее", {"example_pl": "Syn chodzi teraz do zerówki"}),
    9603: (T + "«Każdego ranka» — книжно", {"example_pl": "Codziennie rano jeżdżę do szkoły autobusem szkolnym"}),
    9606: (T + "«Moi» — лишнее", {"example_pl": "Koledzy z klasy pomagają mi w zadaniach domowych"}),
    9638: (T + "«Moja ortografia» — калька", {"example_pl": "Z ortografią bywa u mnie różnie"}),
    9642: (T + "«moje słownictwo jest większe» — калька", {"example_pl": "Dzięki serialom po niemiecku mam coraz bogatsze słownictwo"}),
    9756: (T + "«jest twój» — калька", {"example_pl": "Jakiej marki masz samochód?"}),
    9758: (T + "«Mój portfel zniknął» — калька", {"example_pl": "Zniknął mi portfel"}),
    9783: (T + "«Czy» — книжно", {"example_pl": "Mogę pożyczyć twoją książkę?"}),
    9796: (T + "«mojego» — лишнее", {"example_pl": "Potrzebuję paragonu do zeznania podatkowego"}),
    9832: (T + "«Czy» — книжно", {"example_pl": "Jako student dostanę zniżkę?"}),
    9852: (T + "«moje» — лишнее", {"example_pl": "Zajrzę szybko na konto bankowe"}),
    9878: (T + "нет слова карточки", {"example_pl": "Muszę jeszcze załatwić parę sprawunków"}),
    9915: (T + "«Jaki jest twój» — калька", {"example_pl": "Jaki masz numer konta?"}),
    9935: (T + "«Moja» — лишнее", {"example_pl": "Mama zawsze kupuje róże w kwiaciarni na rogu"}),
}

REPLACE = []

SPLIT_LATER = {}
