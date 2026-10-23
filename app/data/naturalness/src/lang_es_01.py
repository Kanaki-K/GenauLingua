"""Вычитка испанского, порция p001 (A1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    41: (T + 'повтор «va al trabajo» (62, 72)', {"example_es": 'Me encanta mi trabajo'}),
    62: (T + 'повтор «va al trabajo en…» (72)', {"example_es": 'He dejado el coche delante de casa'}),
    103: (T + '«Seguro que viene» — без ситуации', {"example_es": 'Seguro que llega tarde'}),
    105: (T + '«Visitamos a la abuela» — учебниково', {"example_es": 'Este fin de semana visitamos a la abuela'}),
    113: (T + '«Se toma una cerveza» — без ситуации', {"example_es": '¿Nos tomamos una cerveza?'}),
    117: (T + '«La pera está dulce» — учебниково', {"example_es": '¡Qué dulce está esta pera!'}),
    127: (T + '«Compra una flor roja» — учебниково', {"example_es": '¡Qué flor tan bonita!'}),
    137: (T + '«Me trae flores» — без ситуации', {"example_es": '¿Me traes el cargador?'}),
    141: (T + '«Comen panecillos» — повтор «desayuno» (138)', {"example_es": '¿Me compras unos panecillos?'}),
    144: (T + '«Voy en autobús» — оборвано', {"example_es": 'Voy al colegio en autobús'}),
    160: (T + 'повтор 402 «Estoy aquí / Está aquí»', {"example_es": 'Tu móvil está ahí, en la mesa'}),
    163: (T + 'нет слова карточки «el agradecimiento»', {"example_es": 'Un pequeño regalo en agradecimiento'}),
    167: (T + 'повтор 305 «Está bien»', {"example_es": 'Este es mi sitio'}),
    189: (T + '«La escuela está allí» — учебниково', {"example_es": 'El aparcamiento está allí, detrás del súper'}),
    211: (T + '«Te invito» — оборвано', {"example_es": '¡Esta noche invito yo!'}),
    238: (T + '«Comemos a las doce» — учебниково', {"example_es": '¿A qué hora comemos?'}),
    244: (T + '«Vamos a Berlín» — без ситуации', {"example_es": 'Mañana vamos a la playa en coche'}),
    248: (T + 'повтор «va en…» (62, 72)', {"example_es": 'Mi hija va al colegio en bici'}),
    267: (T + '«La comida está lista» — повтор 11635', {"example_es": '¿Estás listo? Nos vamos'}),
    274: (T + '«Me gusta comer pescado» — учебниково', {"example_es": 'Los viernes comemos pescado'}),
    278: (T + '«Vamos al aeropuerto» — учебниково', {"example_es": 'Te llevo al aeropuerto'}),
    286: (T + 'нет слова карточки «la mujer / la esposa»', {"example_es": 'Mi mujer trabaja en un hospital'}),
    305: (T + 'повтор 167 «Está bien»', {"example_es": 'La casa es bastante grande para todos'}),
    307: (T + '«Trabaja en el jardín» — учебниково', {"example_es": 'El abuelo trabaja en el jardín todo el día'}),
    315: (T + '«Müller» — не испанская фамилия', {"example_es": 'Estimada señora García'}),
    323: (T + '«Compra verdura fresca» — учебниково', {"example_es": 'La verdura la compro en el mercado'}),
    328: (T + 'без ситуации', {"example_es": 'Justo ahora estoy saliendo'}),
    330: (T + '«Me gusta tomar té» — нет слова «con gusto»', {"example_es": '¿Vienes con nosotros? – ¡Con mucho gusto!'}),
    348: (T + '«Es muy feliz» — без ситуации', {"example_es": 'Se la ve muy feliz con su nuevo trabajo'}),
    374: (T + '«El autobús para en la parada» — тавтология', {"example_es": 'Sostén un momento el bolso, por favor'}),
    376: (T + '«Me da la mano» — без ситуации', {"example_es": 'Dame la mano, que cruzamos'}),
    400: (T + '«Müller» — не испанская фамилия', {"example_es": 'Buenas tardes, señor García, pase, por favor'}),
    402: (T + 'повтор 160', {"example_es": '¡Ven aquí!'}),
    406: (T + '«Está sentado atrás» — без ситуации', {"example_es": 'En el coche los niños van atrás'}),
    415: (T + '«El perro es muy bonito» — учебниково', {"example_es": 'Nuestro perro se llama Leo'}),
    428: (T + 'повтор 426 «Esta es su…»', {"example_es": 'Los niños juegan con sus amigos'}),
    431: (T + 'повтор 338 «en la ciudad»', {"example_es": 'Vivo en España desde hace dos años'}),
    456: (T + 'повтор 429 «tomo café por la mañana»', {"example_es": '¿Nos tomamos un café?'}),
    467: (T + '«Compro pan» — учебниково', {"example_es": '¿Dónde compras el pan?'}),
    481: (T + '«Vamos al cine» — учебниково', {"example_es": 'Esta noche ponen una buena película en el cine'}),
    500: (T + 'повтор 165 «a las tres»', {"example_es": '¿Viene también tu hermana?'}),
    509: (T + '«Está enferma» — без ситуации', {"example_es": 'Hoy mi hija está enferma y se queda en casa'}),
}

REPLACE = []

SPLIT_LATER = {}
