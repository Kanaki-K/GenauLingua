"""Шаг 2, en, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    2172: (T + "word in example", {"x_en": "The printer in the office is constantly breaking down"}),
    2183: (T + "word in example", {"t_en": "system, attachment, (in der Anlage) attached"}),
    2223: (T + "word in example", {"t_en": "order, assignment, job"}),
    2225: (T + "word in example", {"x_en": "Since her father died she has been getting to grips with her family history"}),
    2250: (T + "natural", {"x_en": "The doctor found the high blood test results worrying and sent me to a specialist"}),
    2261: (T + "word in example", {"t_en": "to master, to control, to have a good command of"}),
    2316: (T + "word in example", {"x_en": "From today citizens can book an appointment at the town hall online"}),
    2422: (T + "word in example", {"t_en": "addition, supplement, (als Ergänzung) to go with"}),
    2443: (T + "word in example", {"x_en": "I'll possibly come later"}),
}

REPLACE = []
SPLIT_LATER = {}
