"""Вычитка испанского, порция p011 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    2178: (T + '«No toques eso» — без ситуации', {"example_es": '¡No lo toques, quema!'}),
    2192: (T + 'повтор 1903 «En vez de…»', {"example_es": 'En lugar de quejarte, ayúdame'}),
    2205: (T + '«Es realmente molesto» — без ситуации', {"example_es": 'Este ruido es realmente molesto'}),
    2217: (T + 'нет слова карточки «atento»', {"example_es": 'Es un chico muy atento en clase'}),
    2220: (T + '«Apúntatelo» — оборвано', {"example_es": 'Apunta la dirección, que si no se te olvida'}),
    2221: (T + 'повтор 6382 «Nos repartimos»', {"example_es": 'El trabajo lo repartimos entre tres'}),
    2258: (T + '«Te lo puedes quedar» — без ситуации', {"example_es": 'El libro te lo puedes quedar, te lo regalo'}),
    2286: (T + '«Hemos vencido al rival» — книжно', {"example_es": 'Hemos derrotado al mejor equipo de la liga'}),
    2290: (T + '«No puedes entrar en la habitación» — учебниково', {"example_es": 'Nunca he pisado esa casa'}),
    2309: (T + '«Taladro un agujero» — тавтология', {"example_es": 'Los domingos no se puede taladrar la pared'}),
    2311: (T + '«Entrena boxeo» — коряво', {"example_es": 'Mi hija hace boxeo dos veces por semana'}),
    2335: (T + 'повтор 1397 «una tienda nueva»', {"example_es": 'Próximamente en cines'}),
    2339: (T + 'повтор 2093 «estoy enfermo»', {"example_es": 'Mañana hay huelga, por eso voy en bici'}),
    2342: (T + 'повтор «es diabético» (13061)', {"example_es": 'Para los diabéticos hay dulces sin azúcar'}),
    2353: (T + '«Pago el doble del precio» — без ситуации', {"example_es": 'El billete de última hora cuesta el doble'}),
    2385: (T + 'повтор 2184 «Enciende la…»', {"example_es": '¿Quién ha encendido la radio?'}),
    2426: (T + '«Tenemos que subir los precios» — без ситуации', {"example_es": 'El casero quiere subir el alquiler'}),
    2430: (T + '«Necesito una explicación» — калька', {"example_es": 'Me debes una explicación'}),
}

REPLACE = []

SPLIT_LATER = {}
