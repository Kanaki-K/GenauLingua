"""Шаг 2, cs, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    13013: (T + "в примере klinicky", {"t_cs": "klinický, klinicky"}),
    13077: (T + "в примере katetr, в переводе katétr", {"x_cs": "Po operaci kyčle měl děda tři dny katétr a stěžoval si na to každému"}),
    13142: (T + "в примере chorobně", {"t_cs": "chorobný, patologický, chorobně"}),
    13143: (T + "в примере plasticky", {"t_cs": "plastický, živý, plasticky"}),
    13517: (T + "в примере při tom, в переводе přitom", {"x_cs": "V sobotu malujeme kuchyň a přitom nám pomáhají sousedé"}),
    13528: (T + "в примере nespočetněkrát", {"t_cs": "nespočetný, (unzählige Male) nespočetněkrát"}),
    13674: (T + "в примере dát vařit, не postavit na sporák", {"x_cs": "Postavím zatím na sporák vodu na těstoviny"}),
    14060: (T + "в примере vyrozumět", {"t_cs": "dát vědět, uvědomit, vyrozumět"}),
    14221: (T + "в примере mluví sama se sebou", {"t_cs": "samomluva, (Selbstgespräche führen) mluvit sám se sebou"}),
}

REPLACE = []
SPLIT_LATER = {}
