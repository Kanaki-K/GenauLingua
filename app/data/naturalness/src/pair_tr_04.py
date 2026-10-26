"""Шаг 2, tr, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    67: (T + "word in example", {"t_tr": "fırında pişirmek, (pasta) yapmak"}),
    98: (T + "word in example", {"t_tr": "bildirim, haber, (Bescheid sagen) haber vermek"}),
    170: (T + "word in example", {"t_tr": "buna, ayrıca, yanında"}),
    214: (T + "word in example", {"t_tr": "razı, anlaştık, kabul"}),
    774: (T + "word in example", {"t_tr": "şey, mesele, (Sachen) eşyalar"}),
    993: (T + "word in example", {"t_tr": "yanından, bitti, geçti"}),
    1000: (T + "word in example", {"t_tr": "tanıtmak, tanıştırmak, hayal etmek"}),
    1013: (T + "word in example", {"t_tr": "değiştirmek, bozdurmak, çevirmek"}),
    1031: (T + "meaning", {"x_tr": "Güneş batıda batar"}),
}

REPLACE = []
SPLIT_LATER = {}
