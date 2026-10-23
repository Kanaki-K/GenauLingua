"""QA d05 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    8462: ('проверка выборок: «w natarciu» о самокатах — военная калька; по-польски «zyskiwać popularność»', {'translation_pl': 'natarcie, (auf dem Vormarsch) zyskiwać popularność', 'example_pl': 'Hulajnogi elektryczne od dwóch lat zyskują w naszym mieście popularność'}),
    8624: ('проверка выборок: «live out his need to run around» — неестественно; есть в W «give free rein to»', {'example_en': 'In the new house with a garden my son can finally give free rein to his need to run around'}),
    8869: ('проверка выборок: действие сейчас — продолженное время', {'example_en': 'The barman is making me a cocktail'}),
    9292: ('проверка выборок: «мой фантастический портрет» — прилагательное не к тому слову', {'example_ru': 'Художник нарисовал с меня фантастический портрет', 'example_uk': 'Художник намалював з мене фантастичний портрет'}),
    9536: ('проверка выборок: по-британски «a pair of compasses»', {'example_en': 'I draw a circle with a pair of compasses'}),
    10045: ('проверка выборок: «Mir ist das ernst» = «я серьёзно», а не «я принимаю всерьёз»', {'example_tr': 'Bu konuda ciddiyim'}),
}

REPLACE = []

SPLIT_LATER = {}
