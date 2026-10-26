"""Шаг 2, pl, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    14290: (T + "word in example", {"t_pl": "napisać do kogoś, zapisać na kreskę, (anschreiben lassen) kupować na kreskę"}),
    14713: (T + "word in example", {"t_pl": "kazanie, (Predigten halten) prawić kazania"}),
    14730: (T + "word in example", {"t_pl": "inscenizować, wystawiać, urządzać na pokaz"}),
    15788: (T + "word in example", {"t_pl": "kwitnący, (blühend aussehen) wyglądać kwitnąco"}),
}

REPLACE = []
SPLIT_LATER = {}
