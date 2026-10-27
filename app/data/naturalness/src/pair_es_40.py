"""Шаг 2, es, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    9887: (T + "в примере no se compra", {"t_es": "en venta, sobornable, (nicht käuflich) no se compra"}),
    10921: (T + "в примере con cinismo", {"t_es": "cínico, con cinismo"}),
    11012: (T + "в примере hostilidad, слово hostil", {"x_es": "Nuestra gata está muy hostil con el cachorro nuevo y bufa cuando se acerca demasiado"}),
    11027: (T + "se desea disfraz — калька", {"t_es": "deseado, bienvenido, (… erwünscht) se ruega", "x_es": "En la invitación pone «se ruega venir disfrazado», y mi marido lleva desde ayer buscando su sombrero de pirata"}),
}

REPLACE = []
SPLIT_LATER = {}
