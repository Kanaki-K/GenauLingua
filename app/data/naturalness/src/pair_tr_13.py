"""Шаг 2, tr, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    2773: (T + "word in example", {"t_tr": "saygı, düşüncelilik, (Rücksicht nehmen) düşünmek"}),
    2792: (T + "word in example", {"t_tr": "değiştirmek, vites değiştirmek, (Modus) açmak"}),
    2909: (T + "word in example", {"t_tr": "ilişki, iletişim, kullanım"}),
    3019: (T + "word in example", {"t_tr": "geri almak, caymak, cayma hakkını kullanmak"}),
}

REPLACE = []
SPLIT_LATER = {}
