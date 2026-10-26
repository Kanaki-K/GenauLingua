"""Шаг 2, it, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    1534: (T + "word in example", {"t_it": "caloroso, cordiale, calorosamente"}),
    2895: (T + "word in example", {"t_it": "pernottare, passare la notte"}),
    6347: (T + "word in example", {"t_it": "noto, famoso, conosciuto"}),
    10420: (T + "word in example", {"t_it": "estraneo, straniero, (ich bin fremd hier) non sono di qui"}),
    17834: (T + "word in example", {"t_it": "il bene, la merce, la tenuta"}),
    18564: (T + "word in example", {"t_it": "a lungo, molto tempo, (wie lange) da quanto tempo"}),
}

REPLACE = []
SPLIT_LATER = {}
