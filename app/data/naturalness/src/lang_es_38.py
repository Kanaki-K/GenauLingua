"""Вычитка испанского, порция p038 (B2/C1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    18663: (T + 'повтор 18922 «descansar después de comer»', {"example_es": 'Déjalo descansar, está enfermo'}),
    18728: (T + '«me ayuda a mantenerme organizado» — калька', {"example_es": 'Por las mañanas tengo mi pequeña rutina: café, ducha, periódico'}),
    18747: (T + 'повтор 18772 «pescar al amanecer»', {"example_es": 'Salimos al amanecer para evitar el tráfico'}),
    18810: (T + '«en Berlín» — без нужды', {"example_es": 'Viví durante un tiempo en Madrid, pero a la larga la ciudad era demasiado ruidosa para mí'}),
    7553: (T + '«con gusto» — норм, но короче', {"example_es": 'Para el viaje largo te cedo mi asiento de la ventanilla'}),
    7668: (T + '«esforzar mucho la vista» — калька', {"example_es": 'Leer sin gafas me cansa la vista'}),
}

REPLACE = []

SPLIT_LATER = {}
