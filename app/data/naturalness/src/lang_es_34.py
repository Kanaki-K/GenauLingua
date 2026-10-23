"""Вычитка испанского, порция p034 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    14465: (T + 'повтор 15429 «hace volar una cometa»', {"example_es": 'En el cuento el caballero mata al dragón'}),
    14512: (T + 'повтор 12141 «los espectadores aplauden»', {"example_es": 'Los niños aplauden cada truco del mago'}),
    14526: (T + 'учебниково', {"example_es": 'El capellán del hospital pasa a ver a los enfermos'}),
    14541: (T + '«Mi familia religiosa celebra» — калька', {"example_es": 'Mis abuelos son muy religiosos'}),
    15045: (T + '«es muy feliz con nosotros» — коряво', {"example_es": 'Su hijo adoptivo es de Colombia'}),
    15106: (T + '«spätzle» — не испанский быт', {"example_es": 'Mi madrastra me enseñó a hacer croquetas caseras'}),
}

REPLACE = []

SPLIT_LATER = {}
