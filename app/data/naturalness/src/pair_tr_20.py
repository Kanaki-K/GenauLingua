"""Шаг 2, tr, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    12143: (T + "word in example", {"t_tr": "kaybeden, (schlechter Verlierer) kaybetmeyi bilmeyen"}),
    12492: (T + "word in example", {"t_tr": "sokma, sokulan yer"}),
    12535: (T + "word in example", {"t_tr": "baygın, güçsüz, (ohnmächtig werden) bayılmak"}),
    12588: (T + "word in example", {"t_tr": "veba, salgın, (wie die Pest hassen) ölesiye nefret etmek"}),
    12972: (T + "word in example", {"t_tr": "güneş yanığı, (Sonnenbrand bekommen) güneşte yanmak"}),
}

REPLACE = []
SPLIT_LATER = {}
