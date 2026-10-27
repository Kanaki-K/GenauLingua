"""Шаг 2, es, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    13077: (T + "word in example", {"x_es": "Después de la operación de cadera mi abuelo llevó un catéter tres días y se quejó a todo el mundo"}),
    13517: (T + "word in example", {"t_es": "en este caso, para ello"}),
    13673: (T + "word in example", {"t_es": "las braguitas, el calzoncito"}),
    14009: (T + "word in example", {"t_es": "dependiente, (angewiesen sein auf) depender de"}),
    14029: (T + "word in example", {"x_es": "¿Quién le transmite la mala noticia?"}),
    14120: (T + "word in example", {"t_es": "las palabras claras, (Klartext reden) hablar claro"}),
}

REPLACE = []
SPLIT_LATER = {}
