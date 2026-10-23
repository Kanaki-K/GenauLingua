"""Вычитка французского, порция p040 (C1), 23.10: повтор «À soixante-dix ans, mon grand-père a encore…», нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    9569: (T + "повтор 10885 «À soixante-dix ans, mon grand-père a encore»", {"example_fr": "Il n'est jamais trop tard pour apprendre une langue"}),
    9887: (T + "нет слова карточки «corruptible»", {"example_fr": "Tout le monde est corruptible, il suffit d'y mettre le prix"}),
}

REPLACE = []

SPLIT_LATER = {}
