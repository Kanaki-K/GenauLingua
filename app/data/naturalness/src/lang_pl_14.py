"""Вычитка польского, порция p014 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    3067: (T + "«z moimi … jest harmonijne» — книжно", {"example_pl": "Wspólne życie z rodzicami układa się harmonijnie"}),
    6312: (T + "«rzeczy» — бледно для Zeug", {"example_pl": "Posprzątaj swoje graty"}),
    6319: (T + "«To jest całkowicie» — тяжело", {"example_pl": "To zupełnie niemożliwe"}),
    6353: (T + "«to jest rozkaz» — тяжело", {"example_pl": "Załóż czapkę, to rozkaz!"}),
    6356: (T + "«Mój» — лишнее", {"example_pl": "Starszy brat zawsze bronił mnie w szkole"}),
    6370: (T + "«To jest ewidentnie błędne» — калька", {"example_pl": "To ewidentnie błąd"}),
    6384: (T + "«jeden krok» — калька", {"example_pl": "Zrób krok do przodu"}),
    6411: (T + "«Pieniądze nie wystarczają» — калька", {"example_pl": "Nie wystarczy mi pieniędzy do końca miesiąca"}),
    6427: (T + "«Moja» — лишнее", {"example_pl": "Mama była zachwycona twoim ciastem"}),
    6451: (T + "«On jest» — лишнее", {"example_pl": "Najwyraźniej jest chory"}),
    6452: (T + "«swoje» — лишнее", {"example_pl": "Muszę sprawdzić maile"}),
    6457: (T + "«Czy» — книжно", {"example_pl": "Wolno tu robić zdjęcia?"}),
    6477: (T + "«Oni» — лишнее", {"example_pl": "Żądają za dużo pieniędzy"}),
    6480: (T + "«Wszędzie tutaj jest» — тяжело", {"example_pl": "Wszędzie tu brud"}),
    6530: (T + "«Czy» — книжно", {"example_pl": "Mogę na chwilę wejść?"}),
    6548: (T + "«ciężka do niesienia» — калька", {"example_pl": "Ta skrzynka jest strasznie ciężka"}),
    6557: (T + "«Moja» — лишнее", {"example_pl": "Lekarka mówi, że kieliszek wina to mniej więcej jedna jednostka alkoholu"}),
    6560: (T + "«Mój» — лишнее", {"example_pl": "Telefon jest połączony z wifi"}),
    6603: (T + "«on» — лишнее", {"example_pl": "Badanie wykaże, czy ma rację"}),
    6661: (T + "«Czy możesz» — книжно", {"example_pl": "Możesz tu zawrócić?"}),
    6672: (T + "«Czy możesz zidentyfikować» — книжно", {"example_pl": "Możesz rozpoznać tego mężczyznę na zdjęciu?"}),
    6684: (T + "«posiadać» — книжно", {"example_pl": "Chciałbym kiedyś mieć własny samochód"}),
    6710: (T + "«bałaganem» — не слово карточки", {"example_pl": "Nie chce mi się zajmować tymi wszystkimi gratami"}),
    6711: (T + "«To jest całkowicie» — тяжело", {"example_pl": "To zupełnie nieważne"}),
    6714: (T + "«To jest być może» — калька", {"example_pl": "To chyba za drogie dla nas"}),
    6751: (T + "«Czy» — книжно", {"example_pl": "Można samemu wymienić baterię?"}),
    6758: (T + "«To jest» — тяжело", {"example_pl": "To całkiem możliwe"}),
    6759: (T + "«naszych» — лишнее", {"example_pl": "Musimy zrobić kopię zapasową danych"}),
    6761: (T + "«Mój … miał udział» — калька", {"example_pl": "Brat był zamieszany w drobny wypadek, ale nic mu nie jest"}),
    6785: (T + "«czy mogę» — книжно", {"example_pl": "Przepraszam, mogę ci na chwilę przerwać?"}),
    6809: (T + "«Mój» — лишнее", {"example_pl": "Dziadek był na froncie w czasie wojny"}),
}

REPLACE = []

SPLIT_LATER = {}
