"""Шаг 2, es, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    14318: (T + "word in example", {"x_es": "El portador de la carta espera una respuesta delante de la puerta"}),
    14539: (T + "word in example", {"x_es": "Sin el manuscrito delante no puedo dar un discurso, se me olvida todo"}),
    15066: (T + "word in example", {"t_es": "lésbico, lesbiana"}),
    15073: (T + "word in example", {"t_es": "la asociación, la colaboración, la relación de pareja"}),
    15101: (T + "word in example", {"t_es": "el conocido, la amistad, (eine Bekanntschaft machen) conocer a alguien"}),
}

REPLACE = []
SPLIT_LATER = {}
