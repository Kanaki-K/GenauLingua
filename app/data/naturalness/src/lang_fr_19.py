"""Вычитка французского, порция p019 (B1), 23.10: чувства и еда — кальки, повторы «mamie fait…», «bistrot…», «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    10434: (T + "«très volontiers» — калька gern", {"example_fr": "C'est une mère très aimante"}),
    10436: (T + "«exultent devant la neige» — книжно", {"example_fr": "Toute la salle exulte quand le groupe arrive sur scène"}),
    10443: (T + "«une situation menaçante» — книжно", {"example_fr": "Le ciel est menaçant, on rentre"}),
    10459: (T + "повтор 10233 «que ça (ne) marche (pas)»", {"example_fr": "Je doute qu'il dise la vérité"}),
    10460: (T + "«peureux et a peur» — тавтология", {"example_fr": "Mon fils est très peureux, il dort avec la lumière"}),
    10462: (T + "учебниково", {"example_fr": "J'apprécie ton honnêteté"}),
    10463: (T + "повтор 10233 «Je crains que»", {"example_fr": "Je redoute un peu la réunion de demain"}),
    10464: (T + "«Je dois reconsidérer» — калька", {"example_fr": "Laisse-moi reconsidérer ta proposition avant de dire oui"}),
    10548: (T + "«Nous devons être réalistes quant à» — канцелярит", {"example_fr": "Sois réaliste, on n'aura jamais fini avant vendredi"}),
    10812: (T + "повтор «siffloter» (8285)", {"example_fr": "Les enfants jouent joyeusement dans le jardin"}),
    11136: (T + "«Le quotidien est agité» — книжно", {"example_fr": "En ce moment, c'est un peu agité au boulot"}),
    11337: (T + "повтор «effraient» (10372)", {"example_fr": "Le masque de son frère a effrayé la petite"}),
    11378: (T + "«réussir cette tâche» — книжно", {"example_fr": "Je ne l'aurais jamais cru capable de ça"}),
    11542: (T + "без ситуации", {"example_fr": "Je défends toujours mes amis"}),
    11562: (T + "«Nous avons eu» — книжно", {"example_fr": "On a eu une conversation amicale et on a tout clarifié"}),
    11650: (T + "«Trinquons» — книжно", {"example_fr": "On trinque au champagne !"}),
    11677: (T + "«nous buvons» — книжно", {"example_fr": "Après le repas, on boit une petite eau-de-vie"}),
    11708: (T + "«L'enfant avale» — учебниково", {"example_fr": "Je n'arrive pas à avaler ces gros comprimés"}),
    11711: (T + "повтор «mamie fait le meilleur» (11859)", {"example_fr": "Le dimanche, on mange des crêpes au Nutella"}),
    11732: (T + "нет слова карточки «assoiffé»", {"example_fr": "Après le match, les joueurs sont assoiffés"}),
    11816: (T + "«currywurst» — не по-французски", {"example_fr": "On mange vite un sandwich au snack"}),
    11847: (T + "«Nous prenons» — книжно", {"example_fr": "On prend la bruschetta en entrée"}),
    11850: (T + "повтор «pour la toux» (11851)", {"example_fr": "Ne mange pas trop de bonbons avant le dîner"}),
    11854: (T + "повтор «mamie fait elle-même» (11974, 11937)", {"example_fr": "Dans le Nord, on mange beaucoup de chou"}),
    11891: (T + "нет слова карточки «le rafraîchissement»", {"example_fr": "Des rafraîchissements sont offerts à l'entrée"}),
    11944: (T + "повтор «au bistrot boire» (11945, 11724)", {"example_fr": "On a dormi dans une vieille auberge à la montagne"}),
    11945: (T + "повтор «au bistrot boire» (11944)", {"example_fr": "Le petit bistrot du coin fait un très bon café"}),
    11969: (T + "«eau minérale gazeuse» — громоздко", {"example_fr": "Plate ou gazeuse ? — Plate, s'il vous plaît"}),
    11991: (T + "повтор 11677 «après le repas, on boit»", {"example_fr": "Ma tante fait sa liqueur de cerises elle-même"}),
    12001: (T + "«au café pour boire un café» — тавтология", {"example_fr": "C'est un habitué, le serveur connaît sa commande par cœur"}),
    12007: (T + "«rend le plat plus intéressant» — калька", {"example_fr": "Il manque un peu d'assaisonnement"}),
    12027: (T + "повтор «mamie fait de la confiture» (11937)", {"example_fr": "La gelée de groseilles va très bien avec le fromage"}),
    12028: (T + "«nous avons fait rôtir» — книжно", {"example_fr": "À Noël, on mange de la dinde"}),
    12098: (T + "«C'est un plaisir pour moi» — калька", {"example_fr": "Ça me fait très plaisir de te voir"}),
}

REPLACE = []

SPLIT_LATER = {}
