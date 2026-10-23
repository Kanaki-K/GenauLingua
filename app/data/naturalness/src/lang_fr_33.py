"""Вычитка французского, порция p033 (B2), 23.10: служебные слова, одежда, речь — повторы, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    12947: (T + "«L'enfant est» — учебниково", {"example_fr": "Le médecin dit que le petit est en pleine santé"}),
    13519: (T + "повтор 13552 «une heure et demie»; «Nous sommes restés»", {"example_fr": "Le film dure une heure et demie"}),
    13520: (T + "«Nous allons vers le sud» — книжно", {"example_fr": "En automne, les oiseaux partent vers le sud"}),
    13523: (T + "«le problème est-il apparu» — книжно", {"example_fr": "Comment c'est arrivé ?"}),
    13682: (T + "«parce qu'il fait froid» — учебниково", {"example_fr": "Prends un pull, il fait frais le soir"}),
    13777: (T + "повтор 13719 «pyjama tout le dimanche»", {"example_fr": "Tu peux garder ton manteau, il fait froid ici"}),
    14010: (T + "повтор 13979 «Ne me mens pas»", {"example_fr": "Il ment à tout le monde, même à sa mère"}),
    14020: (T + "повтор «il reste du gâteau» (6383)", {"example_fr": "Tu peux garder la monnaie qui reste"}),
    14060: (T + "повтор 14055 «préviens dès que … arrive»", {"example_fr": "Il faut informer la famille de l'accident"}),
    14078: (T + "повтор 10161 «ce maudit ordinateur»", {"example_fr": "Ce foutu bus est encore en retard"}),
    14079: (T + "«Nous avons eu» — книжно", {"example_fr": "On a eu une conversation agréable autour d'un café"}),
}

REPLACE = []

SPLIT_LATER = {}
