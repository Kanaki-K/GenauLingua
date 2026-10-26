"""Шаг 2, tr, порция 16: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    7718: (T + "word in example", {"t_tr": "kıt, kıl payı, dar"}),
    7984: (T + "word in example", {"t_tr": "fark etmek, anlamak, gerçekleştirmek"}),
    8193: (T + "word in example", {"t_tr": "çekmek, küçülmek, azalmak"}),
    8595: (T + "word in example", {"t_tr": "koşturup durmak, koşuşturmak"}),
    8796: (T + "word in example", {"t_tr": "karıştırmak, açmak, (Unsinn anstellen) saçmalık yapmak"}),
    8837: (T + "word in example", {"t_tr": "amir, patron, üst"}),
}

REPLACE = []
SPLIT_LATER = {}
