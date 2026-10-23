"""Вычитка итальянского, порция p048 (C2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    14320: (T + 'повтор 7204 «prestazione notevole»', {"example_it": 'È stata davvero una bella serata'}),
    14688: (T + '«volentieri» — калька', {"example_it": 'Ti riparo il portatile, ma non sono mica uno stregone!'}),
    14777: (T + '«volentieri» — калька', {"example_it": 'Ascolta ancora il suo vecchio disco dei Beatles'}),
    15260: (T + '«a Berlino» — без нужды', {"example_it": 'Mio padre biologico vive a Torino'}),
    15278: (T + "повтор 12129 «senza l'orsacchiotto non si addormenta»", {"example_it": 'Mio figlio ha ricevuto un orsetto alla nascita'}),
    15783: (T + 'без ситуации', {"example_it": "Con la bassa marea si può camminare fino all'isola"}),
    15845: (T + '«frigorifero» — книжно', {"example_it": 'Il vecchio frigo finisce in discarica'}),
    15855: (T + '«domato e tranquillo» — учебниково', {"example_it": 'Questo cavallo selvaggio è stato domato in un mese'}),
    16652: (T + '«racconta volentieri» — калька', {"example_it": 'Mio nonno racconta spesso di quando da studente ha passato una notte in galera per essersi arrampicato su una fontana'}),
    16694: (T + 'повтор 7028 «giocare a carte per passare il tempo»', {"example_it": 'Per ammazzare il tempo in aeroporto leggo'}),
}

REPLACE = []

SPLIT_LATER = {}
