"""Шаг 2, pl, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    10048: (T + "word in example", {"t_pl": "szczery, uczciwy, (ehrlich gesagt) szczerze mówiąc"}),
    10197: (T + "word in example", {"t_pl": "zadowolony, ucieszony, rad"}),
    10231: (T + "word in example", {"t_pl": "puszczać, puścić, zostawiać w spokoju"}),
    10281: (T + "word in example", {"t_pl": "ryczeć, wyć, płakać"}),
    10318: (T + "word in example", {"t_pl": "sprawiedliwy, uczciwy, sprawiedliwie"}),
    10360: (T + "word in example", {"t_pl": "zły, nieprzyjemny, niedobry"}),
    10361: (T + "word in example", {"t_pl": "pomocny, chętny do pomocy, (behilflich sein) pomóc"}),
    10382: (T + "word in example", {"t_pl": "mroczny, ponury, ponuro"}),
    10415: (T + "word in example", {"t_pl": "żałosny, okropny, żałośnie"}),
    10418: (T + "word in example", {"t_pl": "rozproszenie uwagi, rozrywka, oderwanie się"}),
}

REPLACE = []
SPLIT_LATER = {}
