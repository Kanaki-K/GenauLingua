"""Вычитка испанского, порция p037 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    17557: (T + '«Tengo que empujar» — калька', {"example_es": 'Empuja la palanca hacia la izquierda'}),
    17958: (T + 'повтор 17956 «los científicos»', {"example_es": 'Me encanta explorar las callejuelas de las ciudades que visito'}),
    18183: (T + '«un cuchitril totalmente caótico» — не тот смысл', {"example_es": 'Alquila un cuchitril cerca de la universidad'}),
    18217: (T + 'повтор 18385 «cambiar las sábanas»', {"example_es": 'Las sábanas se están secando en el balcón'}),
    18235: (T + 'повтор 6519 «refugio de la lluvia»', {"example_es": 'La cabaña del fondo del jardín es nuestro escondite'}),
}

REPLACE = []

SPLIT_LATER = {}
