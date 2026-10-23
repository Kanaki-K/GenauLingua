"""Вычитка французского, порция p020 (B1), 23.10: досуг и здоровье — «nous» → «on», повторы, нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    12146: (T + "«nous allons» — книжно", {"example_fr": "Ce week-end, on va pêcher avec papi"}),
    12156: (T + "«Nous allons» — книжно", {"example_fr": "Demain, on va plonger en Corse"}),
    12157: (T + "«nous jouons» — книжно", {"example_fr": "Au Japon, le baseball est super populaire"}),
    12163: (T + "«traversons le lac à la rame» — повтор 12378", {"example_fr": "J'ai perdu une rame, on tourne en rond !"}),
    12378: (T + "повтор 12163 «traverse … à la rame»", {"example_fr": "Tiens bien ta pagaie, le courant est fort"}),
    12219: (T + "«se solde par un nul» — книжно", {"example_fr": "Ils ont fait match nul, un partout"}),
    12245: (T + "«nous campons» — книжно", {"example_fr": "Le week-end prochain, on campe à la montagne"}),
    12259: (T + "«nous sommes allés» — книжно", {"example_fr": "Samedi, on est allés en boîte de nuit"}),
    12269: (T + "«Nous jouons» — книжно", {"example_fr": "On joue parfois au poker entre amis"}),
    12299: (T + "«nous descendons» — книжно", {"example_fr": "Cet été, on descend la Dordogne en canoë"}),
    12348: (T + "«Jouons» — книжно", {"example_fr": "On joue au jeu de mime ?"}),
    12364: (T + "«Nous jouons» — книжно", {"example_fr": "On joue au frisbee au parc ?"}),
    12485: (T + "«mal à tous les os» — калька", {"example_fr": "Il fait si humide que j'ai mal jusqu'aux os"}),
    12501: (T + "учебниково", {"example_fr": "Il y a un virus qui circule au bureau"}),
    12518: (T + "«n'est plus aussi bonne» — калька", {"example_fr": "Avec l'âge, ma mémoire n'est plus ce qu'elle était"}),
    12525: (T + "нет слова карточки «le souffle»", {"example_fr": "Attends, je reprends mon souffle"}),
    12532: (T + "«après avoir couru» — книжно", {"example_fr": "Après la course, mon pouls est à 150"}),
    12540: (T + "«Existe-t-il» — книжно", {"example_fr": "Il n'y a pas encore de remède contre cette maladie"}),
    12545: (T + "«J'ai besoin d'un examen médical» — без ситуации", {"example_fr": "Pour le club de foot, il faut un certificat médical"}),
    12559: (T + "«Tu dois prendre» — без ситуации", {"example_fr": "Ce médicament, il faut le prendre avant le repas"}),
    12588: (T + "«détester comme la peste» — не та идиома", {"example_fr": "Ce genre de personnes, je les fuis comme la peste"}),
    12602: (T + "«Ses battements sont très rapides» — учебниково", {"example_fr": "À l'échographie, on entend les battements de cœur du bébé"}),
    12625: (T + "нет слова карточки «accro»", {"example_fr": "Il est complètement accro au café"}),
    12630: (T + "«transpire … tout trempé» — громоздко", {"example_fr": "Je transpire beaucoup quand il fait chaud"}),
    12646: (T + "нет слова карточки «s'occuper de»", {"example_fr": "Elle s'occupe de sa vieille mère tous les jours"}),
    12727: (T + "повтор 12967 «aide-soignant(e)… chez grand-parent»", {"example_fr": "L'aide-soignant de nuit est très gentil avec les patients"}),
}

REPLACE = []

SPLIT_LATER = {}
