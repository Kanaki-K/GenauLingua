"""Вычитка итальянского, порция p045 (C1/C2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    8286: (T + '«volentieri» — калька', {"example_it": 'Mi ha aiutato di buon grado'}),
    8359: (T + 'повтор 10364 «resistere al cioccolato»', {"example_it": 'Alla fine ha ceduto alla tentazione'}),
    8393: (T + 'без ситуации', {"example_it": 'La presenza non è strettamente necessaria'}),
    8487: (T + '«Devi proprio» — калька', {"example_it": 'Smettila di ficcanasare tra le mie cose!'}),
    8498: (T + '«il nostro incontro» — книжно', {"example_it": 'Fissiamo una data?'}),
    8572: (T + '«Dobbiamo» — калька', {"example_it": 'Bisogna modificare il piano per renderlo più realistico'}),
}

REPLACE = []

SPLIT_LATER = {}
