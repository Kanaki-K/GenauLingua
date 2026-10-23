"""Вычитка итальянского, порция p009 (B1), 23.10: повторы («moneta per il carrello», «si è bloccato di nuovo», «clicca sul link»), голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    1397: (T + "«Apriamo un nuovo negozio» — учебниково", {"example_it": "In via Roma inaugurano un nuovo negozio"}),
    1445: (T + "повтор 8865 «dal parrucchiere»", {"example_it": "La parrucchiera mi ha tagliato troppo i capelli"}),
    1447: (T + "повтор 17481 «Come funziona»", {"example_it": "La lavastoviglie non funziona più"}),
    1452: (T + "«Compro una macchina usata» — учебниково", {"example_it": "Lo zaino l'ho comprato usato"}),
    1457: (T + "«Schmidt / Weber» — не итальянские фамилии", {"example_it": "Il suo cognome da nubile è Rossi, ma dal matrimonio si chiama Bianchi"}),
    1467: (T + "повтор 151, 1707 «moneta per il carrello»", {"example_it": "In questa fontana i turisti buttano monete"}),
    1519: (T + "«Il custode lo ripara» — без ситуации", {"example_it": "Il custode ha già cambiato la lampadina"}),
    1532: (T + "«Giriamo intorno alla città» — коряво", {"example_it": "Intorno al lago c'è un sentiero"}),
    1566: (T + "«Il libro è da qualche parte» — учебниково", {"example_it": "Il telecomando è da qualche parte sul divano"}),
    1572: (T + "«si incontrano qui» — без ситуации", {"example_it": "I ragazzi del quartiere si incontrano al parco"}),
    1590: (T + "повтор 1946 «Domani facciamo un test»", {"example_it": "Il compito in classe di matematica è andato bene"}),
    1595: (T + "повтор 1138 «Clicca sul link»", {"example_it": "Clicca due volte sull'icona"}),
    1640: (T + "повтор 2714 «si è bloccato di nuovo»", {"example_it": "Porto il portatile in ufficio ogni giorno"}),
    1663: (T + "«Partiamo alle 8» — учебниково", {"example_it": "Partiamo appena smette di piovere"}),
    1707: (T + "повтор 151 «moneta per il carrello»", {"example_it": "Colleziono monete antiche"}),
    1712: (T + "повтор 450 «ti richiamo dopo»", {"example_it": "Ci vediamo dopo al bar"}),
    1728: (T + "«a Berlino» — без нужды", {"example_it": "Mia nipote studia a Bologna"}),
    1734: (T + "«Non è necessario» — оборвано", {"example_it": "Non è necessario portare niente"}),
    1758: (T + "«È il mio dovere» — калька", {"example_it": "Non è un favore, è un tuo dovere"}),
}

REPLACE = []

SPLIT_LATER = {}
