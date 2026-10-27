"""Шаг 2, cs, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    8848: (T + "в примере ochranka", {"t_cs": "bezpečnostní služba, ostraha, ochranka"}),
    9446: (T + "в примере francouzsky", {"t_cs": "francouzský, francouzsky"}),
    9729: (T + "в примере majlant", {"x_cs": "Nové kolo mě stálo celé jmění!"}),
    9746: (T + "в примере korunka (zub)", {"t_cs": "koruna, (Zahn) korunka"}),
    9823: (T + "в примере výtěžek", {"t_cs": "příjem, tržba, výtěžek"}),
}

REPLACE = []
SPLIT_LATER = {}
