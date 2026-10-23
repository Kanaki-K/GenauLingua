"""Вычитка английского, порция p017 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    8856: (T + 'повтор 8769 «cabin crew»', {"example_en": 'The whole crew of the ship went ashore'}),
    8863: (T + 'тавтология', {"example_en": 'The painter is coming on Monday to paint the kitchen'}),
    8878: (T + 'учебниково', {"example_en": 'The cook at the canteen makes the best chips'}),
    8879: (T + 'учебниково', {"example_en": 'The employee at the town hall explained everything really well'}),
    8932: (T + 'учебниково', {"example_en": 'The school secretary gave me the form'}),
    8933: (T + 'учебниково', {"example_en": 'The architect drew up the plans for our house'}),
    9030: (T + 'учебниково', {"example_en": 'On Saturday the author is signing books at the bookshop'}),
    9040: (T + 'повтор 8776 «hang the picture»', {"example_en": 'He nails a board onto the old fence'}),
    9050: (T + 'книжно', {"example_en": 'He has a little side business giving guitar lessons'}),
    9137: (T + "повтор 8865 «go to the hairdresser's»", {"example_en": 'The barber downstairs gives a great cut'}),
    9161: (T + 'учебниково', {"example_en": 'The new recruit struggled in the first week'}),
    9164: (T + 'канцелярит', {"example_en": 'For your passport you need to go to the passport office'}),
    9165: (T + 'без ситуации', {"example_en": 'The safety officer checks all the exits'}),
    9174: (T + 'книжно', {"example_en": 'The poor intern mostly does photocopying'}),
    9267: (T + 'книжно', {"example_en": 'My work colleagues are great'}),
    9471: (T + 'тавтология', {"example_en": 'My grandad is very learned in history'}),
    9482: (T + 'учебниково', {"example_en": 'She had a very strict upbringing'}),
    9547: (T + 'тавтология', {"example_en": "The baker's apprentice gets up at three"}),
    9589: (T + 'без ситуации', {"example_en": 'I failed my driving test'}),
    9605: (T + 'повтор «At break … playground»', {"example_en": 'The kids play football in the playground'}),
    9610: (T + 'учебниково', {"example_en": 'When the school bell rings, everyone runs outside'}),
    9613: (T + 'учебниково', {"example_en": 'My son is scared to show his school report'}),
    9733: (T + 'без ситуации', {"example_en": 'Grandma sent me a cheque for 100 pounds for my birthday'}),
    9735: (T + 'книжно', {"example_en": 'Everyone pays their share'}),
    9758: (T + 'повтор 1466 «wallet»', {"example_en": "I've left my wallet at home"}),
    9761: (T + 'учебниково', {"example_en": 'Every year we donate something to charity'}),
    9915: (T + 'повтор «What is your…?»', {"example_en": 'Can you send me your account number?'}),
}

REPLACE = []

SPLIT_LATER = {}
