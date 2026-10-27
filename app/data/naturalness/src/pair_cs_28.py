"""Шаг 2, cs, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    7883: (T + "в примере dutě", {"t_cs": "dutý, dutě"}),
    8116: (T + "в примере dostat se, не zaplést se", {"x_cs": "Zapletl jsem se do toho úplně nevinně"}),
    8217: (T + "в примере drasticky", {"t_cs": "drastický, drasticky"}),
    8654: (T + "в примере nesrovnatelně", {"t_cs": "nesrovnatelný, nesrovnatelně"}),
}

REPLACE = []
SPLIT_LATER = {}
