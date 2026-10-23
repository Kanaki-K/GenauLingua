"""QA d02 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    1665: ('проверка выборок: в примере «I\'m not in the mood», а в W только «desire» — слово не узнаётся', {'translation_en': 'desire, mood', 'example_en': "I'm not in the mood"}),
    1572: ('проверка выборок: «mladistvý» — юридический термин (несовершеннолетний правонарушитель); в быту «dospívající»', {'translation_cs': 'dospívající, mladý člověk', 'example_cs': 'Dospívající se tady scházejí'}),
    2160: ('проверка выборок: «correct» — не тот оттенок; «stimmt» = «true»', {'example_en': "That's true, though"}),
    2249: ('проверка выборок: «The processing of …» — канцелярит', {'example_en': 'Processing the application takes about three days'}),
    1801: ('проверка выборок: «je ještě otevřený» — калька с «ist noch offen»', {'example_cs': 'Náš cíl cesty na léto ještě není jasný, možná Chorvatsko'}),
    2116: ('проверка выборок: «успеваю всё домашнее задание» — нет глагола «сделать»', {'example_ru': 'С тех пор как я изменил управление временем, я наконец успеваю сделать всё домашнее задание', 'example_uk': 'Відколи я змінив управління часом, я нарешті встигаю зробити все домашнє завдання'}),
    2377: ('проверка выборок: «fällt ein guter Gedanke ein» — неживое сочетание; по-немецки «eine gute Idee»', {'example_de': 'Mir fällt gerade eine gute Idee ein', 'example_ru': 'Мне только что пришла на ум хорошая идея', 'example_uk': 'Мені щойно спала на думку гарна ідея', 'example_en': 'A good idea has just come to mind', 'example_tr': 'Aklıma şimdi güzel bir fikir geldi', 'example_pl': 'Właśnie przychodzi mi do głowy dobry pomysł', 'example_it': 'Mi viene in mente proprio ora una buona idea', 'example_es': 'Se me ocurre ahora mismo una buena idea', 'example_fr': "Une bonne idée vient de me venir à l'esprit", 'example_cs': 'Zrovna mě napadl dobrý nápad'}),
    2434: ('проверка выборок: потеряно «mir» — «облегчает мне»', {'example_tr': 'Bu işimi kolaylaştırıyor'}),
    2670: ('проверка выборок: «задуматься» — слово W «задумчивый/замислений» не узнаётся', {'example_ru': 'После этого фильма я ходил совсем задумчивый', 'example_uk': 'Після цього фільму я ходив зовсім замислений'}),
    2587: ('проверка выборок: «Nous y arriverons» — книжно для бытовой фразы', {'example_fr': "On y arrivera d'une manière ou d'une autre"}),
}

REPLACE = []

SPLIT_LATER = {}
