"""Шаг 2, en, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    8267: (T + "word in example", {"t_en": "to make progress, to get ahead, to move forward"}),
    8350: (T + "word in example", {"t_en": "to take (a path), to choose, to smash in"}),
    8520: (T + "word in example", {"x_en": "The candles light up the room with a warm glow"}),
    8553: (T + "word in example", {"x_en": "At midnight everyone sets off their fireworks in the street"}),
    18826: (T + "word in example", {"t_en": "delay, arrears, (im Verzug sein) to be in arrears"}),
    18845: (T + "word in example", {"t_en": "slowed, slowed down, at reduced speed"}),
}

REPLACE = []
SPLIT_LATER = {}
