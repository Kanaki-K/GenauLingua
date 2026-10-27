"""Шаг 2, cs, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    2797: (T + "в примере dát gól", {"t_cs": "střílet, vstřelit, (ein Tor schießen) dát gól"}),
    2812: (T + "в примере ztišit", {"t_cs": "snižovat, snížit, (die Stimme senken) ztišit"}),
    2824: (T + "в примере sluníčko", {"t_cs": "slunce, sluneční svit, (Kosewort) sluníčko"}),
    2923: (T + "в примере nezdravě", {"t_cs": "nezdravý, nezdravě"}),
    2925: (T + "в примере zbytečně", {"t_cs": "zbytečný, nepotřebný, zbytečně"}),
    2926: (T + "в примере nemít pravdu", {"t_cs": "nespravedlnost, (Unrecht haben) mýlit se, nemít pravdu"}),
    2951: (T + "в примере neumí prohrávat", {"t_cs": "poražený, poražená, (kein guter Verlierer sein) neumět prohrávat"}),
    3009: (T + "вежливое Vám с большой буквы", {"x_cs": "Promiňte, s tím Vám nepomůžu"}),
    3055: (T + "в примере svižně", {"t_cs": "rychlý, svižný, svižně"}),
}

REPLACE = []
SPLIT_LATER = {}
