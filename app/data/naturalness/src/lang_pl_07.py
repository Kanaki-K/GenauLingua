"""Вычитка польского, порция p007 (A2–B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    17747: (T + "«Mój» — лишнее", {"example_pl": "Stary aparat fotograficzny wciąż świetnie działa"}),
    18144: (T + "«Moja» — лишнее", {"example_pl": "Przyjaciółka mieszka obok"}),
    18184: (T + "«swój» — лишнее", {"example_pl": "Muszę posprzątać pokój"}),
    18369: (T + "«Nasza … mieszkania mieszka» — повтор", {"example_pl": "Właścicielka mieszkania mieszka na parterze"}),
    18607: (T + "«Dotychczas» — книжно", {"example_pl": "Do tej pory wszystko szło dobrze"}),
    18812: (T + "«To jest» — тяжело", {"example_pl": "To aktualna wersja aplikacji"}),
    18970: (T + "«To jest» — тяжело", {"example_pl": "To jego rower, mój stoi w piwnicy"}),
    18983: (T + "«numer mniejszy» — коряво", {"example_pl": "Spodnie są na mnie za luźne, potrzebuję o numer mniejsze"}),
    18984: (T + "«Niebieski kolor» — лишнее", {"example_pl": "Niebieski naprawdę ci pasuje"}),
    17: (T + "«Moja» — лишнее", {"example_pl": "Ciocia pracuje jako opiekunka w domu opieki"}),
    44: (T + "«On» — лишнее", {"example_pl": "Pracuje w gabinecie"}),
    47: (T + "«Proszę,» — лишнее", {"example_pl": "Oddychaj głęboko"}),
    66: (T + "«wystarczająco jedzenia» — коряво", {"example_pl": "W podróż zawsze bierzemy dużo jedzenia dla niemowląt"}),
    82: (T + "«Moi» — лишнее", {"example_pl": "Dziadkowie mają gospodarstwo z krowami i kurami"}),
    101: (T + "«poprawy zdrowia» — калька", {"example_pl": "Szybkiego wyzdrowienia!"}),
    149: (T + "«Moja» — лишнее", {"example_pl": "Siostra uczy się na pracownicę biurową"}),
    159: (T + "«Ona» — лишнее", {"example_pl": "Gotuje kuskus z warzywami"}),
    190: (T + "«Ona» — лишнее", {"example_pl": "Otwiera puszkę tuńczyka"}),
    333: (T + "«Ona» — лишнее", {"example_pl": "Jest rozwiedziona"}),
    340: (T + "«swoją» — лишнее", {"example_pl": "Proszę pokazać kartę ubezpieczenia zdrowotnego"}),
    386: (T + "«Mój» — лишнее", {"example_pl": "Mąż jest teraz gospodarzem domowym i zajmuje się dziećmi"}),
    468: (T + "«Moja» — лишнее", {"example_pl": "Mama wyuczyła się na sprzedawczynię"}),
    485: (T + "«Sprzątam swoje ciuchy» — калька", {"example_pl": "Porządkuję ciuchy"}),
    499: (T + "«Moja» — лишнее", {"example_pl": "Koleżanka z pracy ma dziś urodziny i przyniesie ciasto"}),
    510: (T + "«On» — лишнее", {"example_pl": "Leży w szpitalu"}),
    592: (T + "«Moja» — лишнее", {"example_pl": "Przyjaciółka nie toleruje produktów mlecznych"}),
    632: (T + "«Nasz» — лишнее", {"example_pl": "Sąsiad odebrał za nas paczkę"}),
    636: (T + "«Jak brzmi twoje nazwisko» — книжно", {"example_pl": "Jak masz na nazwisko?"}),
    638: (T + "«Moja» — лишнее", {"example_pl": "Żona jest pielęgniarką i w tym tygodniu ma nocne dyżury"}),
    689: (T + "«Moja» — лишнее", {"example_pl": "Córka jeszcze wierzy w zajączka wielkanocnego"}),
    700: (T + "«Czy» — книжно", {"example_pl": "Jest tu wolne miejsce parkingowe?"}),
    708: (T + "«Ona» — лишнее", {"example_pl": "Nakleja sobie plaster na ranę"}),
    711: (T + "«Ona» — лишнее", {"example_pl": "Zbiera grzyby w lesie"}),
    725: (T + "«Moja» — лишнее", {"example_pl": "Opiekunka praktyk co rano tłumaczy mi zadania"}),
    751: (T + "«Ona» — лишнее", {"example_pl": "Regularnie uprawia sport"}),
}

REPLACE = []

SPLIT_LATER = {}
