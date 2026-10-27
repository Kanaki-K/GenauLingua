"""Шаг 2, cs, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    12219: (T + "в примере nerozhodně", {"t_cs": "nerozhodný, nerozhodnutý, nerozhodně"}),
    12296: (T + "в примере venčit", {"t_cs": "venčení, (Gassi gehen) venčit psa"}),
    12535: (T + "в примере omdlel", {"t_cs": "omdlelý, bezmocný, (ohnmächtig werden) omdlít"}),
    12551: (T + "в примере smrtelně", {"t_cs": "smrtelný, smrtící, smrtelně"}),
    12557: (T + "в примере ve formě", {"t_cs": "fit, v kondici, ve formě"}),
    12559: (T + "в примере brát", {"t_cs": "vzít si, brát, zaujmout"}),
    12571: (T + "в примере vržou, не skřípat", {"x_cs": "Staré dřevěné schody skřípou při každém kroku"}),
    12595: (T + "в примере fyzicky", {"t_cs": "fyzický, tělesný, fyzicky"}),
    12972: (T + "в примере spálit se od slunce", {"t_cs": "spálenina od slunce, (einen Sonnenbrand bekommen) spálit se od slunce"}),
    12975: (T + "в примере нет pohoda", {"x_cs": "Pro svou pohodu potřebuju každý den čerstvý vzduch"}),
}

REPLACE = []
SPLIT_LATER = {}
