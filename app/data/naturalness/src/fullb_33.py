"""Полная вычитка, порция 33: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    13013: (T + "ru/uk «клинически белая» — калька", {"example_ru": "Приёмная у стоматолога такая белая, прямо как в клинике, что я нервничаю, едва сажусь", "example_uk": "Приймальня в стоматолога така біла, як у клініці, що я нервую, щойно сідаю"}),
    13150: (T + "en «the most children are always standing» — неуклюже", {"example_en": "There's an albino kangaroo at the zoo, and there are always more children in front of its enclosure than anywhere else"}),
    13527: (T + "ru/uk «Это, в свою очередь, другая проблема» — книжно", {"example_ru": "А это опять же совсем другая проблема", "example_uk": "А це знову ж таки зовсім інша проблема"}),
    14039: (T + "ru/uk «Факт есть факт: если…» — не к месту", {"example_ru": "Факт: если мы сейчас не выедем, опоздаем на поезд", "example_uk": "Факт: якщо ми зараз не виїдемо, запізнимося на поїзд"}),
    14055: (T + "ru «уведомлю», uk «сповіщу», en «notify» — канцелярит", {"example_ru": "Я тебе сообщу, как только приеду", "example_uk": "Я тобі повідомлю, щойно приїду", "example_en": "I'll let you know as soon as I arrive"}),
    14120: (T + "es «hablar con palabras claras» — неестественно", {"example_es": "Ahora vamos a hablar claro: ¿quién se ha comido el chocolate del armario?"}),
    14197: (T + "ru/uk «по рации радиосообщение» — тавтология", {"example_ru": "Таксист получает радиосообщение со следующим адресом и сразу разворачивается", "example_uk": "Таксист отримує радіоповідомлення з наступною адресою й одразу розвертається"}),
    14221: (T + "ru «ведёт разговоры сама с собой», cs «vede rozhovory» — книжно", {"example_ru": "Она часто разговаривает сама с собой, когда нервничает", "example_cs": "Když je nervózní, často mluví sama se sebou"}),
}

REPLACE = []
SPLIT_LATER = {}
