"""Вычитка итальянского, порция p003 (A1/A2), 23.10: повторы («dal medico», «… anni», «gentile»), голые фразы, «volentieri»"""

T = "вычитка итальянского: "

FIXES = {
    267: (T + "повтор 11635 «La cena è pronta»", {"example_it": "Sei pronto? Usciamo"}),
    826: (T + "повтор 14375 «mi piace molto la canzone»", {"example_it": "Oggi fa molto caldo"}),
    1426: (T + "«Voliamo in Spagna» — учебниково", {"example_it": "Domani voliamo a Barcellona"}),
    1441: (T + "«Nel mio tempo libero» — калька", {"example_it": "Nel tempo libero leggo molto"}),
    1458: (T + "«Il mio luogo di nascita è Berlino» — канцелярит", {"example_it": "Nel modulo scrivi anche il luogo di nascita"}),
    1463: (T + "«Il libro mi appartiene» — книжно", {"example_it": "Di chi è questa borsa? – Appartiene a mia sorella"}),
    1589: (T + "нет слова карточки «la classe»", {"example_it": "In classe siamo in venticinque"}),
    1695: (T + "«Partecipo volentieri» — калька gern", {"example_it": "Chi vuole partecipare alla gara?"}),
    1739: (T + "повтор 1542 «scaffale … alto»", {"example_it": "Le coperte sono di sopra"}),
    2007: (T + "«Aspetto giù» — оборвано", {"example_it": "Ti aspetto giù al portone"}),
    2109: (T + "повтор 1032 «Il tempo è …»", {"example_it": "Che giornata meravigliosa!"}),
    2354: (T + "«Prenoto una camera doppia» — учебниково", {"example_it": "Vorrei una camera doppia per due notti"}),
    2453: (T + "«Mandami un fax» — устарело", {"example_it": "Chi usa ancora il fax?"}),
    6228: (T + "«È molto lontano» — без ситуации", {"example_it": "La stazione è lontana da qui?"}),
    6250: (T + "повтор 6292 «La borsa è …»", {"example_it": "L'esame è stato più difficile del previsto"}),
    6252: (T + "«Guarda qui» — без ситуации", {"example_it": "Guarda, nevica!"}),
    6483: (T + "повтор 68 «al secondo piano»", {"example_it": "L'ufficio è al terzo piano"}),
    8334: (T + "нет слова карточки «completare»", {"example_it": "Completa le frasi con le parole giuste"}),
    8735: (T + "повтор 41 «Il lavoro mi piace»", {"example_it": "Ho trovato un nuovo lavoro!"}),
    8797: (T + "«mi aiuta al lavoro» — учебниково", {"example_it": "Il mio collega oggi è in ferie"}),
    9441: (T + "повтор 8742 «Il mio … è gentile»", {"example_it": "La maestra di mia figlia è giovanissima"}),
    10438: (T + "«Mi congratulo con te per il tuo successo» — книжно", {"example_it": "Ti faccio gli auguri per la promozione!"}),
    12121: (T + "повтор 2176 «L'inizio … difficile»", {"example_it": "Alla partenza della gara erano in cento"}),
    13282: (T + "повтор 13331 «dal medico»", {"example_it": "Vado al mare con gli amici"}),
    13293: (T + "«Sono alla stazione» — учебниково", {"example_it": "Ci vediamo al bar alle sei"}),
    13314: (T + "повтор 13331 «dal medico»", {"example_it": "Arrivo adesso dal lavoro"}),
    13375: (T + "повтор «Ho … anni» (13388, 13526)", {"example_it": "Ho dieci minuti di pausa"}),
    13387: (T + "повтор 52 «Mi alzo alle …»", {"example_it": "Lavoro otto ore al giorno"}),
    13392: (T + "повтор «la chiave» (271)", {"example_it": "Qualcuno ha bussato alla porta"}),
    13498: (T + "повтор «Ho … anni»", {"example_it": "Ci vediamo tra venti minuti"}),
    13968: (T + "повтор 1039 «Arrivederci»", {"example_it": "Grazie della telefonata, arrivederci!"}),
    14913: (T + "повтор 8742 «Il mio … è molto gentile»", {"example_it": "Il mio partner cucina benissimo"}),
    15183: (T + "нет слова карточки «single»", {"example_it": "È ancora single"}),
    17202: (T + "повтор 1211 «Il treno … binario tre»", {"example_it": "Scusi, è questo il binario per Milano?"}),
    17250: (T + "«Visitiamo il nuovo appartamento» — учебниково", {"example_it": "Domani visitiamo il Colosseo"}),
    17342: (T + "повтор 17335 «i monumenti»", {"example_it": "La guida turistica parlava anche italiano"}),
    17489: (T + "«Ripara la macchina» — учебниково", {"example_it": "Mio padre ripara tutto da solo"}),
    18610: (T + "повтор 595 «Aspetta un minuto»", {"example_it": "Un secondo, arrivo!"}),
}

REPLACE = []

SPLIT_LATER = {}
