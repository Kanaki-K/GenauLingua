"""Вычитка польского, порция p027 (B2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    7109: (T + "«Potrafisz odgadnąć» — книжно", {"example_pl": "Zgadniesz tę zagadkę?"}),
    7118: (T + "«W przestrzeni stepu» — калька", {"example_pl": "Na stepie, w tej bezkresnej dali, godzinami nie widać ani jednego domu"}),
    7120: (T + "«Moi» — лишнее", {"example_pl": "Rodzice nie pochwalają mojej decyzji"}),
    7134: (T + "порядок слов", {"example_pl": "Tej nocy gwiazdy świecą bardzo jasno"}),
    7135: (T + "«Nasz» — лишнее", {"example_pl": "Kocur idzie za instynktem i co noc poluje w ogrodzie na myszy"}),
    7139: (T + "«Moja» — лишнее", {"example_pl": "Stara koszulka jest już cała podarta"}),
    7150: (T + "«mój» — лишнее", {"example_pl": "Bez etui telefon dawno by się rozbił, ciągle go upuszczam"}),
    7166: (T + "«mój» — лишнее", {"example_pl": "Totalnie schrzaniłem ten projekt i szef jest wściekły"}),
    7180: (T + "«… to owoce, które lubię jeść» — коряво", {"example_pl": "Lubię jabłka, gruszki i tym podobne owoce"}),
    7189: (T + "«mój» — лишнее", {"example_pl": "W nocy syn zakrada się do kuchni i je czekoladę"}),
    7196: (T + "«kawiarnia łączy … kawiarnię» — повтор", {"example_pl": "To małe miejsce łączy księgarnię z kawiarnią"}),
    7199: (T + "«swój» — лишнее", {"example_pl": "Cały wolny czas poświęcam rodzinie"}),
    7211: (T + "«każdego ranka» → «co rano»", {"example_pl": "Stary kundel co rano szczeka na sąsiadów"}),
    7221: (T + "«Mój» — лишнее", {"example_pl": "Wujek prowadzi małą restaurację w centrum"}),
    7233: (T + "«Twoje auto» — калька", {"example_pl": "Blokujesz autem wyjazd"}),
    7234: (T + "«Nasz» — лишнее", {"example_pl": "Kot odmawia nowej karmy i siedzi obrażony przed miską"}),
    7272: (T + "«Mój» — лишнее", {"example_pl": "Tata nigdy nie dążył do dużych pieniędzy, chciał tylko mieć czas dla rodziny"}),
    7276: (T + "«Efekt … jest zerowy» — калька", {"example_pl": "Ten drogi szampon nie daje żadnego efektu"}),
    7306: (T + "«Jego odpowiedź była» — калька", {"example_pl": "Odpowiedział bardzo mgliście"}),
    7317: (T + "«Sama robię to wieki» — коряво", {"example_pl": "Pomożesz mi złożyć pranie? Samej zajmie mi to wieki"}),
    7344: (T + "«swoją» — лишнее", {"example_pl": "Kiedy mogę odzyskać wiertarkę? Potrzebuję jej w weekend"}),
    7351: (T + "«mojej» — лишнее", {"example_pl": "Z pensji jakoś sobie radzę"}),
    7359: (T + "«naszą» — лишнее", {"example_pl": "Chcemy rozszerzyć działalność i otworzyć nowe sklepy"}),
    7363: (T + "«Mój pies … moim» — лишнее", {"example_pl": "Pies jest poniekąd moim najlepszym przyjacielem"}),
    7368: (T + "«pojmuję sytuację» — книжно", {"example_pl": "Szybko pojmuję, o co chodzi"}),
    7371: (T + "«Moje» — лишнее", {"example_pl": "Dziecko czasem płacze zupełnie bez powodu i nie wiem, co robić"}),
    7389: (T + "«tik oka» — коряво", {"example_pl": "Ma nerwowy tik powieki"}),
    7393: (T + "«Mój» — лишнее", {"example_pl": "Bon traci ważność pod koniec miesiąca, muszę go szybko wykorzystać"}),
    7414: (T + "«Nasz» — лишнее", {"example_pl": "Nowy sąsiad to dziwny człowiek, nigdy się nie wita i nocami chodzi po ogrodzie"}),
    7427: (T + "«swoje» — лишнее", {"example_pl": "Szerokie spodnie znowu są modne, powinnam była zatrzymać te stare z lat dziewięćdziesiątych"}),
    7443: (T + "«przeprowadzić rozmowy» — книжно", {"example_pl": "Wi-fi w hotelu było tak niestabilne, że ani razu nie udało mi się porozmawiać przez telefon"}),
    7454: (T + "«Mój» — лишнее", {"example_pl": "Ulubiony długopis zniknął w biurze bez śladu, pewnie ktoś go zabrał"}),
    7467: (T + "«moje pieniądze na urlop» — коряво", {"example_pl": "Na naprawę auta poszły wszystkie pieniądze odłożone na urlop"}),
    7468: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez święto przesunęliśmy imprezę na wcześniej, na piątek"}),
    7471: (T + "«Moja» — лишнее", {"example_pl": "Mała siostrzenica przesuwa palcem nawet po zdjęciach w książkach, bo myśli, że to telefon"}),
}

REPLACE = []

SPLIT_LATER = {}
