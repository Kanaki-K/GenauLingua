"""Шаг 2, es, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    2205: (T + "word in example", {"t_es": "molesto, enfadado, (wie ärgerlich!) ¡qué fastidio!"}),
    2217: (T + "word in example", {"t_es": "atento, considerado, (aufmerksam zuhören) escuchar con atención"}),
    2344: (T + "word in example", {"t_es": "denso, tupido, hermético"}),
    2421: (T + "word in example", {"x_es": "Fue un proyecto de éxito"}),
    2422: (T + "word in example", {"x_es": "Como complemento de la ensalada hay pan recién hecho"}),
}

REPLACE = []
SPLIT_LATER = {}
