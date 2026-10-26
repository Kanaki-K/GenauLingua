"""Шаг 2, en, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    8397: (T + "meaning inverted", {"x_en": "My husband makes up for his lack of cooking skills with a lot of cheese on everything"}),
    8411: (T + "word in example", {"t_en": "useless, pointless, needlessly"}),
    8556: (T + "word in example", {"x_en": "The haircut from the cheap hairdresser is disastrous, my daughter has been wearing a hat for three days"}),
}

REPLACE = []
SPLIT_LATER = {}
