"""Шаг 2, pl, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    857: (T + "word in example", {"t_pl": "spacerować, przechadzać się, (spazieren gehen) iść na spacer"}),
    999: (T + "word in example", {"t_pl": "profilaktyka, (zur Vorsorge) profilaktycznie"}),
    1171: (T + "word in example", {"t_pl": "podnosić, podnieść, przechowywać"}),
    1192: (T + "word in example", {"t_pl": "wystarczający, dostateczny, wystarczająco"}),
    1219: (T + "word in example", {"t_pl": "bezgotówkowy, bezgotówkowo"}),
    1279: (T + "word in example", {"x_pl": "Moja ścieżka edukacyjna nie była prosta: najpierw szkoła zawodowa, potem matura, potem studia"}),
    1289: (T + "word in example", {"t_pl": "przypadek pożaru, (im Brandfall) w razie pożaru"}),
}

REPLACE = []
SPLIT_LATER = {}
