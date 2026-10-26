"""Шаг 2, pl, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    2043: (T + "word in example", {"t_pl": "unikanie, zapobieganie, (zur Vermeidung) żeby uniknąć"}),
    7088: (T + "word in example", {"t_pl": "wdzierać się, wnikać, dostać się"}),
    18460: (T + "word in example", {"t_pl": "wycierać, wytrzeć"}),
    18589: (T + "word in example", {"t_pl": "następny, najbliższy, (nächste Woche) w przyszłym tygodniu"}),
    18638: (T + "word in example", {"t_pl": "pośpiech, szybciej, (Beeilung!) pośpiesz się"}),
}

REPLACE = []
SPLIT_LATER = {}
