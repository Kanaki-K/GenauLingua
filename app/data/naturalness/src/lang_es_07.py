"""Вычитка испанского, порция p007 (A2/B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    18752: (T + 'повтор 2233 «dormir hasta tarde»', {"example_es": 'Los domingos comemos siempre en casa de los abuelos'}),
    17915: (T + '«tiene que examinarme» — калька', {"example_es": 'El médico me examinó con calma'}),
    18184: (T + 'повтор 681 «la habitación»', {"example_es": 'El domingo ordenamos el sótano'}),
    18216: (T + '«Cocino sopa en una olla» — учебниково', {"example_es": 'La olla es demasiado pequeña para toda la pasta'}),
    18248: (T + 'повтор 6483 «en el tercer piso»', {"example_es": '¿En qué piso vives?'}),
    18660: (T + '«Tengo que descansar» — оборвано', {"example_es": 'Después de comer el abuelo descansa una hora'}),
    18933: (T + 'повтор 995 «Por la mañana trabajo»', {"example_es": 'Por las mañanas trabajamos y por las tardes estudiamos'}),
    18967: (T + 'повтор «la farmacia»', {"example_es": 'La tienda está cerrada los domingos, tenemos que esperar hasta el lunes'}),
    18969: (T + '«los Müller» — не испанская фамилия', {"example_es": '¿Conoces a los Ruiz? Su hijo va a la misma clase que el nuestro'}),
    18988: (T + '«en Berlín» — без нужды', {"example_es": 'Desde que vives en Londres, te echo mucho de menos'}),
    44: (T + '«Trabaja en el despacho» — учебниково', {"example_es": 'He convertido la habitación de invitados en un despacho'}),
    85: (T + '«Tomo café en una taza» — тавтология', {"example_es": 'A los niños les doy vasos de plástico'}),
    152: (T + 'повтор 8759 «hoy no está»', {"example_es": 'El jefe me ha dado el viernes libre'}),
    231: (T + '«estoy cogiendo un resfriado» — без ситуации', {"example_es": 'Creo que he pillado un resfriado'}),
    241: (T + 'повтор 10 «¿Cuál es … dirección?»', {"example_es": 'Vuestro piso es precioso'}),
    333: (T + '«Está divorciada» — без ситуации', {"example_es": 'Mis padres están divorciados desde hace años'}),
    412: (T + '«Como pan con miel» — учебниково', {"example_es": '¿Una cucharadita de miel en el té?'}),
    477: (T + '«Pesa dos kilos» — без ситуации', {"example_es": 'Un kilo de manzanas, por favor'}),
    485: (T + 'нет слова карточки «los trapos»', {"example_es": 'Coge tus trapos y vámonos'}),
    496: (T + 'повтор 8792 «es cocinero»', {"example_es": 'El cocinero del restaurante es de Galicia'}),
    510: (T + '«Está en el hospital» — без ситуации', {"example_es": 'El abuelo lleva una semana en el hospital'}),
    579: (T + '«Necesito harina para hornear» — калька', {"example_es": 'Para la pizza hace falta medio kilo de harina'}),
    611: (T + '«La luna brilla con fuerza» — книжно', {"example_es": 'Esta noche hay luna llena'}),
    636: (T + 'повтор 253 «¿Cuál es tu apellido?»', {"example_es": 'El apellido se escribe con dos eles'}),
    700: (T + 'повтор 717 «¿Hay … libre aquí?»', {"example_es": 'El aparcamiento de debajo de casa siempre está lleno'}),
    708: (T + '«Se pone una tirita» — учебниково', {"example_es": 'Ponte una tirita en la ampolla'}),
    711: (T + '«Recoge setas» — учебниково', {"example_es": 'En otoño vamos a buscar setas'}),
    750: (T + 'повтор 49 «El libro está en…»', {"example_es": 'La estantería está llena de periódicos viejos'}),
}

REPLACE = []

SPLIT_LATER = {}
