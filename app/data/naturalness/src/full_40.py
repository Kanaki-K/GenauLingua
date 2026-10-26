"""Полная вычитка, порция 40: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    9569: (T + "de/tr/pl/cs «дед в 70 выучился плавать» — везде «никогда не поздно выучить язык»", {"example_de": "Es ist nie zu spät, eine Sprache zu erlernen", "example_ru": "Никогда не поздно освоить новый язык", "example_uk": "Ніколи не пізно опанувати нову мову", "example_en": "It's never too late to master a language", "example_tr": "Bir dil öğrenmek için asla geç değil", "example_pl": "Nigdy nie jest za późno, żeby nauczyć się języka", "example_it": "Non è mai troppo tardi per imparare una lingua", "example_es": "Nunca es tarde para aprender un idioma", "example_fr": "Il n'est jamais trop tard pour apprendre une langue", "example_cs": "Nikdy není pozdě naučit se nový jazyk"}),
    10822: (T + "ru/uk «паспорт» — «потерянный ключ от машины»", {"example_ru": "В душе меня озарило, где лежит потерянный ключ от машины", "example_uk": "У душі мене осяяло, де лежить загублений ключ від машини"}),
}

REPLACE = []
SPLIT_LATER = {}
