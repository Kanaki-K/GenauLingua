"""Шаг 2, cs, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    11511: (T + "в примере vytrvale", {"t_cs": "vytrvalý, neústupný, vytrvale"}),
    11531: (T + "в примере nepříjemně", {"t_cs": "nepříjemný, nepříjemně"}),
    11605: (T + "в примере ohromeně", {"t_cs": "ohromený, bez slov, ohromeně"}),
    11925: (T + "в примере jíst", {"t_cs": "sníst, jíst, spotřebovat"}),
    12329: (T + "в примере švihadlo", {"t_cs": "lano, provaz, (Springseil) švihadlo"}),
    12926: (T + "в примере znetvořeně", {"t_cs": "znetvořený, zkreslený, znetvořeně"}),
    13065: (T + "в примере sterilně", {"t_cs": "sterilní, neplodný, sterilně"}),
    13124: (T + "в примере mít kocovinu", {"t_cs": "s kocovinou, (verkatert sein) mít kocovinu"}),
    14263: (T + "в примере žvanit", {"t_cs": "žvanění, tlachání, (schwafeln) žvanit"}),
}

REPLACE = []
SPLIT_LATER = {}
