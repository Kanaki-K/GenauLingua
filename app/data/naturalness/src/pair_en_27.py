"""Шаг 2, en, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    7102: (T + "word in example", {"t_en": "to be due to, to approach, (zukommen auf) to come one's way"}),
    7145: (T + "word in example", {"t_en": "to retreat, to give way, (nicht von der Seite weichen) not to leave someone's side"}),
    7159: (T + "word in example", {"t_en": "to point, to interpret, to indicate"}),
    7176: (T + "word in example", {"t_en": "to cause, to bring about, (Wunder bewirken) to work wonders"}),
    7212: (T + "word in example", {"t_en": "shine, splendour, gleam"}),
    7303: (T + "word in example", {"x_en": "The new law enables many people to study"}),
    7421: (T + "word in example", {"x_en": "The children ate all the chocolate from the cupboard unnoticed"}),
}

REPLACE = []
SPLIT_LATER = {}
