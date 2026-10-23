"""Вычитка испанского, порция p020 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    12163: (T + 'повтор 12378 «cruzar remando»', {"example_es": '¡He perdido un remo, damos vueltas en círculo!'}),
    12378: (T + 'повтор 12163', {"example_es": 'Agarra bien la pala, la corriente es fuerte'}),
    12219: (T + '«termina empatado» — без ситуации', {"example_es": 'Empataron a uno'}),
    12348: (T + '«Juguemos» — книжно', {"example_es": '¿Jugamos a las charadas?'}),
    12485: (T + '«me duelen todos los huesos» — без ситуации', {"example_es": 'Con esta humedad me duelen los huesos'}),
    12501: (T + 'учебниково', {"example_es": 'En la oficina hay un virus que va de mano en mano'}),
    12518: (T + '«ya no es tan buena» — калька', {"example_es": 'Con los años la memoria ya no es lo que era'}),
    12532: (T + '«Después de correr tengo el pulso muy alto» — учебниково', {"example_es": 'Después de la carrera tengo el pulso a 150'}),
    12545: (T + '«Necesito un examen médico» — без ситуации', {"example_es": 'Para el club de fútbol hace falta un certificado médico'}),
    12559: (T + '«Tienes que tomar el medicamento» — без ситуации', {"example_es": 'Este medicamento hay que tomarlo antes de las comidas'}),
    12588: (T + '«odiar como a la peste» — не та идиома', {"example_es": 'A esa gente la evito como a la peste'}),
    12602: (T + 'учебниково', {"example_es": 'En la ecografía se oyen los latidos del bebé'}),
    12625: (T + 'нет слова карточки «enganchado»', {"example_es": 'Está completamente enganchado al café'}),
    12630: (T + '«sudo y me empapo» — громоздко', {"example_es": 'Cuando hace calor sudo muchísimo'}),
    12727: (T + 'повтор 12967 «cuidadora en casa de la abuela»', {"example_es": 'El enfermero de noche es muy amable con los pacientes'}),
}

REPLACE = []

SPLIT_LATER = {}
