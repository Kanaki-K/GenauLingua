"""Вычитка английского, порция p032 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    11748: (T + 'повтор «gran bakes … Christmas»', {"example_en": 'The kids decorated the Christmas biscuits'}),
    11762: (T + 'книжно', {"example_en": 'The meat was tough, impossible to cut'}),
    12188: (T + 'повтор 7336 «promoted to the second…»', {"example_en": 'On Sundays he plays in an amateur league'}),
    12209: (T + 'калька', {"example_en": "Today we're just lazing about at home"}),
    12235: (T + 'повтор 12282 «go bowling»', {"example_en": 'The bowling alley is closed on Mondays'}),
    12282: (T + 'калька', {"example_en": "On Friday we're going bowling with friends"}),
    12644: (T + 'калька', {"example_en": "Don't spit on the ground!"}),
    12653: (T + 'калька', {"example_en": 'Let me catch my breath for a moment'}),
    12686: (T + 'повтор шаблона «no backbone, no courage»', {"example_en": 'He hurt his spine when he fell'}),
    12825: (T + 'повтор 13067 «visit him every Sunday»', {"example_en": "Since Grandad can't get up on his own any more, he lives in a care home"}),
}

REPLACE = []

SPLIT_LATER = {}
