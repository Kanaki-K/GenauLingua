"""Шаг 2, es, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    8663: (T + "в примере a fondo", {"t_es": "detallado, exhaustivo, a fondo"}),
    11316: (T + "в примере con malicia", {"t_es": "malicioso, burlón, con malicia"}),
    11377: (T + "в примере una idiotez", {"t_es": "idiota, estúpido, una idiotez"}),
    11449: (T + "нет devoto", {"x_es": "Nuestro perro me es totalmente devoto y me sigue a todas partes, hasta al baño"}),
    11486: (T + "нет triunfar", {"x_es": "Mi hijo triunfa: por primera vez le ha ganado al abuelo al ajedrez"}),
}

REPLACE = []
SPLIT_LATER = {}
