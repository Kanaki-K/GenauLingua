"""Шаг 2, it, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    12893: (T + "word in example", {"t_it": "guarire, rimettersi, ristabilirsi"}),
    12909: (T + "word in example", {"t_it": "mentale, mentalmente"}),
    13567: (T + "word in example", {"t_it": "qualche, certo, (manch einer) più d'uno"}),
    14118: (T + "word in example", {"t_it": "mediare, trasmettere, procurare (un lavoro)", "x_it": "Il lavoro in albergo me l'ha procurato mia zia"}),
    14603: (T + "word in example", {"t_it": "solenne, solennemente"}),
}

REPLACE = []
SPLIT_LATER = {}
