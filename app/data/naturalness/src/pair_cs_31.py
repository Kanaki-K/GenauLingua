"""Шаг 2, cs, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    10764: (T + "в примере morálně", {"t_cs": "morální, morálně"}),
    10781: (T + "в примере rozzlobil se", {"t_cs": "rozzlobený, rozhněvaný, (zornig werden) rozzlobit se"}),
    10796: (T + "в примере žádané, не toužit", {"x_cs": "Tolik lidí touží po limitovaných teniskách, že stojí celou noc před obchodem"}),
    11341: (T + "в примере zákeřně", {"t_cs": "zákeřný, záludný, zákeřně"}),
    11371: (T + "в примере vada", {"t_cs": "slabost, vada, promáčklina"}),
    11503: (T + "в примере ustaraně", {"t_cs": "ustaraný, sklíčený, ustaraně"}),
    11512: (T + "в примере melodramaticky", {"t_cs": "melodramatický, melodramaticky"}),
    11558: (T + "в примере taktně", {"t_cs": "taktní, ohleduplný, taktně"}),
    11564: (T + "в примере obezřetně", {"t_cs": "obezřetný, rozvážný, obezřetně"}),
    11568: (T + "в примере překrásně", {"t_cs": "překrásný, překrásně"}),
}

REPLACE = []
SPLIT_LATER = {}
