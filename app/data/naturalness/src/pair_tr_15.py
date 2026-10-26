"""Шаг 2, tr, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    6855: (T + "word in example", {"t_tr": "işlemek, kutlamak, (Fehler) yapmak"}),
    6898: (T + "word in example", {"t_tr": "sağlamak, temin etmek, (Zeit) ayırmak"}),
    6934: (T + "word in example", {"t_tr": "hazır bulunan, mevcut, katılmış"}),
    6989: (T + "word in example", {"t_tr": "patlak, yassı, dümdüz"}),
    7012: (T + "word in example", {"t_tr": "etrafa bakmak, göz atmak, bakınmak"}),
    7023: (T + "word in example", {"t_tr": "kuvvetli, güçlü, ağır (koku)"}),
    7042: (T + "word in example", {"t_tr": "temin etmek, sağlamak, bulmak"}),
    7066: (T + "word in example", {"t_tr": "tetiklemek, yol açmak, (Panik) sokmak"}),
    7240: (T + "word in example", {"t_tr": "temsil etmek, betimlemek, göstermek"}),
    7294: (T + "meaning", {"x_tr": "Bu ihtimali dışlayamayız"}),
}

REPLACE = []
SPLIT_LATER = {}
