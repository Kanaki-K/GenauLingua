"""Шаг 2, fr, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    6848: (T + "в примере doucement", {"t_fr": "doux, doucement"}),
    6873: (T + "в примере descendre", {"t_fr": "en bas, (herunterkommen) descendre"}),
    6876: (T + "в примере descendre", {"t_fr": "en bas, vers le bas, (hinuntergehen) descendre"}),
    6898: (T + "в примере se ménager", {"t_fr": "procurer, se procurer, (sich Zeit verschaffen) se ménager du temps"}),
    6927: (T + "в примере remplaçant", {"t_fr": "le substitut, le remplacement, le remplaçant"}),
    6970: (T + "в примере être valable", {"t_fr": "s'appliquer, passer pour, être valable"}),
    6992: (T + "в примере lacer", {"t_fr": "nouer, attacher, lacer"}),
    7005: (T + "в примере approximativement", {"t_fr": "grossier, approximatif, approximativement"}),
    7032: (T + "в примере marcher", {"t_fr": "marcher au pas, défiler, marcher"}),
    7076: (T + "в примере en pente", {"t_fr": "de travers, bizarre, en pente"}),
    7124: (T + "в примере à l'origine", {"t_fr": "original, initial, à l'origine"}),
    7291: (T + "в примере individuellement", {"t_fr": "individuel, séparé, individuellement"}),
    7313: (T + "нет global", {"x_fr": "Le réchauffement climatique est un problème global pour notre avenir"}),
    7456: (T + "в примере officieusement", {"t_fr": "officieux, non officiel, officieusement"}),
    7532: (T + "в примере monter", {"t_fr": "en haut, vers le haut, (heraufkommen) monter"}),
}

REPLACE = []
SPLIT_LATER = {}
