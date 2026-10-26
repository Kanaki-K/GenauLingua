"""Шаг 2, tr, порция 2: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    554: (T + "word in example", {"t_tr": "yatmak, uzanmak, bulunmak"}),
    655: (T + "word in example", {"t_tr": "asla, hiçbir zaman, hiç"}),
    817: (T + "word in example", {"t_tr": "kız kardeş, abla, hemşire"}),
    894: (T + "word in example", {"t_tr": "üniversite eğitimi, üniversite"}),
    1102: (T + "word in example", {"t_tr": "almaya gitmek, almaya gelmek"}),
    1153: (T + "word in example", {"t_tr": "iştah, (Guten Appetit) afiyet olsun"}),
    1160: (T + "word in example", {"t_tr": "iş yeri, çalışma yeri"}),
}

REPLACE = []
SPLIT_LATER = {}
