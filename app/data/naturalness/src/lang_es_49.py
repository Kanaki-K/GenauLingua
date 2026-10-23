"""Вычитка испанского, порция p049 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    16932: (T + '«Es necesaria una revisión» — канцелярит', {"example_es": 'El abogado pide la revisión del juicio'}),
    17315: (T + 'повтор 6493 «ve saliendo, te sigo»', {"example_es": 'Id saliendo, os seguimos en coche'}),
    17386: (T + '«a Berlín» — без нужды', {"example_es": 'Después de las vacaciones volvemos mañana en avión a Tenerife'}),
    17680: (T + 'повтор 17746 «detecta el movimiento y enciende la luz»', {"example_es": 'El sensor de lluvia enciende solo los limpiaparabrisas'}),
    17726: (T + 'учебниково', {"example_es": 'Este canal de televisión solo pone series'}),
}

REPLACE = []

SPLIT_LATER = {}
