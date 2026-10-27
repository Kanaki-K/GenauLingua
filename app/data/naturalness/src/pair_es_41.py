"""Шаг 2, es, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    11147: (T + "в примере con afán", {"t_es": "afanoso, diligente, con afán"}),
    12792: (T + "le afectan a mi madre a la psique — коряво", {"x_es": "Tres semanas sin sol cada febrero afectan a la psique de mi madre"}),
    12809: (T + "planta de leucemia — калька", {"x_es": "En la carrera solidaria del colegio los niños recaudan dinero para la unidad de leucemia del hospital"}),
}

REPLACE = []
SPLIT_LATER = {}
