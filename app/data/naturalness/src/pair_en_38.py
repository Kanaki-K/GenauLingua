"""Шаг 2, en, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    7366: (T + "word in example", {"x_en": "My son has truly tidied his room without me saying a word"}),
    7608: (T + "word in example", {"t_en": "to schedule, to start, to set aside (time)"}),
    7654: (T + "word in example", {"t_en": "to give away, to hand over, to give up"}),
    7665: (T + "word in example", {"t_en": "to prevail, to exercise, (Gnade walten lassen) to show mercy"}),
    7679: (T + "word in example", {"x_en": "The assembly of the new cot took three hours and two arguments"}),
    7738: (T + "word in example", {"t_en": "to be granted, to fall to, to be given"}),
    18653: (T + "natural", {"x_en": "He's always late"}),
    18769: (T + "word in example", {"t_en": "procedure, schedule, order (of events)"}),
    18783: (T + "word in example", {"t_en": "Middle Ages, (mittelalterlich) medieval"}),
}

REPLACE = []
SPLIT_LATER = {}
