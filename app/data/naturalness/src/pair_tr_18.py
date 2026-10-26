"""Шаг 2, tr, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    10035: (T + "word in example", {"t_tr": "şeytan, iblis, (was zum Teufel) ne halt"}),
    10221: (T + "word in example", {"t_tr": "akıllı, zeki, kurnaz"}),
    10222: (T + "word in example", {"t_tr": "yapabilen, yetenekli, (zu allem fähig) her şey beklenir"}),
    10245: (T + "word in example", {"t_tr": "felaket, kaza, talihsizlik"}),
    10254: (T + "word in example", {"t_tr": "isteksizce, istemeyerek, (ungern tun) sevmemek"}),
    10297: (T + "word in example", {"t_tr": "faydalı, yararlı, yardımcı"}),
    10360: (T + "word in example", {"t_tr": "kötü, nahoş, (ungutes Gefühl) içi rahat olmamak"}),
}

REPLACE = []
SPLIT_LATER = {}
