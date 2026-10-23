"""Вычитка французского, порция p047 (C2), 23.10: повторы «après le repas, nous buvons», «idée idiote», «gueule de bois»; «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    11610: (T + "повтор 10345 «idée idiote»; нет слова «débile»", {"example_fr": "C'est quoi, cette idée débile ?"}),
    11613: (T + "«volontiers» — калька", {"example_fr": "C'est un vrai philanthrope, il aide tout le monde"}),
    11954: (T + "«Nous fêtons» — книжно", {"example_fr": "On fête notre mariage dans un petit domaine viticole au bord de la Moselle"}),
    11956: (T + "«nous prenons» — книжно", {"example_fr": "On prend l'apéritif sur la terrasse ?"}),
    11997: (T + "повтор 11677 «Après le repas, nous buvons»", {"example_fr": "Mon grand-père offre toujours un verre de porto aux invités"}),
    12945: (T + "«de l'enfant a augmenté» — учебниково", {"example_fr": "Une température corporelle de 37 degrés, c'est normal"}),
    13124: (T + "повтор 6944 «j'ai une gueule de bois»", {"example_fr": "Le lendemain du mariage, tout le monde avait la gueule de bois"}),
}

REPLACE = []

SPLIT_LATER = {}
