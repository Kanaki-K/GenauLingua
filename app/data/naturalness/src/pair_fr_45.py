"""Шаг 2, fr, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    8191: (T + "в примере chauffer", {"t_fr": "chaud (fam.), délicat, (brenzlig werden) chauffer"}),
    8198: (T + "в примере un mystère", {"t_fr": "mystérieux, énigmatique, un mystère"}),
    8350: (T + "в примере emprunter une voie", {"t_fr": "prendre, défoncer, emprunter (une voie)"}),
    8375: (T + "нет convenir", {"x_fr": "Alors, on convient de quoi : on se retrouve samedi à dix heures ?"}),
    8449: (T + "в примере sclérose en plaques", {"t_fr": "multiple, (multiple Sklerose) la sclérose en plaques"}),
    8470: (T + "в примере à toute vitesse", {"t_fr": "rapidement, en flèche, à toute vitesse"}),
    8535: (T + "в примере inexorablement", {"t_fr": "inexorable, impossible à arrêter, inexorablement"}),
    8564: (T + "нет inaudible", {"x_fr": "Ma chatte s'approche de façon presque inaudible et me saute sur les genoux"}),
    18804: (T + "в примере tomber mal", {"t_fr": "inopportun, (ungelegen kommen) tomber mal"}),
    18828: (T + "нет anniversaire/jubilé", {"x_fr": "Pour l'anniversaire de leurs cinquante ans de mariage, mes grands-parents dansent sur leur chanson comme autrefois"}),
    18843: (T + "в примере précipitamment", {"t_fr": "précipité, hâtif, précipitamment"}),
}

REPLACE = []
SPLIT_LATER = {}
