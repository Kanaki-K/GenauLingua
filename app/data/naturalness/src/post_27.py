"""QA d03 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    2773: ('проверка выборок: слово W (consideration / уважение / повага) в примере не узнаётся; uk «повинен» — калька', {'example_en': 'You should show more consideration for others', 'example_ru': 'Тебе следует проявлять больше уважения к другим', 'example_uk': 'Тобі варто виявляти більше поваги до інших'}),
    2902: ('проверка выборок: «übersetzen lassen» — перевели в бюро, а не сам', {'example_ru': 'Свидетельство о рождении мне перевели в бюро переводов у вокзала', 'example_uk': 'Свідоцтво про народження мені переклали в бюро перекладів біля вокзалу', 'example_pl': 'Akt urodzenia dałem do przetłumaczenia w biurze tłumaczeń przy dworcu'}),
    2958: ('проверка выборок: о расходах — «élevés», не «chers»', {'example_fr': 'Le t-shirt ne coûte que cinq euros, mais les frais de livraison depuis la Chine sont deux fois plus élevés'}),
    2921: ('проверка выборок: нет артикля — «the risk of an accident»', {'example_en': "When it's icy the risk of an accident is so high that I'd rather take the bus"}),
    6528: ('проверка выборок: слово W «обмаль» узнаётся лучше «мало»', {'example_uk': 'Грошей обмаль'}),
    6566: ('проверка выборок: «hangs crooked» — нужно продолженное время', {'example_en': 'The picture is hanging crooked on the wall'}),
    6625: ('проверка выборок: «You\'re surely hungry» — не по-английски', {'example_en': "You'll certainly be hungry after the journey"}),
    6882: ('проверка выборок: «у проміжку» — неживо', {'example_uk': 'Між справами в мене ще є трохи часу'}),
    7033: ('проверка выборок: «šel jsem do posilovny» несколько раз — по-чешски «byl jsem v posilovně»', {'example_cs': 'Tento týden jsem byl několikrát v posilovně'}),
    7077: ('проверка выборок: «формує глину» — неживо; слово W «ліпити»', {'example_uk': 'Художник ліпить із глини своїми руками'}),
    7129: ('проверка выборок: «Я надеюсь, что я…» — двойное «я»', {'example_ru': 'Надеюсь, я пройду через это трудное время', 'example_uk': 'Сподіваюся, я пройду через цей важкий час'}),
    7218: ('проверка выборок: «przetworzyć informację» — о машине; о человеке «przetrawić» (есть в W)', {'example_pl': 'Muszę najpierw przetrawić tę informację'}),
    6925: ('проверка выборок: в W «practically», в примере «virtually»', {'example_en': "That's practically a guarantee"}),
}

REPLACE = []

SPLIT_LATER = {}
