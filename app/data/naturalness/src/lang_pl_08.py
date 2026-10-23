"""Вычитка польского, порция p008 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    779: (T + "«Ona» — лишнее", {"example_pl": "Smaruje ranę maścią"}),
    819: (T + "«Mój» — лишнее", {"example_pl": "Teść świetnie gotuje"}),
    887: (T + "«w moim» — лишнее", {"example_pl": "Maluję ścianę w pokoju"}),
    921: (T + "«Jaki jest twój» — калька", {"example_pl": "Jaki masz numer telefonu?"}),
    938: (T + "«mój» — лишнее", {"example_pl": "Z tych winogron wujek robi wino"}),
    939: (T + "«Jaki jest twój» — калька", {"example_pl": "Jaki masz wymarzony zawód?"}),
    940: (T + "«z balkonem i jasne» — порядок", {"example_pl": "Wreszcie znaleźliśmy wymarzone mieszkanie: jasne, z balkonem"}),
    984: (T + "«Mój» — лишнее", {"example_pl": "Dziadek od pięciu lat jest wdowcem i mieszka sam"}),
    1012: (T + "нет слова карточки, «słuszne» — книжно", {"example_pl": "Zmiana firmy wyszła mi na dobre"}),
    1021: (T + "«Mój» — лишнее", {"example_pl": "Dziadek co roku przebiera się za Świętego Mikołaja"}),
    1030: (T + "«Moi» — лишнее", {"example_pl": "Rodzice przyjechali do Niemiec Zachodnich w latach osiemdziesiątych"}),
    1044: (T + "«Mój płaszcz … jest» — калька", {"example_pl": "Płaszcz zimowy mam za cienki na minus dziesięć stopni"}),
    1122: (T + "«Moja» — лишнее", {"example_pl": "Mama przysięga na akupunkturę przy bólach głowy"}),
    1154: (T + "«Mój pracodawca jest» — калька", {"example_pl": "Mam bardzo uczciwego pracodawcę"}),
    1158: (T + "«Czy» — книжно", {"example_pl": "Potrzebuję pozwolenia na pracę?"}),
    1169: (T + "«trwa» → «potrwa»", {"example_pl": "Mój pobyt potrwa trzy miesiące"}),
    1178: (T + "«mój … jako kucharz» — коряво", {"example_pl": "Po szkole siostrzeniec dostał miejsce nauki zawodu kucharza"}),
    1192: (T + "«Czas nie jest wystarczający» — калька", {"example_pl": "Na to zadanie nie ma wystarczająco czasu"}),
    1213: (T + "«moją» — лишнее", {"example_pl": "Bankomat wciągnął mi kartę bankową"}),
    1214: (T + "«Mój» — лишнее", {"example_pl": "Brat jest bankowcem i zna się na kredytach"}),
    1220: (T + "«On» — лишнее", {"example_pl": "Ma długą brodę"}),
    1233: (T + "«Jego ocena jest zadowalająca» — калька", {"example_pl": "Dostał ocenę dostateczną"}),
    1298: (T + "«Ona» — лишнее", {"example_pl": "Pracuje w księgowości"}),
    1305: (T + "«W moim … panuje» — книжно", {"example_pl": "W pokoju mam chaos"}),
    1356: (T + "«swój» — лишнее", {"example_pl": "Najpierw musisz wpisać PIN"}),
    1358: (T + "«swoje» — лишнее", {"example_pl": "Urządzam mieszkanie"}),
}

REPLACE = []

SPLIT_LATER = {}
