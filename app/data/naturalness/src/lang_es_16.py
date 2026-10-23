"""Вычитка испанского, порция p016 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    8055: (T + 'повтор «la llave»', {"example_es": 'Hurga en el bolso buscando el móvil'}),
    8056: (T + 'нет слова карточки «ágil»', {"example_es": 'El pequeño es ágil como una ardilla'}),
    8058: (T + '«radicalmente corto» — калька', {"example_es": 'He hecho un cambio radical: ¡pelo corto!'}),
    8083: (T + '«hace mucho bochorno» — коряво', {"example_es": '¿Salimos un momento? Aquí dentro uno se ahoga'}),
    8145: (T + 'повтор «desayuno incluido» (6819)', {"example_es": 'La cuota incluye diez clases de yoga'}),
    8166: (T + 'повтор 7017 «ha pasado mucho en su vida»', {"example_es": 'En esos años vivió momentos muy duros'}),
    8182: (T + 'повтор шаблона «los libros uno encima de otro»', {"example_es": 'Las cajas están una encima de otra en el sótano'}),
    8303: (T + '«Con esta guadaña he segado» — тавтология', {"example_es": 'Mi abuelo todavía siega la hierba con guadaña'}),
    8380: (T + '«mostrarte lo agradecido» — книжно', {"example_es": 'Te estoy muy agradecido por tu ayuda'}),
    8401: (T + '«atar la maleta» — неживо', {"example_es": 'Ata bien las bicis en el techo del coche'}),
    8409: (T + 'повтор «en otoño las hojas»', {"example_es": 'Se me ha caído un botón de la chaqueta'}),
    8440: (T + 'повтор «la llave»', {"example_es": 'Se me ha perdido el cargador'}),
    8595: (T + '«quieren corretear» — калька', {"example_es": 'Los niños corretean por el jardín'}),
    8660: (T + 'повтор «en otoño las hojas»', {"example_es": 'Mi hija quiere una habitación morada'}),
    8758: (T + '«Mi carrera es importante para mí» — калька', {"example_es": 'Para ella la carrera es lo primero'}),
    8782: (T + '«viven muchos animales» — учебниково', {"example_es": 'A los niños les encanta pasar las vacaciones en la granja'}),
    8829: (T + '«en Berlín» — без нужды', {"example_es": 'Mañana estoy en Bilbao por trabajo'}),
}

REPLACE = []

SPLIT_LATER = {}
