"""Шаг 2, es, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    98: (T + "word in example", {"t_es": "la respuesta, (Bescheid sagen) avisar"}),
    393: (T + "word in example", {"t_es": "caliente, (es ist heiß) hacer calor"}),
    858: (T + "word in example", {"t_es": "la diversión, (Spaß machen) ser divertido"}),
    993: (T + "word in example", {"t_es": "de largo, terminado, acabado"}),
    1003: (T + "word in example", {"t_es": "cálido, templado, calentito"}),
    1064: (T + "word in example", {"x_es": "¿Qué deseas por tu cumpleaños?"}),
}

REPLACE = []
SPLIT_LATER = {}
