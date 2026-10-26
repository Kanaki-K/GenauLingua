"""Шаг 2, en, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    13101: (T + "spelling", {"x_en": "After the fatty food at the wedding my dad's gallbladder played up again"}),
    13517: (T + "word in example", {"t_en": "in doing so, here, with it"}),
    14029: (T + "word in example", {"t_en": "to deliver, to convey, to break (news)"}),
    14055: (T + "word in example", {"t_en": "to notify, to communicate, to let know"}),
}

REPLACE = []
SPLIT_LATER = {}
