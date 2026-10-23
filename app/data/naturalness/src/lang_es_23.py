"""Вычитка испанского, порция p023 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    15152: (T + '«Deberíamos tratar al prójimo» — книжно', {"example_es": 'Hay que ayudar al prójimo'}),
    15166: (T + '«me duele el muslo de correr» — коряво', {"example_es": 'Después de la carrera me duelen los muslos'}),
    15206: (T + '«Me duele el codo, me he caído» — коряво', {"example_es": 'Me he caído sobre el codo'}),
    15209: (T + '«en Berlín» — без нужды', {"example_es": 'Mi medio hermano vive en Granada'}),
    15263: (T + '«El niño crece» — учебниково', {"example_es": 'Se crió en un orfanato'}),
    15314: (T + '«El niño está sentado» — учебниково', {"example_es": 'El peque ya sabe usar el orinal solo'}),
    15388: (T + '«quiere cazar» — калька', {"example_es": 'El gato caza ratones en el desván'}),
    15402: (T + '«Estamos sentados a la sombra» — учебниково', {"example_es": 'Ven a sentarte a la sombra, hace mucho calor'}),
    15411: (T + 'повтор 15574 «tumbarse en la hierba»', {"example_es": 'Esta mañana la hierba todavía está mojada'}),
    15443: (T + 'повтор 15744 «la gallina pone un huevo»', {"example_es": 'Los vecinos tienen cinco gallinas en el jardín'}),
    15444: (T + '«Queremos plantar tomates» — учебниково', {"example_es": 'Vamos a plantar un árbol por el nacimiento del bebé'}),
    15455: (T + 'повтор 10227 «El ambiente aquí es…»', {"example_es": 'En esta casa hay un ambiente raro'}),
    15463: (T + '«cruzamos el océano en avión» — неживо', {"example_es": 'Mi sueño es cruzar el océano en barco'}),
    15465: (T + '«fuera hace un frío insoportable» — калька', {"example_es": 'No soporto el frío'}),
    15475: (T + '«La helada de esa noche» — книжно', {"example_es": 'Con la helada se murieron las flores del balcón'}),
    15482: (T + '«La oscuridad de la noche» — книжно', {"example_es": 'Mi hijo tiene miedo a la oscuridad'}),
    15609: (T + 'учебниково', {"example_es": 'El tractor ara el campo'}),
    15618: (T + 'повтор 15454 «dar de comer a los peces»', {"example_es": 'El dentista tiene un acuario enorme en la sala de espera'}),
    15786: (T + '«y hemos disfrutado de la naturaleza» — книжно', {"example_es": 'Hemos paseado por la orilla del río'}),
    15859: (T + 'повтор «canta por la mañana» (15727)', {"example_es": 'La abuela tiene un canario que se llama Piolín'}),
}

REPLACE = []

SPLIT_LATER = {}
