"""Шаг 2, es, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    14809: (T + "Tatort испанцу неизвестен", {"x_es": "Para una escena de una serie policíaca mi tío estuvo sentado en una cafetería como extra"}),
    16627: (T + "в примере tener respeto", {"t_es": "rendir, tributar, (Respekt zollen) tener respeto"}),
    16660: (T + "se las da de lugarteniente suyo — коряво", {"x_es": "Cuando mis padres no están, mi hermano mayor se cree su lugarteniente"}),
}

REPLACE = []
SPLIT_LATER = {}
