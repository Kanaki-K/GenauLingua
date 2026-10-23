"""Вычитка итальянского, порция p031 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    10760: (T + 'повтор «debole per il cioccolato» (10267)', {"example_it": 'Ha una certa tendenza a esagerare'}),
    10816: (T + 'учебниково', {"example_it": 'Con la stanchezza la percezione del tempo cambia'}),
    11716: (T + '«mangiamo» — не тот быт', {"example_it": 'Per il Ringraziamento gli americani mangiano il tacchino'}),
    11728: (T + 'учебниково', {"example_it": "Per l'anniversario ci siamo regalati un astice"}),
}

REPLACE = []

SPLIT_LATER = {}
