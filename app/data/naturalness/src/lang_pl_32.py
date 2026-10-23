"""Вычитка польского, порция p032 (B2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    11739: (T + "«moje» — лишнее", {"example_pl": "Spaghetti z sosem pomidorowym dzieci zawsze zjedzą"}),
    11748: (T + "«Moja» — лишнее", {"example_pl": "Babcia co roku piecze pyszne ciasteczka na Boże Narodzenie"}),
    11757: (T + "«mój» — лишнее", {"example_pl": "Na urodziny chłopak robi wszystkim drinka z mango i limonką"}),
    11774: (T + "«Każdego ranka» → «Co rano»", {"example_pl": "Co rano piję szklankę soku pomarańczowego"}),
    11776: (T + "«Moje» — лишнее", {"example_pl": "Dzieci wolą sushi od pizzy, nigdy bym nie pomyślała"}),
    11781: (T + "порядок слов", {"example_pl": "U nas w piątki ulubione danie to pieczony łosoś z ziemniakami"}),
    11841: (T + "«Nasze» — лишнее", {"example_pl": "Dziecko najbardziej lubi słoiczek z marchewką, a resztę wypluwa"}),
    11979: (T + "«Mój» — лишнее", {"example_pl": "Lekarz mówi, że trzeba jeść powoli, bo uczucie sytości przychodzi dopiero po dwudziestu minutach"}),
    12185: (T + "«odbywa się na arenie» — книжно", {"example_pl": "Koncert jest w dużej hali widowiskowej"}),
    12189: (T + "«Nasza … wszyscy» — коряво", {"example_pl": "Suczka miała miot sześciu szczeniąt i każdy chce jednego"}),
    12196: (T + "«Moja» — лишнее", {"example_pl": "Ciocia jest myśliwą i jesienią zawsze przywozi nam dziczyznę z lasu"}),
    12200: (T + "«moja» — лишнее", {"example_pl": "W zawodach pływackich w sobotę córka startuje po raz pierwszy"}),
    12207: (T + "«Mój» — лишнее", {"example_pl": "Syn jest w harcerstwie i latem przez dwa tygodnie śpi w namiocie w lesie"}),
    12209: (T + "«tylko obijać się» — коряво", {"example_pl": "Dziś chcemy się po prostu poobijać w domu"}),
    12223: (T + "«Mój» — лишнее", {"example_pl": "Syn trenuje karate dwa razy w tygodniu"}),
    12227: (T + "«kiedy» искажает смысл", {"example_pl": "Finał oglądaliśmy całą ulicą, a na koniec Niemcy zostały mistrzem świata"}),
    12260: (T + "«Parkiet jest pełny» — калька", {"example_pl": "W klubie na parkiecie zawsze jest tłok"}),
    12393: (T + "«nasz» — лишнее", {"example_pl": "Sąsiad kupuje petardy już w grudniu, a pies od 31. chowa się pod łóżkiem"}),
    12411: (T + "«swoją» — лишнее", {"example_pl": "Dziadek w każdą sobotę chodzi do punktu bukmacherskiego i stawia dwa euro na ulubioną drużynę"}),
    12600: (T + "«Stary mężczyzna» — книжно", {"example_pl": "Starszy pan pali cygaro"}),
    12612: (T + "«Mój» — лишнее", {"example_pl": "Tata ma problemy z nerkami i musi dużo pić"}),
    12633: (T + "«Mój» — лишнее", {"example_pl": "Sąsiad przez dziesięć lat był alkoholikiem, dziś nie pije nawet piwa"}),
    12635: (T + "«naszego» — лишнее", {"example_pl": "Weterynarz obejrzał kota"}),
    12639: (T + "«mój» — лишнее", {"example_pl": "Od wypadku na motocyklu kuzyn jest sparaliżowany od pasa w dół"}),
    12714: (T + "«w moim samochodzie» — лишнее", {"example_pl": "W nocy ktoś przeciął mi wszystkie cztery opony"}),
    12730: (T + "«moja» — лишнее", {"example_pl": "Może tak często śni mi się szkoła, bo podświadomość jeszcze nie zapomniała egzaminu"}),
    12731: (T + "«Nasz … był nieranny» — коряво", {"example_pl": "Kot spadł z balkonu na drugim piętrze i na szczęście wyszedł z tego nieranny"}),
    12732: (T + "«Moja … z moimi problemami» — лишнее", {"example_pl": "Terapeutka naprawdę mi pomaga"}),
    12736: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez budowę na A7 przez cały dzień są dziś utrudnienia"}),
    12741: (T + "«dlatego czuję się źle» — коряво", {"example_pl": "Mam okres, więc kiepsko się czuję"}),
    12797: (T + "«moje … mój» — лишнее", {"example_pl": "Lekarz mówi, że tętnice mam jak na swój wiek w dobrym stanie"}),
    12834: (T + "«Ona» — лишнее", {"example_pl": "Pracuje jako psychiatra w dużym szpitalu"}),
}

REPLACE = []

SPLIT_LATER = {}
