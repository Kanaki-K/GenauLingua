"""Шаг 2, tr, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    101: (T + "word in example", {"t_tr": "iyileşme, düzelme, (gute Besserung) geçmiş olsun", "x_tr": "Geçmiş olsun, acil şifalar dilerim"}),
    381: (T + "word in example", {"t_tr": "en önemli şey, önemli olan"}),
    18144: (T + "word in example", {"t_tr": "yan tarafta, bitişikte, yan"}),
}

REPLACE = []
SPLIT_LATER = {}
