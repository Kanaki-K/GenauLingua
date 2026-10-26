"""Полная вычитка, порция 50: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    18388: (T + "ru/uk/en/it/es/fr «твоя комната — свинарник» — везде «после вечеринки кухня как свинарник»", {"example_ru": "После вечеринки наша кухня выглядит как свинарник", "example_uk": "Після вечірки наша кухня схожа на свинарник", "example_en": "After the party our kitchen looks like a pigsty", "example_tr": "Partiden sonra mutfağımız ahıra döndü", "example_it": "Dopo la festa la nostra cucina sembra un porcile", "example_es": "Después de la fiesta nuestra cocina parece una pocilga", "example_fr": "Après la fête, notre cuisine, c'est un vrai foutoir"}),
    18908: (T + "de/tr/pl/cs «соседский малыш кричит» — везде «непрестанный шум со стройки»", {"example_de": "Der unaufhörliche Lärm von der Baustelle macht mich wahnsinnig", "example_ru": "Непрестанный шум со стройки сводит меня с ума", "example_uk": "Невпинний шум із будмайданчика зводить мене з розуму", "example_en": "The incessant noise from the building site is driving me mad", "example_tr": "Şantiyeden gelen aralıksız gürültü beni deli ediyor", "example_pl": "Nieustanny hałas z budowy doprowadza mnie do szału", "example_it": "Il rumore incessante dei lavori mi fa impazzire", "example_es": "El ruido incesante de las obras me vuelve loco", "example_fr": "Le bruit incessant des travaux me rend fou", "example_cs": "Nepřetržitý hluk ze stavby mě přivádí k šílenství"}),
}

REPLACE = []
SPLIT_LATER = {}
