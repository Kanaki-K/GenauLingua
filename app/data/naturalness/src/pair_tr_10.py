"""Шаг 2, tr, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    1789: (T + "word in example", {"t_tr": "kural, adet, (in der Regel) genellikle"}),
    1899: (T + "word in example", {"t_tr": "güçlendirmek, (sich stärken) güç toplamak"}),
    2049: (T + "word in example", {"t_tr": "çılgın, deli, (verrückt werden) çıldırmak"}),
    2145: (T + "word in example", {"t_tr": "ret, iptal, hayır"}),
}

REPLACE = []
SPLIT_LATER = {}
