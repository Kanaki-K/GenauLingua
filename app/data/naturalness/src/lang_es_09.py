"""Вычитка испанского, порция p009 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    1397: (T + '«Abrimos una nueva tienda» — учебниково', {"example_es": 'En la calle Mayor inauguran una tienda nueva'}),
    1445: (T + 'повтор 8865 «al peluquero»', {"example_es": 'La peluquera me ha cortado demasiado el pelo'}),
    1447: (T + 'повтор 17481 «¿Cómo funciona?»', {"example_es": 'El lavavajillas ya no funciona'}),
    1452: (T + '«Compro un coche usado» — учебниково', {"example_es": 'La mochila la compré de segunda mano'}),
    1457: (T + '«Schmidt / Weber» — не испанские фамилии', {"example_es": 'Su apellido de soltera es López, pero desde la boda se llama Martín'}),
    1467: (T + 'повтор 151, 1707 «moneda para el carro»', {"example_es": 'En esta fuente los turistas tiran monedas'}),
    1519: (T + '«El conserje lo arregla» — без ситуации', {"example_es": 'El conserje ya ha cambiado la bombilla'}),
    1532: (T + '«Damos un rodeo alrededor de la ciudad» — коряво', {"example_es": 'Alrededor del lago hay un sendero'}),
    1566: (T + '«El libro está por ahí» — учебниково', {"example_es": 'El mando estará por ahí, en algún sitio del sofá'}),
    1572: (T + '«se reúnen aquí» — без ситуации', {"example_es": 'Los jóvenes del barrio se reúnen en el parque'}),
    1590: (T + 'повтор 1946 «Mañana tenemos un…»', {"example_es": 'El examen de matemáticas ha salido bien'}),
    1595: (T + 'повтор 1138 «clic en el enlace»', {"example_es": 'Haz doble clic en el icono'}),
    1640: (T + 'повтор 2714 «se ha vuelto a colgar»', {"example_es": 'Me llevo el portátil a la oficina todos los días'}),
    1663: (T + '«Salimos a las 8» — учебниково', {"example_es": 'Salimos en cuanto deje de llover'}),
    1707: (T + 'повтор 151 «moneda para el carro»', {"example_es": 'Colecciono monedas antiguas'}),
    1712: (T + 'повтор 450 «te llamo luego»', {"example_es": 'Nos vemos luego en el bar'}),
    1728: (T + '«en Berlín» — без нужды', {"example_es": 'Mi sobrina estudia en Salamanca'}),
    1734: (T + '«No es necesario» — оборвано', {"example_es": 'No es necesario traer nada'}),
    1758: (T + '«Es mi deber» — калька', {"example_es": 'No es un favor, es tu obligación'}),
}

REPLACE = []

SPLIT_LATER = {}
