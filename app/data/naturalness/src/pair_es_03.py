"""Шаг 2, es, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    1673: (T + "word in example", {"t_es": "masculino, varonil, macho"}),
    6347: (T + "word in example", {"t_es": "conocido, famoso, (kommt mir bekannt vor) me suena"}),
    10027: (T + "word in example", {"t_es": "mejor, más bien, (lieber tun) preferir"}),
    10420: (T + "word in example", {"t_es": "ajeno, extraño, (ich bin fremd hier) no soy de aquí"}),
    12514: (T + "word in example", {"t_es": "el cigarrillo, el cigarro"}),
    17166: (T + "word in example", {"t_es": "el enlace, la conexión, el transbordo"}),
    17834: (T + "word in example", {"t_es": "el bien, la mercancía, la finca"}),
}

REPLACE = []
SPLIT_LATER = {}
