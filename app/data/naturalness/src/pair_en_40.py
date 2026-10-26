"""Шаг 2, en, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    9887: (T + "word in example", {"t_en": "for sale, corruptible, (nicht käuflich) can't be bought"}),
    10873: (T + "word in example", {"x_en": "With his wedding speech my brother got a lot of laughs"}),
    10908: (T + "word in example", {"t_en": "leniency, forbearance, (um Nachsicht bitten) to ask someone to bear with one"}),
    10938: (T + "word in example", {"x_en": "On her first flight my mum was in mortal fear, now she flies to Tenerife every winter"}),
    11022: (T + "word in example", {"t_en": "heartbreak, lovesickness, (Liebeskummer haben) to be heartbroken"}),
}

REPLACE = []
SPLIT_LATER = {}
