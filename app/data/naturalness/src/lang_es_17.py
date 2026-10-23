"""Вычитка испанского, порция p017 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    8856: (T + 'повтор 8769 «la tripulación del avión»', {"example_es": 'Toda la tripulación del barco bajó a tierra'}),
    8861: (T + '«nos llamó la atención por el seto» — коряво', {"example_es": 'El presidente de la asociación de huertos vino a hablarnos del seto'}),
    8863: (T + '«El pintor ha pintado» — тавтология', {"example_es": 'El pintor viene el lunes a pintar la cocina'}),
    8878: (T + 'учебниково', {"example_es": 'La cocinera del comedor hace las mejores patatas fritas'}),
    8879: (T + 'учебниково', {"example_es": 'La empleada del ayuntamiento me lo explicó todo muy bien'}),
    8932: (T + 'учебниково', {"example_es": 'El secretario del colegio me dio el formulario'}),
    8933: (T + 'учебниково', {"example_es": 'El arquitecto ha dibujado los planos de nuestra casa'}),
    9030: (T + '«La autora ha escrito» — учебниково', {"example_es": 'El sábado la autora firma libros en la librería'}),
    9040: (T + 'повтор 8776 «colgar el cuadro»', {"example_es": 'Clava una tabla en la valla vieja'}),
    9050: (T + '«muy gratificante» — книжно', {"example_es": 'Tiene un pequeño negocio aparte: da clases de guitarra'}),
    9137: (T + 'повтор 8865 «ir al peluquero»', {"example_es": 'El barbero de debajo de casa corta de maravilla'}),
    9161: (T + 'учебниково', {"example_es": 'El nuevo recluta lo pasó mal la primera semana'}),
    9164: (T + '«oficina correspondiente» — канцелярит', {"example_es": 'Para el DNI tienes que ir a la comisaría'}),
    9165: (T + 'без ситуации', {"example_es": 'El encargado de seguridad revisa todas las salidas'}),
    9174: (T + '«tareas sencillas» — книжно', {"example_es": 'La becaria sobre todo hace fotocopias, la pobre'}),
    9267: (T + '«simpáticos y serviciales» — книжно', {"example_es": 'Mis compañeros de trabajo son majísimos'}),
    9471: (T + '«erudito que sabe mucho» — тавтология', {"example_es": 'Mi abuelo es muy erudito en historia'}),
    9482: (T + 'учебниково', {"example_es": 'Recibió una educación muy estricta'}),
    9547: (T + '«El aprendiz aprende» — тавтология', {"example_es": 'El aprendiz de la panadería se levanta a las tres'}),
    9589: (T + 'без ситуации', {"example_es": 'He suspendido el examen de conducir'}),
    9603: (T + '«Cada mañana» — калька', {"example_es": 'Por las mañanas voy al colegio en el autobús escolar'}),
    9605: (T + '«En el recreo … del colegio» — повтор', {"example_es": 'Los niños juegan al fútbol en el patio del colegio'}),
    9610: (T + '«suena a las ocho de la mañana» — учебниково', {"example_es": 'Cuando suena el timbre de la escuela, todos salen corriendo'}),
    9613: (T + 'учебниково', {"example_es": 'Mi hijo tiene miedo de enseñar el boletín de notas'}),
    9733: (T + '«Recibo un cheque» — без ситуации', {"example_es": 'La abuela me ha mandado un cheque de 100 euros por mi cumpleaños'}),
    9735: (T + '«parte de las ganancias es pequeña» — книжно', {"example_es": 'Cada uno paga su parte'}),
    9758: (T + 'повтор 1466 «la cartera»', {"example_es": 'Me he dejado la cartera en casa'}),
    9761: (T + '«para niños pobres» — учебниково', {"example_es": 'Cada año donamos algo a una asociación'}),
    9915: (T + 'повтор «¿Cuál es tu…?»', {"example_es": '¿Me mandas el número de cuenta?'}),
}

REPLACE = []

SPLIT_LATER = {}
