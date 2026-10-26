"""Шаг 2, tr, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    8629: (T + "word in example", {"t_tr": "kalıpla kesmek, kesmek, geçmek"}),
    8640: (T + "word in example", {"t_tr": "hazır bulunma, orada olma, (im Beisein) yanında"}),
    11290: (T + "word in example", {"t_tr": "hoş görmemek, izin vermemek, kabul etmemek"}),
}

REPLACE = []
SPLIT_LATER = {}
