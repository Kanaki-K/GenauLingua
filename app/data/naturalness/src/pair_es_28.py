"""Шаг 2, es, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    8264: (T + "word in example", {"t_es": "cubrir, salvar, entretener (el hambre)"}),
    8403: (T + "word in example", {"t_es": "el uno delante del otro, (Geheimnisse voreinander) el uno con el otro"}),
    8411: (T + "word in example", {"t_es": "inútil, inútilmente"}),
}

REPLACE = []
SPLIT_LATER = {}
