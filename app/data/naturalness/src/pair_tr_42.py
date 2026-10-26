"""Шаг 2, tr, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    12889: (T + "word in example", {"t_tr": "nüks, eski alışkanlığa dönüş, yeniden başlama"}),
    13572: (T + "word in example", {"t_tr": "özellikle de, üstelik, hele"}),
    13713: (T + "word in example", {"t_tr": "giyinmek, giymek"}),
    13750: (T + "word in example", {"t_tr": "giydirmek, giyinmek, (makam) işgal etmek"}),
    14118: (T + "word in example", {"t_tr": "arabuluculuk yapmak, aktarmak, aracı olmak"}),
    14168: (T + "word in example", {"t_tr": "demek, belirtmek, söylemek"}),
    14184: (T + "word in example", {"t_tr": "açıklama, duruş"}),
    15145: (T + "word in example", {"t_tr": "yeni gelen, çaylak, yeni öğrenci"}),
}

REPLACE = []
SPLIT_LATER = {}
