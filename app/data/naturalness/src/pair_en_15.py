"""Шаг 2, en, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    6855: (T + "word in example", {"t_en": "to commit, to celebrate, to make (a mistake)"}),
    6887: (T + "word in example", {"x_en": "What kind of bread do you want?"}),
    6898: (T + "word in example", {"t_en": "to provide, to get, to make (time)"}),
    6913: (T + "word in example", {"t_en": "successful, well done, a success"}),
    6935: (T + "word in example", {"t_en": "to widen, to expand, to stretch"}),
    6965: (T + "word in example", {"t_en": "to break off, to drop out, to cut short"}),
    6970: (T + "word in example", {"t_en": "to apply, to be considered, to be valid"}),
    6998: (T + "word in example", {"t_en": "to record, to grasp, to capture"}),
    7006: (T + "word in example", {"t_en": "to suppose, to suspect, to assume"}),
    7010: (T + "word in example", {"t_en": "to prevent, to hinder, to stop from"}),
    7065: (T + "word in example", {"x_en": "That was an unusual idea for the party"}),
    7076: (T + "word in example", {"t_en": "crooked, weird, sloping"}),
    7240: (T + "word in example", {"t_en": "to depict, to represent, to show"}),
    7370: (T + "word in example", {"x_en": "Leave me alone, I'm just bingeing a film"}),
}

REPLACE = []
SPLIT_LATER = {}
