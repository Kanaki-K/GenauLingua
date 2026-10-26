"""Шаг 2, it, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    7102: (T + "word in example", {"t_it": "spettare, avvicinarsi, (auf jdn. zukommen) aspettare"}),
    7145: (T + "word in example", {"t_it": "ritirarsi, cedere, allontanarsi"}),
    7176: (T + "word in example", {"t_it": "causare, ottenere, (Wunder bewirken) fare miracoli"}),
    7206: (T + "word in example", {"t_it": "portare fuori, far uscire, lanciare"}),
    7212: (T + "word in example", {"t_it": "la lucentezza, lo splendore, il luccichio"}),
    7250: (T + "word in example", {"x_it": "Dalla ristrutturazione risparmiamo una quantità enorme sul riscaldamento"}),
    7436: (T + "word in example", {"t_it": "particolare, particolarmente"}),
    7438: (T + "word in example", {"x_it": "Ho comprato dieci biglietti della lotteria: tutti biglietti non vincenti"}),
}

REPLACE = []
SPLIT_LATER = {}
