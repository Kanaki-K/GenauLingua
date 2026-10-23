"""Вычитка польского, порция p001 (A1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    8: (T + "«Jaki jest twój adres» — калька", {"example_pl": "Jaki masz adres?"}),
    61: (T + "«masz na myśli przez» — калька", {"example_pl": "Co chciałeś powiedzieć tą wypowiedzią?"}),
    62: (T + "«Ona» — лишнее", {"example_pl": "Jeździ do pracy samochodem"}),
    72: (T + "«koleją» — книжно", {"example_pl": "Do pracy jeżdżę pociągiem"}),
    74: (T + "«On» — лишнее", {"example_pl": "Niedługo wróci do domu"}),
    96: (T + "«Jaki jest twój zawód» — калька", {"example_pl": "Jaki masz zawód?"}),
    107: (T + "«Chodzę do łóżka» — калька", {"example_pl": "Wcześnie kładę się do łóżka"}),
    113: (T + "«On» — лишнее", {"example_pl": "Pije piwo"}),
    117: (T + "«smakuje słodko» — калька", {"example_pl": "Ta gruszka jest słodka"}),
    127: (T + "«Ona» — лишнее", {"example_pl": "Kupuje czerwony kwiat"}),
    137: (T + "«On» — лишнее", {"example_pl": "Przynosi mi kwiaty"}),
    141: (T + "«Oni» — лишнее", {"example_pl": "Na śniadanie jedzą bułki"}),
    160: (T + "«On» — лишнее", {"example_pl": "Jest tutaj"}),
    164: (T + "«jesteś miły» — не тот смысл", {"example_pl": "Dziękuję, to bardzo miłe"}),
    195: (T + "«A ty» — лишнее", {"example_pl": "Idziesz z nami dziś wieczorem?"}),
    225: (T + "«On» — лишнее", {"example_pl": "Jest z Monachium"}),
    250: (T + "«to jest błędne» — коряво", {"example_pl": "Niestety, to błędna odpowiedź"}),
    253: (T + "«Jakie jest twoje nazwisko» — калька", {"example_pl": "Jak masz na nazwisko?"}),
    269: (T + "«Ona» — лишнее", {"example_pl": "Ma gorączkę"}),
    274: (T + "«Chętnie jem» — калька gern", {"example_pl": "Lubię ryby"}),
    276: (T + "«On» — лишнее", {"example_pl": "Nie je mięsa"}),
    282: (T + "«To zdjęcie jest słodkie» — калька", {"example_pl": "Słodkie zdjęcie!"}),
    307: (T + "«Ona» — лишнее", {"example_pl": "Pracuje w ogrodzie"}),
    316: (T + "порядок слов", {"example_pl": "Bardzo mi się to podoba"}),
    323: (T + "«Ona» — лишнее", {"example_pl": "Kupuje świeże warzywa"}),
    328: (T + "порядок слов", {"example_pl": "Właśnie jestem zajęty"}),
    345: (T + "«on» — лишнее", {"example_pl": "Myślę, że przyjdzie"}),
    348: (T + "«Ona» — лишнее", {"example_pl": "Jest bardzo szczęśliwa"}),
    354: (T + "«W lecie» → «Latem»", {"example_pl": "Latem chętnie grillujemy"}),
    358: (T + "«dla twojej rodziny» — калька", {"example_pl": "Serdeczne pozdrowienia dla całej rodziny"}),
    365: (T + "«Ona» — лишнее", {"example_pl": "Ma krótkie włosy"}),
    376: (T + "«Ona» — лишнее", {"example_pl": "Podaje mi rękę"}),
    391: (T + "«Oni» — лишнее", {"example_pl": "Biorą ślub w czerwcu"}),
    406: (T + "«On» — лишнее", {"example_pl": "Siedzi z tyłu"}),
    422: (T + "«Ja» — лишнее", {"example_pl": "Jestem studentem"}),
    427: (T + "«Jakie jest pana imię» — калька", {"example_pl": "Jak brzmi pana nazwisko?"}),
    443: (T + "«Ona» — лишнее", {"example_pl": "Ma na sobie ciepłą kurtkę"}),
    456: (T + "«Każdego ranka» — книжно", {"example_pl": "Codziennie rano piję kawę"}),
    463: (T + "«Chętnie jem» — калька gern", {"example_pl": "Lubię gotowane ziemniaki z masłem"}),
    479: (T + "«Ona» — лишнее", {"example_pl": "Zawozi dziecko do przedszkola"}),
    490: (T + "«Ona» — лишнее", {"example_pl": "Potrzebuje nowych ubrań"}),
    509: (T + "«Ona» — лишнее", {"example_pl": "Jest chora"}),
    518: (T + "«skorzystać z długopisu» — книжно", {"example_pl": "Mogę pożyczyć twój długopis?"}),
    527: (T + "«zjeść razem» — неполно", {"example_pl": "Możemy jutro razem zjeść obiad"}),
}

REPLACE = []

SPLIT_LATER = {}
