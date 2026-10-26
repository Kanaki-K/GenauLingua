"""Шаг 2, pl, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    8105: (T + "word in example", {"t_pl": "schodzić, zejść, odjeżdżać"}),
    8250: (T + "word in example", {"t_pl": "dotyczyć, odnosić się, (was ... anbelangt) jeśli chodzi o"}),
    8293: (T + "word in example", {"t_pl": "wszechstronny, kompleksowy, dokładny"}),
    8356: (T + "word in example", {"x_pl": "Wspomniane ciasto, o którym wszyscy mówią, niestety już ktoś zjadł"}),
    8449: (T + "word in example", {"t_pl": "liczny, wielokrotny, (multiple Sklerose) stwardnienie rozsiane"}),
    8470: (T + "word in example", {"t_pl": "gwałtownie, szybko, błyskawicznie"}),
    8534: (T + "word in example", {"t_pl": "krążyć wokół, okrążać, zakreślić"}),
    8568: (T + "word in example", {"t_pl": "zewnętrzny, (von extern) z zewnątrz"}),
    8596: (T + "word in example", {"t_pl": "wziąć na dywanik, ochrzanić, dać ochrzan"}),
    18843: (T + "word in example", {"t_pl": "pochopny, pospieszny, w pośpiechu"}),
}

REPLACE = []
SPLIT_LATER = {}
