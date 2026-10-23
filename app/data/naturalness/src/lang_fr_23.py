"""Вычитка французского, порция p023 (B1), 23.10: семья и природа — «nous» → «on», повторы, учебниковое"""

T = "вычитка французского: "

FIXES = {
    15152: (T + "«Nous devrions traiter nos semblables» — книжно", {"example_fr": "Il se croit supérieur à ses semblables"}),
    15166: (T + "«à cause de la course» — коряво", {"example_fr": "Après la course, j'ai mal aux cuisses"}),
    15206: (T + "«J'ai mal au coude, je suis tombé» — коряво", {"example_fr": "Je suis tombé sur le coude"}),
    15263: (T + "«L'enfant grandit» — учебниково", {"example_fr": "Il a grandi dans un foyer pour enfants"}),
    15314: (T + "«L'enfant est assis» — учебниково", {"example_fr": "Le petit sait déjà aller sur le pot tout seul"}),
    15388: (T + "«veut chasser» — калька", {"example_fr": "Le chat chasse les souris dans le grenier"}),
    15402: (T + "«Nous sommes assis» — книжно", {"example_fr": "Viens t'asseoir à l'ombre, il fait trop chaud"}),
    15409: (T + "нет слова карточки «la zone»", {"example_fr": "Dans cette zone, il n'y a presque pas de réseau"}),
    15411: (T + "повтор 15574 «s'allonger dans l'herbe / sur la pelouse»", {"example_fr": "L'herbe est encore mouillée ce matin"}),
    15436: (T + "«nous allons» — книжно", {"example_fr": "En été, on va sur la côte"}),
    15443: (T + "повтор 15744 «la poule pond un œuf»", {"example_fr": "Mes voisins ont cinq poules dans le jardin"}),
    15444: (T + "«Nous voulons planter» — книжно", {"example_fr": "On va planter un arbre pour la naissance du bébé"}),
    15455: (T + "повтор 10227 «L'ambiance ici est…»", {"example_fr": "Il y a une atmosphère bizarre dans cette maison"}),
    15457: (T + "«Nous avons sauté» — книжно", {"example_fr": "On a sauté par-dessus le petit ruisseau"}),
    15462: (T + "«nous avons vu» — книжно", {"example_fr": "Dans la forêt, on a vu un renard roux"}),
    15463: (T + "«nous avons traversé l'océan en avion» — неживо", {"example_fr": "Mon rêve, c'est de traverser l'océan en bateau"}),
    15465: (T + "«le froid dehors est insupportable» — калька", {"example_fr": "Je ne supporte pas le froid"}),
    15468: (T + "«Nous prenons» — книжно", {"example_fr": "On prend le petit sentier à travers la forêt"}),
    15475: (T + "«Le gel cette nuit-là» — книжно", {"example_fr": "Avec le gel, les fleurs du balcon sont mortes"}),
    15482: (T + "«L'obscurité de la nuit» — книжно", {"example_fr": "Mon fils a peur de l'obscurité"}),
    15609: (T + "учебниково", {"example_fr": "Le tracteur laboure le champ"}),
    15618: (T + "повтор 15454 «nourrir les poissons»", {"example_fr": "Le dentiste a un grand aquarium dans la salle d'attente"}),
    15786: (T + "«Nous nous sommes promenés … et avons profité» — книжно", {"example_fr": "On s'est promenés au bord de la rivière"}),
    15828: (T + "«Nous nourrissons» — книжно", {"example_fr": "On donne les restes aux poules"}),
    15853: (T + "«nous avons vu» — книжно", {"example_fr": "Dans la mer, on a vu une méduse venimeuse"}),
    15859: (T + "повтор 15727 «chante le matin»", {"example_fr": "Mamie a un canari qui s'appelle Titi"}),
}

REPLACE = []

SPLIT_LATER = {}
