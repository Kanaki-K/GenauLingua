"""Шаг 2, es, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    10565: (T + "natural", {"x_es": "Esta guitarra nueva es muy guay"}),
    10595: (T + "word in example", {"t_es": "responder de, ser responsabilidad de"}),
    10693: (T + "word in example", {"x_es": "El médico se muestra confiado en que el abuelo podrá volver a andar después de la operación"}),
    10734: (T + "word in example", {"t_es": "cariñoso, cariñosamente"}),
}

REPLACE = []
SPLIT_LATER = {}
