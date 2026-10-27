"""Шаг 2, cs, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    9887: (T + "в примере nedá se koupit", {"t_cs": "na prodej, úplatný, (nicht käuflich) nedá se koupit"}),
    10822: (T + "в примере osvítilo", {"t_cs": "osvícení, (eine Erleuchtung haben) osvítit"}),
    10833: (T + "в примере uboze", {"t_cs": "ubohý, chudý, uboze"}),
    10858: (T + "в примере nedbale", {"t_cs": "nedbalý, odbytý, nedbale"}),
    10875: (T + "в примере spokojeně", {"t_cs": "spokojený, spokojeně"}),
    10876: (T + "в примере глагол zklamalo", {"t_cs": "zklamávající, (enttäuschend sein) zklamat"}),
    10890: (T + "в примере lituje se", {"t_cs": "sebelítost, (in Selbstmitleid baden) litovat se"}),
    10921: (T + "в примере cynicky", {"t_cs": "cynický, cynicky"}),
    10971: (T + "в примере panicky", {"t_cs": "panický, panicky"}),
    10975: (T + "в примере nebojácně", {"t_cs": "nebojácný, nebojácně"}),
    10990: (T + "в примере zmateně", {"t_cs": "zmatený, podrážděný, zmateně"}),
    10992: (T + "в примере nezlobí", {"t_cs": "nevychovaný, zlobivý, (ungezogen sein) zlobit"}),
    11003: (T + "в примере autenticky", {"t_cs": "autentický, pravý, autenticky"}),
    11012: (T + "в примере nepřátelsky", {"t_cs": "nepřátelský, nepřátelsky"}),
    11025: (T + "в примере sarkasticky", {"t_cs": "sarkastický, sarkasticky"}),
}

REPLACE = []
SPLIT_LATER = {}
