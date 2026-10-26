"""Шаг 2, en, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    18: (T + "word in example", {"t_en": "traffic light, lights"}),
    1395: (T + "fragment", {"x_en": "My parents don't allow me to do that"}),
    1860: (T + "word in example", {"t_en": "oneself, myself, yourself"}),
    2079: (T + "word in example", {"t_en": "caution, watch out, careful"}),
    6347: (T + "word in example", {"t_en": "well-known, famous, familiar"}),
    10420: (T + "word in example", {"t_en": "strange, foreign, (fremd sein) to be a stranger"}),
    13262: (T + "word in example", {"t_en": "just, once, for a moment"}),
    13392: (T + "word in example", {"t_en": "someone, somebody, anyone"}),
    13416: (T + "word in example", {"t_en": "nobody, no one, not anybody"}),
}

REPLACE = []
SPLIT_LATER = {}
