"""Шаг 2, tr, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    6324: (T + "word in example", {"x_tr": "Oradan dışarı çık"}),
    6364: (T + "word in example", {"t_tr": "nokta, puan, (Punkt acht) tam saat sekiz"}),
    6715: (T + "word in example", {"x_tr": "Tipik Max, yine geç kalıyor"}),
    7464: (T + "word in example", {"t_tr": "iyilik, refah, (zum Wohl) şerefe"}),
    13338: (T + "word in example", {"t_tr": "ona, buna"}),
    13446: (T + "word in example", {"t_tr": "bu sayede, böylece, bu yüzden"}),
    13815: (T + "word in example", {"t_tr": "ah, of, ha"}),
    14899: (T + "word in example", {"t_tr": "adam, tip, biri"}),
    15929: (T + "word in example", {"t_tr": "kurban, (kazada) ölen ya da yaralanan"}),
}

REPLACE = []
SPLIT_LATER = {}
