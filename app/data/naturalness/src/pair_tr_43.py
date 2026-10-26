"""Шаг 2, tr, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    16416: (T + "word in example", {"t_tr": "affetmek, çıkarmak, bağışlamak"}),
    16446: (T + "word in example", {"t_tr": "mahkeme, divan"}),
    16533: (T + "word in example", {"t_tr": "savunmak, taraf olmak, (für etwas plädieren) -den yana olmak"}),
}

REPLACE = []
SPLIT_LATER = {}
