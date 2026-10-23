"""Вычитка итальянского, порция p022 (B1), 23.10: речь, культура, семья — повторы, кальки, «Berlino»"""

T = "вычитка итальянского: "

FIXES = {
    14046: (T + "нет слова карточки «affrontare»", {"example_it": "Domani affronto l'argomento con lui"}),
    14061: (T + "«Sincere congratulazioni per l'esame superato» — калька", {"example_it": "Congratulazioni per l'esame!"}),
    14235: (T + "«L'abbiamo suggellato» — книжно", {"example_it": "Abbiamo concluso l'affare con una stretta di mano"}),
    14374: (T + "повтор «si comporta come» (14814)", {"example_it": "Mia figlia vuole un vestito da principessa per il compleanno"}),
    14390: (T + "повтор 12141 «hanno applaudito forte»", {"example_it": "Alla fine dello spettacolo tutto il pubblico era in piedi"}),
    14405: (T + "«Voglio filmarlo» — калька", {"example_it": "Aspetta, lo filmo!"}),
    14411: (T + "повтор 14437 «Abbiamo visitato il vecchio…»", {"example_it": "In Thailandia ci sono templi ovunque"}),
    14437: (T + "повтор 14411", {"example_it": "I monaci del monastero fanno la loro birra"}),
    14448: (T + "«castello di sabbia» — не то значение", {"example_it": "Abbiamo visitato un castello medievale"}),
    14449: (T + "«I suoni della musica» — калька", {"example_it": "Adoro il suono di questa vecchia chitarra"}),
    14451: (T + "«una persona benedetta» — калька", {"example_it": "Con tre nipoti mi sento davvero fortunata"}),
    14456: (T + "«visita Berlino» — без нужды", {"example_it": "Sua Santità il Papa visita Milano"}),
    14466: (T + "«narratore molto bravo» — не то значение", {"example_it": "In questo libro il narratore è un gatto"}),
    14469: (T + "нет слова карточки «la hit»", {"example_it": "Questa canzone è diventata la hit dell'estate"}),
    14481: (T + "«a Berlino» — без нужды", {"example_it": "I suoi quadri sono esposti in una galleria a Milano"}),
    14496: (T + "«a Berlino» — без нужды", {"example_it": "La cantante tiene un concerto a Napoli la settimana prossima"}),
    14937: (T + "повтор 14896 «Mamma, dove…»", {"example_it": "Il piccolo piange, vuole la mamma"}),
    14953: (T + "«molto importante per me» — калька", {"example_it": "La nostra amicizia dura dalle elementari"}),
    14966: (T + "«a Berlino» — без нужды", {"example_it": "Dopo il divorzio si è trasferita a Firenze"}),
    14976: (T + "«ed è molto educato» — тавтология", {"example_it": "È un vero gentiluomo, mi apre sempre la porta"}),
    15006: (T + "«Com'è il vostro rapporto?» — калька", {"example_it": "Ho un ottimo rapporto con i vicini"}),
    15013: (T + "нет слова карточки «imparentato»", {"example_it": "Siamo imparentati, ma alla lontana"}),
    15034: (T + "«ha visitato la chiesa» — учебниково", {"example_it": "Il vescovo viene a benedire la nuova chiesa"}),
}

REPLACE = []

SPLIT_LATER = {}
