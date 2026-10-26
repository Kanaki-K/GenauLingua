"""Шаг 2, en, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    10784: (T + "word in example", {"t_en": "disgust, (vor Ekel) disgusted"}),
    11286: (T + "word in example", {"x_en": "Doing a parachute jump at sixty is the kind of craziness only my uncle would come up with"}),
    11348: (T + "grammar", {"x_en": "With my leg in plaster I'm condemned to doing nothing and watching series all day"}),
    11590: (T + "word in example", {"x_en": "My son had the boldness to ask the head whether homework could be scrapped"}),
}

REPLACE = []
SPLIT_LATER = {}
