"""Вычитка испанского, порция p032 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    11748: (T + 'повтор «la abuela hornea … en Navidad»', {"example_es": 'Los niños han decorado las galletas de Navidad'}),
    11752: (T + 'нет слова карточки «causar»', {"example_es": 'El perro ha causado un buen lío en el salón'}),
    11762: (T + '«demasiado dura para comerla» — книжно', {"example_es": 'La carne estaba correosa, imposible de cortar'}),
    12188: (T + 'повтор 7336 «ha subido a segunda»', {"example_es": 'Los domingos juega en una liga de aficionados'}),
    12209: (T + '«solo queremos holgazanear» — калька', {"example_es": 'Hoy toca vaguear en casa'}),
    12235: (T + 'повтор 12282 «ir a jugar a los bolos»', {"example_es": 'Los lunes la bolera está cerrada'}),
    12282: (T + '«queremos ir» — калька', {"example_es": 'El viernes vamos a jugar a los bolos con unos amigos'}),
    12644: (T + '«No se debe escupir» — калька', {"example_es": '¡No escupas en el suelo!'}),
    12653: (T + '«Tengo que respirar hondo» — калька', {"example_es": 'Déjame respirar hondo un momento'}),
    12686: (T + '«No tiene carácter, no tiene valor» — калька', {"example_es": 'Se lesionó la columna vertebral al caerse'}),
    12825: (T + 'повтор 13067 «lo visitamos los domingos»', {"example_es": 'Desde que el abuelo ya no puede levantarse solo, vive en una residencia'}),
}

REPLACE = []

SPLIT_LATER = {}
