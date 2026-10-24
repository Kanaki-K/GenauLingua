"""Вычитка английского, порция p049 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    16932: (T + 'канцелярит', {"example_en": 'The lawyer is asking for a review of the case'}),
    17315: (T + "повтор 6493 «go on ahead, I'll follow»", {"example_en": "You lot set off, we'll follow on by car"}),
    17386: (T + '«to Berlin» — без нужды', {"example_en": "After the holiday we're flying back to Glasgow tomorrow"}),
    17680: (T + 'повтор 17746 «detects movement … light»', {"example_en": 'The rain sensor switches the wipers on by itself'}),
    17726: (T + 'учебниково', {"example_en": 'This TV channel only shows series'}),
}

REPLACE = []

SPLIT_LATER = {}
