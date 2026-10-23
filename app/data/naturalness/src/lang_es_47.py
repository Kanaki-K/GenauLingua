"""Вычитка испанского, порция p047 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    11610: (T + 'повтор 10345 «idea idiota»', {"example_es": '¡Qué idea más tonta!'}),
    11613: (T + '«con gusto» — калька', {"example_es": 'Es un verdadero filántropo, ayuda a todo el mundo'}),
    11956: (T + 'без ситуации', {"example_es": '¿Tomamos el aperitivo en la terraza?'}),
    11997: (T + 'повтор 11677 «después de comer bebemos»', {"example_es": 'El abuelo siempre ofrece una copa de oporto a los invitados'}),
    12945: (T + 'учебниково', {"example_es": 'Una temperatura corporal de 37 grados es normal'}),
    13124: (T + 'повтор 6944 «tengo una resaca tremenda»', {"example_es": 'El día después de la boda todos estaban resacosos'}),
    14218: (T + '«señora Schmidt» — не испанская фамилия', {"example_es": 'En la excursión del colegio la persona de contacto, por si pasa algo, es la señora Gómez'}),
}

REPLACE = []

SPLIT_LATER = {}
