"""Шаг 2, tr, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    15147: (T + "word in example", {"t_tr": "tanıklık etmek, göstermek, dünyaya getirmek"}),
    15774: (T + "tense", {"x_tr": "Şemsiyesiz çıktık ve eve sırılsıklam döndük"}),
    16679: (T + "word in example", {"t_tr": "tazmin etmek, tazminat vermek"}),
}

REPLACE = []
SPLIT_LATER = {}
