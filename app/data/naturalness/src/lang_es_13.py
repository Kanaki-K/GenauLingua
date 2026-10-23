"""Вычитка испанского, порция p013 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    2792: (T + 'нет слова карточки «cambiar»', {"example_es": '¡En la cuesta cambia de marcha!'}),
    2808: (T + '«Eso es obvio» — без ситуации', {"example_es": '¡Por supuesto que voy yo también!'}),
    2809: (T + 'нет слова карточки «enviar»', {"example_es": 'Te envío el archivo esta noche'}),
    2813: (T + '«Veo una serie» — учебниково', {"example_es": 'Estamos viendo una serie buenísima'}),
    2828: (T + 'нет слова карточки «la preocupación»', {"example_es": 'Las preocupaciones no le dejan dormir'}),
    2850: (T + '«Aquí apesta» — без ситуации', {"example_es": 'El queso apesta, pero está buenísimo'}),
    2884: (T + '«Ahora mismo es tendencia» — без ситуации', {"example_es": 'Hay una tendencia a trabajar cada vez más desde casa'}),
    2887: (T + 'повтор 1672 «el grifo gotea»', {"example_es": 'Del techo gotea agua'}),
    2898: (T + '«Me sorprendes» — без ситуации', {"example_es": 'Me has sorprendido con esta noticia'}),
    2906: (T + '«Esto es habitual aquí» — без ситуации', {"example_es": 'Aquí es habitual dejar propina'}),
    2944: (T + '«de Berlín» — без нужды', {"example_es": 'Los precios aquí son comparables a los de Madrid'}),
    2953: (T + 'повтор 18988 «te echo de menos»', {"example_es": '¿Echas de menos a tu familia?'}),
    2963: (T + 'повтор 2041 «no pierdas el tiempo»', {"example_es": '¡No desperdicies el agua!'}),
    2972: (T + 'нет слова карточки «la comprensión»', {"example_es": 'Gracias por su comprensión'}),
    2975: (T + 'повтор 2974 «infringir las normas»', {"example_es": 'Quien infringe la prohibición paga una multa'}),
    2999: (T + '«Transmite tanta calidez» — коряво', {"example_es": 'El calor de la chimenea es agradabilísimo'}),
    3003: (T + 'повтор 3059 «Mañana me voy / Vuelvo mañana»', {"example_es": '¿Cuándo os vais de vacaciones?'}),
    3006: (T + 'повтор 3005 «tirar»', {"example_es": 'Las cajas viejas las tiro'}),
    3059: (T + '«Vuelvo mañana» — оборвано', {"example_es": '¿Volvemos en tren o en coche?'}),
}

REPLACE = []

SPLIT_LATER = {}
