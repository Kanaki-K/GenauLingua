"""Шаг 2, fr, порция 22: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    14422: (T + "raconter des contes — неестественно", {"x_fr": "Arrête de me raconter des contes de fées !"}),
    14945: (T + "в примере séparément", {"t_fr": "séparé, séparément"}),
    15006: (T + "quels rapports vous avez entre vous — коряво", {"x_fr": "Quels sont vos rapports, à vous deux ?"}),
}

REPLACE = []
SPLIT_LATER = {}
