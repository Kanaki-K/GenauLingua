"""Шаг 2, cs, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    15593: (T + "в примере kynout, не vykynout", {"x_cs": "Kynuté těsto musí ještě hodinu vykynout na teplém místě"}),
    16157: (T + "в примере anketa", {"t_cs": "průzkum, anketa, výslech"}),
    16190: (T + "в примере přeslechnout se", {"t_cs": "vyslýchat, (sich verhören) přeslechnout se"}),
}

REPLACE = []
SPLIT_LATER = {}
