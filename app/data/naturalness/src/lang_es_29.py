"""Вычитка испанского, порция p029 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    8886: (T + '«hizo las nuevas canciones» — коряво', {"example_es": 'El productor del grupo también es su mánager'}),
    8909: (T + 'нет слова карточки «activo»', {"example_es": 'A los ochenta sigue activísima'}),
    8951: (T + 'повтор 8877 «viene todos los …»', {"example_es": 'Compartimos una señora de la limpieza con los vecinos'}),
    8954: (T + '«Otra vez tengo que» — калька', {"example_es": 'El trabajo sucio siempre me toca a mí'}),
    9210: (T + '«en Hamburgo» — без нужды', {"example_es": 'Mi marido está esta semana en Bilbao por trabajo, así que llevo yo sola a los niños al colegio'}),
    10391: (T + '«Mi amado y yo nos vamos» — книжно', {"example_es": 'Espera el regreso de su amado'}),
}

REPLACE = []

SPLIT_LATER = {}
