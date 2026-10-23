"""Вычитка испанского, порция p021 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    13008: (T + '«La inflamación por fin se ha curado» — неживо', {"example_es": 'Tengo una inflamación en la rodilla'}),
    13059: (T + '«me duele la tráquea» — неживо', {"example_es": 'El trozo de manzana se me fue por la tráquea'}),
    13060: (T + '«en Múnich» — лишнее', {"example_es": 'Después del partido tenía la voz ronca de tanto gritar'}),
    13067: (T + 'повтор 12807 «la abuela vive en una residencia»', {"example_es": 'Los domingos visitamos al abuelo en la residencia de ancianos'}),
    13096: (T + 'повтор 12798 «dolor de barriga»', {"example_es": 'El peque se queja de dolor de tripa todos los lunes por la mañana'}),
    13097: (T + 'учебниково', {"example_es": 'Mi médico de cabecera se jubila, tengo que buscar otro'}),
    13103: (T + 'учебниково', {"example_es": '¡Deja de bostezar, que es contagioso!'}),
    13141: (T + '«El niño tiene un rasguño» — учебниково', {"example_es": 'Solo es un rasguño, no hace falta tirita'}),
    13168: (T + 'повтор 11851 «sabe asqueroso»', {"example_es": '¿Puedes pasar por la farmacia a por jarabe para la tos?'}),
    13369: (T + '«Necesito algo de comer» — калька', {"example_es": '¿Tienes algo de comer?'}),
    13394: (T + 'нет слова карточки «para acá»', {"example_es": 'Ven para acá, que aquí hay sitio'}),
    13407: (T + '«Ni tú ni yo lo sabemos» — книжно', {"example_es": 'No tengo ni tiempo ni dinero'}),
    13473: (T + 'нет слова карточки «semejante»', {"example_es": 'Con semejante tiempo nos quedamos en casa'}),
    13478: (T + 'повтор «en primer lugar, no tengo tiempo»', {"example_es": 'En primer lugar, los deberes; luego, la tele'}),
    13508: (T + 'нет слова карточки «cuarto»', {"example_es": 'Quedó cuarto en la carrera'}),
    13511: (T + 'повтор 8182 «los libros uno encima de otro»', {"example_es": 'Los platos están apilados unos encima de otros en el fregadero'}),
    13558: (T + 'повтор 6838 «ya es la … taza de café»', {"example_es": 'Vivo en el séptimo y el ascensor está roto'}),
    13590: (T + '«Una décima parte de la población vive en la ciudad» — неверно', {"example_es": 'Perdió por una décima de segundo'}),
    13631: (T + '«necesita ropa» — коряво', {"example_es": 'El peque corretea desnudo por el jardín'}),
    13645: (T + '«El botón ya no está» — без ситуации', {"example_es": '¿Me puedes coser este botón?'}),
    13660: (T + 'повтор 13703 «disfrazado de pirata»', {"example_es": 'Todos vinieron disfrazados a la fiesta'}),
    13662: (T + 'повтор 12339 «dejar … en el vestuario/guardarropa»', {"example_es": 'En el teatro los abrigos se dejan en el guardarropa'}),
    13758: (T + '«cuando vayamos a la playa» — громоздко', {"example_es": 'No te olvides la crema solar para la playa'}),
    13769: (T + 'повтор 13719 «los domingos ando en…»', {"example_es": 'Mi abuelo se toma el café en bata'}),
    13770: (T + 'повтор 13746 «zapatillas de casa»', {"example_es": 'En casa los invitados se quitan los zapatos y se ponen zapatillas'}),
    13817: (T + 'повтор «las llaves»', {"example_es": '¡Maldita sea, he perdido el tren!'}),
    13861: (T + '«Sí, señor, lo hago» — коряво', {"example_es": '¡A sus órdenes, jefe!'}),
    13866: (T + '«Lo veo con subtítulos» — оборвано', {"example_es": 'Veo las series con subtítulos'}),
    13881: (T + 'нет слова карточки «la broma»', {"example_es": '¡Era solo una broma!'}),
    13884: (T + 'повтор 8796 «No hagas tonterías»', {"example_es": 'Deja de decir tonterías'}),
    13893: (T + '«informa sobre el acontecimiento» — учебниково', {"example_es": 'Toda la prensa habla de la boda del príncipe'}),
    13911: (T + '«Aquí tienes un aviso importante» — канцелярит', {"example_es": '¡Gracias por la pista!'}),
    13924: (T + '«Puedo simplemente ignorar» — калька', {"example_es": 'Ignora sus comentarios tontos'}),
    13925: (T + '«¿Puedes escuchar esto?» — калька', {"example_es": '¡Escucha esto!'}),
    13957: (T + 'повтор 13877 «No, no tengo ganas»', {"example_es": '¿Tienes hambre? – No, estoy bien'}),
    13973: (T + 'без ситуации', {"example_es": 'Este pitido del horno me pone de los nervios'}),
    13983: (T + 'повтор 10122 «no estoy sordo»', {"example_es": 'El león ruge en su jaula'}),
    13995: (T + '«¡Adiós, amigo mío!» — книжно', {"example_es": '¡Adiós, y gracias por todo!'}),
}

REPLACE = []

SPLIT_LATER = {}
