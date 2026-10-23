"""Вычитка испанского, порция p024 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    15933: (T + '«La novela trata de un asesinato» — учебниково', {"example_es": 'Ha habido un asesinato en nuestro barrio'}),
    15938: (T + 'повтор «abuelo en el ejército» (8744)', {"example_es": 'Mi hermano hace la mili en el ejército'}),
    15947: (T + '«Amo mi libertad» — без ситуации', {"example_es": 'Desde que tengo carné, por fin tengo mi libertad'}),
    15950: (T + 'нет слова карточки «el talego»', {"example_es": 'Se pasó tres años en el talego'}),
    15951: (T + '«Necesito una prueba de eso» — коряво', {"example_es": '¿Tienes pruebas?'}),
    15967: (T + '«puede liberar» — калька', {"example_es": 'La policía ha liberado a los rehenes'}),
    15973: (T + '«El preso está sentado» — учебниково', {"example_es": 'Pasó la noche en la celda'}),
    15974: (T + '«defender mi opinión» — книжно', {"example_es": 'Siempre defiende a su hermana pequeña'}),
    15985: (T + '«El emperador gobernó el país» — учебниково', {"example_es": 'Napoleón se hizo coronar emperador'}),
    15993: (T + '«Estoy a su disposición» — без ситуации', {"example_es": 'Estoy a tu disposición si necesitas algo'}),
    15995: (T + '«El perro nos ataca» — неживо', {"example_es": 'El perro de los vecinos ha atacado a nuestro gato'}),
    15996: (T + '«Tengo la sospecha de que miente» — шаблон', {"example_es": 'Tengo una sospecha, pero ninguna prueba'}),
    16006: (T + '«en Múnich» — без нужды', {"example_es": 'Su marido trabaja de fiscal en Sevilla'}),
    16009: (T + '«Los testigos tienen que declarar» — тавтология', {"example_es": 'La semana que viene tiene que declarar ante el juez'}),
    16013: (T + '«ayuda el ejército» — коряво', {"example_es": 'Tras la inundación los militares ayudan a los vecinos'}),
    16028: (T + 'учебниково', {"example_es": 'En el cuento todo el reino está en peligro'}),
    16086: (T + '«trato regio para nosotros» — коряво', {"example_es": 'En el hotel nos trataron a cuerpo de rey'}),
    16089: (T + '«en Berlín» — без нужды', {"example_es": 'El congreso se celebra la semana que viene en Madrid'}),
    16099: (T + '«proteger mi privacidad» — калька', {"example_es": 'No subo fotos de los niños, es su intimidad'}),
    16101: (T + 'повтор «vigilar» (16029)', {"example_es": '¿Me vigilas las cosas mientras nado?'}),
    16103: (T + '«fue importante para el caso» — книжно', {"example_es": 'La comparecencia del testigo es mañana'}),
    16104: (T + 'повтор 16146 «la policía detuvo»', {"example_es": 'Lo detuvieron a la salida de la tienda'}),
    16106: (T + '«Mi día a día está bien organizado» — книжно', {"example_es": 'Todo está organizado para el viaje'}),
    16133: (T + 'повтор 16152 «el rey … años»', {"example_es": '¿Quién gobierna el país ahora?'}),
    16134: (T + 'повтор 16128 «está en la cárcel»', {"example_es": 'El atraco al banco duró diez minutos'}),
    16140: (T + '«El sello es importante» — коряво', {"example_es": 'La carta lleva el sello del rey'}),
    16281: (T + '«Votemos» — книжно', {"example_es": '¿Votamos adónde vamos?'}),
    16343: (T + '«sentencia sabia» — книжно', {"example_es": 'La jueza fue muy dura con él'}),
    16345: (T + '«¿Me ocupas un sitio?» — калька', {"example_es": '¿Está ocupado este sitio?'}),
    16355: (T + 'повтор 16717 «coche patrulla delante de casa»', {"example_es": 'El coche patrulla va con la sirena puesta'}),
    16702: (T + 'повтор 15976 «visita nuestro colegio»', {"example_es": 'La ministra de Sanidad habla esta noche en la tele'}),
    17057: (T + 'повтор 17081 «Estamos a bordo/en la cubierta»', {"example_es": '¡Bienvenidos a bordo!'}),
    17081: (T + 'повтор 17057', {"example_es": 'En la cubierta hace viento, ponte una chaqueta'}),
    17099: (T + 'повтор «¿De quién es…?» (13462)', {"example_es": 'Los vehículos de más de 3,5 toneladas no pueden pasar'}),
    17105: (T + '«a Berlín» — без нужды', {"example_es": 'El avión a Tenerife sale a las ocho'}),
}

REPLACE = []

SPLIT_LATER = {}
