"""Полная вычитка, порция 34: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    14249: (T + "ru/uk «время отхода ко сну» — канцелярит", {"example_ru": "Дочь уже в восемь лет доказывает своё, как адвокат, когда речь заходит о том, во сколько ложиться спать", "example_uk": "Донька вже у вісім років доводить своє, як адвокатка, коли йдеться про те, о котрій лягати спати"}),
    14318: (T + "en/it/es/fr «bearer/portatore/portador/porteur» — так не говорят; uk «посланець» — книжно", {"example_uk": "Кур'єр зі святковим тортом подзвонив не в ті двері, і сусідка страшенно зраділа", "example_en": "The man delivering the birthday cake rang the wrong doorbell, and the neighbour was over the moon", "example_it": "Il fattorino con la torta di compleanno ha suonato alla porta sbagliata, e la vicina è stata felicissima", "example_es": "El repartidor de la tarta de cumpleaños llamó a la puerta equivocada, y la vecina se puso contentísima", "example_fr": "Le livreur du gâteau d'anniversaire a sonné à la mauvaise porte, et la voisine était ravie"}),
    14479: (T + "ru/uk «бас очень глубокий» — калька", {"example_ru": "Бас в этой песне очень низкий", "example_uk": "Бас у цій пісні дуже низький"}),
    14514: (T + "ru/uk «он как фантом» — неестественно", {"example_ru": "Полиция уже много лет ищет взломщика, но он прямо как призрак", "example_uk": "Поліція вже багато років шукає зломщика, але він наче примара"}),
    14539: (T + "pl/it/es/fr/cs «без рукописи» — в речи так не говорят", {"example_pl": "Bez kartki nie umiem wygłosić przemówienia, bo wszystko zapominam", "example_it": "Senza un foglio davanti non riesco a fare un discorso, altrimenti dimentico tutto", "example_es": "Sin el papel delante no puedo dar un discurso, se me olvida todo", "example_fr": "Sans mes notes, je ne peux pas faire de discours, sinon j'oublie tout", "example_cs": "Bez papíru nedokážu mít projev, jinak všechno zapomenu"}),
    14653: (T + "tr «kokteyl yaratıyor» — калька", {"example_tr": "Barmenimiz her cuma yeni bir kokteyl icat ediyor ve ona bir müdavimin adını veriyor"}),
    14763: (T + "ru/uk «настоящий шедевр» — не тот смысл (мастерский ход)", {"example_ru": "Загнать собаку в ванну без лакомства — это был настоящий мастерский ход", "example_uk": "Загнати пса у ванну без ласощів — це був справжній майстерний хід"}),
    14839: (T + "fr «je ne tombe sur aucune note juste» — неестественно", {"example_fr": "Pendant le chant choral du réveillon, je chante tout bas parce que je chante complètement faux"}),
    15044: (T + "ru «арендодатель», uk «орендодавець» — канцелярит", {"example_ru": "Хозяин квартиры сразу выполнил нашу просьбу и починил отопление", "example_uk": "Власник квартири одразу виконав наше прохання й полагодив опалення"}),
    15117: (T + "ru/uk «спрятал на записке» — неуклюже", {"example_ru": "Предложение руки и сердца он написал на записке и спрятал в её печенье с предсказанием", "example_uk": "Пропозицію руки і серця він написав на записці й сховав у її печиві з передбаченням"}),
}

REPLACE = []
SPLIT_LATER = {}
