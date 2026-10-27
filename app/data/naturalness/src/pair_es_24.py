"""Шаг 2, es, порция 24: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    15983: (T + "word in example", {"t_es": "la escena del crimen, el lugar del crimen"}),
    16025: (T + "word in example", {"t_es": "ilegal, ilegalmente"}),
    16086: (T + "word in example", {"t_es": "regio, real, (königlich behandeln) tratar a cuerpo de rey"}),
    16345: (T + "word in example", {"t_es": "ocupar, (einen Platz besetzen) guardar un sitio"}),
}

REPLACE = []
SPLIT_LATER = {}
