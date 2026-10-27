"""Шаг 2, cs, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    1104: (T + "в примере odložit", {"t_cs": "složit (zkoušku), sundat si, odložit"}),
    1106: (T + "в примере čte z papíru", {"t_cs": "přečíst, odečíst, číst (z papíru)"}),
    1148: (T + "в примере požádat o ruku", {"t_cs": "žádost, návrh, (Heiratsantrag) požádat o ruku"}),
    1219: (T + "в примере bezhotovostně", {"t_cs": "bezhotovostní, bezhotovostně"}),
}

REPLACE = []
SPLIT_LATER = {}
