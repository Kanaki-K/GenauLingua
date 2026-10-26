"""Шаг 2, en, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    14486: (T + "tense", {"x_en": "The boy is drumming on the pot with sticks"}),
    15073: (T + "word in example", {"x_en": "After a twenty-year relationship the two of them have decided to get married after all"}),
    15102: (T + "word in example", {"x_en": "For the adoption of an animal from the shelter you have to sign a contract"}),
}

REPLACE = []
SPLIT_LATER = {}
