"""Вычитка испанского, порция p030 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    10469: (T + 'нет слова карточки «las agallas»', {"example_es": 'Hay que tener agallas para decirle que no al jefe'}),
    10472: (T + 'учебниково', {"example_es": 'No me presiones, decido yo solo'}),
    10473: (T + '«por haber ganado la lotería» — громоздко', {"example_es": '¡Qué suertudo, ha vuelto a ganar!'}),
    10496: (T + '«se comporta como un idiota» — шаблон', {"example_es": '¡Un poco de decencia, por favor!'}),
    10498: (T + '«hacer esta tarea» — книжно', {"example_es": 'Es incapaz de freír un huevo'}),
    10509: (T + '«prendada de él, le gustaba mucho» — тавтология', {"example_es": 'Se quedó prendada de su sentido del humor'}),
    10515: (T + '«la necesidad de agua es muy grande» — калька', {"example_es": 'Sentí la necesidad de hablar con alguien'}),
    10521: (T + '«tan cálido y bonito» — книжно', {"example_es": '¡Ven aquí, dame un abrazo!'}),
    10522: (T + '«para mis obras de arte» — книжно', {"example_es": 'La naturaleza es mi mayor fuente de inspiración'}),
    10523: (T + '«por eso tenemos que tener cuidado» — книжно', {"example_es": 'Es un tema delicado, cuidado con lo que dices'}),
    10530: (T + 'учебниково', {"example_es": 'Solo soy un pobre pecador, dice riéndose'}),
    10533: (T + '«El tormento de esperar una respuesta» — книжно', {"example_es": 'Esperar los resultados es un auténtico tormento'}),
    10555: (T + '«El niño está inquieto» — учебниково', {"example_es": 'El bebé está inquieto, seguro que le están saliendo los dientes'}),
    10581: (T + 'повтор 10325 «me ha quitado el aparcamiento»', {"example_es": 'Ese sinvergüenza me vendió un coche averiado'}),
    10598: (T + '«El niño solloza» — учебниково', {"example_es": 'Sollozaba al teléfono'}),
    10634: (T + '«frente a la decisión de la administración» — книжно', {"example_es": 'Contra la burocracia, por desgracia, somos impotentes'}),
    10662: (T + 'повтор 10345 «una idea idiota»', {"example_es": 'Deja de hacer preguntas idiotas'}),
    10755: (T + 'повтор 10390 «… me dice que algo no va bien»', {"example_es": 'Fíate de tu intuición'}),
}

REPLACE = []

SPLIT_LATER = {}
