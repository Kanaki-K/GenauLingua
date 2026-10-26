"""Шаг 2, pl, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    8645: (T + "word in example", {"t_pl": "poradzić sobie, dokonać, (es bewerkstelligen) udać się"}),
    8692: (T + "word in example", {"t_pl": "znaczny, godny uwagi, (beachtlich gut) zaskakująco dobrze"}),
    9239: (T + "word in example", {"t_pl": "służący, (die Dienstboten) służba"}),
    11449: (T + "word in example", {"t_pl": "oddany, uległy, wiernie"}),
}

REPLACE = []
SPLIT_LATER = {}
