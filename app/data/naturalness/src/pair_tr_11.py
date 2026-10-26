"""Шаг 2, tr, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    2221: (T + "word in example", {"t_tr": "bölmek, paylaştırmak, bölüşmek"}),
    2223: (T + "word in example", {"t_tr": "sipariş, görev, iş"}),
    2225: (T + "word in example", {"t_tr": "ele almak, üzerinde durmak, uğraşmak"}),
    2254: (T + "word in example", {"t_tr": "hayran bırakmak, (sich begeistern für) bayılmak"}),
    2258: (T + "word in example", {"t_tr": "saklamak, kendinde kalmak, aklında tutmak"}),
    2264: (T + "word in example", {"t_tr": "yük olmak, zorlamak, yıpratmak"}),
    2342: (T + "word in example", {"t_tr": "şeker hastası, diyabet hastası, diyabetli"}),
    2422: (T + "word in example", {"x_tr": "Salataya ek olarak taze ekmek var"}),
    2424: (T + "word in example", {"t_tr": "teslim alma, alma, korunma"}),
    2428: (T + "word in example", {"t_tr": "hatıra, anı, hatırlatma"}),
    2440: (T + "word in example", {"t_tr": "yiyen, (wählerischer Esser) zor beğenen biri"}),
}

REPLACE = []
SPLIT_LATER = {}
