"""Полная вычитка, порция 41: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    11065: (T + "ru/uk «утюг» — «ключ снаружи в двери»", {"example_ru": "Я иногда такая неосторожная, что оставляю ключ снаружи в двери", "example_uk": "Я іноді така необережна, що залишаю ключ ззовні в дверях"}),
    12766: (T + "ru/uk/en/it/es/fr «диабет у детей» — везде «у деда диабет, следит за питанием»", {"example_ru": "У дедушки диабет, и ему приходится следить за питанием", "example_uk": "У дідуся діабет, і йому доводиться стежити за харчуванням", "example_en": "My grandad has diabetes and has to watch what he eats", "example_it": "Mio nonno ha il diabete e deve stare attento a quello che mangia", "example_es": "Mi abuelo tiene diabetes y tiene que vigilar lo que come", "example_fr": "Mon grand-père a du diabète et doit faire attention à ce qu'il mange"}),
}

REPLACE = []
SPLIT_LATER = {}
