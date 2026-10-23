"""Вычитка французского, порция p030 (B2), 23.10: чувства — учебниковые фразы, «nous» → «on», повторы"""

T = "вычитка французского: "

FIXES = {
    10469: (T + "нет слова карточки «le cran»", {"example_fr": "Il faut du cran pour dire non à son chef"}),
    10472: (T + "учебниково", {"example_fr": "Ne me pousse pas, je décide tout seul"}),
    10473: (T + "нет слова карточки «veinard»", {"example_fr": "Quel veinard, il a encore gagné !"}),
    10496: (T + "«se comporte comme un idiot» — повтор шаблона", {"example_fr": "Un peu de décence, s'il te plaît !"}),
    10498: (T + "«accomplir cette tâche» — книжно", {"example_fr": "Il est incapable de faire un œuf au plat"}),
    10503: (T + "«Nous devons … nous allons» — книжно", {"example_fr": "Il faut se serrer les coudes, sinon on va perdre"}),
    10509: (T + "«séduite par lui, il lui plaisait» — тавтология", {"example_fr": "Elle a tout de suite été séduite par son humour"}),
    10515: (T + "«le besoin d'eau est très grand» — калька", {"example_fr": "J'ai ressenti le besoin de parler à quelqu'un"}),
    10521: (T + "«si chaleureux et agréable» — книжно", {"example_fr": "Viens, fais-moi un gros câlin !"}),
    10522: (T + "«pour mes œuvres» — книжно", {"example_fr": "La nature est ma plus grande source d'inspiration"}),
    10523: (T + "«donc nous devons être prudents» — книжно", {"example_fr": "C'est un sujet sensible, fais attention à ce que tu dis"}),
    10530: (T + "учебниково", {"example_fr": "Je ne suis qu'un pauvre pécheur, dit-il en riant"}),
    10533: (T + "«Le supplice de l'attente d'une réponse» — книжно", {"example_fr": "Attendre les résultats, c'est un vrai supplice"}),
    10555: (T + "«L'enfant est agité» — учебниково", {"example_fr": "Le bébé est agité, il fait sûrement ses dents"}),
    10570: (T + "«Il est regrettable» — книжно", {"example_fr": "C'est bien regrettable qu'il ne puisse pas venir"}),
    10576: (T + "повтор 10504 «l'ambiance … tendue»", {"example_fr": "Le match était captivant jusqu'à la dernière minute"}),
    10581: (T + "повтор 10325 «pris ma place de parking»", {"example_fr": "Cette crapule m'a vendu une voiture en panne"}),
    10598: (T + "«L'enfant sanglote» — учебниково", {"example_fr": "Elle sanglotait au téléphone"}),
    10600: (T + "«nous allons surmonter» — книжно", {"example_fr": "On va surmonter ça ensemble, j'en suis sûr"}),
    10630: (T + "«nous aurions dû» — книжно", {"example_fr": "C'était une décision hâtive, on aurait dû réfléchir plus longtemps"}),
    10634: (T + "«nous sommes» — книжно", {"example_fr": "Face à l'administration, on est malheureusement impuissants"}),
    10650: (T + "«nous avons fait» — книжно", {"example_fr": "Petites, on a fait un serment : rester meilleures amies pour toujours"}),
    10662: (T + "повтор 10345 «une idée idiote»", {"example_fr": "Arrête de poser des questions idiotes"}),
    10692: (T + "«Nous ne devrions» — книжно", {"example_fr": "Il ne faut rien précipiter"}),
    10755: (T + "повтор 10390 «… me dit que quelque chose ne va pas»", {"example_fr": "Fais confiance à ton intuition"}),
}

REPLACE = []

SPLIT_LATER = {}
