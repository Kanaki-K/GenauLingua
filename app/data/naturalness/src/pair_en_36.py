"""Шаг 2, en, порция 36: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    16286: (T + "word in example", {"t_en": "terror, terrorism, (Terror machen) to terrorise"}),
    16913: (T + "word in example", {"t_en": "murderous, gruelling, a killer"}),
    17154: (T + "word in example", {"x_en": "Can we speed up a bit?"}),
}

REPLACE = []
SPLIT_LATER = {}
