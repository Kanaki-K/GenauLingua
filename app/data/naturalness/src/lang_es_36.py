"""Вычитка испанского, порция p036 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    16320: (T + 'повтор 15424 «el jardín como su territorio»', {"example_es": 'Los lobos defienden su territorio'}),
    16855: (T + '«a Múnich … Bayern» — оставить смысл', {"example_es": 'Desde que mi hermano se mudó a Barcelona, para nuestra familia es un desertor y anima al Barça'}),
    16956: (T + '«de Berlín» — без нужды', {"example_es": 'Mi madre va a la gran reunión de Madrid como delegada de la asociación de huertos'}),
    17146: (T + '«Mi salida es» — калька', {"example_es": 'La salida está prevista mañana a las siete'}),
    17153: (T + 'без ситуации', {"example_es": 'En el camino de vuelta paramos a comer'}),
}

REPLACE = []

SPLIT_LATER = {}
