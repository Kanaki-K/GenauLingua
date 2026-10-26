"""Шаг 2, it, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    7598: (T + "word in example", {"x_it": "Dopo il litigio ci è voluta una settimana per ripristinare la pace tra i fratelli"}),
    7608: (T + "word in example", {"t_it": "fissare, avviare, prevedere (il tempo)"}),
    7637: (T + "word in example", {"x_it": "Il profumo di pane appena sfornato al mattino penetra fino in camera da letto"}),
    7663: (T + "word in example", {"x_it": "L'appuntamento dal dentista è in un orario scomodo, proprio nella pausa pranzo di mia figlia"}),
    7669: (T + "word in example", {"x_it": "Durante la vaccinazione mio figlio distoglie lo sguardo e conta ad alta voce fino a dieci"}),
    7704: (T + "word in example", {"t_it": "all'occorrenza, se necessario, al limite"}),
    7734: (T + "word in example", {"t_it": "stendere, spargere, diffondersi"}),
    7744: (T + "word in example", {"t_it": "portare, condurre, (wo soll das hinführen) dove andremo a finire"}),
    18425: (T + "word in example", {"x_it": "Dopo dieci traslochi in dieci anni mio fratello finalmente è diventato stanziale e ha comprato casa"}),
    18783: (T + "word in example", {"t_it": "il Medioevo, (mittelalterlich) medievale"}),
}

REPLACE = []
SPLIT_LATER = {}
