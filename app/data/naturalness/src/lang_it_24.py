"""Вычитка итальянского, порция p024 (B1), 23.10: право, власть, транспорт — повторы, учебниковые фразы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    15933: (T + "«Il giallo parla di un omicidio» — учебниково", {"example_it": "C'è stato un omicidio nel nostro quartiere"}),
    15938: (T + "повтор «nonno nell'esercito» (8744)", {"example_it": "Mio fratello fa il servizio nell'esercito"}),
    15947: (T + "«Amo la mia libertà» — без ситуации", {"example_it": "Da quando ho la patente, finalmente ho la mia libertà"}),
    15950: (T + "нет слова карточки «la galera»", {"example_it": "Si è fatto tre anni di galera"}),
    15951: (T + "«Mi serve una prova di questo» — коряво", {"example_it": "Hai delle prove?"}),
    15967: (T + "«può liberare» — калька", {"example_it": "La polizia ha liberato gli ostaggi"}),
    15973: (T + "«Il prigioniero sta nella sua cella» — учебниково", {"example_it": "Ha passato la notte in cella"}),
    15974: (T + "«difendere la mia opinione» — книжно", {"example_it": "Difende sempre la sorellina"}),
    15985: (T + "«L'imperatore ha governato il paese» — учебниково", {"example_it": "Napoleone si è fatto incoronare imperatore"}),
    15993: (T + "«Sono a disposizione» — оборвано", {"example_it": "Sono a tua disposizione se ti serve qualcosa"}),
    15995: (T + "«Il cane ci attacca» — неживо", {"example_it": "Il cane dei vicini ha attaccato il nostro gatto"}),
    15996: (T + "«Ho il sospetto che menta» — повтор шаблона", {"example_it": "Ho un sospetto, ma nessuna prova"}),
    16000: (T + "«A Berlino» — оставляем, но короче", {"example_it": "Il capitano ha dato l'ordine di ritirarsi"}),
    16006: (T + "«a Monaco» — без нужды", {"example_it": "Suo marito lavora come pubblico ministero a Bologna"}),
    16009: (T + "«I testimoni devono deporre» — тавтология", {"example_it": "La settimana prossima deve testimoniare in tribunale"}),
    16013: (T + "«aiutano i militari» — коряво", {"example_it": "Dopo l'alluvione i militari aiutano gli abitanti"}),
    16028: (T + "учебниково", {"example_it": "Nella fiaba tutto il regno è in pericolo"}),
    16089: (T + "«a Berlino» — без нужды", {"example_it": "Il congresso si terrà la settimana prossima a Roma"}),
    16099: (T + "«proteggere la mia privacy» — калька", {"example_it": "Non pubblico foto dei bambini, è la loro privacy"}),
    16101: (T + "повтор «sorveglia» (16029)", {"example_it": "Puoi custodirmi le cose mentre nuoto?"}),
    16104: (T + "повтор 16146 «La polizia ha arrestato»", {"example_it": "L'hanno fermato all'uscita del negozio"}),
    16106: (T + "«La mia quotidianità è ben organizzata» — книжно", {"example_it": "È tutto organizzato per il viaggio"}),
    16133: (T + "повтор 16152 «il re … anni»", {"example_it": "Chi governa il paese adesso?"}),
    16134: (T + "повтор 16128 «È in prigione»", {"example_it": "La rapina in banca è durata dieci minuti"}),
    16140: (T + "«Il sigillo è importante» — коряво", {"example_it": "La lettera porta il sigillo del re"}),
    16343: (T + "«sentenza saggia» — книжно", {"example_it": "La giudice è stata molto severa con lui"}),
    16345: (T + "«Mi occupi un posto?» — калька", {"example_it": "Questo posto è occupato?"}),
    16355: (T + "повтор 16717 «volante davanti a casa»", {"example_it": "La volante corre a sirene spiegate"}),
    16702: (T + "повтор 15976 «visita la nostra scuola»", {"example_it": "La ministra della salute parla stasera in tv"}),
    17057: (T + "повтор 17081 «Siamo sul/a bordo»", {"example_it": "Benvenuti a bordo!"}),
    17081: (T + "повтор 17057", {"example_it": "Sul ponte c'è vento, mettiti una giacca"}),
    17099: (T + "повтор «Di chi è …?» (13462)", {"example_it": "I veicoli oltre 3,5 tonnellate non possono passare"}),
    17105: (T + "«per Berlino» — без нужды", {"example_it": "L'aereo per Palermo parte alle otto"}),
}

REPLACE = []

SPLIT_LATER = {}
