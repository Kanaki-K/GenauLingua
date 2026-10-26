"""Шаг 2, it, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    11077: (T + "word in example", {"t_it": "dolce, grazioso, amabile (vino)"}),
    11162: (T + "word in example", {"t_it": "doloroso, penoso, dolorosamente"}),
    11163: (T + "word in example", {"t_it": "istintivo, istintivamente"}),
    11164: (T + "word in example", {"t_it": "eroico, eroicamente"}),
    12264: (T + "word in example", {"t_it": "il tappetino, il materassino", "x_it": "A ginnastica mio figlio può finalmente fare le capriole sul materassino"}),
    12284: (T + "word in example", {"x_it": "«Allora, bello, hai di nuovo tirato la palla nel giardino del vicino?», chiede mio padre a mio figlio"}),
    12755: (T + "word in example", {"t_it": "fisico, fisicamente"}),
    12808: (T + "word in example", {"x_it": "Schiarendosi rumorosamente la gola il nonno fa capire che adesso vuole fare il suo discorso"}),
}

REPLACE = []
SPLIT_LATER = {}
