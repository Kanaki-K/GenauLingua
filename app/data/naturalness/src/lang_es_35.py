"""Вычитка испанского, порция p035 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    15254: (T + '«señor Müller» — не испанская фамилия', {"example_es": 'Nuestro GPS habla con una voz masculina grave, mis hijos lo llaman señor Pérez'}),
    15312: (T + '«en Berlín» — без нужды', {"example_es": 'Su hijastra ahora estudia en Salamanca'}),
    16150: (T + 'нет слова карточки «la bandera»', {"example_es": 'Los aficionados agitan banderas en el estadio'}),
    16182: (T + '«Tienes que firmar» — калька', {"example_es": 'Firme aquí, por favor'}),
    16183: (T + '«Quieren acusarlo» — калька', {"example_es": 'Lo acusan de robo, pero no ha hecho nada'}),
    16186: (T + '«pero eso solo traería» — книжно', {"example_es": 'Después del ataque quería venganza, pero así solo habría más problemas'}),
    16198: (T + 'повтор 16189 «pasaporte falso»', {"example_es": 'Un bolso de Chanel a 30 euros es seguro una falsificación'}),
    16206: (T + '«por su mal comportamiento» — книжно', {"example_es": 'De castigo, una semana sin móvil'}),
    16256: (T + '«El código regula el comportamiento» — книжно', {"example_es": 'Entre los moteros hay un código de honor'}),
}

REPLACE = []

SPLIT_LATER = {}
