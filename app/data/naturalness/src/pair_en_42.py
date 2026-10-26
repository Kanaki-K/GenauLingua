"""Шаг 2, en, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    14118: (T + "word in example", {"t_en": "to mediate, to convey, to get (someone a job)"}),
    14148: (T + "word in example", {"t_en": "to notice, to remark, (jemandem etwas anmerken) can tell"}),
    14181: (T + "word in example", {"t_en": "to perform, to present, to recite"}),
    14587: (T + "word in example", {"t_en": "Jewish woman, (Jüdin sein) to be Jewish"}),
}

REPLACE = []
SPLIT_LATER = {}
