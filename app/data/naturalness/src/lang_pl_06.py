"""Вычитка польского, порция p006 (A2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    6326: (T + "«To jest zbyt» — книжно", {"example_pl": "To za niebezpieczne"}),
    6482: (T + "«Czuję się słaby» — калька", {"example_pl": "Jestem dziś jakiś słaby"}),
    6496: (T + "«on» — лишнее", {"example_pl": "Nie zauważasz, że kłamie?"}),
    6657: (T + "«Mój … swojej» — лишнее", {"example_pl": "Wujek słynie w całej wsi z szarlotki"}),
    6753: (T + "порядок слов", {"example_pl": "Udało się z tą wizytą?"}),
    7057: (T + "«Mój» — лишнее", {"example_pl": "Mąż jest w tym tygodniu na targach w Kolonii"}),
    8792: (T + "«Mój mąż jest» — тяжело", {"example_pl": "Mąż to świetny kucharz"}),
    8868: (T + "«pracuje … z pracy» — повтор", {"example_pl": "Koleżanka z pracy siedzi w tym samym biurze"}),
    8980: (T + "«swoje» — лишнее", {"example_pl": "Jutro wysyłam podanie o pracę"}),
    9006: (T + "«Mój ojciec» — книжно", {"example_pl": "Tata jest handlowcem"}),
    9591: (T + "«Moi … chętni do pomocy» — книжно", {"example_pl": "Koledzy z klasy są bardzo mili i chętnie pomagają"}),
    10077: (T + "«To jest dziwne» — тяжело", {"example_pl": "To dziwne"}),
    10328: (T + "«Moja» — лишнее", {"example_pl": "Siostra jest bardzo inteligentna i studiuje medycynę"}),
    11039: (T + "«Moja praca» — калька", {"example_pl": "Praca bywa u mnie dość stresująca"}),
    12138: (T + "«są wakacje» — тяжело", {"example_pl": "Nareszcie wakacje!"}),
    12461: (T + "«Moja … w wieku» — книжно", {"example_pl": "Babcia zmarła w zeszłym roku, miała 95 lat"}),
    13149: (T + "«Mój» — лишнее", {"example_pl": "Brat pracuje jako pielęgniarz"}),
    13295: (T + "«Czy» — книжно", {"example_pl": "To twój telefon?"}),
    13346: (T + "«tu … w domu» — повтор", {"example_pl": "Nikogo nie ma w domu"}),
    13379: (T + "«To jest wprawdzie» — тяжело", {"example_pl": "Wprawdzie drogie, ale dobre"}),
    14031: (T + "«w moim» — лишнее", {"example_pl": "Zapisuję krótką notatkę w notesie"}),
    14529: (T + "«Moja» — лишнее", {"example_pl": "Babcia nigdy nie straciła wiary, nawet w trudnych czasach"}),
    14608: (T + "«Na karnawale» — предлог", {"example_pl": "W karnawał w Kolonii całe miasto jest na nogach"}),
    14898: (T + "«Ja i moja dziewczyna» — калька", {"example_pl": "Z dziewczyną jesteśmy razem od trzech lat"}),
    14905: (T + "«Mój» — лишнее", {"example_pl": "Wujek od dwudziestu lat mieszka w Kanadzie"}),
    14923: (T + "«Moja» — лишнее", {"example_pl": "Ciocia piecze pyszne ciasta"}),
    14944: (T + "«Mój» — лишнее", {"example_pl": "Brat jest już dorosły"}),
    14946: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn przyjeżdża jutro w odwiedziny"}),
    14999: (T + "«Mój» — лишнее", {"example_pl": "Sąsiad jest dość głośny"}),
    15048: (T + "«Moja … bardzo słodka» — тяжело", {"example_pl": "Wnuczka ma trzy lata i jest przesłodka"}),
    15376: (T + "«Moja» — лишнее", {"example_pl": "Córka marzy o własnym koniu"}),
    16035: (T + "«w wyborach» — лишнее", {"example_pl": "Na którą partię głosujesz?"}),
    17162: (T + "«Moja» — лишнее", {"example_pl": "Żona jest w tym tygodniu na wyjeździe"}),
    17488: (T + "«Silnik … jest zepsuty» — калька", {"example_pl": "Zepsuł mi się silnik w samochodzie"}),
}

REPLACE = []

SPLIT_LATER = {}
