"""Вычитка итальянского, порция p030 (B2), 23.10: чувства — учебниковые фразы, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    10469: (T + "нет слова карточки «il fegato»", {"example_it": "Ci vuole fegato per dire di no al capo"}),
    10472: (T + "учебниково", {"example_it": "Non spingermi, decido da solo"}),
    10473: (T + "«Sei un fortunato ad aver vinto» — громоздко", {"example_it": "Che fortunato, ha vinto di nuovo!"}),
    10496: (T + "«si comporta come un idiota» — повтор шаблона", {"example_it": "Un po' di decenza, per favore!"}),
    10498: (T + "«svolgere questo compito» — книжно", {"example_it": "È incapace di cuocere un uovo"}),
    10509: (T + "«presa da lui, le piaceva tanto» — тавтология", {"example_it": "È rimasta subito presa dal suo umorismo"}),
    10515: (T + "«il bisogno di acqua è molto grande» — калька", {"example_it": "Ho sentito il bisogno di parlare con qualcuno"}),
    10521: (T + "«così caldo e bello» — книжно", {"example_it": "Vieni qui, dammi un abbraccio!"}),
    10522: (T + "«per le mie opere d'arte» — книжно", {"example_it": "La natura è la mia più grande ispirazione"}),
    10523: (T + "«perciò dobbiamo essere prudenti» — книжно", {"example_it": "È un tema delicato, attento a quello che dici"}),
    10530: (T + "учебниково", {"example_it": "Sono solo un povero peccatore, dice ridendo"}),
    10533: (T + "«Il tormento dell'attesa» — книжно", {"example_it": "Aspettare i risultati è un vero tormento"}),
    10555: (T + "«Il bambino è irrequieto» — учебниково", {"example_it": "Il bebè è irrequieto, forse stanno spuntando i denti"}),
    10570: (T + "без ситуации", {"example_it": "È davvero spiacevole che non possa venire"}),
    10581: (T + "повтор 10325 «mi ha rubato il parcheggio»", {"example_it": "Quel farabutto mi ha venduto una macchina rotta"}),
    10598: (T + "«Il bambino singhiozza» — учебниково", {"example_it": "Singhiozzava al telefono"}),
    10634: (T + "«Contro la decisione dell'ufficio» — книжно", {"example_it": "Contro la burocrazia purtroppo siamo impotenti"}),
    10662: (T + "повтор 10345 «idea stupida/idiota»", {"example_it": "Smettila di fare domande idiote"}),
    10755: (T + "повтор 10390 «… mi dice che qualcosa non va»", {"example_it": "Fidati della tua intuizione"}),
}

REPLACE = []

SPLIT_LATER = {}
