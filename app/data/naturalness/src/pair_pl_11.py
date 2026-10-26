"""Шаг 2, pl, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    2154: (T + "word in example", {"t_pl": "realizacja, obsługa, (Schadensabwicklung) likwidacja szkody"}),
    2181: (T + "word in example", {"t_pl": "unosić, unieść, podnosić"}),
    2217: (T + "word in example", {"t_pl": "uważny, troskliwy, uważnie"}),
    2351: (T + "word in example", {"t_pl": "głupi, durny, głupio"}),
    2353: (T + "word in example", {"t_pl": "podwójny, podwójnie, dwa razy"}),
    2371: (T + "word in example", {"t_pl": "samodzielny, samodzielnie, na własną odpowiedzialność"}),
    2386: (T + "word in example", {"t_pl": "zasypiać, zasnąć, drętwieć"}),
    2398: (T + "typo", {"x_pl": "Do bezy potrzebuję tylko białka, żółtko pójdzie do ciasta"}),
    2402: (T + "word in example", {"t_pl": "przyjmować, odbierać, witać"}),
}

REPLACE = []
SPLIT_LATER = {}
