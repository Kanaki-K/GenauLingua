"""Шаг 2, es, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    16398: (T + "в примере pasar factura", {"t_es": "el tributo, el precio, (seinen Tribut fordern) pasar factura"}),
    16430: (T + "в примере irse de rositas", {"t_es": "impunemente, (ungestraft davonkommen) irse de rositas"}),
    16559: (T + "в примере artillería pesada", {"t_es": "el cañón, la pieza de artillería, (schweres Geschütz) la artillería pesada"}),
}

REPLACE = []
SPLIT_LATER = {}
