"""Вычитка английского, порция p045 (C1/C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    8286: (T + 'без ситуации', {"example_en": 'He readily agreed to help'}),
    8359: (T + 'повтор 10364 «resist chocolate»', {"example_en": 'In the end he succumbed to temptation'}),
    8393: (T + 'оборвано', {"example_en": 'Attendance is not mandatory'}),
    8457: (T + 'книжно', {"example_en": 'We need to clear up the misunderstanding before the guests arrive'}),
    8487: (T + 'калька', {"example_en": 'Stop snooping around in my things!'}),
    8498: (T + 'книжно', {"example_en": 'Shall we fix a date?'}),
    8527: (T + '«Munich» — без нужды', {"example_en": 'A house with a garden in London on my salary? Completely unrealistic'}),
    8572: (T + 'калька', {"example_en": 'The plan needs tweaking to make it more realistic'}),
}

REPLACE = []

SPLIT_LATER = {}
