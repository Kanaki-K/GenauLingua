"""Шаг 2, pl, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    6324: (T + "word in example", {"t_pl": "na zewnątrz, (heraus!) wyjdź stamtąd"}),
    6329: (T + "word in example", {"t_pl": "rzeczywiście, faktycznie, naprawdę"}),
    6468: (T + "word in example", {"t_pl": "dogadać się, porozumieć się, umówić się"}),
    6473: (T + "word in example", {"t_pl": "dziać się, zdarzać się, stać się"}),
    6528: (T + "word in example", {"t_pl": "skąpy, ledwie, (knapp sein) mało"}),
    6613: (T + "word in example", {"t_pl": "przyjść tutaj, podejść, tu przyjść"}),
    7288: (T + "word in example", {"t_pl": "właściwy, rzeczywisty, prawdziwy"}),
    7464: (T + "word in example", {"t_pl": "dobro, pomyślność, (zum Wohl!) na zdrowie"}),
    8448: (T + "word in example", {"t_pl": "patrzeć, zerkać, popatrzeć"}),
    8994: (T + "word in example", {"t_pl": "ubiegać się, starać się, reklamować"}),
    10128: (T + "word in example", {"t_pl": "szalony, obłędny, (das ist irre) to szaleństwo"}),
    10129: (T + "word in example", {"t_pl": "zainteresowanie, (Interesse haben) interesować się"}),
    10266: (T + "word in example", {"t_pl": "dramatyczny, (nicht dramatisch machen) nie dramatyzować"}),
    12461: (T + "word in example", {"t_pl": "umierać, umrzeć, ginąć"}),
    12474: (T + "word in example", {"t_pl": "obudzony, rozbudzony, (wach sein) nie spać"}),
    13300: (T + "word in example", {"t_pl": "mieć na myśli, uważać, sądzić"}),
    13315: (T + "word in example", {"t_pl": "z tego, o tym, z niego, z niej"}),
    13335: (T + "word in example", {"t_pl": "o tym, to, tego"}),
    13384: (T + "word in example", {"x_pl": "Wczoraj przed dworcem mój rower został skradziony"}),
    13920: (T + "word in example", {"t_pl": "opisywać, opisać"}),
    13967: (T + "word in example", {"t_pl": "wymawiać, wymówić, wypowiadać"}),
}

REPLACE = []
SPLIT_LATER = {}
