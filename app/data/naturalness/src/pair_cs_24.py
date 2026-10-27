"""Шаг 2, cs, порция 24: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    15941: (T + "в примере lidé", {"t_cs": "lid, národ, lidé"}),
    15981: (T + "в примере obyvatel, не občan", {"x_cs": "Spousta občanů podepsala petici proti novému obchvatu"}),
    16000: (T + "в примере hejtman", {"t_cs": "kapitán, setník, hejtman"}),
    16025: (T + "в примере nelegálně", {"t_cs": "nelegální, protizákonný, nelegálně"}),
    16036: (T + "в примере přiznat se", {"t_cs": "přiznání, doznání, (ein Geständnis machen) přiznat se"}),
}

REPLACE = []
SPLIT_LATER = {}
