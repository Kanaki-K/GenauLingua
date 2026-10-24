"""Вычитка английского, порция p036 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    16320: (T + 'повтор 15424 «the garden as territory»', {"example_en": 'Wolves defend their territory'}),
    16855: (T + '«Munich … Bayern» — оставить смысл', {"example_en": "Since my brother moved to Manchester he's a deserter in our family's eyes and cheers for United"}),
    16956: (T + '«in Berlin» — без нужды', {"example_en": "My mum is going to the big meeting in London as the allotment club's delegate"}),
    17146: (T + 'калька', {"example_en": 'Departure is at seven tomorrow morning'}),
    17153: (T + 'без ситуации', {"example_en": 'On the way back we stopped for lunch'}),
}

REPLACE = []

SPLIT_LATER = {}
