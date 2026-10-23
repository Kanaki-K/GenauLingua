"""Вычитка испанского, порция p025 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    17148: (T + '«hasta la otra orilla» — тавтология', {"example_es": 'Cogemos el ferry para cruzar el río'}),
    17173: (T + '«El pasajero sube al avión» — учебниково', {"example_es": 'Los pasajeros del vuelo a Málaga deben ir a la puerta 12'}),
    17184: (T + 'без ситуации', {"example_es": '¿Damos un rodeo por la panadería?'}),
    17194: (T + '«Gira en la próxima calle» — неполно', {"example_es": 'En la próxima calle gira a la izquierda'}),
    17209: (T + '«Müller» — не испанская фамилия', {"example_es": 'Tengo una reserva a nombre de Martínez'}),
    17410: (T + '«sale temprano» — оборвано', {"example_es": 'El barco pesquero vuelve al puerto lleno de pescado'}),
    17502: (T + '«lo hace todo más fácil» — калька', {"example_es": 'A mi abuelo le dan miedo las nuevas tecnologías'}),
    17516: (T + '«accionar el interruptor» — калька', {"example_es": 'Me puso el brazo por encima de los hombros'}),
    17533: (T + '«Formo parte de una gran red» — коряво', {"example_es": 'En el mundo de la moda tiene una gran red de contactos'}),
    17541: (T + '«Tienes que actualizar» — калька', {"example_es": 'Hay que actualizar el software'}),
    17578: (T + 'повтор «el ascensor está roto» (13558)', {"example_es": '¿Cogemos el ascensor o vamos por las escaleras?'}),
    17587: (T + '«por una avería» — оборвано', {"example_es": 'Llegamos tarde por una avería del coche'}),
    17590: (T + '«ofrece muchas funciones» — реклама', {"example_es": '¿En qué plataforma se puede ver la película?'}),
    17662: (T + '«spätzle … Suabia» — не испанский быт', {"example_es": 'Esta noche comemos lentejas con chorizo'}),
    17768: (T + '«Tenemos un trato» — калька', {"example_es": '¡Trato hecho!'}),
    17771: (T + 'повтор 15617 «vacas en el prado»', {"example_es": 'La leche viene directamente de la vaca del vecino'}),
    17779: (T + 'учебниково', {"example_es": 'En invierno el ganado se queda en el establo'}),
    17792: (T + 'без ситуации', {"example_es": 'El sector del turismo lo está pasando mal'}),
    17921: (T + '«Hagamos» — книжно', {"example_es": '¿Hacemos un pequeño experimento?'}),
    17931: (T + '«El niño mide» — учебниково', {"example_es": 'Mi hijo ya mide 120 centímetros'}),
    18054: (T + 'повтор 17946 «para la tarta»', {"example_es": 'Un kilogramo de tomates, por favor'}),
    18115: (T + '«Ahora me voy a casa» — калька', {"example_es": 'Bueno, me vuelvo a casa'}),
    18187: (T + '«son muy amables» — учебниково', {"example_es": 'En el edificio los vecinos se conocen todos'}),
    18194: (T + '«solemos sentarnos» — калька', {"example_es": 'En invierno pasamos las tardes delante de la chimenea'}),
}

REPLACE = []

SPLIT_LATER = {}
