"""Шаг 2, es, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    7088: (T + "word in example", {"t_es": "entrar a la fuerza, penetrar, entrar"}),
    7090: (T + "word in example", {"t_es": "infinito, interminable, infinitamente"}),
    7092: (T + "word in example", {"t_es": "cortar, salir, (abgeschnitten sein) quedarse incomunicado"}),
    18307: (T + "word in example", {"t_es": "la farola, el farol, el farolillo"}),
    18473: (T + "word in example", {"t_es": "el sitio para dormir, el lugar para dormir"}),
    19030: (T + "word in example", {"x_es": "La considero una buena idea, ¡vamos a intentarlo!"}),
}

REPLACE = []
SPLIT_LATER = {}
