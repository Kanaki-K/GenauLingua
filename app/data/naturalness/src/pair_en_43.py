"""Шаг 2, en, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    15700: (T + "word in example", {"t_en": "to kill, to shoot, to bag"}),
    16405: (T + "word in example", {"t_en": "state of alert, standby, high alert"}),
    16532: (T + "word in example", {"x_en": "Because the jacket has a small stain on the sleeve I'm getting a twenty per cent discount"}),
}

REPLACE = []
SPLIT_LATER = {}
