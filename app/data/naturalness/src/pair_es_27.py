"""Шаг 2, es, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    7102: (T + "word in example", {"t_es": "corresponder, acercarse, (auf jdn. zukommen) venirse encima"}),
    7108: (T + "word in example", {"x_es": "La tienda concede un diez por ciento de descuento a los estudiantes"}),
    7145: (T + "word in example", {"t_es": "retroceder, ceder, apartarse"}),
    7147: (T + "word in example", {"t_es": "la vara, el palo, la barra"}),
    7176: (T + "word in example", {"t_es": "causar, lograr, (Wunder bewirken) hacer milagros"}),
    7196: (T + "word in example", {"x_es": "La pequeña cafetería une librería y barra de café"}),
    7213: (T + "word in example", {"x_es": "Eso le confiere a todo el asunto otro carácter"}),
    7436: (T + "word in example", {"t_es": "especial, especialmente"}),
}

REPLACE = []
SPLIT_LATER = {}
