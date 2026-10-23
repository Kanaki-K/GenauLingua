"""Вычитка испанского, порция p003 (A1/A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    826: (T + 'повтор «hace calor» — уже есть 454', {"example_es": 'Me gusta mucho esta canción'}),
    1426: (T + '«Volamos a España» — учебниково', {"example_es": 'Mañana volamos a Barcelona'}),
    1441: (T + '«En mi tiempo libre» — калька', {"example_es": 'En el tiempo libre leo mucho'}),
    1458: (T + '«Mi lugar de nacimiento es Berlín» — канцелярит', {"example_es": 'En el formulario pon también el lugar de nacimiento'}),
    1463: (T + '«El libro me pertenece» — книжно', {"example_es": '¿De quién es este bolso? – Pertenece a mi hermana'}),
    1589: (T + 'нет слова карточки «la clase»', {"example_es": 'En clase somos veinticinco'}),
    1695: (T + '«Me apunto encantado» — без ситуации', {"example_es": '¿Quién quiere participar en la carrera?'}),
    1739: (T + 'повтор 1542 «estantería … alta»', {"example_es": 'Las mantas están arriba'}),
    2007: (T + '«Espero abajo» — оборвано', {"example_es": 'Te espero abajo, en el portal'}),
    2109: (T + 'повтор 1032 «Hace un tiempo…»', {"example_es": '¡Qué día tan maravilloso!'}),
    2354: (T + '«Reservo una habitación doble» — учебниково', {"example_es": 'Quería una habitación doble para dos noches'}),
    2453: (T + '«Mándame un fax» — устарело', {"example_es": '¿Quién usa todavía el fax?'}),
    6228: (T + '«Está muy lejos» — без ситуации', {"example_es": '¿La estación está lejos de aquí?'}),
    6250: (T + 'повтор 6292 «La bolsa es…»', {"example_es": 'El examen fue más difícil de lo previsto'}),
    6252: (T + '«Mira aquí» — без ситуации', {"example_es": '¡Mira, está nevando!'}),
    6483: (T + 'повтор 68 «en el segundo piso»', {"example_es": 'La oficina está en la tercera planta'}),
    8334: (T + 'нет слова карточки «completar»', {"example_es": 'Completa las frases con las palabras correctas'}),
    8735: (T + 'повтор 41 «me gusta mi trabajo»', {"example_es": '¡He encontrado un trabajo nuevo!'}),
    8797: (T + '«me ayuda en el trabajo» — учебниково', {"example_es": 'Mi compañero hoy está de vacaciones'}),
    9441: (T + 'повтор 8742 «Mi … es simpático»', {"example_es": 'La maestra de mi hija es jovencísima'}),
    10438: (T + '«Te felicito por tu éxito» — книжно', {"example_es": '¡Te felicito por el ascenso!'}),
    12121: (T + 'повтор 2176 «El comienzo … difícil»', {"example_es": 'En la salida de la carrera había cien corredores'}),
    13282: (T + 'повтор 13331 «al médico»', {"example_es": 'Voy al mar con los amigos'}),
    13293: (T + '«Estoy en la estación» — учебниково', {"example_es": 'Quedamos en el bar a las seis'}),
    13314: (T + 'повтор 13331 «del médico»', {"example_es": 'Vuelvo ahora del trabajo'}),
    13375: (T + 'повтор «Tengo … años»', {"example_es": 'Tengo diez minutos de descanso'}),
    13387: (T + 'повтор 52 «Me levanto a las…»', {"example_es": 'Trabajo ocho horas al día'}),
    13392: (T + 'повтор «la llave»', {"example_es": '¿Alguien quiere un café?'}),
    13498: (T + 'повтор «Tengo … años»', {"example_es": 'Nos vemos dentro de veinte minutos'}),
    13968: (T + 'повтор «Hasta luego»', {"example_es": 'Gracias por la llamada, ¡hasta luego!'}),
    14913: (T + 'повтор 8742 «Mi … es muy amable»', {"example_es": 'Mi pareja cocina de maravilla'}),
    15183: (T + '«Es soltero» — без ситуации', {"example_es": 'Sigue soltero a los cuarenta'}),
    17202: (T + 'повтор 1211 «el tren … vía tres»', {"example_es": 'Perdone, ¿es esta la vía para Madrid?'}),
    17250: (T + '«Visitamos el piso nuevo» — учебниково', {"example_es": 'Mañana visitamos la Alhambra'}),
    17342: (T + 'повтор 17335 «los monumentos»', {"example_es": 'La guía turística hablaba también español'}),
    17489: (T + '«Repara el coche» — учебниково', {"example_es": 'Mi padre lo arregla todo él solo'}),
    18610: (T + 'повтор 595 «Espera un minuto»', {"example_es": '¡Un segundo, ya voy!'}),
}

REPLACE = []

SPLIT_LATER = {}
