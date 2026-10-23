"""QA d07 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    11244: ('проверка выборок: «the tension is huge for my daughter» — неестественно', {'example_en': 'Before her driving test my daughter is under enormous strain'}),
    11262: ('проверка выборок: «es para mí más aprecio» — не по-испански', {'example_es': 'Un gracias sincero del jefe es para mí una muestra de aprecio mayor que cualquier prima'}),
    11391: ('проверка выборок: «frechsten» — озорные, а не «неприличные»', {'example_ru': 'Бабушка совсем не ханжа: она рассказывает самые озорные анекдоты во всей семье'}),
    11413: ('проверка выборок: «тысяча» — подлежащее в ед. числе («переслала»); tr — нужен винительный «videoyu»', {'example_ru': 'Дед, танцующий на свадьбе, был таким уморительным, что видео уже переслала тысяча человек', 'example_uk': 'Дід, що танцював на весіллі, був такий страшенно смішний, що відео вже переслала тисяча людей', 'example_tr': 'Dedemin düğünde dans etmesi o kadar komikti ki videoyu bin kişi paylaştı'}),
    11474: ('проверка выборок: «voní» — пахнет приятно; о подозрительной рыбе так не говорят', {'example_cs': 'Ta ryba má trochu pochybný zápach, radši ji nebudeme jíst'}),
    11495: ('проверка выборок: «Kimse yanılmaz değil» — двойное отрицание; слово W «hatasız»', {'example_tr': 'Kimse hatasız değil, hepimiz zaman zaman hata yapıyoruz'}),
    11504: ('проверка выборок: «ho un freddo pietoso» — не по-итальянски', {'example_it': "Senza giacca alla fermata dell'autobus tremo penosamente dal freddo"}),
    11543: ('проверка выборок: Hausmeister у дома — «domovník», не «školník»; потеряно «finde ich»', {'example_cs': 'Přijde mi pobuřující, že domovník pořád vyhání děti z hřiště'}),
    11745: ('проверка выборок: «обов\'язково належить» — калька с «gehört»', {'example_uk': 'До смаженої ковбаски в Тюрингії обов\'язково подають гостру гірчицю'}),
    11870: ('проверка выборок: потеряно «им» — моет родитель, а не кто-то', {'example_pl': 'Żeberka dzieci jedzą zupełnie bez sztućców, a potem muszę im myć całe twarze', 'example_cs': 'Žebírka jedí děti úplně bez příboru a potom jim musím umýt celý obličej'}),
    11915: ('проверка выборок: о тесте по-турецки «mayalanmak», не «fermente olmak»', {'example_tr': 'Ekmek hamuru en az iki saat mayalanmalı'}),
    11926: ('проверка выборок: «en büyük leziz lokma» — несочетаемо', {'example_tr': 'Köpeğimiz için bir parça peynir en leziz lokma'}),
    12200: ('проверка выборок: порядок слов — «на соревновании … впервые участвует» тяжело', {'example_ru': 'В субботу дочь впервые участвует в соревновании по плаванию', 'example_uk': 'У суботу донька вперше бере участь у змаганні з плавання'}),
}

REPLACE = []

SPLIT_LATER = {
    12296: 'die Gassi — Gassi не существительное с артиклем, только «Gassi gehen»; снять артикль или переделать строку',
}
