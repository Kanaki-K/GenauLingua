"""Вычитка испанского, порция p010 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    831: (T + '«Cada vez … más rara vez» — коряво', {"example_es": 'Nos vemos muy rara vez'}),
    1774: (T + '«¡Salud! Por tu salud» — тавтология', {"example_es": '¡Salud! ¡Por los novios!'}),
    1791: (T + 'повтор 13659 «el paraguas»', {"example_es": 'Con este viento se me ha roto el paraguas'}),
    1820: (T + '«El revisor controla» — тавтология', {"example_es": 'El revisor me ha puesto una multa'}),
    1877: (T + 'нет слова карточки «cuidadoso»', {"example_es": 'Es muy cuidadosa en su trabajo'}),
    1883: (T + 'повтор 857 «dar un paseo»', {"example_es": 'Un paseo después de cenar sienta bien'}),
    1898: (T + '«Llama constantemente» — без ситуации', {"example_es": 'Me interrumpe constantemente'}),
    1902: (T + 'повтор 1513 «La próxima parada es la estación central»', {"example_es": 'Bájate en la tercera parada'}),
    1908: (T + '«Los precios suben» — учебниково', {"example_es": 'La temperatura sigue subiendo'}),
    1944: (T + 'повтор «¿Tienes fiebre?»; нет слова «temperatura»', {"example_es": '¿Qué temperatura hace fuera?'}),
    1967: (T + '«Practico mucho deporte» — калька', {"example_es": 'Practica deporte desde pequeño'}),
    1996: (T + 'повтор «al trabajo en bici»', {"example_es": 'Para cuidar el medio ambiente, apaga la luz'}),
    2070: (T + '«Mañana me paso» — оборвано', {"example_es": '¿Me paso por tu casa esta tarde?'}),
    2080: (T + 'повтор 13931 «Mañana tengo una entrevista»', {"example_es": 'La entrevista de trabajo ha ido genial'}),
    2134: (T + '«Es muy fiable» — без ситуации', {"example_es": 'Marcos es muy fiable, puedes contar con él'}),
}

REPLACE = []

SPLIT_LATER = {}
