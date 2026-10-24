"""Вычитка английского, порция p035 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    15254: (T + '«Mr Müller» — не английская фамилия', {"example_en": 'Our satnav speaks with a deep male voice, my kids call him Mr Jones'}),
    15312: (T + '«in Berlin» — без нужды', {"example_en": 'His stepdaughter is now studying in Durham'}),
    16150: (T + 'нет слова карточки «flag»', {"example_en": 'The fans are waving flags in the stadium'}),
    16182: (T + 'калька', {"example_en": 'Sign here, please'}),
    16183: (T + 'калька', {"example_en": "They're accusing him of theft, but he hasn't done anything"}),
    16198: (T + 'повтор 16189 «fake passport»', {"example_en": 'A Chanel bag for thirty quid has to be a fake'}),
    16206: (T + 'книжно', {"example_en": 'As a punishment, no phone for a week'}),
    16256: (T + 'книжно', {"example_en": 'Bikers have a code of honour'}),
}

REPLACE = []

SPLIT_LATER = {}
