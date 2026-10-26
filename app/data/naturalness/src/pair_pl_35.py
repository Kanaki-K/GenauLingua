"""Шаг 2, pl, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    15530: (T + "word in example", {"t_pl": "tama, grobla, wał"}),
    15593: (T + "word in example", {"t_pl": "wyrosnąć, wyrastać, wschodzić"}),
    16155: (T + "word in example", {"t_pl": "prezydentka, przewodnicząca, prezeska"}),
    16157: (T + "word in example", {"t_pl": "ankieta, sondaż, przesłuchanie"}),
    16190: (T + "word in example", {"t_pl": "przesłuchiwać, (sich verhören) przesłyszeć się"}),
    16215: (T + "word in example", {"t_pl": "przykazanie, nakaz, oferta (na aukcji)"}),
    16220: (T + "word in example", {"t_pl": "zastrzelić, strzelać do"}),
}

REPLACE = []
SPLIT_LATER = {}
