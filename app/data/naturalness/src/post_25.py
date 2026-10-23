"""QA d01 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    280: ('проверка выборок: «out of form» не по-британски; нужно «out of shape»', {'example_en': "I'm out of shape at the moment"}),
    287: ('проверка выборок: «available» нет в W; слово должно узнаваться', {'example_en': 'The room is free'}),
    521: ('проверка выборок: «можем смотреть вместе» — оборвано, во что смотреть; по смыслу «заглянуть в мой»', {'example_ru': 'Ты забыл учебник? Можем вместе посмотреть в мой', 'example_uk': 'Ти забув підручник? Можемо разом подивитися в мій', 'example_cs': 'Zapomněl jsi učebnici? Můžeme se dívat spolu do mojí'}),
    202: ('проверка выборок: «nous le ferons simplement demain» — книжно, не разговор', {'example_fr': 'Alors on le fera demain, tout simplement'}),
    795: ('проверка выборок: «To jest złe» — оценка морали; «Das ist schlecht» = «To źle»', {'example_pl': 'To źle'}),
    1009: ('проверка выборок: потеряно gerade «сейчас»', {'example_uk': 'Пральна машина зараз працює', 'example_en': 'The washing machine is on at the moment'}),
    1054: ('проверка выборок: «home town» нет в W (место жительства) и значит другое — родной город', {'example_en': 'Where I live is a small village, but I work in the city'}),
    1445: ('проверка выборок: британское «to the hairdresser\'s», и действие сейчас', {'example_en': "I'm going to the hairdresser's"}),
}

REPLACE = []

SPLIT_LATER = {}
