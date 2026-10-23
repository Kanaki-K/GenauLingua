"""Вычитка французского, порция p031 (B2), 23.10: учебниковые фразы, повтор «chocolat», «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    10760: (T + "повтор «faible pour le chocolat» (10267)", {"example_fr": "Il a un penchant pour les blagues douteuses"}),
    10816: (T + "учебниково", {"example_fr": "Avec la fatigue, la perception du temps change"}),
    11716: (T + "«nous mangeons» — книжно", {"example_fr": "Pour Thanksgiving, les Américains mangent de la dinde"}),
    11728: (T + "учебниково", {"example_fr": "Pour notre anniversaire de mariage, on s'est offert un homard"}),
    11731: (T + "нет слова карточки «picoler»", {"example_fr": "Le week-end, il picole avec ses copains"}),
}

REPLACE = []

SPLIT_LATER = {}
