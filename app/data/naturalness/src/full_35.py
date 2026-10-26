"""Полная вычитка, порция 35: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    15320: (T + "ru/uk «не успел бы на поезд» — «без запасного ключа ночевал бы в подъезде»", {"example_ru": "Ты моя спасительница! Без твоего запасного ключа я бы ночевал в подъезде", "example_uk": "Ти моя рятівниця! Без твого запасного ключа я б ночував у під'їзді"}),
    16198: (T + "de/tr/pl/cs «паспорт оказался поддельным» — везде «сумка Chanel за 30 евро — подделка»", {"example_de": "Eine Chanel-Tasche für dreißig Euro ist garantiert eine Fälschung", "example_ru": "Сумка Chanel за тридцать евро — это точно подделка", "example_uk": "Сумка Chanel за тисячу гривень — це точно підробка", "example_en": "A Chanel bag for thirty quid has to be a fake", "example_tr": "Otuz avroya Chanel çanta kesin sahtedir", "example_pl": "Torebka Chanel za trzydzieści euro to na pewno podróbka", "example_it": "Una borsa Chanel a 30 euro è per forza una contraffazione", "example_es": "Un bolso de Chanel a 30 euros es seguro una falsificación", "example_fr": "Ce sac Chanel à 30 euros, c'est forcément une contrefaçon", "example_cs": "Kabelka Chanel za třicet eur je určitě padělek"}),
    16206: (T + "de/tr/pl/cs «наказание было строгим» — везде «в наказание неделя без телефона»", {"example_de": "Zur Bestrafung gibt es eine Woche kein Handy", "example_ru": "В наказание — неделя без телефона", "example_uk": "Як покарання — тиждень без телефона", "example_en": "As a punishment, no phone for a week", "example_tr": "Ceza olarak bir hafta telefon yok", "example_pl": "Za karę tydzień bez telefonu", "example_it": "Per punizione niente telefono per una settimana", "example_es": "De castigo, una semana sin móvil", "example_fr": "Comme punition, il est privé de téléphone pendant une semaine", "example_cs": "Za trest týden bez mobilu"}),
    16256: (T + "de/tr/pl/cs книжное «кодекс регулирует поведение» — везде «у байкеров свой кодекс чести»", {"example_de": "Unter Bikern gibt es einen eigenen Kodex", "example_ru": "У байкеров свой кодекс чести", "example_uk": "У байкерів є свій кодекс честі", "example_en": "Bikers have a code of honour", "example_tr": "Motorcuların kendi onur kuralları var", "example_pl": "Motocykliści mają swój kodeks honorowy", "example_it": "Tra i motociclisti c'è un codice d'onore", "example_es": "Entre los moteros hay un código de honor", "example_fr": "Chez les motards, il y a un code d'honneur", "example_cs": "Motorkáři mají svůj kodex cti"}),
}

REPLACE = []
SPLIT_LATER = {}
