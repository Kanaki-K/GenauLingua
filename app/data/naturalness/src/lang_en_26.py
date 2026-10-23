"""Вычитка английского, порция p026 (B1/B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    18244: (T + 'без ситуации', {"example_en": "They're going to erect a new school in our area"}),
    18317: (T + 'громоздко', {"example_en": "When we're late we go in by the back door"}),
    18320: (T + 'тавтология', {"example_en": 'Careful, the teapot is still hot'}),
    18349: (T + 'повтор 18412', {"example_en": 'We decorate the tree together'}),
    18412: (T + 'повтор 18349', {"example_en": "I've decorated the hall with balloons"}),
    18935: (T + 'повтор «decorate the house»', {"example_en": 'At Christmas time the shops are packed'}),
    18378: (T + 'канцелярит', {"example_en": 'He has no permanent residence'}),
    18429: (T + 'книжно', {"example_en": 'The little town on the coast was a dream'}),
    18639: (T + 'не тот смысл', {"example_en": "He's always running after his big brother"}),
    18664: (T + 'нет слова карточки «rush»', {"example_en": 'In the rush I forgot my phone'}),
    18725: (T + 'книжно', {"example_en": 'This is my future office!'}),
    18744: (T + 'калька', {"example_en": "I'm not going to sit around all day"}),
    18751: (T + 'повтор 18823 «the train is delayed»', {"example_en": 'The delayed flight finally took off'}),
    18878: (T + 'калька', {"example_en": 'We need to set off early'}),
    18910: (T + 'книжно', {"example_en": 'The previous tenant left the furniture'}),
    18949: (T + 'повтор 18948', {"example_en": "Thursday evening's no good for me, sorry"}),
    19045: (T + '«to Hamburg» — без нужды', {"example_en": "Next summer we're moving to Manchester, my husband has found a job there"}),
    1272: (T + 'калька', {"example_en": 'Keep a cool head'}),
    7092: (T + 'повтор 9899 «cut off the label»', {"example_en": "They've cut off our electricity"}),
}

REPLACE = []

SPLIT_LATER = {}
