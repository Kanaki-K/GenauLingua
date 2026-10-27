"""Шаг 2, es, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    6370: (T + "word in example", {"x_es": "Eso es evidentemente falso"}),
    6383: (T + "word in example", {"t_es": "sobrante, restante, (übrig sein) quedar"}),
    6398: (T + "word in example", {"t_es": "ser correcto, cuadrar, votar"}),
    6418: (T + "word in example", {"t_es": "comprender, agarrar, (nicht fassen können) no poder creer"}),
    6486: (T + "word in example", {"t_es": "montar guardia, vigilar, velar"}),
    6506: (T + "word in example", {"t_es": "el esfuerzo, la molestia, (sich Mühe geben) esforzarse"}),
    6519: (T + "word in example", {"t_es": "el refugio, la cobertura, (in Deckung gehen) ponerse a cubierto"}),
    6600: (T + "word in example", {"x_es": "Después del cine los amigos se separaron"}),
    6622: (T + "word in example", {"t_es": "en su lugar, en cambio, en vez de eso"}),
    6645: (T + "word in example", {"t_es": "central, principal, céntrico"}),
    6706: (T + "word in example", {"t_es": "poco común, raro, inusual"}),
    6761: (T + "word in example", {"t_es": "implicado, enredado, envuelto"}),
    6784: (T + "word in example", {"t_es": "emplear, usar, poner (en servicio)"}),
    6813: (T + "word in example", {"t_es": "transmitir, contagiar, transferir"}),
}

REPLACE = []
SPLIT_LATER = {}
