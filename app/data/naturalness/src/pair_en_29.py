"""Шаг 2, en, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    8909: (T + "word in example", {"t_en": "working, active, (tätig sein als) to work as"}),
    8953: (T + "word in example", {"x_en": "In winter the cable car transports thousands of skiers up the mountain every day"}),
    9214: (T + "word in example", {"x_en": "My mum has ten subordinates, but at home the cat is still in charge"}),
    9268: (T + "natural", {"x_en": "Before we buy the old flat, we're getting a surveyor to look at all the rooms"}),
}

REPLACE = []
SPLIT_LATER = {}
