"""Вычитка испанского, порция p012 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    2448: (T + '«No es justo» — оборвано', {"example_es": '¡No es justo, me toca a mí!'}),
    2461: (T + '«en Hamburgo» — без нужды', {"example_es": 'Una vez al mes tengo que ir a la sede de la empresa en Barcelona'}),
    2490: (T + 'нет слова карточки «la frustración»', {"example_es": 'De la frustración se comió todo el chocolate'}),
    2497: (T + 'повтор 1011 «al fondo del pasillo»', {"example_es": 'En el avión prefiero el asiento de pasillo'}),
    2508: (T + '«El rival es fuerte» — учебниково', {"example_es": 'Mañana jugamos contra un rival fortísimo'}),
    2586: (T + 'повтор 13392 «… a la puerta»', {"example_es": '¿Hay alguien que hable inglés?'}),
    2618: (T + '«Me gusta ver comedias» — учебниково', {"example_es": '¿Vemos una comedia esta noche?'}),
    2620: (T + '«Tenemos que resolver el conflicto» — книжно', {"example_es": 'Entre los dos hermanos siempre hay conflicto'}),
    2626: (T + '«Es correcto» — оборвано', {"example_es": 'La respuesta es correcta'}),
    2658: (T + '«Conduzco el coche por la ciudad» — учебниково', {"example_es": 'Él conduce y yo leo el mapa'}),
}

REPLACE = []

SPLIT_LATER = {}
