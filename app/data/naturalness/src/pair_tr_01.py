"""Шаг 2, tr, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    103: (T + "word in example", {"t_tr": "kesinlikle, kesin, mutlaka"}),
    141: (T + "word in example", {"x_tr": "Fırından birkaç küçük ekmek alır mısın?"}),
    187: (T + "word in example", {"t_tr": "yine de, ama, ki"}),
    196: (T + "word in example", {"t_tr": "karanlık, koyu, (dunkel werden) kararmak"}),
    200: (T + "word in example", {"t_tr": "izni olmak, -ebilmek"}),
    305: (T + "word in example", {"t_tr": "tamamen, oldukça, gayet"}),
    335: (T + "word in example", {"t_tr": "dükkân, mağaza, iş"}),
    366: (T + "word in example", {"t_tr": "sahip olmak, var olmak"}),
    416: (T + "word in example", {"t_tr": "açlık, (Hunger haben) aç olmak"}),
    450: (T + "word in example", {"t_tr": "şimdi, şu an"}),
    507: (T + "word in example", {"t_tr": "mal olmak, fiyatı olmak, tutmak"}),
}

REPLACE = []
SPLIT_LATER = {}
