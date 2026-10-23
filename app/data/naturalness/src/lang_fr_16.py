"""Вычитка французского, порция p016 (B1), 23.10: «nous» → «on», нет слова карточки, кальки, повторы"""

T = "вычитка французского: "

FIXES = {
    7718: (T + "нет слова карточки «à peine»", {"example_fr": "On a à peine le temps, il faut se dépêcher"}),
    7748: (T + "«Nous devons» — книжно", {"example_fr": "Il faut encore décharger le camion"}),
    7759: (T + "«nous sommes de nouveau» — книжно", {"example_fr": "Enfin, on est tous réunis !"}),
    7864: (T + "«nous devons monter» — книжно", {"example_fr": "Le chemin est très raide, on monte doucement"}),
    8056: (T + "нет слова карточки «vif»", {"example_fr": "Le petit est vif comme un écureuil"}),
    8058: (T + "«radicalement court» — калька", {"example_fr": "J'ai fait un changement radical : cheveux courts !"}),
    8083: (T + "«Il fait si étouffant» — коряво", {"example_fr": "On sort un moment ? On étouffe ici"}),
    8109: (T + "«nous débarrassons» — книжно", {"example_fr": "Après le repas, c'est moi qui débarrasse la table"}),
    8129: (T + "«Nous avons» — книжно", {"example_fr": "On a un temps limité pour tout organiser"}),
    8145: (T + "повтор «petit-déjeuner compris» (6819)", {"example_fr": "Le forfait comprend dix séances de sport"}),
    8166: (T + "повтор 7017 «traversé des épreuves»", {"example_fr": "Pendant ces années, il a vécu des moments très durs"}),
    8303: (T + "«Avec cette faux, j'ai fauché» — коряво", {"example_fr": "Mon grand-père coupe encore l'herbe à la faux"}),
    8335: (T + "«détourner le regard» — не тот смысл", {"example_fr": "Il ne sait pas fermer les yeux quand quelqu'un a besoin d'aide"}),
    8380: (T + "«me montrer reconnaissant» — книжно", {"example_fr": "Je te suis très reconnaissant pour ton aide"}),
    8401: (T + "«attacher la valise» — неживо", {"example_fr": "Attache bien les vélos sur le toit de la voiture"}),
    8409: (T + "повтор «en automne, les feuilles»", {"example_fr": "Le bouton de ma veste est tombé"}),
    8524: (T + "«Nous avons convenu» — книжно", {"example_fr": "On a convenu de se retrouver demain à deux heures"}),
    8595: (T + "«veulent courir partout» — калька", {"example_fr": "Les enfants courent partout dans le jardin"}),
    8622: (T + "«Il est inhabituel de» — книжно", {"example_fr": "Ici, c'est peu courant de boire de la bière le matin"}),
    8660: (T + "повтор «en automne, les feuilles»", {"example_fr": "Ma fille veut une chambre violette"}),
    8679: (T + "«habillé si chic» — коряво", {"example_fr": "Tu veux aller où, habillé comme ça ?"}),
    8758: (T + "«Ma carrière est importante pour moi» — калька", {"example_fr": "Pour elle, la carrière passe avant tout"}),
    8782: (T + "«Beaucoup d'animaux vivent» — учебниково", {"example_fr": "Les enfants adorent passer les vacances à la ferme"}),
    8838: (T + "нет слова карточки «la direction»", {"example_fr": "La direction du club de sport cherche encore un trésorier"}),
}

REPLACE = []

SPLIT_LATER = {}
