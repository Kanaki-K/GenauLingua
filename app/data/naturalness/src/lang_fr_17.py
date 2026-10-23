"""Вычитка французского, порция p017 (B1), 23.10: учебниковые «X делает свою работу» → живые сцены, «nous» → «on», повторы"""

T = "вычитка французского: "

FIXES = {
    8856: (T + "повтор 8769 «l'équipage de l'avion»", {"example_fr": "Tout l'équipage du bateau est descendu à terre"}),
    8861: (T + "«nous a parlé à cause de la haie» — калька", {"example_fr": "Le président de l'association des jardins ouvriers est venu nous parler de notre haie"}),
    8863: (T + "«Le peintre a peint» — тавтология", {"example_fr": "Le peintre vient repeindre la cuisine lundi"}),
    8878: (T + "учебниково", {"example_fr": "La cuisinière de la cantine fait les meilleures frites"}),
    8879: (T + "учебниково", {"example_fr": "L'employée de la mairie m'a tout très bien expliqué"}),
    8932: (T + "учебниково", {"example_fr": "Le secrétaire de l'école m'a donné le formulaire"}),
    8933: (T + "«a conçu une nouvelle maison» — учебниково", {"example_fr": "L'architecte a dessiné les plans de notre maison"}),
    9030: (T + "«L'autrice a écrit» — учебниково", {"example_fr": "L'autrice dédicace son livre à la librairie samedi"}),
    9040: (T + "повтор «accrocher le tableau» (8776)", {"example_fr": "Il cloue une planche sur la vieille clôture"}),
    9050: (T + "«très épanouissante» — книжно", {"example_fr": "Il a une petite activité à côté, il donne des cours de guitare"}),
    9161: (T + "учебниково", {"example_fr": "La nouvelle recrue a eu du mal la première semaine"}),
    9164: (T + "«service compétent» — канцелярит", {"example_fr": "Pour la carte grise, il faut aller au service d'à côté"}),
    9165: (T + "без ситуации непонятно", {"example_fr": "Le délégué de classe parle au nom de tous les élèves"}),
    9174: (T + "«aide à des tâches simples» — книжно", {"example_fr": "La stagiaire fait surtout des photocopies, la pauvre"}),
    9233: (T + "«Pour le travail sur le terrain» — калька", {"example_fr": "Avec mon travail sur le terrain, je suis rarement au bureau"}),
    9267: (T + "«sympathiques et serviables» — книжно", {"example_fr": "Mes collègues de travail sont super sympas"}),
    9457: (T + "«Je lis … en ce moment» — калька", {"example_fr": "J'en suis seulement au premier chapitre"}),
    9471: (T + "«savant qui sait» — тавтология", {"example_fr": "Mon grand-père est très savant en histoire"}),
    9482: (T + "учебниково", {"example_fr": "Elle a reçu une éducation très stricte"}),
    9547: (T + "«L'apprenti apprend» — тавтология", {"example_fr": "L'apprenti de la boulangerie se lève à trois heures"}),
    9589: (T + "«échoué à l'examen» — книжно", {"example_fr": "J'ai raté le permis, je dois le repasser"}),
    9603: (T + "«Chaque matin, je vais à l'école en» — калька", {"example_fr": "Le matin, je prends le bus scolaire"}),
    9605: (T + "«récré … récréation» — повтор", {"example_fr": "Les enfants jouent au foot dans la cour de récréation"}),
    9610: (T + "«retentit à huit heures du matin» — книжно", {"example_fr": "À la sonnerie de l'école, tout le monde court dehors"}),
    9613: (T + "учебниково", {"example_fr": "Mon fils a peur de montrer son bulletin"}),
    9733: (T + "«Je reçois un chèque» — без ситуации", {"example_fr": "Mamie m'a envoyé un chèque de 100 euros pour mon anniversaire"}),
    9735: (T + "«part des bénéfices est faible» — книжно", {"example_fr": "Chacun paie sa part"}),
    9761: (T + "«Nous voulons donner» — книжно", {"example_fr": "Chaque année, on fait un don à une association"}),
    9770: (T + "нет слова карточки «gratuit»", {"example_fr": "L'entrée est gratuite pour les enfants"}),
    9905: (T + "«Nous faisons» — книжно", {"example_fr": "On fait les comptes à la fin du mois"}),
    9950: (T + "«nous achetons» — книжно", {"example_fr": "Au grand magasin, on trouve de tout"}),
}

REPLACE = []

SPLIT_LATER = {}
