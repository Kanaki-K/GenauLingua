"""Вычитка английского, порция p040 (C1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    9569: (T + 'повтор 10885 «grandad at seventy»', {"example_en": "It's never too late to master a language"}),
    9887: (T + 'нет слова карточки «corruptible»', {"example_en": 'Everyone is corruptible, you just have to find the price'}),
    10919: (T + 'нет слова карточки «to deny»; «Hamburg»', {"example_en": "My dad can't deny his Yorkshire accent, even after thirty years in London"}),
}

REPLACE = []

SPLIT_LATER = {}
