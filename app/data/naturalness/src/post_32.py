"""QA d08 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    13125: ('проверка выборок: uk «рідкою» = жидкой; нужно «рідкісною»', {'example_uk': 'Проказа стала сьогодні дуже рідкісною хворобою'}),
    12526: ('проверка выборок: прилагательное, а в примере глагол «hat angeschossen»', {'example_de': 'Im Wald haben wir ein angeschossenes Reh gefunden', 'example_ru': 'В лесу мы нашли подстреленную косулю', 'example_uk': 'У лісі ми знайшли підстрелену козулю', 'example_en': 'In the forest we found a deer that had been shot', 'example_tr': 'Ormanda vurulmuş bir karaca bulduk', 'example_pl': 'W lesie znaleźliśmy postrzeloną sarnę', 'example_it': 'Nel bosco abbiamo trovato un capriolo ferito', 'example_es': 'En el bosque encontramos un corzo herido de bala', 'example_fr': 'Dans la forêt, on a trouvé un chevreuil blessé par balle', 'example_cs': 'V lese jsme našli postřelenou srnu'}),
    12531: ('проверка выборок: «işemek» грубо; первое в W «çiş yapmak»', {'example_tr': 'Hemen çiş yapmam lazım'}),
    12571: ('проверка выборок: «стонет / sténá» — слова W «кряхтеть / hekat» не узнаются', {'example_ru': 'Он кряхтит под тяжестью', 'example_uk': 'Він кректає під вагою', 'example_cs': 'Heká pod tíhou nákladu'}),
    12589: ('проверка выборок: «bleeding on his head» — по-английски «from his head»', {'example_en': 'After the accident, he had heavy bleeding from his head'}),
    12642: ('проверка выборок: «such a good ear and hearing» — склейка; о музыке по-английски «a good ear»', {'translation_en': 'hearing, ear', 'example_en': 'My sister has such a good ear that she can play any song on the piano after hearing it once'}),
    12770: ('проверка выборок: «мне очень на пользу» — нет глагола', {'example_ru': 'После напряжённой недели вечер в одиночестве в ванне очень идёт мне на пользу', 'example_uk': 'Після напруженого тижня вечір на самоті у ванні дуже йде мені на користь'}),
    12920: ('проверка выборок: «затерплий» — онемевший, не то; слово W «напружений»', {'example_uk': "Після довгої роботи за комп'ютером я весь напружений"}),
    12929: ('проверка выборок: «forgotten the fuse» — непонятно; забыл выключить', {'example_en': "I got an electric shock changing the light because I'd forgotten to switch off the fuse"}),
    12961: ('проверка выборок: запятая перед «и» между частями сложного', {'example_ru': 'Опухоль была злокачественной, и её нужно было удалить', 'example_uk': 'Пухлина була злоякісною, і її потрібно було видалити'}),
    12992: ('проверка выборок: «для спасательной операции нашей кошки» — не по-русски', {'example_ru': 'Спасательная операция для нашей кошки на дереве потребовала двух пожарных и длинной лестницы', 'example_uk': 'Рятувальна операція для нашої кішки на дереві потребувала двох пожежників і довгої драбини'}),
    13038: ('проверка выборок: «даже ещё делает» — тяжело', {'example_ru': 'Наш старый семейный врач до сих пор делает визиты на дом, если у тебя температура'}),
    13163: ('проверка выборок: заголовок «das Stimmbänder» — это множественное; единственное das Stimmband', {'word_de': 'Stimmband'}),
    13309: ('проверка выборок: «orada» = там; «sind schon da» = здесь', {'example_tr': 'Diğerleri zaten burada'}),
    13659: ('проверка выборок: потеряно «jetzt»', {'example_tr': 'Şemsiyemi unuttum, şimdi de yağmur yağıyor'}),
    13713: ('проверка выборок: «fırına … giyiniyor» — оборвано, нет «идя в»', {'example_tr': 'Dedem fırına giderken bile takım elbiseyle giyiniyor, eskiden böyle yapılırdı diyor'}),
}

REPLACE = []

SPLIT_LATER = {}
