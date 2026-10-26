"""Шаг 2, it, порция 50: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    18086: (T + "word in example", {"t_it": "il soggetto del test, il partecipante, la persona per il test"}),
}

REPLACE = []
SPLIT_LATER = {}
