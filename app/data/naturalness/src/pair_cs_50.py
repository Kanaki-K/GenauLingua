"""Шаг 2, cs, порция 50: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    18086: (T + "в примере testovací osoby", {"t_cs": "testovaná osoba, testovací osoba, účastník testu"}),
    18098: (T + "в примере experimentálně", {"t_cs": "experimentální, pokusný, experimentálně"}),
    18470: (T + "в примере při svíčkách", {"t_cs": "světlo svíček, svit svíček, (bei Kerzenlicht) při svíčkách"}),
    18927: (T + "в примере odříhnout", {"t_cs": "říhnout si, krknout si, odříhnout"}),
}

REPLACE = []
SPLIT_LATER = {}
