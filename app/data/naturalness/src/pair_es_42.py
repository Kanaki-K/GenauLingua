"""Шаг 2, es, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    12839: (T + "no saques joroba — неестественно", {"x_es": "«¡Ponte recto, que te va a salir joroba!», dice mi madre cada vez que estoy con el portátil"}),
    13578: (T + "recogen dinero — калька", {"x_es": "En el mercadillo de pasteles los niños recaudan dinero a favor del viaje de fin de curso"}),
    14118: (T + "в примере conseguir", {"t_es": "mediar, transmitir, conseguir (a alguien)"}),
}

REPLACE = []
SPLIT_LATER = {}
