"""Вычитка французского, порция p014 (B1), 23.10: «nous» → «on», нет слова карточки, кальки"""

T = "вычитка французского: "

FIXES = {
    3067: (T + "«est harmonieuse» — книжно", {"example_fr": "La vie commune avec ma belle-mère n'est pas toujours facile"}),
    6369: (T + "нет слова карточки «éloigné»", {"example_fr": "La gare n'est pas très éloignée, dix minutes à pied"}),
    6383: (T + "нет слова карточки «en trop»", {"example_fr": "Il y a une part de gâteau en trop, tu la veux ?"}),
    6415: (T + "фраза оборвана", {"example_fr": "J'apprécie beaucoup ton aide"}),
    6418: (T + "«concevoir» — книжно", {"example_fr": "J'ai du mal à saisir ce qu'il veut dire"}),
    6427: (T + "нет слова карточки «enchanté»", {"example_fr": "Ma mère était enchantée de ton gâteau"}),
    6451: (T + "порядок слов неживой", {"example_fr": "Apparemment, il est malade"}),
    6475: (T + "«Nous avons besoin» — книжно", {"example_fr": "Il nous faut une protection contre la pluie"}),
    6481: (T + "«une nature aimable» — калька", {"example_fr": "C'est dans sa nature d'aider les autres"}),
    6485: (T + "«Nous ne pouvons pas» — книжно", {"example_fr": "On ne peut pas l'empêcher"}),
    6486: (T + "нет слова карточки «monter la garde»", {"example_fr": "Le chien monte la garde devant la maison"}),
    6495: (T + "«Nous devons» — книжно", {"example_fr": "Il faut agir vite"}),
    6520: (T + "«Continuons tout simplement» — коряво", {"example_fr": "Bon, on continue !"}),
    6536: (T + "нет слова карточки «presque»", {"example_fr": "J'ai presque raté le train"}),
    6541: (T + "нет слова карточки «se tirer»", {"example_fr": "Allez, on se tire !"}),
    6572: (T + "без ситуации непонятно", {"example_fr": "Tiens-toi bien, ça va secouer !"}),
    6583: (T + "«se rendent visite mutuellement» — калька", {"example_fr": "Le respect doit être mutuel"}),
    6587: (T + "«Nous devons clarifier cela» — книжно", {"example_fr": "Il faut qu'on clarifie ça"}),
    6599: (T + "«de haut en bas» — не то значение", {"example_fr": "Le vent a mis le vieil arbre à terre"}),
    6610: (T + "без ситуации непонятно", {"example_fr": "Je te préviens, c'est très épicé"}),
    6621: (T + "нет слова карточки «quelque»", {"example_fr": "Ça te dit quelque chose ?"}),
    6638: (T + "«donne beaucoup de joie» — калька", {"example_fr": "Mon travail me donne beaucoup de satisfaction"}),
    6643: (T + "нет слова карточки «piloter»", {"example_fr": "On peut piloter la lumière du salon depuis le portable"}),
    6663: (T + "«Nous devons» — книжно", {"example_fr": "Il faut tester le nouveau programme"}),
    6707: (T + "нет слова карточки «énorme»", {"example_fr": "Il y a eu un orage énorme cette nuit"}),
    6710: (T + "«pas envie de tout ce bazar» — коряво", {"example_fr": "Range ton bazar, s'il te plaît !"}),
    6737: (T + "«Nous devons» — книжно", {"example_fr": "Il faut prendre une décision"}),
    6743: (T + "«un mètre de distance avec moi» — коряво", {"example_fr": "Garde tes distances avec ce chien"}),
    6759: (T + "«Nous devons» — книжно", {"example_fr": "Pense à sauvegarder tes données"}),
    6784: (T + "нет слова карточки «utiliser»", {"example_fr": "On utilise des drones pour retrouver les randonneurs perdus"}),
    6600: (T + "нет слова карточки «séparément»", {"example_fr": "Après le cinéma, on est rentrés séparément"}),
    6813: (T + "нет слова карточки «retransmettre»", {"example_fr": "Le match est retransmis en direct ce soir"}),
    6814: (T + "«Nous sortons» — книжно", {"example_fr": "On sort un moment"}),
    6816: (T + "«Nous devons rentrer» — книжно", {"example_fr": "Il faut qu'on rentre, il commence déjà à faire nuit"}),
    6819: (T + "нет слова карточки «inclus»", {"example_fr": "Le petit-déjeuner est inclus dans le prix"}),
}

REPLACE = []

SPLIT_LATER = {}
