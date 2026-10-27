"""Шаг 2, es, порция 37: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    17196: (T + "por sus cincuenta años — неестественно", {"x_es": "Por su cincuenta cumpleaños mi padre saltó por primera vez en paracaídas"}),
    17305: (T + "в примере regreso", {"t_es": "el vuelo de vuelta, el vuelo de regreso"}),
    17719: (T + "в примере petróleo", {"t_es": "el queroseno, el petróleo"}),
    17870: (T + "como seguridad — калька", {"x_es": "Para tener seguridad en la jubilación mi madre ahorra cada mes un poco de dinero en una cuenta aparte"}),
    18034: (T + "в примере ciencia forense", {"t_es": "la ciencia forense, la policía científica"}),
    18208: (T + "veranda в испанском редко", {"x_es": "Por la tarde nos gusta sentarnos en el porche a tomar té"}),
    18243: (T + "пример про Boulevardpresse", {"t_es": "el bulevar, (die Boulevardpresse) la prensa amarilla"}),
}

REPLACE = []
SPLIT_LATER = {}
