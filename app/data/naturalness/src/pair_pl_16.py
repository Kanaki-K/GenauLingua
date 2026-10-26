"""Шаг 2, pl, порция 16: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    7725: (T + "word in example", {"t_pl": "szybki, szybko, elegancki"}),
    7785: (T + "word in example", {"t_pl": "płynny, płynnie, ciekły"}),
    8046: (T + "word in example", {"t_pl": "podchodzić, podejść, dziać się"}),
    8245: (T + "word in example", {"t_pl": "napięty, jędrny, (straff ziehen) mocno naciągnąć"}),
    8789: (T + "word in example", {"t_pl": "ustawiać, nastawić, zatrudniać"}),
}

REPLACE = []
SPLIT_LATER = {}
