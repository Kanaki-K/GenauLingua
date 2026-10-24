"""Вычитка английского, порция p034 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    14465: (T + 'повтор 15429 «fly a kite»', {"example_en": 'In the fairy tale the knight slays the dragon'}),
    14512: (T + 'повтор 12141 «audience claps loudly»', {"example_en": "The kids clap at every one of the magician's tricks"}),
    14526: (T + 'учебниково', {"example_en": 'The hospital chaplain visits the patients'}),
    14541: (T + 'калька', {"example_en": 'My grandparents are very religious'}),
    15045: (T + 'коряво', {"example_en": 'Their adopted son is from Colombia'}),
    15106: (T + '«spätzle» — не английский быт', {"example_en": 'My stepmother taught me how to make pancakes from scratch'}),
}

REPLACE = []

SPLIT_LATER = {}
