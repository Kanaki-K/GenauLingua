"""Шаг 2, fr, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    14809: (T + "Tatort французу неизвестен", {"x_fr": "Pour une scène d'une série policière, mon oncle a fait le figurant assis dans un café"}),
}

REPLACE = []
SPLIT_LATER = {}
