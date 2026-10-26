"""Шаг 2, en, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    1827: (T + "word in example", {"t_en": "smart, stylish, (sich schick machen) to dress up"}),
    1832: (T + "tense", {"x_en": "My heart is beating fast"}),
    1908: (T + "word in example", {"t_en": "to rise, to climb, to go up"}),
    1980: (T + "word in example", {"x_en": "I'll take on the responsibility"}),
    2039: (T + "word in example", {"t_en": "to postpone, to misplace, to mislay"}),
    2072: (T + "word in example", {"x_en": "The preparation for the party took longer than the party itself"}),
    2145: (T + "word in example", {"t_en": "refusal, cancellation, (eine Absage) to cancel"}),
}

REPLACE = []
SPLIT_LATER = {}
