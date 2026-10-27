"""Шаг 2, es, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    9050: (T + "word in example", {"x_es": "Además de su trabajo, tiene otra actividad: da clases de guitarra"}),
    9823: (T + "word in example", {"x_es": "Con los ingresos del mercadillo la clase se va de colonias"}),
    9941: (T + "word in example", {"x_es": "Compro casi todos los días en la tienda de alimentación de la esquina"}),
}

REPLACE = []
SPLIT_LATER = {}
