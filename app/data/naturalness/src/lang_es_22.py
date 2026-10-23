"""Вычитка испанского, порция p022 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    14046: (T + 'нет слова карточки «abordar»', {"example_es": 'Mañana abordo el tema con él'}),
    14061: (T + '«Mi más sincera enhorabuena» — книжно', {"example_es": '¡Enhorabuena por el examen!'}),
    14235: (T + '«Lo sellamos» — книжно', {"example_es": 'Cerramos el trato con un apretón de manos'}),
    14374: (T + 'повтор «se comporta como» (14814)', {"example_es": 'Mi hija quiere un vestido de princesa para su cumpleaños'}),
    14390: (T + 'повтор 12141 «aplaudió con fuerza»', {"example_es": 'Al final del espectáculo todo el público estaba de pie'}),
    14405: (T + '«Quiero filmar eso» — калька', {"example_es": '¡Espera, que lo grabo!'}),
    14411: (T + 'повтор 14437 «Hemos visitado el antiguo…»', {"example_es": 'En Tailandia hay templos por todas partes'}),
    14437: (T + 'повтор 14411', {"example_es": 'Los monjes del monasterio hacen su propia cerveza'}),
    14448: (T + '«castillo de arena» — не то значение', {"example_es": 'Hemos visitado un castillo medieval'}),
    14449: (T + '«Los sonidos de la música» — калька', {"example_es": 'Me encanta el sonido de esta guitarra vieja'}),
    14451: (T + '«una persona bendecida» — калька', {"example_es": 'Con tres nietos me siento muy afortunada'}),
    14456: (T + '«visita Berlín» — без нужды', {"example_es": 'Su Santidad el Papa visita Madrid'}),
    14466: (T + '«tiene mucho talento» — не то значение', {"example_es": 'En este libro el narrador es un gato'}),
    14469: (T + 'нет слова карточки «el hit»', {"example_es": 'Esta canción se ha convertido en el hit del verano'}),
    14481: (T + '«de Berlín» — без нужды', {"example_es": 'Sus cuadros cuelgan en una galería de Madrid'}),
    14496: (T + '«en Berlín» — без нужды', {"example_es": 'La cantante da un concierto en Sevilla la semana que viene'}),
    14502: (T + '«bailar ballet» — калька', {"example_es": 'Mi hija hace ballet desde los cinco años'}),
    14937: (T + 'повтор 14896 «Mamá, ¿dónde…?»', {"example_es": 'El peque llora, quiere a su mami'}),
    14953: (T + '«muy importante para mí» — калька', {"example_es": 'Nuestra amistad viene del colegio'}),
    14966: (T + '«a Berlín» — без нужды', {"example_es": 'Después del divorcio se mudó a Málaga'}),
    14976: (T + '«y muy educado» — тавтология', {"example_es": 'Es un auténtico caballero, siempre me abre la puerta'}),
    15006: (T + '«¿Cómo es vuestra relación?» — калька', {"example_es": 'Tengo muy buena relación con mis vecinos'}),
    15013: (T + 'нет слова карточки «emparentado»', {"example_es": 'Estamos emparentados, pero de lejos'}),
    15034: (T + '«ha visitado la iglesia» — учебниково', {"example_es": 'El obispo viene a bendecir la iglesia nueva'}),
}

REPLACE = []

SPLIT_LATER = {}
