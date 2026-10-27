"""Шаг 2, es, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    11511: (T + "в примере con tenacidad", {"x_es": "Mi hijo es tenaz: pregunta cada día cuándo vamos por fin a la playa"}),
    11513: (T + "sensual про гончарство — неуместно", {"x_es": "La alfarería es un trabajo muy sensorial, sientes el barro bajo las manos"}),
    11514: (T + "нет bobo", {"x_es": "Yo, como un bobo, me he dejado la llave en casa"}),
    12357: (T + "в примере a tiro", {"t_es": "el alcance de tiro, (in Schussweite) a tiro"}),
    13114: (T + "в примере pedir la cabeza", {"t_es": "la cabellera, el escalpo, (jemandes Skalp fordern) pedir la cabeza"}),
}

REPLACE = []
SPLIT_LATER = {}
