"""Шаг 2, en, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    6398: (T + "word in example", {"t_en": "to be right, to vote, to add up"}),
    6411: (T + "word in example", {"t_en": "to be enough, to pass, to last"}),
    6418: (T + "word in example", {"t_en": "to grab, to grasp mentally, to take in"}),
    6460: (T + "word in example", {"x_en": "I have quite a few things to do"}),
    6486: (T + "word in example", {"x_en": "She kept watch all night at her sick son's bedside"}),
    6560: (T + "Wi-Fi", {"x_en": "My phone is connected to the Wi-Fi"}),
    6563: (T + "word in example", {"t_en": "to maintain, to preserve, to keep (calm)"}),
    6609: (T + "word in example", {"x_en": "The toilets are located on the first floor"}),
    6620: (T + "word in example", {"t_en": "to manage, properly, (sich zurechtfinden) to find one's way around"}),
    6714: (T + "word in example", {"x_en": "That's possibly too expensive for us"}),
    6743: (T + "word in example", {"x_en": "Please keep a distance of one metre from me"}),
    6762: (T + "word in example", {"t_en": "to look, to show up, (sich blicken lassen) to come and see"}),
    6774: (T + "word in example", {"x_en": "Nothing can keep me from it"}),
    6784: (T + "word in example", {"t_en": "to use, to deploy, to put on (extra trains)"}),
    6816: (T + "word in example", {"x_en": "We need to go back now, it's getting dark"}),
    6819: (T + "word in example", {"x_en": "We're locked in the lift"}),
}

REPLACE = []
SPLIT_LATER = {}
