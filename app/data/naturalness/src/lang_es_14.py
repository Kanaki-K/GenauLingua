"""Вычитка испанского, порция p014 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    3067: (T + '«es armoniosa» — книжно', {"example_es": 'La convivencia con mi suegra no siempre es fácil'}),
    13392: (T + 'повтор 6505 «llaman a la puerta»', {"example_es": '¿Alguien quiere un café?'}),
    6369: (T + 'нет слова карточки «alejado»', {"example_es": 'La estación no está muy alejada, a diez minutos a pie'}),
    6383: (T + 'нет слова карточки «sobrante»', {"example_es": 'Hay un trozo de pastel sobrante, ¿lo quieres?'}),
    6415: (T + '«Lo aprecio mucho» — оборвано', {"example_es": 'Aprecio mucho tu ayuda'}),
    6418: (T + '«No puedo comprenderlo» — книжно', {"example_es": 'Me cuesta comprender lo que quiere decir'}),
    6427: (T + 'нет слова карточки «encantado»', {"example_es": 'Mi madre está encantada con tu tarta'}),
    6481: (T + '«un carácter amable» — калька', {"example_es": 'Ayudar a los demás está en su carácter'}),
    6486: (T + 'нет слова карточки «montar guardia»', {"example_es": 'El perro monta guardia delante de la casa'}),
    6520: (T + '«Sigamos sin más» — коряво', {"example_es": '¡Venga, seguimos!'}),
    6541: (T + 'нет слова карточки «largarse»', {"example_es": '¡Venga, nos largamos!'}),
    6572: (T + 'без ситуации', {"example_es": '¡Agárrate bien, que va a botar!'}),
    6583: (T + '«se visitan mutuamente» — калька', {"example_es": 'El respeto tiene que ser mutuo'}),
    6599: (T + '«salta arriba y abajo» — не то значение', {"example_es": 'El viento ha tirado al suelo el árbol viejo'}),
    6610: (T + 'без ситуации', {"example_es": 'Te advierto que pica mucho'}),
    6621: (T + 'нет слова карточки «algún»', {"example_es": '¿Te suena de algún sitio?'}),
    6638: (T + '«me da mucha alegría» — калька', {"example_es": 'Este trabajo me da muchas satisfacciones'}),
    6707: (T + 'нет слова карточки «enorme»', {"example_es": 'Anoche hubo una tormenta enorme'}),
    6710: (T + '«todo ese rollo» — коряво', {"example_es": '¡Cuántos trastos llevas en el coche!'}),
    6727: (T + 'повтор «la llave»', {"example_es": 'He registrado todo el piso buscando el pasaporte'}),
    6730: (T + '«a Berlín» — без нужды', {"example_es": 'Nos estamos acercando a Toledo, en diez minutos llegamos'}),
    6743: (T + '«un metro de distancia conmigo» — коряво', {"example_es": 'Guarda la distancia con ese perro'}),
    6784: (T + 'нет слова карточки «emplear»', {"example_es": 'Para buscar a los excursionistas perdidos emplean drones'}),
    6600: (T + 'нет слова карточки «separados»', {"example_es": 'Después del cine volvimos a casa separados'}),
    6813: (T + 'нет слова карточки «transmitir»', {"example_es": 'El partido se transmite en directo esta noche'}),
    6819: (T + 'нет слова карточки «incluido»', {"example_es": 'El desayuno está incluido en el precio'}),
}

REPLACE = []

SPLIT_LATER = {}
