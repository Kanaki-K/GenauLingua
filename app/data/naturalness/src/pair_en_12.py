"""Шаг 2, en, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    2490: (T + "word in example", {"x_en": "After the argument I was full of frustration"}),
    2497: (T + "word in example", {"t_en": "corridor, gear, aisle"}),
    2521: (T + "word in example", {"t_en": "legal, statutory, by law"}),
    2553: (T + "word in example", {"t_en": "homesickness, longing for home, (Heimweh haben) to be homesick"}),
    2592: (T + "word in example", {"t_en": "Jew, (Jude sein) to be Jewish"}),
    2596: (T + "word in example", {"t_en": "candidate, applicant, contestant"}),
    2599: (T + "word in example", {"t_en": "purchase, buying, buy"}),
    2643: (T + "word in example", {"t_en": "warehouse, camp, (auf Lager) in stock"}),
    2734: (T + "natural", {"x_en": "He stayed away in protest"}),
}

REPLACE = []
SPLIT_LATER = {}
