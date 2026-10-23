"""Вычитка польского, порция p033 (B2), 23.10: кальки, лишние местоимения, опечатка → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    12887: (T + "«Mój» — лишнее", {"example_pl": "Brat za dużo pali trawkę i to mnie martwi"}),
    12918: (T + "«Oszczędzanie … jest» — книжно", {"example_pl": "To dość krótkowzroczne oszczędzać akurat na zimowych oponach"}),
    12930: (T + "«wszyscy ludzie na poboczu» — коряво", {"example_pl": "Kiedy karawan powoli przejeżdżał przez wieś, ludzie przy drodze przystawali"}),
    12957: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn ma zespół Downa i od dziesięciu lat pracuje w piekarni"}),
    12978: (T + "«mój» — лишнее", {"example_pl": "Po trzech nieprzespanych nocach kolega miał psychozę i musiał iść do szpitala"}),
    12983: (T + "«to tylko mój syn» — коряво", {"example_pl": "Ślady krwi w przedpokoju zostawił tylko syn, skaleczył się w palec przy majsterkowaniu"}),
    12992: (T + "«Akcja ratunkowa naszego kota» — коряво", {"example_pl": "Na akcję ratunkową dla kota na drzewie trzeba było dwóch strażaków i długiej drabiny"}),
    12999: (T + "«mojego» — лишнее", {"example_pl": "W każdym odcinku ulubionego serialu kryminalnego komisarz czyta raport z sekcji zwłok przy śniadaniu"}),
    13001: (T + "«na moim nadgarstku» — коряво", {"example_pl": "Pielęgniarka kładzie mi dwa palce na tętnicy na nadgarstku i liczy w milczeniu"}),
    13023: (T + "«swoją» — лишнее", {"example_pl": "Do nowego lekarza rodzinnego musiałem przynieść starą kartę pacjenta, to były dwa grube segregatory"}),
    13068: (T + "запятые вокруг «proszę»", {"example_pl": "Daj mi, proszę, od razu szklankę wody, po treningu umieram z pragnienia"}),
    13098: (T + "«swoje» — лишнее", {"example_pl": "Przepis na knedle ze śliwkami prababcia zdradziła dopiero na łożu śmierci"}),
    13110: (T + "«Nasza» — лишнее", {"example_pl": "Stara pralka jest w stadium końcowym, wiruje już tylko z głośnym stukaniem"}),
    13155: (T + "«swoich» — лишнее", {"example_pl": "Tata u lekarza zupełnie otwarcie mówi o hemoroidach, a mama za każdym razem się czerwieni"}),
    13158: (T + "«Nasz» — лишнее", {"example_pl": "Stary odkurzacz po włączeniu już tylko charczy"}),
    13516: (T + "«Moja» — лишнее", {"example_pl": "Żona nie może się o tym dowiedzieć, to niespodzianka"}),
    13517: (T + "«przy tym pomagają» — порядок", {"example_pl": "W sobotę malujemy kuchnię, pomogą nam przy tym sąsiedzi"}),
    13529: (T + "«Nasz» — лишнее", {"example_pl": "Domek letniskowy stoi pośród winnic, najbliższa wieś jest pięć kilometrów dalej"}),
    13544: (T + "«Mój» — лишнее", {"example_pl": "Pies boi się burzy, przez niego w sylwestra zostajemy w domu"}),
    13545: (T + "«Nasza» — лишнее", {"example_pl": "Córka ma teraz dwa i pół roku i na wszystko mówi nie"}),
    13666: (T + "«Rękawy mojego swetra są» — калька", {"example_pl": "Sweter ma za długie rękawy"}),
    13670: (T + "порядок слов", {"example_pl": "Tę bransoletkę córka zrobiła mi sama"}),
    13673: (T + "опечатка «Założ» → «Załóż»", {"example_pl": "Załóż dziecku świeże majteczki"}),
    13687: (T + "«Mój» — лишнее", {"example_pl": "Naszyjnik całkiem mi się splątał w walizce"}),
    13690: (T + "«Obcasy w moich butach» — калька", {"example_pl": "Te buty mają za wysokie obcasy"}),
    13692: (T + "«W peruce … jego przebranie» — коряво", {"example_pl": "Przebranie z peruką i okularami było tak dobre, że nawet żona go nie poznała"}),
    13694: (T + "«Moja» — лишнее", {"example_pl": "Nowa fryzura wygląda super"}),
    14017: (T + "«On jest» — лишнее", {"example_pl": "Jest rzecznikiem naszej grupy"}),
    14019: (T + "«Jego charakter pisma jest» — калька", {"example_pl": "Ma strasznie nieczytelny charakter pisma"}),
    14026: (T + "«Z mojej strony nie mam» — коряво", {"example_pl": "Z mojej strony nie ma żadnych zastrzeżeń do tego planu"}),
    14047: (T + "«każdego ranka» → «co rano»", {"example_pl": "Co rano budzi mnie pikanie budzika"}),
    14058: (T + "«nie jest dostępny» — калька", {"example_pl": "W tym tygodniu szef jest nieosiągalny"}),
    14060: (T + "«kiedy on przyjdzie» — лишнее", {"example_pl": "Powiadom mnie od razu, jak tylko przyjdzie"}),
    14064: (T + "«Trochę pochwały» — коряво", {"example_pl": "Odrobina pochwały od szefa dobrze by zrobiła całemu zespołowi"}),
    14114: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez różnice polityczne wujek i tata od lat ze sobą nie rozmawiają"}),
    14220: (T + "«na zewnątrz» → «na dworze»", {"example_pl": "Nie mam ochoty na plotki w biurowej kuchni, dlatego w porze lunchu wolę jeść na dworze"}),
}

REPLACE = []

SPLIT_LATER = {}
