"""Шаг 2, pl, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    6330: (T + "word in example", {"t_pl": "precz, z dala, (fort sein) nie ma (kogoś)"}),
    6369: (T + "word in example", {"t_pl": "odległy, oddalony, (zehn Minuten entfernt) dziesięć minut stąd"}),
    6486: (T + "word in example", {"t_pl": "stać na warcie, pilnować, czuwać"}),
    6493: (T + "word in example", {"t_pl": "naprzód, z góry, (vorausgehen) przodem"}),
    6506: (T + "word in example", {"t_pl": "wysiłek, trud, (sich Mühe geben) postarać się"}),
    6519: (T + "word in example", {"t_pl": "osłona, schronienie, (in Deckung gehen) schować się"}),
    6521: (T + "word in example", {"t_pl": "pełen życia, żywy, ożywiony"}),
    6605: (T + "word in example", {"t_pl": "delikatny, wykwintny, czuły"}),
    6637: (T + "word in example", {"t_pl": "widok, widoczność, punkt widzenia"}),
    6734: (T + "word in example", {"t_pl": "porządny, porządnie, jak należy", "x_pl": "W twoim pokoju jest bardzo porządnie"}),
    6784: (T + "word in example", {"t_pl": "stosować, angażować, uruchamiać"}),
}

REPLACE = []
SPLIT_LATER = {}
