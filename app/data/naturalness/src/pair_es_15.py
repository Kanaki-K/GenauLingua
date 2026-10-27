"""Шаг 2, es, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    6859: (T + "word in example", {"x_es": "Ante los precios, ahora cocinamos más en casa"}),
    6873: (T + "word in example", {"t_es": "abajo, hacia abajo, (herunterkommen) bajar"}),
    6876: (T + "word in example", {"t_es": "abajo, hacia abajo, (hinuntergehen) bajar"}),
    6933: (T + "word in example", {"t_es": "notar, darse cuenta, fijarse"}),
    6952: (T + "word in example", {"t_es": "partir, ponerse en marcha, forzar"}),
    6989: (T + "word in example", {"t_es": "desinflado, pinchado, llano"}),
    6998: (T + "word in example", {"t_es": "registrar, comprender, captar"}),
    7001: (T + "word in example", {"t_es": "el apuro, el aprieto, la pinza"}),
    7005: (T + "word in example", {"t_es": "grosero, aproximado, (grob gerechnet) calculando por encima"}),
    7072: (T + "word in example", {"x_es": "Nuestro perro localiza cualquier golosina en el piso"}),
    7076: (T + "word in example", {"t_es": "torcido, inclinado, raro"}),
    7124: (T + "word in example", {"t_es": "original, inicial, originalmente"}),
    7291: (T + "word in example", {"t_es": "individual, suelto, individualmente"}),
    7456: (T + "word in example", {"t_es": "extraoficial, no oficial, extraoficialmente"}),
}

REPLACE = []
SPLIT_LATER = {}
