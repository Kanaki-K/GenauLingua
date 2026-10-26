"""Шаг 2, pl, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    7756: (T + "word in example", {"t_pl": "powodzić się, wieść się"}),
    7809: (T + "word in example", {"t_pl": "zrzucić, przynosić zysk, dawać (plon)"}),
    7827: (T + "word in example", {"t_pl": "wściekły, szalony, (rasend werden) wpaść w szał"}),
    7849: (T + "word in example", {"t_pl": "zwolnić, udostępnić, dopuścić"}),
    7850: (T + "word in example", {"t_pl": "zużyty, wyczerpany, (aufgebraucht sein) skończyć się"}),
    7900: (T + "word in example", {"t_pl": "przelać się, wykipieć"}),
}

REPLACE = []
SPLIT_LATER = {}
