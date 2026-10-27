"""Шаг 2, cs, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    1673: (T + "в примере samci", {"t_cs": "mužský, mužný, (bei Tieren) samec"}),
    6347: (T + "в примере povědomá", {"t_cs": "známý, povědomý"}),
    6558: (T + "в примере uprostřed", {"t_cs": "střed, (in der Mitte) uprostřed"}),
    9441: (T + "в примере učitelka", {"t_cs": "učitel, učitelka"}),
    10061: (T + "в примере zlobíš se", {"t_cs": "naštvaný, zlý, (böse sein) zlobit se"}),
    10420: (T + "в примере нет cizí", {"x_cs": "Promiňte, jsem tady cizí, kde je nádraží?"}),
    13265: (T + "в примере na zahradě", {"t_cs": "v, ve, na"}),
    13282: (T + "в примере na pláž", {"t_cs": "k, do, na"}),
    13317: (T + "в примере tímhle", {"t_cs": "tento, tenhle"}),
    13592: (T + "в примере počtvrté", {"t_cs": "čtvrtý, (zum vierten Mal) počtvrté"}),
    17166: (T + "в примере přestup", {"t_cs": "přípoj, připojení, přestup"}),
}

REPLACE = []
SPLIT_LATER = {}
