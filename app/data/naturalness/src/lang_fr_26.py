"""Вычитка французского, порция p026 (B1/B2), 23.10: дом и время — «nous» → «on», повторы «décorer», «entre-temps», «train en retard»"""

T = "вычитка французского: "

FIXES = {
    18244: (T + "«Ils veulent construire» — без ситуации", {"example_fr": "On va construire une nouvelle école dans le quartier"}),
    18317: (T + "«Nous utilisons … nous sommes» — книжно", {"example_fr": "Quand on est en retard, on passe par l'entrée de derrière"}),
    18320: (T + "«une théière de thé» — тавтология", {"example_fr": "Attention, la théière est encore chaude"}),
    18349: (T + "повтор «Nous décorons» (18412)", {"example_fr": "On décore le sapin tous ensemble"}),
    18412: (T + "повтор «Nous décorons» (18349)", {"example_fr": "J'ai décoré la salle avec des ballons"}),
    18935: (T + "повтор «décorer la maison» (18349)", {"example_fr": "Pendant la période de Noël, les magasins sont bondés"}),
    18378: (T + "«Où est votre domicile fixe» — канцелярит", {"example_fr": "Il n'a pas de domicile fixe"}),
    18414: (T + "«Nous nous chauffons» — книжно", {"example_fr": "On se chauffe au gaz"}),
    18429: (T + "«très idyllique» — книжно", {"example_fr": "La petite ville sur la côte était un vrai rêve"}),
    18438: (T + "«nous fermons» — книжно", {"example_fr": "La nuit, on ferme les stores pour qu'il fasse noir"}),
    18489: (T + "«Nous transformons» — книжно", {"example_fr": "On transforme le grenier en chambre"}),
    18639: (T + "«je te cours après» — не тот смысл", {"example_fr": "Il court toujours derrière son grand frère"}),
    18664: (T + "нет слова карточки «la hâte»", {"example_fr": "Dans la hâte, j'ai oublié mon portable"}),
    18678: (T + "«Nous devons d'abord attendre» — книжно", {"example_fr": "On attend de voir ce qu'il dit"}),
    18697: (T + "повтор 18683 «Entre-temps»", {"example_fr": "Maintenant, il habite à Lyon"}),
    18725: (T + "«devraient apprendre de nous» — книжно", {"example_fr": "Voici mon futur bureau !"}),
    18744: (T + "«Nous ne voulons pas» — книжно", {"example_fr": "Je ne vais pas rester assis à rien faire toute la journée"}),
    18751: (T + "повтор 18823 «Le train est retardé / en retard»", {"example_fr": "Le vol retardé a enfin décollé"}),
    18878: (T + "«Nous devrions» — книжно", {"example_fr": "Il faut partir de bonne heure"}),
    18910: (T + "«a accompli beaucoup de choses» — книжно", {"example_fr": "Le locataire précédent a laissé ses meubles"}),
    18948: (T + "«nous regardons» — книжно", {"example_fr": "Le dimanche soir, on regarde toujours une série ensemble"}),
    18949: (T + "«nous allons» — книжно; повтор 18948", {"example_fr": "Jeudi soir, je suis pris, désolé"}),
    19001: (T + "«nous avons porté plainte» — книжно", {"example_fr": "Après le cambriolage, on a tout de suite porté plainte"}),
    19030: (T + "«Je considère que … essayons» — книжно", {"example_fr": "Je trouve que c'est une bonne idée, on essaie !"}),
    1272: (T + "«Nous devons» — книжно", {"example_fr": "Il faut garder la tête froide"}),
    7092: (T + "повтор 9899 «couper l'étiquette»", {"example_fr": "On nous a coupé l'électricité"}),
}

REPLACE = []

SPLIT_LATER = {}
