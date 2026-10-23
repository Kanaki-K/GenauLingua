"""Вычитка итальянского, порция p010 (B1), 23.10: повторы («La prossima fermata è la stazione centrale», «colloquio di lavoro», «ombrello»), тавтологии, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    1791: (T + "повтор 13659 «Ho dimenticato l'ombrello»", {"example_it": "Con questo vento si è rotto l'ombrello"}),
    1820: (T + "«Il controllore controlla» — тавтология", {"example_it": "Il controllore mi ha fatto la multa"}),
    1877: (T + "нет слова карточки «accurato»", {"example_it": "È una persona molto accurata nel lavoro"}),
    1883: (T + "повтор 857 «fare una passeggiata»", {"example_it": "Una passeggiata dopo cena fa bene"}),
    1898: (T + "«Chiama continuamente» — без ситуации", {"example_it": "Mi interrompe continuamente"}),
    1902: (T + "повтор 1513 «La prossima fermata è la stazione centrale»", {"example_it": "Scendi alla terza fermata"}),
    1908: (T + "«I prezzi aumentano» — учебниково", {"example_it": "La temperatura sale ancora"}),
    1944: (T + "повтор «Hai la febbre?»; нет слова «temperatura»", {"example_it": "Che temperatura c'è fuori?"}),
    1967: (T + "«Pratico molto sport» — калька", {"example_it": "Pratica sport da quando era piccolo"}),
    1996: (T + "повтор «al lavoro in bici»", {"example_it": "Per l'ambiente usiamo meno plastica"}),
    2070: (T + "«Passo domani» — оборвано", {"example_it": "Passo da te stasera?"}),
    2080: (T + "повтор 13931 «Domani ho un colloquio»", {"example_it": "Il colloquio di lavoro è andato benissimo"}),
    2134: (T + "«È molto affidabile» — без ситуации", {"example_it": "Marco è molto affidabile, puoi contare su di lui"}),
}

REPLACE = []

SPLIT_LATER = {}
