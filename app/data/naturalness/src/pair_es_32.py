"""Шаг 2, es, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    12181: (T + "word in example", {"t_es": "el cambio, la variedad, (zur Abwechslung) para variar"}),
    12235: (T + "word in example", {"x_es": "Los lunes no se puede jugar a los bolos"}),
    12662: (T + "word in example", {"t_es": "el desmayo, la impotencia, (in Ohnmacht fallen) desmayarse"}),
    12674: (T + "word in example", {"t_es": "el aliento, la respiración, (in einem Atemzug) de un trago"}),
}

REPLACE = []
SPLIT_LATER = {}
