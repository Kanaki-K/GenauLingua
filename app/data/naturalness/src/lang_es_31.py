"""Вычитка испанского, порция p031 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    10760: (T + 'повтор 10267 «debilidad por el chocolate»', {"example_es": 'Tiene cierta tendencia a exagerar'}),
    10816: (T + 'учебниково', {"example_es": 'Con el cansancio cambia la percepción del tiempo'}),
    11308: (T + '«en Múnich» — без нужды', {"example_es": 'Los alquileres en Madrid son increíblemente altos, por una habitación se paga lo que aquí por un piso'}),
    11716: (T + '«comemos pavo» — не тот быт', {"example_es": 'En Acción de Gracias los estadounidenses comen pavo'}),
    11728: (T + 'учебниково', {"example_es": 'Por nuestro aniversario nos dimos el capricho de un bogavante'}),
}

REPLACE = []

SPLIT_LATER = {}
