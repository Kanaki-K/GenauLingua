"""Вычитка итальянского, порция p021 (B1), 23.10: служебные слова, одежда, речь — повторы, нет слова карточки, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    13008: (T + "«L'infiammazione è guarita» — неживо", {"example_it": "Ho un'infiammazione al ginocchio"}),
    13097: (T + "учебниково", {"example_it": "Il mio medico di famiglia va in pensione, ne devo trovare un altro"}),
    13369: (T + "«Mi serve qualcosa da mangiare» — калька", {"example_it": "Hai qualcosa da mangiare?"}),
    13394: (T + "нет слова карточки «di qua»", {"example_it": "Vieni di qua, c'è posto"}),
    13407: (T + "«Né tu né io lo sappiamo» — книжно", {"example_it": "Non ho né tempo né soldi"}),
    13473: (T + "нет слова карточки «tale/così»", {"example_it": "Con un tempo così restiamo a casa"}),
    13478: (T + "повтор «primo, non ho tempo»", {"example_it": "Primo, si fanno i compiti, poi la tv"}),
    13508: (T + "нет слова карточки «quarto»", {"example_it": "È arrivato quarto nella gara"}),
    13558: (T + "повтор 6838 «già il …° caffè di oggi»", {"example_it": "Abito al settimo piano e l'ascensore è rotto"}),
    13590: (T + "«un decimo della popolazione vive in città» — неверно", {"example_it": "Ha perso per un decimo di secondo"}),
    13645: (T + "«il bottone non c'è più» — без ситуации", {"example_it": "Mi puoi riattaccare questo bottone?"}),
    13660: (T + "повтор 13703 «travestito da pirata»", {"example_it": "Alla festa sono venuti tutti mascherati"}),
    13662: (T + "повтор 12339 «lasciare … nello spogliatoio/al guardaroba»", {"example_it": "A teatro si lasciano i cappotti al guardaroba"}),
    13769: (T + "повтор 13719 «gira tutta la domenica»", {"example_it": "Mio nonno beve il caffè in vestaglia"}),
    13817: (T + "повтор «le chiavi»", {"example_it": "Maledizione, ho perso il treno!"}),
    13861: (T + "«Sissignore, lo faccio» — коряво", {"example_it": "Sissignore, capo!"}),
    13866: (T + "«Guardo con i sottotitoli» — оборвано", {"example_it": "Guardo le serie con i sottotitoli"}),
    13881: (T + "нет слова карточки «lo scherzo»", {"example_it": "Era solo uno scherzo!"}),
    13884: (T + "повтор 8796 «Non combinare sciocchezze»", {"example_it": "Smettila di dire stupidaggini"}),
    13893: (T + "«parla dell'evento» — учебниково", {"example_it": "Tutta la stampa parla del matrimonio del principe"}),
    13911: (T + "«Ecco un'indicazione importante» — канцелярит", {"example_it": "Grazie per il suggerimento!"}),
    13924: (T + "«Posso semplicemente ignorare» — калька", {"example_it": "Ignora i suoi commenti stupidi"}),
    13925: (T + "«Puoi ascoltarlo un attimo?» — калька", {"example_it": "Ascolta un po' questo!"}),
    13957: (T + "повтор 13877 «No, non mi va»", {"example_it": "Hai fame? – No, sto bene"}),
    13973: (T + "без ситуации", {"example_it": "Questo bip del forno mi dà fastidio"}),
    13983: (T + "повтор 10122 «non sono sordo»", {"example_it": "Il leone ruggisce nella gabbia"}),
    13995: (T + "«Arrivederci, amico mio» — книжно", {"example_it": "Addio, e grazie di tutto!"}),
}

REPLACE = []

SPLIT_LATER = {}
