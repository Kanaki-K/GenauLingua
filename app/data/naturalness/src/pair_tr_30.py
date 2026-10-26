"""Шаг 2, tr, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    10472: (T + "word in example", {"t_tr": "ısrar etmek, acele ettirmek, sıkıştırmak"}),
    10509: (T + "word in example", {"t_tr": "hayran, etkilenmiş, önyargılı"}),
    10544: (T + "word in example", {"t_tr": "çaresiz, (ausgeliefert sein) insafına kalmak"}),
    10567: (T + "word in example", {"t_tr": "tahrik, motor, motivasyon"}),
    10591: (T + "word in example", {"t_tr": "kızdırmak, sinirlendirmek"}),
    10595: (T + "word in example", {"t_tr": "hesap vermek, sorumluluğunu taşımak"}),
    10602: (T + "word in example", {"t_tr": "soğukkanlılık, versiyon, (aus der Fassung bringen) allak bullak etmek"}),
}

REPLACE = []
SPLIT_LATER = {}
