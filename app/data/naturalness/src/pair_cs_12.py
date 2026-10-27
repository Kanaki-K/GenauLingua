"""Шаг 2, cs, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    2448: (T + "в примере fér", {"t_cs": "spravedlivý, férový, fér (hovor.)"}),
    2462: (T + "в примере rychle", {"t_cs": "rychlý, pevný, rychle"}),
    2485: (T + "в примере существительное klid", {"x_cs": "U nás na vesnici je to velmi klidné"}),
    2490: (T + "в примере frustrovaný, не frustrace", {"x_cs": "Po hádce jsem cítil velkou frustraci"}),
    2497: (T + "в примере ulička", {"t_cs": "chodba, rychlost, (im Flugzeug) ulička"}),
    2530: (T + "в примере bezlepkově", {"t_cs": "bezlepkový, bez lepku, bezlepkově"}),
    2582: (T + "в примере interně", {"t_cs": "interní, vnitřní, interně"}),
    2652: (T + "в примере živě", {"t_cs": "živý, rušný, živě"}),
    2654: (T + "в примере nesnáším", {"t_cs": "trpět, snášet, (nicht leiden können) nesnášet"}),
    2692: (T + "в примере objektivně", {"t_cs": "objektivní, nestranný, objektivně"}),
    2702: (T + "в примере optimisticky", {"t_cs": "optimistický, optimisticky"}),
}

REPLACE = []
SPLIT_LATER = {}
