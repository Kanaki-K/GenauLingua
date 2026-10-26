"""Полная вычитка, порция 38: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    18663: (T + "de/tr/pl/cs «после еды хочу отдохнуть» — везде «пусть отдыхает, он болеет»", {"example_de": "Lass ihn ruhen, er ist krank", "example_ru": "Не буди его, пусть отдыхает, он болеет", "example_uk": "Не буди його, хай відпочиває, він хворий", "example_en": "Let him rest, he's ill", "example_tr": "Bırak dinlensin, hasta", "example_pl": "Daj mu odpocząć, jest chory", "example_it": "Lascialo riposare, è malato", "example_es": "Déjalo descansar, está enfermo", "example_fr": "Laisse-le se reposer, il est malade", "example_cs": "Nech ho odpočívat, je nemocný"}),
    18728: (T + "de/tr/pl/cs книжное «рутина помогает быть организованным» — везде «утром у меня своя рутина: кофе, душ, газета»", {"example_de": "Morgens habe ich meine kleine Routine: Kaffee, Dusche, Zeitung", "example_ru": "Утром у меня свой маленький распорядок: кофе, душ, новости", "example_uk": "Зранку в мене свій маленький розпорядок: кава, душ, новини", "example_en": "In the morning I have my little routine: coffee, shower, paper", "example_tr": "Sabahları küçük bir rutinim var: kahve, duş, gazete", "example_pl": "Rano mam swoją małą rutynę: kawa, prysznic, gazeta", "example_it": "Al mattino ho la mia piccola routine: caffè, doccia, giornale", "example_es": "Por las mañanas tengo mi pequeña rutina: café, ducha, periódico", "example_fr": "Le matin, j'ai ma petite routine : café, douche, journal", "example_cs": "Ráno mám svou malou rutinu: káva, sprcha, noviny"}),
    18747: (T + "de/tr/pl/cs «на рыбалку на рассвете» — везде «выехали на рассвете, чтобы не попасть в пробки»", {"example_de": "Wir sind im Morgengrauen losgefahren, um dem Stau zu entgehen", "example_ru": "Мы выехали на рассвете, пока дороги ещё пустые", "example_uk": "Ми виїхали на світанку, поки дороги ще порожні", "example_en": "We set off at dawn to avoid the traffic", "example_tr": "Trafiğe kalmamak için şafakta yola çıktık", "example_pl": "Wyjechaliśmy o świcie, żeby uniknąć korków", "example_it": "Siamo partiti all'alba per evitare il traffico", "example_es": "Salimos al amanecer para evitar el tráfico", "example_fr": "On est partis à l'aube pour éviter les bouchons", "example_cs": "Vyrazili jsme za svítání, abychom se vyhnuli zácpám"}),
    18755: (T + "ru/uk «годовщина свадьбы» — везде «годовщина падения Стены»", {"example_ru": "В годовщину падения Берлинской стены в Берлине проходит большой концерт", "example_uk": "У річницю падіння Берлінського муру в Берліні відбувається великий концерт"}),
    18779: (T + "uk «двенадцать блюд» — «дарим друг другу подарки»", {"example_uk": "На Святвечір ми даруємо одне одному подарунки"}),
}

REPLACE = []
SPLIT_LATER = {}
