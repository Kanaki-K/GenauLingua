"""Вычитка итальянского, порция p017 (B1), 23.10: профессии и деньги — учебниковые фразы, тавтологии, повторы"""

T = "вычитка итальянского: "

FIXES = {
    8856: (T + "повтор 8769 «l'equipaggio dell'aereo è molto gentile»", {"example_it": "Tutto l'equipaggio della nave è sceso a terra"}),
    8863: (T + "«Il pittore ha dipinto» — тавтология", {"example_it": "L'imbianchino viene lunedì a ridipingere la cucina"}),
    8878: (T + "учебниково", {"example_it": "La cuoca della mensa fa le patatine più buone"}),
    8933: (T + "учебниково", {"example_it": "L'architetto ha disegnato i progetti della nostra casa"}),
    9030: (T + "«L'autrice ha scritto» — учебниково", {"example_it": "Sabato l'autrice firma copie in libreria"}),
    9040: (T + "повтор 8776 «appendere il quadro»", {"example_it": "Inchioda una tavola sulla vecchia recinzione"}),
    9050: (T + "«molto appagante» — книжно", {"example_it": "Ha una piccola attività in proprio: dà lezioni di chitarra"}),
    9137: (T + "повтор 8865 «tornare dal parrucchiere»", {"example_it": "Il barbiere sotto casa taglia benissimo"}),
    9161: (T + "учебниково", {"example_it": "La nuova recluta ha fatto fatica la prima settimana"}),
    9164: (T + "«ufficio competente» — канцелярит", {"example_it": "Per la carta d'identità devi andare all'ufficio anagrafe"}),
    9165: (T + "без ситуации", {"example_it": "L'incaricato della sicurezza controlla tutte le uscite"}),
    9482: (T + "учебниково", {"example_it": "Ha ricevuto un'educazione molto severa"}),
    9547: (T + "«L'apprendista impara» — тавтология", {"example_it": "L'apprendista del forno si alza alle tre"}),
    9589: (T + "без ситуации", {"example_it": "Sono stato bocciato all'esame di guida"}),
    9733: (T + "«Ricevo un assegno» — без ситуации", {"example_it": "La nonna mi ha mandato un assegno di 100 euro per il compleanno"}),
    9735: (T + "«parte del guadagno è piccola» — книжно", {"example_it": "Ognuno paga la sua parte"}),
    9758: (T + "повтор 1466 «portafoglio perso/sparito»", {"example_it": "Ho dimenticato il portafoglio a casa"}),
    9761: (T + "«Vogliamo donare … ai bambini poveri» — учебниково", {"example_it": "Ogni anno doniamo qualcosa a un'associazione"}),
    9915: (T + "повтор «Qual è il tuo …?»", {"example_it": "Mi mandi il numero di conto?"}),
}

REPLACE = []

SPLIT_LATER = {}
