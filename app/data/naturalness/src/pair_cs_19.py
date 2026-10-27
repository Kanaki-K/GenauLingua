"""Шаг 2, cs, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    10443: (T + "в примере hrozivě", {"t_cs": "hrozivý, výhružný, hrozivě"}),
    10458: (T + "в примере beznadějně", {"t_cs": "beznadějný, beznadějně"}),
    10607: (T + "в примере глагол vyčítat", {"t_cs": "výčitka, obvinění, (Vorwürfe machen) vyčítat"}),
    10752: (T + "в примере marně", {"t_cs": "marný, zbytečný, marně"}),
    10805: (T + "в примере znepokojivě", {"t_cs": "znepokojivý, alarmující, znepokojivě"}),
    10812: (T + "в примере vesele", {"t_cs": "veselý, spokojený, vesele"}),
    10912: (T + "в примере ušlechtile", {"t_cs": "ušlechtilý, luxusní, ušlechtile"}),
    11134: (T + "в примере záhadně", {"t_cs": "tajemný, záhadný, záhadně"}),
    11229: (T + "в примере zbláznit se", {"t_cs": "zblázněný, šílený, (gaga sein) zbláznit se"}),
    11667: (T + "в примере výborně", {"t_cs": "výborný, lahodný, výborně"}),
    11710: (T + "в примере olizuje", {"t_cs": "lízat, olizovat, téct"}),
    11732: (T + "в примере mít žízeň", {"t_cs": "žíznivý, (durstig sein) mít žízeň"}),
}

REPLACE = []
SPLIT_LATER = {}
