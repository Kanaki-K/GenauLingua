"""Шаг 2, cs, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    7090: (T + "в примере nekonečně", {"t_cs": "nekonečný, nekonečně"}),
    7092: (T + "в примере odříznutý", {"t_cs": "odstřihnout, dopadnout, (abgeschnitten sein) být odříznutý"}),
    18326: (T + "в примере nepříjemně", {"t_cs": "neútulný, nepříjemný, nepříjemně"}),
    18702: (T + "вежливое Vám с большой буквы", {"x_cs": "Brzy se Vám ozvu"}),
    18723: (T + "в примере po splatnosti", {"t_cs": "splatný, prošlý, (überfällig) po splatnosti"}),
    18789: (T + "в примере roztržitě", {"t_cs": "nepřítomný, roztržitý, roztržitě"}),
}

REPLACE = []
SPLIT_LATER = {}
