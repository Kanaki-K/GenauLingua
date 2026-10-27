"""Шаг 2, es, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    2792: (T + "word in example", {"t_es": "cambiar, encender, poner"}),
    2824: (T + "word in example", {"t_es": "el sol, la luz del sol, (fig.) el rayito de sol"}),
    2828: (T + "word in example", {"t_es": "la preocupación, (keine Sorge) no te preocupes"}),
    2872: (T + "word in example", {"t_es": "la división, el reparto"}),
    2922: (T + "word in example", {"x_es": "En el coche los niños siempre están impacientes"}),
    2925: (T + "word in example", {"t_es": "innecesario, innecesariamente"}),
}

REPLACE = []
SPLIT_LATER = {}
