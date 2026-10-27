"""Шаг 2, fr, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    12400: (T + "в примере venir à bout de", {"t_fr": "soulever, assumer, venir à bout de"}),
    12647: (T + "в примере institution", {"t_fr": "l'établissement, l'institution"}),
    12662: (T + "в примере s'évanouir", {"t_fr": "l'évanouissement, l'impuissance, (in Ohnmacht fallen) s'évanouir"}),
}

REPLACE = []
SPLIT_LATER = {}
