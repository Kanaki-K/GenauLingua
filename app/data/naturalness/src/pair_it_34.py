"""Шаг 2, it, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    14318: (T + "word in example", {"x_it": "Il latore della lettera aspetta una risposta davanti alla porta"}),
    14539: (T + "word in example", {"x_it": "Senza il manoscritto davanti non riesco a fare un discorso, altrimenti dimentico tutto"}),
    14542: (T + "word in example", {"x_it": "La finale ha tenuto tutto lo stadio sotto incantesimo"}),
    15073: (T + "word in example", {"t_it": "il partenariato, la collaborazione, la convivenza"}),
}

REPLACE = []
SPLIT_LATER = {}
