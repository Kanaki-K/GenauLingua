"""Вычитка французского, порция p010 (B1), 23.10: «nous» → «on», нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    1774: (T + "«Santé ! À ta santé» — повтор", {"example_fr": "Allez, tchin-tchin ! À ta santé !"}),
    1856: (T + "«nous» → «on»", {"example_fr": "Le week-end, on fait de la voile"}),
    1883: (T + "«Nous faisons une promenade» — книжно", {"example_fr": "On va faire une petite balade"}),
    1926: (T + "нет слова карточки «l'ordre du jour»", {"example_fr": "Quel est le premier point à l'ordre du jour ?"}),
}

REPLACE = []

SPLIT_LATER = {}
