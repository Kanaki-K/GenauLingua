"""Вычитка испанского, порция p027 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    7109: (T + '«adivinar el acertijo» — тавтология', {"example_es": '¡Adivina a quién vi ayer!'}),
    7129: (T + 'повтор 6990 «superar esta época difícil»', {"example_es": 'Con un solo sueldo cuesta salir adelante'}),
    7132: (T + '«Tenemos que apagar» — калька', {"example_es": 'Apaga las velas antes de irte a la cama'}),
    7137: (T + 'без ситуации', {"example_es": 'Vemos ponerse el sol sobre el mar'}),
    7142: (T + '«La hormiga es diminuta» — учебниково', {"example_es": 'El piso es diminuto, pero está en pleno centro'}),
    7145: (T + 'нет слова карточки «ceder»', {"example_es": 'No cedió, aunque todos gritaban'}),
    7161: (T + '«Querían echarlo» — калька', {"example_es": 'Lo echaron del bar'}),
    7180: (T + 'учебниково', {"example_es": 'Fiestas, discursos y cosas por el estilo no son lo mío'}),
    7206: (T + '«¿Puedes sacar eso?» — без ситуации', {"example_es": '¿Puedes sacar la basura?'}),
    7213: (T + '«Eso le confiere» — книжно', {"example_es": 'Eso le da a todo el asunto otro sentido'}),
    7237: (T + '«porque no me encuentro bien» — учебниково', {"example_es": 'Si no se te pasa, acude al médico'}),
    7245: (T + '«listo para salir de viaje» — громоздко', {"example_es": '¿Estáis todos listos para salir?'}),
    7262: (T + '«podría dormirme» — оборвано', {"example_es": 'Estoy tan cansado que me dormiría de pie'}),
    7296: (T + 'повтор 15831 «mosquitos este verano»', {"example_es": 'El tráfico es una auténtica plaga en esta ciudad'}),
    7304: (T + '«de Múnich» — длинно', {"example_es": 'Somos socios de la sección local del Club Alpino'}),
    7308: (T + '«Eso refuerza» — книжно', {"example_es": 'Así mi sospecha se refuerza aún más'}),
    7329: (T + '«El globo flota» — учебниково', {"example_es": 'Un olor a café flota en el aire'}),
    7345: (T + '«de Berlín» — без нужды', {"example_es": 'Vivimos a unos veinte kilómetros al este de Zaragoza'}),
    7398: (T + '«Tengo que afilar» — калька', {"example_es": 'Este cuchillo ya no corta, hay que afilarlo'}),
    7423: (T + 'повтор «la llave»', {"example_es": '¿Te has llevado el paraguas? Va a llover'}),
}

REPLACE = []

SPLIT_LATER = {}
