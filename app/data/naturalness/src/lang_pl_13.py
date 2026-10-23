"""Вычитка польского, порция p013 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    2761: (T + "«Moja» — лишнее", {"example_pl": "Reklamacja zepsutej pralki od trzech tygodni leży u sprzedawcy"}),
    2768: (T + "«dał mu grzywnę» — коряво", {"example_pl": "Sędzia wymierzył mu tylko grzywnę"}),
    2770: (T + "«w moim rowerze» — калька", {"example_pl": "Policja mnie zatrzymała, bo w rowerze nie działało mi tylne światło"}),
    2771: (T + "«każdego ranka» — книжно", {"example_pl": "Zimą codziennie rano muszę najpierw zeskrobać lód z tylnej szyby"}),
    2778: (T + "«Moja referentka» — калька", {"example_pl": "Referentka w urzędzie pracy zmienia mi się co pół roku i muszę wszystko tłumaczyć od nowa"}),
    2781: (T + "«Moja … jako» — тяжело", {"example_pl": "Przyjaciółka jest kierowniczką sprzedaży i więcej siedzi w samolocie niż w biurze"}),
    2788: (T + "«mojej» — лишнее", {"example_pl": "Przy pierwszej szkodzie ubezpieczyciel zapłacił zaskakująco szybko"}),
    2797: (T + "«Mój» — лишнее", {"example_pl": "Syn strzelił na treningu trzy gole i jest strasznie dumny"}),
    2812: (T + "«Możesz, proszę,» — книжно", {"example_pl": "Możesz ściszyć głos?"}),
    2816: (T + "«moja» — лишнее", {"example_pl": "W wiejskim konkursie ciast babcia była już trzy razy zwyciężczynią"}),
    2832: (T + "«Mój» — лишнее", {"example_pl": "Dziadek jest bardzo oszczędny i niczego nie wyrzuca"}),
    2835: (T + "«Po szkole» — смысл (Ausbildung)", {"example_pl": "Po nauce zawodu chce się specjalizować w stomatologii dziecięcej"}),
    2848: (T + "«mojego» — лишнее", {"example_pl": "Potrzebuję doradcy podatkowego do zeznania podatkowego"}),
    2856: (T + "«od dziesięciu lat» — двусмысленно", {"example_pl": "Syn może sam jeździć rowerem w ruchu drogowym dopiero od dziesiątego roku życia"}),
    2862: (T + "«nasz» — лишнее", {"example_pl": "Odkąd syn co noc gra na komputerze, rachunek za prąd wyraźnie wzrósł"}),
    2873: (T + "«Mój» — лишнее", {"example_pl": "Wujek przez trzydzieści lat pracował w telekomunikacji, od kabla telefonicznego po światłowód"}),
    2884: (T + "«Teraz to jest» — тяжело", {"example_pl": "To teraz wielki trend"}),
    2885: (T + "«swojej» — лишнее", {"example_pl": "Zawsze był wierny żonie"}),
    2886: (T + "«Czy to jest» — книжно", {"example_pl": "To woda pitna?"}),
    2911: (T + "«Potrafi obchodzić się» — коряво", {"example_pl": "Umie dobrze obchodzić się z dziećmi"}),
    2916: (T + "«W szkole moich dzieci» — тяжело", {"example_pl": "U dzieci w szkole jest kółko ochrony środowiska, które co miesiąc sprząta park"}),
    2923: (T + "«zdecydowanie zbyt» — книжно", {"example_pl": "Jesz o wiele za niezdrowo"}),
    2934: (T + "«nasz» — лишнее", {"example_pl": "Odkąd syn jest weganinem, mama na święta gotuje dwa menu"}),
    2947: (T + "«przedłużyć książkę» — калька", {"example_pl": "Mogę przedłużyć wypożyczenie książki o tydzień?"}),
    2951: (T + "«Mój» — лишнее", {"example_pl": "Syn nie umie przegrywać, płacze przy każdej grze"}),
    2974: (T + "«To jest» — тяжело", {"example_pl": "To naruszenie przepisów"}),
    2983: (T + "«rezygnuję od lat» — вид", {"example_pl": "Z mięsa zrezygnowałem już lata temu"}),
    2984: (T + "«Moja wiza kończy się» — калька", {"example_pl": "Wiza kończy mi się w maju"}),
    3001: (T + "«Czy» — книжно", {"example_pl": "Ten zegarek jest naprawdę wodoodporny?"}),
    3008: (T + "«Tak dalej trwać» — коряво", {"example_pl": "Tak dłużej nie może trwać!"}),
    3009: (T + "«w tym nie mogę pomóc» — неполно", {"example_pl": "Przepraszam, tu nie mogę panu pomóc"}),
    3027: (T + "«lot mojej siostry odwołano» — книжно", {"example_pl": "Przez huragan na Florydzie odwołali siostrze lot"}),
    3033: (T + "«na moje konto» — калька", {"example_pl": "Płatność nie wpłynęła mi jeszcze na konto"}),
    3034: (T + "«Mój» — лишнее", {"example_pl": "Mąż tak długo skacze po kanałach, aż film jest w połowie"}),
    3040: (T + "«Pan» — регистр", {"example_pl": "Na jaki okres potrzebuje pan samochodu?"}),
    3063: (T + "«Pan» — регистр", {"example_pl": "Podpisaną umowę musi nam pan odesłać do piątku"}),
}

REPLACE = []

SPLIT_LATER = {}
