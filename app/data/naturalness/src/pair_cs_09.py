"""Шаг 2, cs, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    1491: (T + "в примере kluzko", {"t_cs": "kluzký, hladký, (es ist glatt) je kluzko"}),
    1576: (T + "в примере čtverečkovaný", {"t_cs": "kostkovaný, (Heft, Papier) čtverečkovaný"}),
    1645: (T + "в примере нет životní cesta", {"x_cs": "Na své životní cestě děda bydlel v pěti zemích"}),
    1699: (T + "в примере немецкие слова вместо перевода", {"x_cs": "V Bavorsku se dnes druhému stupni základní školy říká střední škola"}),
    1747: (T + "в примере řádně", {"t_cs": "řádný, předpisový, řádně"}),
}

REPLACE = []
SPLIT_LATER = {}
