"""Вычитка испанского, порция p015 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    6833: (T + '«Repasemos otra vez» — книжно', {"example_es": 'Repasamos la lista una última vez'}),
    6872: (T + '«Volvemos a montar» — без ситуации', {"example_es": '¿Montamos la tienda aquí?'}),
    6876: (T + '«Vamos escaleras abajo» — коряво', {"example_es": '¡No mires hacia abajo!'}),
    6889: (T + '«cada detalle» — калька', {"example_es": 'Cuéntamelo todo con todo detalle'}),
    6890: (T + '«me es totalmente desconocida» — книжно', {"example_es": 'El número es desconocido, no lo cojo'}),
    6924: (T + '«totalmente improbable» — калька', {"example_es": 'Es muy poco probable'}),
    6925: (T + '«prácticamente una garantía» — коряво', {"example_es": 'Ya casi he terminado'}),
    6927: (T + '«sustituto del té» — неживо', {"example_es": 'Siempre llevo una batería de repuesto'}),
    6931: (T + 'без ситуации', {"example_es": 'Su jefe lo trasladó a Valencia'}),
    6950: (T + 'повтор 6952 «mañana … partimos»', {"example_es": 'Mañana temprano nos ponemos en camino'}),
    6952: (T + 'повтор 6950', {"example_es": '¿A qué hora partimos?'}),
    6969: (T + '«de que no viene» — коряво', {"example_es": 'Me he dado cuenta de que faltaban veinte euros en la cartera'}),
    6970: (T + '«El billete vale todo el día» — без нужды; нет слова «considerarse»', {"example_es": 'El descuento vale también para los niños'}),
    6994: (T + '«El nudo de mi cuerda» — неживо', {"example_es": 'No consigo deshacer este nudo'}),
    7005: (T + '«aproximadamente» — без слова карточки', {"example_es": 'Es solo un cálculo aproximado'}),
    7032: (T + '«Marchamos por el bosque» — не то значение', {"example_es": 'El 12 de octubre los soldados desfilan por Madrid'}),
    7053: (T + '«Ten preparado un taxi» — калька', {"example_es": 'Ten el móvil a mano, que te llamo'}),
    7061: (T + '«impuestos incluidos» — канцелярит', {"example_es": 'Son 50 euros, envío incluido'}),
    7091: (T + '«¿Has mirado mi mensaje?» — калька', {"example_es": 'Espera, que miro un momento el correo'}),
    7116: (T + 'повтор 6743 «guardar las distancias»', {"example_es": 'Hemos recorrido una gran distancia en bici'}),
    7140: (T + '«Solo sacude la cabeza» — калька', {"example_es": 'Sacude la cabeza sin decir nada'}),
    7190: (T + '«Queremos continuar» — калька', {"example_es": '¿Seguimos la conversación mañana?'}),
    7313: (T + 'нет слова карточки «mundial»', {"example_es": 'El calentamiento global es un problema mundial'}),
    7315: (T + '«de conocimiento general» — канцелярит', {"example_es": 'En general estoy contento con mi trabajo'}),
    7611: (T + 'нет прямого смысла «cuesta abajo»', {"example_es": 'Cuesta abajo la bici va sola'}),
    7715: (T + '«está sentada junta» — калька', {"example_es": 'Los domingos estamos todos juntos a la mesa'}),
}

REPLACE = []

SPLIT_LATER = {}
