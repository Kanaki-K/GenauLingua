"""Вычитка итальянского, порция p006 (A2), 23.10: повторы («le chiavi», «la nostra squadra ha vinto», «dipendenti», «non vedo l'ora»), нет слова карточки, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    481: (T + "повтор 14413 «chiuso il lunedì»", {"example_it": "Stasera c'è un bel film al cinema"}),
    1691: (T + "повтор 8946 «L'azienda ha … dipendenti»", {"example_it": "Il dipendente del mese riceve un buono"}),
    6326: (T + "«È troppo pericoloso» — без ситуации", {"example_it": "Non sporgerti, è pericoloso!"}),
    6528: (T + "«I soldi sono scarsi» — без ситуации", {"example_it": "A fine mese i soldi sono sempre scarsi"}),
    6585: (T + "повтор «le chiavi»", {"example_it": "Dove hai nascosto i regali?"}),
    6646: (T + "«Devo superare l'esame» — учебниково", {"example_it": "Ha superato l'esame al primo tentativo"}),
    6726: (T + "повтор «le chiavi»", {"example_it": "Non lo trovo da nessuna parte"}),
    7057: (T + "«a Colonia» — без нужды", {"example_it": "Mio marito questa settimana è a una fiera a Milano"}),
    7464: (T + "нет слова карточки «il bene»", {"example_it": "Lo faccio per il tuo bene"}),
    7711: (T + "«Iscriviti» — не то слово", {"example_it": "Scrivi il tuo nome nella lista"}),
    8818: (T + "повтор «il conto»", {"example_it": "Il cameriere è stato gentilissimo"}),
    8868: (T + "«lavora nello stesso ufficio» — учебниково", {"example_it": "La mia collega mi sostituisce quando sono malato"}),
    8994: (T + "повтор 8980 «candidatura»", {"example_it": "Ti sei candidato per quel posto?"}),
    9460: (T + "повтор 126 «Hai una matita?»", {"example_it": "Questa penna non scrive più"}),
    9591: (T + "«simpatici e disponibili» — книжно", {"example_it": "Con i miei compagni di classe vado d'accordissimo"}),
    10064: (T + "«Stai attento» — оборвано", {"example_it": "Stai attento, la strada è ghiacciata"}),
    10073: (T + "повтор 13335 «Non me ne ricordo»", {"example_it": "Ti ricordi di me?"}),
    10077: (T + "«È proprio strano» — без ситуации", {"example_it": "Che strano, la porta è aperta"}),
    10091: (T + "«Sono innamorato» — повтор 2040", {"example_it": "È innamorata persa di lui"}),
    10102: (T + "повтор «divertente» (562)", {"example_it": "Tuo padre è proprio spiritoso"}),
    10129: (T + "нет слова карточки «l'interesse»", {"example_it": "Non ho nessun interesse per il calcio"}),
    11772: (T + "повтор 599 «in mensa»", {"example_it": "La caffetteria dell'università è sempre piena"}),
    12108: (T + "«Stasera esco» — оборвано", {"example_it": "Il sabato sera esco con gli amici"}),
    12140: (T + "«Al circo ci sono molti animali» — учебниково", {"example_it": "I bambini vogliono andare al circo"}),
    12142: (T + "повтор 1934 «La nostra squadra ha vinto»", {"example_it": "La squadra si allena tre volte a settimana"}),
    12474: (T + "«Sono ancora sveglio» — без ситуации", {"example_it": "Sei ancora sveglio?"}),
    12477: (T + "«C'è stato un incidente» — оборвано", {"example_it": "C'è stato un incidente in autostrada"}),
    12529: (T + "повтор 199 «fare una doccia veloce»", {"example_it": "I bambini non vogliono mai fare la doccia"}),
    12620: (T + "«Il profumo ha un buon odore» — тавтология", {"example_it": "Che buon profumo! Cos'è?"}),
    13295: (T + "повтор «È tuo/tua …?» (171)", {"example_it": "Il tuo treno parte tra dieci minuti"}),
    13338: (T + "повтор 289 «Non vedo l'ora»", {"example_it": "Ci puoi contare"}),
    13430: (T + "повтор 1326 «Piove, perciò»", {"example_it": "Il treno è in ritardo, quindi prendo un taxi"}),
    13447: (T + "«Un milione … sono molti soldi» — учебниково", {"example_it": "Se vincessi un milione, smetterei di lavorare"}),
    13843: (T + "«La tua voce è bella» — калька", {"example_it": "Hai una voce bellissima"}),
    13853: (T + "«È una bella barzelletta» — калька", {"example_it": "Raccontami una barzelletta!"}),
    13901: (T + "повтор 945 «Ciao, a domani»", {"example_it": "Ciao ciao, a presto!"}),
    14923: (T + "повтор «torte buonissime» (904)", {"example_it": "Mia zia abita in campagna"}),
    14944: (T + "«Mio fratello è già adulto» — учебниково", {"example_it": "Ormai sei grande, decidi tu"}),
    14979: (T + "«Sono cresciuto qui» — без ситуации", {"example_it": "Sono cresciuto a Napoli"}),
    15394: (T + "«L'uccello canta sull'albero» — учебниково", {"example_it": "Un uccello ha fatto il nido sul balcone"}),
    15926: (T + "«Il re porta una corona» — учебниково", {"example_it": "Il re di Spagna è in visita a Roma"}),
    17483: (T + "повтор 8448 «Guarda un po'»", {"example_it": "Ho fatto un video del concerto"}),
}

REPLACE = []

SPLIT_LATER = {}
