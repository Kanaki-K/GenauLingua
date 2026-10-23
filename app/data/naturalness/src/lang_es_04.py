"""Вычитка испанского, порция p004 (A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    81: (T + '«Construyen una casa» — без ситуации', {"example_es": 'Los vecinos se están construyendo una casa nueva'}),
    128: (T + '«La blusa sienta bien» — оборвано', {"example_es": 'Esta blusa es perfecta para la oficina'}),
    161: (T + '«Estoy a favor» — не то значение', {"example_es": 'Para eso he venido'}),
    170: (T + '«tomar con eso» — калька', {"example_es": '¿Qué bebes con la pizza?'}),
    171: (T + 'повтор «Esta es … » (426, 963)', {"example_es": '¿Es tuyo este bolso?'}),
    186: (T + '«a Berlín» — без нужды', {"example_es": 'El tren va directo a Madrid'}),
    216: (T + '«Me gusta comer helado» — учебниково', {"example_es": '¿Vamos a tomar un helado?'}),
    234: (T + '«en Berlín» — без нужды', {"example_es": 'Es mi primera vez en Valencia'}),
    289: (T + 'повтор 293 «estoy contento»', {"example_es": '¡Me alegro mucho de verte!'}),
    318: (T + 'повтор «la farmacia»', {"example_es": 'Vivo justo enfrente del parque'}),
    355: (T + '«Tiene la gripe» — без ситуации', {"example_es": 'Media clase tiene la gripe'}),
    423: (T + '«Tengo una buena idea» — калька', {"example_es": '¡Tengo una idea!'}),
    459: (T + '«la comida» — калька', {"example_es": '¡Se enfría la pasta, ven rápido!'}),
    471: (T + 'повтор 450 «no tengo tiempo»', {"example_es": 'No hay ningún problema'}),
    538: (T + 'нет слова карточки «aburrido»', {"example_es": 'Esta película es aburridísima'}),
    568: (T + 'повтор «al trabajo en…»', {"example_es": 'A veces me despierto por la noche'}),
    582: (T + 'повтор «Este es mi…»', {"example_es": '¿Has visto mi móvil?'}),
    657: (T + '«Dilo otra vez» — грубовато', {"example_es": '¿Me lo explicas otra vez?'}),
    662: (T + '«Hago pasta para comer» — учебниково', {"example_es": 'Esta noche hago pasta con tomate'}),
    677: (T + '«Compra por internet» — оборвано', {"example_es": 'Compro casi todo por internet'}),
    686: (T + '«En el este hace frío» — калька', {"example_es": 'Su familia es de Europa del Este'}),
    773: (T + '«Lleva la mochila a la espalda» — учебниково', {"example_es": 'Me duele la espalda'}),
    782: (T + 'повтор 573 «el mercado»', {"example_es": 'Los sábados hago la compra de toda la semana'}),
    784: (T + '«Es una lástima» — учебниково', {"example_es": '¡Qué pena, no puedo ir!'}),
    792: (T + '«El barco zarpa» — книжно', {"example_es": 'El barco a Mallorca sale a las nueve'}),
    814: (T + '«Está embarazada» — без ситуации', {"example_es": 'Mi hermana está embarazada de tres meses'}),
    840: (T + '«Me gusta cantar» — учебниково', {"example_es": 'Siempre canta en la ducha'}),
    842: (T + 'повтор 1043 «ir a esquiar»', {"example_es": 'He alquilado los esquís'}),
    923: (T + '«Juguemos al tenis» — книжно', {"example_es": '¿Juegas al tenis?'}),
    941: (T + 'повтор «a las tres»', {"example_es": 'Me encontré con Pablo en el centro'}),
    963: (T + 'повтор «Esta es … casa» (426)', {"example_es": 'Nuestra casa está al final de la calle'}),
    976: (T + 'повтор «las llaves»', {"example_es": '¡Se me ha olvidado el cumpleaños de mi madre!'}),
    1011: (T + 'повтор 223 «¿dónde está el baño?»', {"example_es": 'El servicio está al fondo del pasillo'}),
}

REPLACE = []

SPLIT_LATER = {}
