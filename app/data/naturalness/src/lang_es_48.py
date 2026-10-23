"""Вычитка испанского, порция p048 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    14320: (T + 'повтор 7204 «un logro notable»', {"example_es": 'Fue verdaderamente una noche preciosa'}),
    14688: (T + '«con gusto» — калька', {"example_es": 'Te arreglo el portátil, ¡pero no soy ningún brujo!'}),
    15260: (T + '«en Berlín» — без нужды', {"example_es": 'Mi padre biológico vive en Valencia'}),
    15278: (T + 'повтор 12129 «sin su osito no se duerme»', {"example_es": 'A mi hijo le regalaron un osito al nacer'}),
    15783: (T + 'без ситуации', {"example_es": 'Con la marea baja se puede ir andando hasta la isla'}),
    15845: (T + '«La nevera vieja» — оставить, но короче', {"example_es": 'El frigo viejo acaba en el vertedero'}),
    15855: (T + '«domado y tranquilo» — учебниково', {"example_es": 'Domaron a este caballo salvaje en un mes'}),
    16694: (T + 'повтор 7028 «jugar a las cartas para pasar el tiempo»', {"example_es": 'Para matar el tiempo en el aeropuerto, leo'}),
}

REPLACE = []

SPLIT_LATER = {}
