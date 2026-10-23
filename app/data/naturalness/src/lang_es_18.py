"""Вычитка испанского, порция p018 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    10054: (T + '«Voy solo al cine» — порядок', {"example_es": 'Voy al cine yo solo'}),
    10112: (T + '«Tú eres responsable de eso» — книжно', {"example_es": 'El responsable eres tú'}),
    10150: (T + '«Quiere venganza por todo» — коряво', {"example_es": 'Solo piensa en la venganza'}),
    10152: (T + 'без ситуации', {"example_es": 'Después de la fiesta toda la casa está revuelta'}),
    10184: (T + '«Puedo sentir el viento» — калька', {"example_es": '¿Notas esta corriente?'}),
    10190: (T + '«Rezamos cada noche» — учебниково', {"example_es": 'La abuela reza todas las noches'}),
    10208: (T + '«mi mayor punto fuerte» — калька', {"example_es": 'La cocina es mi punto fuerte'}),
    10215: (T + '«La pérdida me pone triste» — калька', {"example_es": 'La pérdida de su perro le afectó mucho'}),
    10218: (T + '«Deberías portarte mejor» — калька', {"example_es": 'Pórtate bien en casa de la abuela, ¿eh?'}),
    10220: (T + '«el niño está obediente» — учебниково', {"example_es": 'Hoy el peque se ha portado muy bien'}),
    10241: (T + '«se tiraron valientes» — коряво', {"example_es": 'Los niños han sido muy valientes en el dentista'}),
    10256: (T + '«Yo, tonto de mí» — шаблон', {"example_es": 'Y yo, como un tonto, me dejé la luz encendida'}),
    10267: (T + 'нет слова карточки «el punto débil»', {"example_es": 'El chocolate es mi punto débil'}),
    10285: (T + 'без ситуации', {"example_es": 'La policía todavía busca el móvil del crimen'}),
    10288: (T + 'повтор 10164 «me resulta incómodo»', {"example_es": 'El ruido del taladro es muy desagradable'}),
    10296: (T + 'повтор 10098 «en contra de mi voluntad»', {"example_es": 'Con un poco de voluntad lo consigues'}),
    10298: (T + '«visión clara para mi vida» — калька', {"example_es": 'La nueva directora tiene una visión clara para la empresa'}),
    10318: (T + '«Repartamos» — книжно', {"example_es": 'Repartimos la tarta de forma justa'}),
    10321: (T + '«Querías asustarme» — неживо', {"example_es": '¡Me has asustado!'}),
    10324: (T + '«¿Qué pena tienes?» — калька', {"example_es": 'Qué pena verte tan triste'}),
    10335: (T + '«huele asqueroso» — калька', {"example_es": 'En la nevera hay un olor asqueroso'}),
    10338: (T + 'повтор 10295 «qué asqueroso»', {"example_es": '¡Esta sopa está asquerosa!'}),
    10347: (T + '«Son pura escoria» — коряво', {"example_es": 'Esos tipos son escoria'}),
    10349: (T + 'нет «unido» как «снова вместе» — повтор 7759', {"example_es": 'Después de la pelea la familia vuelve a estar unida'}),
    10356: (T + '«Con comida atraes» — коряво', {"example_es": 'Con un poco de jamón atraes al gato a casa'}),
    10371: (T + '«defenderte del acoso» — книжно', {"example_es": 'Defiéndete, no te dejes pisar'}),
    10372: (T + '«no me asusta nada tan fácilmente» — коряво', {"example_es": 'Las tormentas asustan mucho a mi perro'}),
    10373: (T + '«le ayuda con los problemas» — книжно', {"example_es": 'Su inteligencia impresiona a todos sus profesores'}),
    10404: (T + 'учебниково', {"example_es": 'Sin disciplina no se llega a ninguna parte'}),
    10405: (T + '«Trabaja muy concentrado» — калька', {"example_es": 'No lo molestes, está muy concentrado'}),
    10406: (T + '«actitud hacia el trabajo» — книжно', {"example_es": 'Siempre tiene una actitud positiva'}),
    10409: (T + 'повтор 10179 «celosa de su hermana»', {"example_es": 'Le tiene un poco de envidia a mi coche nuevo'}),
}

REPLACE = []

SPLIT_LATER = {}
