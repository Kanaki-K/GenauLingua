"""Вычитка английского, порция p046 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    8656: (T + 'повтор «take an umbrella»', {"example_en": "Just in case, I've made a copy of my passport"}),
    9224: (T + '«Hamburg» — без нужды', {"example_en": 'My uncle was chief engineer at a shipyard in Belfast for forty years'}),
    11487: (T + 'книжно', {"example_en": "He's always indecisive when he looks at a menu"}),
}

REPLACE = []

SPLIT_LATER = {}
