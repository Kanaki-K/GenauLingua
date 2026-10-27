"""Шаг 2, es, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    6324: (T + "word in example", {"t_es": "fuera, afuera, (heraus!) ¡sal!"}),
    6421: (T + "word in example", {"t_es": "adelante, hacia delante, (vorwärts gehen) avanzar"}),
    7464: (T + "word in example", {"t_es": "el bien, el bienestar, (zum Wohl!) ¡salud!"}),
    10095: (T + "word in example", {"t_es": "ácido, agrio, enfadado"}),
    13315: (T + "word in example", {"t_es": "de eso, (die Hälfte davon) la mitad"}),
    13338: (T + "word in example", {"t_es": "en eso, (sich darauf freuen) tener ganas de que llegue"}),
    13810: (T + "word in example", {"t_es": "bueno, eh, y bien"}),
    14899: (T + "word in example", {"t_es": "el tipo, el chico, el tío (coloq.)"}),
}

REPLACE = []
SPLIT_LATER = {}
