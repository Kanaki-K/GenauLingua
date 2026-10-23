"""QA d06 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    10088: ('проверка выборок: «Geister» здесь привидения (W «призрак/привид»), а не «духи»', {'example_ru': 'Я не верю в призраков', 'example_uk': 'Я не вірю в привидів', 'example_tr': 'Hayaletlere inanmıyorum'}),
    10530: ('проверка выборок: tr «iyileşmek» — выздороветь; «sich bessern» = исправиться', {'example_tr': 'Günahkâr yaptıklarından pişman ve kendini düzeltmek istiyor', 'example_en': 'The sinner regrets his actions and wants to mend his ways'}),
    10535: ('проверка выборок: «становится слишком» — оборвано', {'example_ru': 'Когда всего становится слишком много, бабушкин сад — моё убежище'}),
    10563: ('проверка выборок: «chciwość na pieniądze» — не сочетается; «żądza pieniędzy» (есть в W)', {'example_pl': 'Jego żądza pieniędzy jest niewiarygodna'}),
    10656: ('проверка выборок: порядок слов — глагол на втором месте', {'example_cs': 'Od stěhování zesláblo pouto se starými přáteli'}),
}

REPLACE = []

SPLIT_LATER = {}
