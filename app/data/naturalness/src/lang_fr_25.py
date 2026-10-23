"""Вычитка французского, порция p025 (B1), 23.10: транспорт, техника, наука, дом — «nous» → «on», повторы, учебниковое"""

T = "вычитка французского: "

FIXES = {
    17148: (T + "«Nous traversons … pour aller de l'autre côté» — тавтология", {"example_fr": "On prend le bac pour traverser la rivière"}),
    17159: (T + "«Nous transportons» — книжно", {"example_fr": "On transporte les meubles en camionnette"}),
    17173: (T + "«Le passager monte dans l'avion» — учебниково", {"example_fr": "Les passagers du vol pour Nice sont attendus porte 12"}),
    17184: (T + "«Nous faisons» — книжно", {"example_fr": "On fait un petit détour par la boulangerie ?"}),
    17194: (T + "«Tourne à la prochaine rue» — неполно", {"example_fr": "Tourne à gauche à la prochaine rue"}),
    17209: (T + "«Müller» — не французская фамилия", {"example_fr": "J'ai une réservation au nom de Martin"}),
    17215: (T + "«Nous prenons» — книжно", {"example_fr": "On prend la prochaine sortie"}),
    17368: (T + "«Nous rangeons» — книжно", {"example_fr": "On range les valises dans le coffre"}),
    17398: (T + "«nous devons» — книжно", {"example_fr": "Avant de partir, il faut rassembler toutes nos affaires"}),
    17409: (T + "«nous avons dû» — книжно", {"example_fr": "À cause des travaux, on a dû prendre une déviation"}),
    17410: (T + "«sort tôt» — оборвано", {"example_fr": "Le bateau de pêche rentre au port plein de poissons"}),
    17485: (T + "повтор 17500 «réseau»; нет слова «signal»", {"example_fr": "Le signal est trop faible ici"}),
    17502: (T + "«rend tout plus facile» — калька", {"example_fr": "Mon grand-père a peur des nouvelles technologies"}),
    17516: (T + "«basculer l'interrupteur» — калька", {"example_fr": "Il m'a mis son bras autour des épaules"}),
    17533: (T + "«Je fais partie d'un grand réseau» — коряво", {"example_fr": "Elle a un grand réseau de contacts dans la mode"}),
    17541: (T + "«Tu dois» — калька", {"example_fr": "Il faut mettre à jour le logiciel"}),
    17578: (T + "повтор «l'ascenseur est en panne» (13558)", {"example_fr": "On prend l'ascenseur ou l'escalier ?"}),
    17587: (T + "«Nous sommes» — книжно", {"example_fr": "On est en retard à cause d'une panne de voiture"}),
    17590: (T + "«propose de nombreuses fonctionnalités» — реклама", {"example_fr": "On peut regarder le film sur quelle plateforme ?"}),
    17662: (T + "«spätzle … Souabe» — не французский быт", {"example_fr": "Ce soir, on mange des lentilles aux saucisses"}),
    17768: (T + "«On a un marché» — калька", {"example_fr": "Marché conclu !"}),
    17771: (T + "повтор 15617 «vaches au pré»", {"example_fr": "Le lait vient directement de la vache du voisin"}),
    17773: (T + "«Nous pouvons» — книжно", {"example_fr": "On peut négocier le prix ?"}),
    17779: (T + "учебниково", {"example_fr": "En hiver, le bétail reste à l'étable"}),
    17792: (T + "«La branche traverse» — двусмысленно", {"example_fr": "Le secteur du tourisme traverse une période difficile"}),
    17921: (T + "«Faisons» — книжно", {"example_fr": "On fait une petite expérience ?"}),
    17931: (T + "«L'enfant mesure» — учебниково", {"example_fr": "Mon fils mesure déjà 120 centimètres"}),
    18054: (T + "повтор 17946 «… pour le gâteau»", {"example_fr": "Un kilogramme de tomates, s'il vous plaît"}),
    18115: (T + "«Maintenant je rentre» — калька", {"example_fr": "Bon, je rentre chez moi"}),
    18136: (T + "«Nous passons» — книжно", {"example_fr": "On passe la nuit dans la cabane"}),
    18187: (T + "«très sympathiques» — учебниково", {"example_fr": "Les habitants de l'immeuble se connaissent tous"}),
    18191: (T + "«Nous cherchons» — книжно", {"example_fr": "On cherche un hébergement pour la nuit"}),
    18194: (T + "«nous sommes souvent assis» — калька", {"example_fr": "En hiver, on passe les soirées devant la cheminée"}),
    18199: (T + "«nous avons réservé» — книжно", {"example_fr": "À l'hôtel, on a réservé une suite avec une belle vue"}),
}

REPLACE = []

SPLIT_LATER = {}
