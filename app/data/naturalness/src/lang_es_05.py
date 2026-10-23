"""Вычитка испанского, порция p005 (A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    1222: (T + '«Me gusta jugar» — учебниково', {"example_es": 'Mi hijo juega al baloncesto en el equipo del colegio'}),
    1228: (T + 'повтор 1317 «darte las gracias»', {"example_es": 'Quiero dar las gracias a todos'}),
    1235: (T + '«¿Puede justificarlo?» — без ситуации', {"example_es": '¿Cómo justificas este gasto?'}),
    1297: (T + 'повтор 1805 «Quisiera reservar»', {"example_es": 'He reservado las vacaciones por internet'}),
    1312: (T + '«Estoy en contra» — без ситуации', {"example_es": '¿Quién está en contra?'}),
    1319: (T + 'повтор «Por eso …» (161)', {"example_es": 'Por eso te llamo'}),
    1342: (T + 'нет слова карточки «fino»', {"example_es": 'El hielo todavía es demasiado fino'}),
    1432: (T + 'повтор «bañarse» (69)', {"example_es": 'El río atraviesa toda la ciudad'}),
    1479: (T + '«Tengo que lavar los platos» — учебниково', {"example_es": '¡Esta noche los platos los lavas tú!'}),
    1505: (T + 'повтор 1634 «has dejado el trabajo»', {"example_es": 'No hay motivo para preocuparse'}),
    1665: (T + '«No tengo ganas» — оборвано', {"example_es": '¿Tienes ganas de un helado?'}),
    1683: (T + 'повтор 584 «Normalmente…»', {"example_es": 'Los martes casi siempre trabajo desde casa'}),
    1685: (T + 'нет слова карточки «la multitud»', {"example_es": 'Había una multitud enorme en el concierto'}),
    1691: (T + 'нет слова карточки «el empleado»', {"example_es": 'El empleado del mes recibe un vale'}),
    1720: (T + 'повтор 2093 «estoy enfermo»', {"example_es": 'Mañana no trabajo, es que es fiesta'}),
    1793: (T + '«Es muy rico» — без ситуации', {"example_es": 'Se casó con un hombre muy rico'}),
    1813: (T + '«no juega ningún papel» — калька', {"example_es": 'En la película tiene un papel pequeño'}),
    1819: (T + 'повтор 1834 «lo he logrado»', {"example_es": '¿Consigues venir a las ocho?'}),
    1843: (T + 'повтор «Hace un tiempo…» (1032)', {"example_es": 'He tenido un sueño horrible'}),
    1865: (T + 'нет слова карточки «poner»', {"example_es": 'Ponte aquí a mi lado'}),
    1903: (T + 'повтор 10027 «té en vez de café»', {"example_es": 'En vez de ver la tele, lee un libro'}),
    1922: (T + '«Navego por internet» — учебниково', {"example_es": 'Me he pasado la tarde navegando por internet'}),
    1989: (T + '«Por cierto, mañana vengo» — коряво', {"example_es": 'Por cierto, ¿has hablado con Marcos?'}),
    1995: (T + '«En Colonia» — без нужды', {"example_es": 'En Zaragoza tienes que hacer transbordo'}),
    2040: (T + '«Me he enamorado» — оборвано', {"example_es": 'Se ha enamorado de su vecina'}),
    2041: (T + 'повтор «la llave»', {"example_es": '¡No pierdas el tiempo!'}),
    2071: (T + '«Estoy preparando la cena» — учебниково', {"example_es": 'Me estoy preparando para el examen'}),
    2089: (T + 'нет слова карточки «a causa de»', {"example_es": 'A causa de la huelga no hay trenes'}),
    2095: (T + '«Todavía trabajo aquí» — не то значение', {"example_es": 'En adelante seguiré trabajando aquí'}),
    2216: (T + 'повтор 6355 «abrir la puerta»', {"example_es": '¿Abres tú el vino?'}),
    2295: (T + 'нет слова карточки «la población»', {"example_es": 'La población de la ciudad está creciendo'}),
    2458: (T + '«Esta comida» — калька', {"example_es": 'El queso es demasiado graso para mí'}),
    2603: (T + 'нет слова карточки «apenas»', {"example_es": 'Sin gafas apenas veo'}),
    2668: (T + 'повтор 631 «Después de comer»', {"example_es": 'Después de que te fuiste, llamó tu madre'}),
    2880: (T + 'повтор 6284 «se me ha olvidado»', {"example_es": 'Es un desastre total'}),
    2950: (T + '«Me he lesionado» — оборвано', {"example_es": 'Me he lesionado la rodilla jugando al fútbol'}),
    6241: (T + '«Eso está bastante bien» — повтор шаблона', {"example_es": 'Hoy hace bastante frío'}),
}

REPLACE = []

SPLIT_LATER = {}
