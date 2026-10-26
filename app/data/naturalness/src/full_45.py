"""Полная вычитка, порция 45: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    8359: (T + "ru/uk/en/it/es/fr «в конце концов он поддался» — везде «перед шоколадом поддаюсь любому искушению»", {"example_ru": "Перед шоколадом я поддаюсь любому искушению", "example_uk": "Перед шоколадом я піддаюся будь-якій спокусі", "example_en": "When it comes to chocolate I succumb to every temptation", "example_it": "Con il cioccolato cedo davvero a ogni tentazione", "example_es": "Con el chocolate sucumbo a cualquier tentación", "example_fr": "Avec le chocolat, je succombe vraiment à toutes les tentations"}),
    8393: (T + "de/tr/pl/cs голое «это не обязательно» — везде «присутствие не обязательно»", {"example_de": "Die Teilnahme ist nicht zwingend", "example_ru": "Посещение не обязательно", "example_uk": "Відвідування не обов'язкове", "example_en": "Attendance is not mandatory", "example_tr": "Katılım zorunlu değil", "example_pl": "Obecność nie jest obowiązkowa", "example_it": "La presenza non è strettamente necessaria", "example_es": "La asistencia no es imprescindible", "example_fr": "La présence n'est pas obligatoire", "example_cs": "Účast není nutná"}),
}

REPLACE = []
SPLIT_LATER = {}
