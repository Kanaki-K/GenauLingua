"""Вычитка итальянского, порция p004 (A2), 23.10: повторы («farmacia», «Questa è la … casa», «la nonna fa…»), кальки, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    81: (T + "«Costruiscono una casa» — без ситуации", {"example_it": "I vicini si stanno costruendo una casa nuova"}),
    128: (T + "«La camicetta veste bene» — калька", {"example_it": "Questa camicetta è perfetta per l'ufficio"}),
    161: (T + "«Sono a favore» — не то значение", {"example_it": "Per questo sono arrivato tardi"}),
    170: (T + "«prendere con questo» — калька", {"example_it": "Cosa ci bevi con la pizza?"}),
    171: (T + "повтор «Questa è la … » (426, 963)", {"example_it": "È tua questa borsa?"}),
    186: (T + "«a Berlino» — без нужды", {"example_it": "Il treno va direttamente a Roma"}),
    189: (T + "повтор «la farmacia» (39, 318, 1089)", {"example_it": "Il parcheggio è lì, dietro il supermercato"}),
    216: (T + "«Mi piace mangiare il gelato» — учебниково", {"example_it": "Andiamo a prendere un gelato?"}),
    234: (T + "«a Berlino» — без нужды", {"example_it": "È la mia prima volta a Venezia"}),
    289: (T + "повтор 293 «Sono contento»; нет «non vedere l'ora»", {"example_it": "Non vedo l'ora di vederti!"}),
    318: (T + "повтор «la farmacia»", {"example_it": "Abito proprio di fronte al parco"}),
    355: (T + "«Ha l'influenza» — без ситуации", {"example_it": "Mezza classe ha l'influenza"}),
    423: (T + "«Ho una buona idea» — калька", {"example_it": "Ho un'idea!"}),
    459: (T + "«Il cibo si fredda» — калька", {"example_it": "La pasta si fredda, vieni subito!"}),
    471: (T + "повтор 450 «non ho tempo»", {"example_it": "Non c'è nessun problema"}),
    538: (T + "нет слова карточки «noioso»", {"example_it": "Questo film è noiosissimo"}),
    568: (T + "повтор «al lavoro in…» (72)", {"example_it": "A volte mi sveglio di notte"}),
    582: (T + "повтор «Questo è il mio …»", {"example_it": "Hai visto il mio telefono?"}),
    614: (T + "повтор 615 «la mattina sono sempre…»", {"example_it": "Domani mattina parto presto"}),
    657: (T + "«Dillo di nuovo» — грубовато", {"example_it": "Me lo spieghi di nuovo?"}),
    662: (T + "«Cucino la pasta per pranzo» — учебниково", {"example_it": "Stasera faccio la pasta al pomodoro"}),
    676: (T + "повтор 904 «la nonna fa … più buona»", {"example_it": "La nonna abita con noi"}),
    677: (T + "«Fa acquisti online» — книжно", {"example_it": "Compro quasi tutto online"}),
    686: (T + "«A est d'inverno fa freddo» — калька", {"example_it": "La sua famiglia viene dall'Europa dell'Est"}),
    773: (T + "«Porta lo zaino sulla schiena» — учебниково", {"example_it": "Ho mal di schiena"}),
    782: (T + "повтор 573 «il mercato»", {"example_it": "Il sabato dormo fino a tardi"}),
    784: (T + "«È un peccato» — учебниково", {"example_it": "Peccato, non posso venire"}),
    792: (T + "«La nave salpa» — книжно", {"example_it": "La nave per la Sardegna parte alle nove"}),
    814: (T + "«È incinta» — без ситуации", {"example_it": "Mia sorella è incinta di tre mesi"}),
    840: (T + "«Mi piace cantare» — учебниково", {"example_it": "Canta sempre sotto la doccia"}),
    842: (T + "повтор 1043 «andare a sciare»", {"example_it": "Ho noleggiato gli sci"}),
    923: (T + "«Giochiamo a tennis» — учебниково", {"example_it": "Giochi a tennis?"}),
    941: (T + "«Ci incontriamo alle tre» — повтор «alle tre»", {"example_it": "Ho incontrato Paolo in centro"}),
    963: (T + "повтор «Questa è la … casa» (426)", {"example_it": "La nostra casa è in fondo alla via"}),
    976: (T + "повтор «le chiavi»", {"example_it": "Ho dimenticato il compleanno di mia madre!"}),
    1011: (T + "повтор 223 «dov'è il bagno»", {"example_it": "Il WC è in fondo al corridoio"}),
}

REPLACE = []

SPLIT_LATER = {}
