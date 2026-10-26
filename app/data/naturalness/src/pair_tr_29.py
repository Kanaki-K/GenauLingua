"""Шаг 2, tr, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    8973: (T + "word in example", {"t_tr": "uygulamak, icra etmek, (Druck) yapmak"}),
    9900: (T + "word in example", {"t_tr": "eski bozuk para, bozukluk"}),
}

REPLACE = []
SPLIT_LATER = {}
