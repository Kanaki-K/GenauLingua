"""Вычитка французского, порция p015 (B1), 23.10: «nous» → «on», нет слова карточки, кальки"""

T = "вычитка французского: "

FIXES = {
    6833: (T + "«Revoyons» — книжно", {"example_fr": "On revoit la liste encore une fois ?"}),
    6836: (T + "«devons-nous procéder» — книжно", {"example_fr": "Comment on procède avec ce problème ?"}),
    6866: (T + "«nous sommes arrivés» — книжно", {"example_fr": "À cause de toi, on est arrivés en retard"}),
    6872: (T + "«Nous remontons» — книжно", {"example_fr": "On monte la tente ici ?"}),
    6873: (T + "нет слова карточки «en bas»", {"example_fr": "Je t'attends en bas, devant l'immeuble"}),
    6876: (T + "нет слова карточки «vers le bas»", {"example_fr": "Ne regarde pas vers le bas !"}),
    6889: (T + "«chaque détail» — калька", {"example_fr": "Raconte-moi tout, dans les moindres détails"}),
    6890: (T + "«m'est complètement inconnue» — книжно", {"example_fr": "Le numéro est inconnu, je ne réponds pas"}),
    6898: (T + "нет слова карточки «procurer»", {"example_fr": "Ce petit boulot lui procure un peu d'argent de poche"}),
    6924: (T + "«complètement improbable» — калька", {"example_fr": "C'est très peu probable"}),
    6925: (T + "«pratiquement une garantie» — коряво", {"example_fr": "J'ai pratiquement fini"}),
    6927: (T + "«substitut au thé» — неживо", {"example_fr": "Le train est annulé, mais il y a un bus de remplacement"}),
    6931: (T + "без ситуации непонятно", {"example_fr": "Son patron l'a transféré à Lyon"}),
    6942: (T + "«Nous installons» — книжно", {"example_fr": "On installe les tables pour la fête"}),
    6950: (T + "«nous nous mettons» — книжно", {"example_fr": "On se met en route demain matin"}),
    6952: (T + "«Nous partons» — книжно", {"example_fr": "À quelle heure on part ?"}),
    6965: (T + "«Nous avons dû» — книжно", {"example_fr": "On a malheureusement dû interrompre le voyage"}),
    6969: (T + "«qu'il ne venait pas» — коряво", {"example_fr": "J'ai constaté qu'il manquait vingt euros dans mon porte-monnaie"}),
    6970: (T + "нет слова карточки «s'appliquer»", {"example_fr": "La réduction s'applique aussi aux enfants"}),
    6992: (T + "нет слова карточки «attacher»", {"example_fr": "Tu peux m'attacher les cheveux ?"}),
    6994: (T + "«Le nœud de ma corde» — неживо", {"example_fr": "Je n'arrive pas à défaire ce nœud"}),
    7032: (T + "нет слова карточки «défiler»", {"example_fr": "Le 14 juillet, les soldats défilent sur les Champs-Élysées"}),
    7041: (T + "«Nous devons nous assurer» — книжно", {"example_fr": "Il faut s'assurer que tout arrive à l'heure"}),
    7053: (T + "«Tiens un taxi prêt» — калька", {"example_fr": "Garde ton téléphone sous la main, je t'appelle"}),
    7061: (T + "«taxes comprises» — канцелярит", {"example_fr": "Ça fait 50 euros, livraison comprise"}),
    7072: (T + "нет слова карточки «retrouver»", {"example_fr": "Notre chien retrouve chaque friandise cachée dans l'appartement"}),
    7091: (T + "«vérifié mon message» — калька", {"example_fr": "Attends, je vérifie juste mes messages"}),
    7116: (T + "повтор «garder ses distances» (6743)", {"example_fr": "On a parcouru une grande distance à vélo"}),
    7140: (T + "«secoue juste la tête» — калька", {"example_fr": "Il secoue la tête sans rien dire"}),
    7190: (T + "«Nous voulons poursuivre» — книжно", {"example_fr": "On poursuit la conversation demain ?"}),
    7224: (T + "«Nous avons … sur ce sujet» — книжно", {"example_fr": "On a des avis différents là-dessus"}),
    7270: (T + "«nous avons besoin» — книжно", {"example_fr": "La situation est critique, il nous faut de l'aide"}),
    7294: (T + "«Nous ne pouvons pas» — книжно", {"example_fr": "On ne peut pas exclure cette possibilité"}),
    7313: (T + "нет слова карточки «mondial»", {"example_fr": "Le réchauffement climatique est un problème mondial"}),
    7315: (T + "«généralement connu» — канцелярит", {"example_fr": "En général, je suis content de mon travail"}),
    7353: (T + "«nous devons» — книжно", {"example_fr": "La clôture est branlante, il faut la réparer"}),
    7611: (T + "нет слова карточки «en descendant»", {"example_fr": "En descendant, le vélo roule tout seul"}),
    7712: (T + "«Cela» — книжно", {"example_fr": "Ça demande beaucoup de patience et de temps"}),
    7715: (T + "«est assise ensemble» — калька", {"example_fr": "Le dimanche, on est tous ensemble autour de la table"}),
}

REPLACE = []

SPLIT_LATER = {}
