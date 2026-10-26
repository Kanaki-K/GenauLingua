"""Шаг 2, tr, порция 50: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    18057: (T + "word in example", {"t_tr": "vat, watt, gelgit düzlüğü"}),
    18388: (T + "word in example", {"t_tr": "domuz ahırı, ahır, çöplük"}),
}

REPLACE = []
SPLIT_LATER = {}
