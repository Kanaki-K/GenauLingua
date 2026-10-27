"""Шаг 2, es, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    16793: (T + "нет pensión alimenticia", {"x_es": "Desde el divorcio mi exmarido paga siempre puntualmente la pensión alimenticia de los niños"}),
    16858: (T + "в примере Hacienda", {"t_es": "el fisco, la administración tributaria, Hacienda"}),
    16941: (T + "в примере colar", {"t_es": "infiltrar, introducir clandestinamente, colar"}),
    18038: (T + "la casa parece un vacío — неестественно", {"x_es": "Desde que los niños se fueron, en casa hay un vacío enorme"}),
}

REPLACE = []
SPLIT_LATER = {}
