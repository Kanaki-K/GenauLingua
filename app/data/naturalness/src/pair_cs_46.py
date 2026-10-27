"""Шаг 2, cs, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    8652: (T + "в примере frontálně", {"t_cs": "frontální, čelní, frontálně"}),
    8663: (T + "в примере důkladně", {"t_cs": "důkladný, podrobný, důkladně"}),
    8689: (T + "в примере neodvolatelně", {"t_cs": "neodvolatelný, definitivní, neodvolatelně"}),
    8692: (T + "в примере pozoruhodně", {"t_cs": "pozoruhodný, značný, pozoruhodně"}),
    9239: (T + "в примере služebnictvo", {"t_cs": "sluha, (die Dienstboten) služebnictvo"}),
    9629: (T + "в примере doporučeně", {"t_cs": "doporučený, zapsaný, (eingeschrieben schicken) doporučeně"}),
    9918: (T + "в примере nechutně bohatý, не prachatý", {"x_cs": "Ten chlap jezdí porschem a má jachtu, musí být prachatý"}),
    11206: (T + "в примере zpustla", {"t_cs": "zchátralý, zpustlý, (verkommen) zpustnout"}),
    11214: (T + "в примере povýšeně", {"t_cs": "povýšený, domýšlivý, povýšeně"}),
    11215: (T + "в примере znepokojivě", {"t_cs": "vzrušující, (Besorgnis erregend) znepokojivý, znepokojivě"}),
    11245: (T + "в примере svědomitě", {"t_cs": "svědomitý, pečlivý, svědomitě"}),
    11316: (T + "в примере škodolibě", {"t_cs": "škodolibý, jízlivý, škodolibě"}),
    11363: (T + "в примере znechuceně", {"t_cs": "znechucený, zhnusený, znechuceně"}),
    11380: (T + "в примере posměšně", {"t_cs": "posměšný, jízlivý, posměšně"}),
    11408: (T + "в примере neúprosně", {"t_cs": "neúprosný, nemilosrdný, neúprosně"}),
    11437: (T + "в примере příkladně", {"t_cs": "příkladný, vzorný, příkladně"}),
    11449: (T + "в примере oddaně", {"t_cs": "oddaný, odevzdaný, oddaně"}),
    11459: (T + "в примере bezcílně", {"t_cs": "bezcílný, bezcílně"}),
    11472: (T + "в примере nemilosrdně", {"t_cs": "nemilosrdný, nelítostný, nemilosrdně"}),
}

REPLACE = []
SPLIT_LATER = {}
