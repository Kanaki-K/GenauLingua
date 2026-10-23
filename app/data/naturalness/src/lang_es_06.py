"""Вычитка испанского, порция p006 (A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    6326: (T + '«Es demasiado peligroso» — без ситуации', {"example_es": '¡No te asomes, es peligroso!'}),
    6585: (T + 'повтор «las llaves»', {"example_es": '¿Dónde has escondido los regalos?'}),
    6646: (T + '«Tengo que aprobar el examen» — учебниково', {"example_es": 'Aprobó el examen a la primera'}),
    6726: (T + 'повтор «las llaves»', {"example_es": 'No lo encuentro por ningún lado'}),
    7057: (T + '«en Colonia» — без нужды', {"example_es": 'Mi marido está esta semana en una feria en Bilbao'}),
    7464: (T + 'нет слова карточки «el bien»', {"example_es": 'Lo hago por tu bien'}),
    7711: (T + '«Apúntate» — не то значение', {"example_es": 'Anota tu nombre en la lista'}),
    8818: (T + 'повтор «la cuenta»', {"example_es": 'El camarero fue amabilísimo'}),
    8868: (T + '«trabaja en la misma oficina» — учебниково', {"example_es": 'Mi compañera me sustituye cuando estoy enfermo'}),
    8994: (T + 'повтор 8980 «solicitud»', {"example_es": '¿Has solicitado ese puesto?'}),
    9460: (T + 'повтор 126 «¿Tienes un lápiz?»', {"example_es": 'Este bolígrafo ya no escribe'}),
    9591: (T + '«simpáticos y serviciales» — книжно', {"example_es": 'Me llevo genial con mis compañeros de clase'}),
    10036: (T + '«con gusto» — оставить, но без ситуации', {"example_es": '¿Me ayudas? – ¡Con mucho gusto!'}),
    10064: (T + '«Sé cuidadoso» — оборвано', {"example_es": 'Ten cuidado, la carretera está helada'}),
    10073: (T + 'повтор 13335 «No me acuerdo»', {"example_es": '¿Te acuerdas de mí?'}),
    10077: (T + '«Eso sí que es raro» — без ситуации', {"example_es": '¡Qué raro, la puerta está abierta!'}),
    10091: (T + '«Estoy enamorado» — повтор 2040', {"example_es": 'Está enamoradísima de él'}),
    10102: (T + 'повтор «divertido» (562)', {"example_es": 'Tu padre es muy gracioso'}),
    10129: (T + 'нет слова карточки «el interés»', {"example_es": 'No tengo ningún interés en el fútbol'}),
    11772: (T + 'повтор 599 «en el comedor»', {"example_es": 'La cafetería de la universidad siempre está llena'}),
    12108: (T + '«Esta noche salgo» — оборвано', {"example_es": 'Los sábados por la noche salgo con los amigos'}),
    12140: (T + '«En el circo hay muchos animales» — учебниково', {"example_es": 'Los niños quieren ir al circo'}),
    12142: (T + 'повтор 1934 «Nuestro equipo ha ganado»', {"example_es": 'El equipo entrena tres veces por semana'}),
    12474: (T + '«Todavía estoy despierto» — без ситуации', {"example_es": '¿Sigues despierto?'}),
    12477: (T + '«Hubo un accidente» — оборвано', {"example_es": 'Ha habido un accidente en la autopista'}),
    12529: (T + 'повтор 199 «ducha rápida»', {"example_es": 'Los niños nunca quieren ducharse'}),
    12620: (T + '«Tu perfume huele bien» — тавтология', {"example_es": '¡Qué bien hueles! ¿Qué perfume es?'}),
    13295: (T + 'повтор «¿Es tuyo…?» (171)', {"example_es": 'Tu tren sale dentro de diez minutos'}),
    13338: (T + '«Me hace mucha ilusión» — нет слова «en eso»', {"example_es": 'Puedes contar con eso'}),
    13430: (T + 'повтор 1326 «Llueve, por eso»', {"example_es": 'El tren va con retraso, por eso cojo un taxi'}),
    13447: (T + '«Un millón es mucho dinero» — учебниково', {"example_es": 'Si ganara un millón, dejaría de trabajar'}),
    13843: (T + '«Tu voz es bonita» — калька', {"example_es": '¡Tienes una voz preciosa!'}),
    13853: (T + '«Es un buen chiste» — калька', {"example_es": '¡Cuéntame un chiste!'}),
    13901: (T + 'повтор 945 «Adiós, hasta mañana»', {"example_es": '¡Chao, hasta pronto!'}),
    14923: (T + 'повтор «pasteles riquísimos» (904)', {"example_es": 'Mi tía vive en el campo'}),
    14944: (T + '«Mi hermano ya es adulto» — учебниково', {"example_es": 'Ya eres mayor, decide tú'}),
    14979: (T + '«Crecí aquí» — без ситуации', {"example_es": 'Me crié en Sevilla'}),
    15394: (T + '«El pájaro canta en el árbol» — учебниково', {"example_es": 'Un pájaro ha hecho el nido en el balcón'}),
    15926: (T + '«El rey lleva una corona» — учебниково', {"example_es": 'El rey de España está de visita en Roma'}),
    17483: (T + 'повтор 8448 «Échale un vistazo»', {"example_es": 'He grabado un vídeo del concierto'}),
}

REPLACE = []

SPLIT_LATER = {}
