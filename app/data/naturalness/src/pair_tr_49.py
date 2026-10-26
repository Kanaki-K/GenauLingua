"""Шаг 2, tr, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    16811: (T + "word in example", {"t_tr": "nükseden, tekrar eden, (rückfällig werden) yeniden suç işlemek", "x_tr": "Hırsız üçüncü kez yeniden suç işledi ve şimdi hapse girecek"}),
    16911: (T + "word in example", {"t_tr": "muhafaza, saklama, gözaltı"}),
    16932: (T + "word in example", {"t_tr": "gözden geçirme, revizyon, yeniden inceleme"}),
}

REPLACE = []
SPLIT_LATER = {}
