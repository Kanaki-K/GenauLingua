"""Вычитка испанского, порция p008 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    772: (T + 'нет слова карточки «vaciar»', {"example_es": 'Antes del viernes tenemos que vaciar el piso'}),
    831: (T + '«Rara vez vengo aquí» — учебниково', {"example_es": 'Cada vez nos vemos más rara vez'}),
    870: (T + '«Müller» — не испанская фамилия', {"example_es": 'Señora Fernández, pase a la consulta, por favor'}),
    873: (T + 'повтор 874 «¿Quién … hoy?»', {"example_es": 'Friega tú, yo seco'}),
    883: (T + 'повтор 1068 «Me he golpeado…»', {"example_es": 'Tienes la frente ardiendo, ¿tienes fiebre?'}),
    921: (T + 'повтор 1736 «tu número»', {"example_es": 'He cambiado de número de teléfono'}),
    1009: (T + '«La lavadora está en marcha» — без ситуации', {"example_es": 'La lavadora pierde agua'}),
    1057: (T + '«en Múnich» — без нужды', {"example_es": 'En la búsqueda de piso en Madrid hace falta mucha paciencia'}),
    1199: (T + '«¡Elige algo!» — без ситуации', {"example_es": 'Elige tú el restaurante'}),
    1201: (T + 'повтор 1104 «quitarse la chaqueta/el abrigo»', {"example_es": 'Quítate los zapatos, por favor'}),
    1230: (T + '«nos atiende bien» — коряво', {"example_es": 'La dependienta está atendiendo a otro cliente'}),
    1241: (T + 'повтор 26 «inscribirme en el curso»', {"example_es": 'En la universidad me he inscrito en un curso de italiano'}),
    1302: (T + '«señora Klein» — не испанская фамилия', {"example_es": 'En nuestra empresa de la organización de la oficina se encarga la señora Romero'}),
    1308: (T + '«Canto en el coro» — учебниково', {"example_es": 'Mi madre canta en el coro de la iglesia'}),
    1337: (T + '«Gírate» — без ситуации', {"example_es": 'Date la vuelta, que te arreglo el cuello'}),
    1358: (T + '«Amueblo mi apartamento» — учебниково', {"example_es": 'Todavía estamos amueblando la casa nueva'}),
    1384: (T + '«Tengo que decidirme» — калька', {"example_es": 'No consigo decidirme'}),
}

REPLACE = []

SPLIT_LATER = {}
