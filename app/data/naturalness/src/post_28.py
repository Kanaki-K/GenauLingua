"""QA d04 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    7227: ('проверка выборок: «en küçük şey» — о размере; слово W «en az»', {'example_tr': 'Yapabileceğimin en azı bu'}),
    7236: ('проверка выборок: «безперервно» — слово W «упродовж» не узнаётся', {'example_uk': 'Малюк плакав упродовж усієї ночі, і ми майже не спали'}),
    7255: ('проверка выборок: «klebt an der Wand» — состояние (прилипла), а не процесс', {'example_ru': 'Бумага прилипла к стене', 'example_uk': 'Папір прилип до стіни', 'example_en': 'The paper is stuck to the wall'}),
    7317: ('проверка выборок: «Одной это целая вечность» — нет глагола, неграмотно', {'example_ru': 'Поможешь мне сложить бельё? Одна я провожусь целую вечность', 'example_uk': 'Допоможеш мені скласти білизну? Сама я провожуся цілу вічність'}),
    7341: ('проверка выборок: «которые я все ещё хочу» читается как «всё ещё»', {'example_ru': 'У кровати лежит стопка книг, и все их я ещё хочу прочитать'}),
    7453: ('проверка выборок: der Gummi — в винительном «einen Gummi»; en «hair tie for my hair» — тавтология', {'example_de': 'Ich brauche einen Gummi für meine Haare', 'example_ru': 'Мне нужна резинка для волос', 'example_uk': 'Мені потрібна гумка для волосся', 'example_en': 'I need a hair tie', 'example_tr': 'Saçım için bir lastiğe ihtiyacım var', 'example_pl': 'Potrzebuję gumki do włosów', 'example_it': 'Mi serve un elastico per i capelli', 'example_es': 'Necesito una goma para el pelo', 'example_fr': "J'ai besoin d'un élastique pour mes cheveux", 'example_cs': 'Potřebuju gumičku do vlasů'}),
    7475: ('проверка выборок: «значима» / «актуальна» — слово W «важный/важливий» не узнаётся', {'example_ru': 'Эта информация для тебя важна', 'example_uk': 'Ця інформація для тебе важлива'}),
    7476: ('проверка выборок: «C\'est à lui que revient un grand merci» — тяжело', {'example_fr': 'Un grand merci lui revient pour cela'}),
    7704: ('проверка выборок: два «if» подряд', {'example_en': "If need be, we can walk in case the bus doesn't come"}),
    7751: ('проверка выборок: «After the cleaning» — лишний артикль', {'example_en': 'After cleaning, the kitchen is spotless, until the kids come in for breakfast five minutes later'}),
    8085: ('проверка выборок: потеряно «mir»', {'example_en': 'Can you help me out with the move today?'}),
    8287: ('проверка выборок: «у своєму тренуванні» — неживо', {'example_uk': 'Після хвороби я відстав у тренуваннях'}),
    8363: ('проверка выборок: «bez úhony» = невредимым; здесь смысл «безнаказанно»', {'example_cs': 'Syn uždiboval z dortu a vyvázl z toho nepotrestaný'}),
    8451: ('проверка выборок: «була для мене занадто» — оборвано', {'example_uk': 'Гострота цього карі була для мене занадто сильна'}),
}

REPLACE = []

SPLIT_LATER = {}
