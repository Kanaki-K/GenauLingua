"""Шаг 2, cs, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    13203: (T + "в примере ztuhlá šíje, не ztuhlost", {"x_cs": "Z dlouhého sezení u notebooku mám pořád ztuhlost v šíji"}),
    13483: (T + "в примере nejmenší, не žádný", {"x_cs": "Nemám vůbec žádnou chuť jít dneska ještě nakupovat"}),
    13484: (T + "в примере napodruhé", {"t_cs": "druhý, (beim zweiten Mal) napodruhé"}),
    13888: (T + "в примере poselství", {"t_cs": "vzkaz, poselství, velvyslanectví"}),
}

REPLACE = []
SPLIT_LATER = {}
