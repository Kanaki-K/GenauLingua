"""Шаг 2, pl, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    6912: (T + "word in example", {"t_pl": "odniesienie, poszewka, (Bezug haben) odnosić się"}),
    6924: (T + "word in example", {"t_pl": "mało prawdopodobny, nieprawdopodobny, niesamowicie"}),
    6935: (T + "word in example", {"t_pl": "rozszerzać, poszerzać, rozciągać się"}),
    6958: (T + "word in example", {"t_pl": "możliwie, w miarę możliwości, (möglichst schnell) jak najszybciej"}),
    7001: (T + "word in example", {"t_pl": "tarapaty, zacisk, (in der Klemme sein) być w kropce"}),
    7005: (T + "word in example", {"t_pl": "grubiański, zgrubny, (grob gerechnet) z grubsza"}),
    7037: (T + "word in example", {"t_pl": "do siebie, wzajemnie, (zueinander halten) trzymać się razem"}),
    7042: (T + "word in example", {"t_pl": "zdobyć, zorganizować, załatwić"}),
    7067: (T + "word in example", {"t_pl": "nie udać się, nie powieść się, ponieść porażkę"}),
    7076: (T + "word in example", {"t_pl": "krzywy, skośny, dziwny"}),
    7078: (T + "word in example", {"t_pl": "cofnięty, anulowany, (rückgängig machen) cofnąć"}),
    7353: (T + "word in example", {"t_pl": "luźny, obluzowany, na sztuki"}),
    7594: (T + "word in example", {"t_pl": "kolorowy, barwny, (farbig drucken) w kolorze"}),
}

REPLACE = []
SPLIT_LATER = {}
