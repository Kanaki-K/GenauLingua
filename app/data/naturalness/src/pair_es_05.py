"""Шаг 2, es, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    1440: (T + "word in example", {"t_es": "voluntario, voluntariamente"}),
    1530: (T + "word in example", {"t_es": "dentro, adentro, (herein!) ¡adelante!"}),
    1537: (T + "word in example", {"t_es": "allá, (hin und zurück) ida y vuelta"}),
    1867: (T + "word in example", {"t_es": "la seguridad, la certeza, (sich sicher fühlen) sentirse seguro"}),
    2036: (T + "word in example", {"t_es": "concertar, acordar, (einen Termin vereinbaren) pedir cita"}),
    6284: (T + "word in example", {"t_es": "completamente, totalmente, por completo"}),
}

REPLACE = []
SPLIT_LATER = {}
