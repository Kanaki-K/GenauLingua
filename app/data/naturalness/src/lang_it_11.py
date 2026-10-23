"""Вычитка итальянского, порция p011 (B1), 23.10: повторы («dormire fino a tardi», «invece di …», «ci dividiamo»), нет слова карточки, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    18752: (T + "повтор 2233 «dormire fino a tardi»", {"example_it": "La domenica pranziamo sempre dai nonni"}),
    2178: (T + "«Non toccarlo» — без ситуации", {"example_it": "Non toccare, scotta!"}),
    2192: (T + "повтор 1903 «Invece di …»", {"example_it": "Anziché lamentarti, aiutami"}),
    2205: (T + "«È davvero fastidioso» — без ситуации", {"example_it": "Questo rumore è davvero fastidioso"}),
    2217: (T + "нет слова карточки «attento»", {"example_it": "È un ragazzo molto attento in classe"}),
    2220: (T + "«Scrivitelo» — оборвано", {"example_it": "Scrivi l'indirizzo, se no lo dimentichi"}),
    2221: (T + "повтор 6382 «Ci dividiamo»", {"example_it": "Il lavoro lo dividiamo in tre"}),
    2258: (T + "«Puoi tenerlo» — без ситуации", {"example_it": "Il libro puoi tenerlo, te lo regalo"}),
    2286: (T + "«sconfitto l'avversario» — книжно", {"example_it": "Abbiamo battuto la squadra più forte del campionato"}),
    2290: (T + "«Non puoi entrare nella stanza» — учебниково", {"example_it": "Non ho mai messo piede in quella casa"}),
    2309: (T + "«Foro il muro con il trapano» — тавтология", {"example_it": "La domenica non si può forare il muro"}),
    2311: (T + "«Fa allenamento di boxe» — коряво", {"example_it": "Mia figlia fa boxe due volte a settimana"}),
    2335: (T + "повтор 1397 «un nuovo negozio»", {"example_it": "Prossimamente al cinema"}),
    2339: (T + "повтор 2093 «sono malato»", {"example_it": "Domani c'è sciopero, per questo vado in bici"}),
    2342: (T + "повтор «è diabetico» (13061)", {"example_it": "Per i diabetici ci sono dolci senza zucchero"}),
    2353: (T + "«Pago il doppio del prezzo» — без ситуации", {"example_it": "Il biglietto all'ultimo minuto costa il doppio"}),
    2385: (T + "повтор 2184 «Accendi la …»", {"example_it": "Chi ha acceso la radio?"}),
    2426: (T + "«Dobbiamo aumentare i prezzi» — без ситуации", {"example_it": "Il proprietario vuole aumentare l'affitto"}),
    2430: (T + "«Ho bisogno di una spiegazione» — калька", {"example_it": "Esigo una spiegazione!"}),
}

REPLACE = []

SPLIT_LATER = {}
