"""Шаг 2, en, порция 24: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    16003: (T + "word in example", {"t_en": "commander, commandant, chief (fire brigade)"}),
    16122: (T + "word in example", {"t_en": "to conquer, to win over, to win (a heart)"}),
    16128: (T + "word in example", {"x_en": "He's been in custody for two years"}),
    16136: (T + "word in example", {"t_en": "to prevail, to rule, to reign"}),
    16142: (T + "word in example", {"t_en": "combat, battle, fighting"}),
    17061: (T + "word in example", {"t_en": "journey, trip, drive"}),
    17069: (T + "word in example", {"t_en": "to stop, to last, to pull over"}),
}

REPLACE = []
SPLIT_LATER = {}
