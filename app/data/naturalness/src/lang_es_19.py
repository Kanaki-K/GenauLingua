"""Вычитка испанского, порция p019 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    10434: (T + '«Lo hago con mucho gusto» — нет слова «cariñoso»', {"example_es": 'Es una madre muy cariñosa'}),
    10436: (T + '«celebran la primera nieve» — книжно', {"example_es": 'Toda la sala aclama al grupo cuando sale al escenario'}),
    10443: (T + '«situación amenazante» — книжно', {"example_es": 'El cielo está amenazante, volvamos a casa'}),
    10459: (T + 'повтор 10233 «que funcione»', {"example_es": 'Dudo que diga la verdad'}),
    10460: (T + '«miedoso y les tiene miedo» — тавтология', {"example_es": 'Mi hijo es muy miedoso, duerme con la luz encendida'}),
    10462: (T + 'учебниково', {"example_es": 'Aprecio tu sinceridad'}),
    10463: (T + 'повтор 10233 «Me temo que»', {"example_es": 'Temo un poco la reunión de mañana'}),
    10548: (T + '«realistas con nuestros objetivos» — книжно', {"example_es": 'Sé realista, no vamos a terminar antes del viernes'}),
    10812: (T + 'повтор 8285 «silba»', {"example_es": 'Los niños juegan alegres en el jardín'}),
    11134: (T + 'повтор «la llave»', {"example_es": 'Mi calcetín ha desaparecido de forma misteriosa'}),
    11136: (T + '«El día a día» — книжно', {"example_es": 'En el trabajo ahora mismo está todo bastante ajetreado'}),
    11337: (T + '«Los ruidos fuertes asustan al niño» — учебниково', {"example_es": 'La máscara de su hermano asustó a la pequeña'}),
    11378: (T + '«sacar adelante la tarea» — книжно', {"example_es": 'Nunca lo habría creído capaz de algo así'}),
    11650: (T + '«Brindemos» — книжно', {"example_es": '¡Brindamos con champán!'}),
    11708: (T + '«El niño se traga» — учебниково', {"example_es": 'No consigo tragar estas pastillas tan grandes'}),
    11711: (T + 'повтор «la abuela hace las mejores»', {"example_es": 'Los domingos desayunamos tortitas con sirope'}),
    11732: (T + 'нет слова карточки «sediento»', {"example_es": 'Después del partido los jugadores están sedientos'}),
    11816: (T + '«currywurst» — не испанский быт', {"example_es": 'Vamos a comer algo rápido en el puesto de comida'}),
    11850: (T + 'повтор «para la tos» (11851)', {"example_es": 'No comas tantos caramelos antes de cenar'}),
    11854: (T + 'повтор «la abuela hace ella misma»', {"example_es": 'En el norte se come mucha col'}),
    11891: (T + 'нет слова карточки «el refrigerio»', {"example_es": 'En la entrada ofrecen un refrigerio'}),
    11944: (T + 'повтор 11945 «vamos al … a tomar»', {"example_es": 'Dormimos en un viejo mesón de montaña'}),
    11945: (T + 'повтор 11944', {"example_es": 'El bistró de la esquina hace un café buenísimo'}),
    11969: (T + '«agua mineral con gas» — громоздко', {"example_es": '¿Con gas o sin gas? – Sin gas, por favor'}),
    11991: (T + 'повтор 11677 «después de comer tomamos»', {"example_es": 'Mi tía hace ella misma licor de cerezas'}),
    12001: (T + '«a la cafetería a tomar café» — тавтология', {"example_es": 'Es cliente habitual, el camarero ya sabe lo que pide'}),
    12007: (T + '«hace la comida más interesante» — калька', {"example_es": 'Le falta un poco de condimento'}),
    12027: (T + 'повтор «la abuela hace cada año»', {"example_es": 'La jalea de grosellas va muy bien con el queso'}),
    12028: (T + '«asamos un pavo» — учебниково', {"example_es": 'En Navidad comemos pavo'}),
    12098: (T + '«Es un placer para mí» — калька', {"example_es": '¡Qué placer verte!'}),
}

REPLACE = []

SPLIT_LATER = {}
