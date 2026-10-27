"""Шаг 2, cs, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    7575: (T + "в примере slibně", {"t_cs": "slibný, slibně"}),
    7608: (T + "в примере vyhradit si", {"t_cs": "stanovit, začít, (Zeit ansetzen) vyhradit si"}),
    7619: (T + "в примере efektivně", {"t_cs": "efektivní, efektivně"}),
    7685: (T + "в примере couvl", {"t_cs": "couvnutí, (einen Rückzieher machen) couvnout"}),
    7704: (T + "в примере v nejhorším", {"x_cs": "V případě potřeby můžeme jít i pěšky, když autobus nepřijede"}),
    7751: (T + "в примере bez poskvrnky", {"t_cs": "bezvadný, neposkvrněný, bez poskvrnky"}),
    18425: (T + "в примере usadit se", {"t_cs": "usedlý, (sesshaft werden) usadit se"}),
}

REPLACE = []
SPLIT_LATER = {}
