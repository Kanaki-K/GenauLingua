"""Шаг 2, tr, порция 37: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    17205: (T + "word in example", {"t_tr": "araba gezisi, kısa tur"}),
    17365: (T + "word in example", {"t_tr": "kısa uğrama, uğramak"}),
    17403: (T + "word in example", {"t_tr": "kaza inişi, (mecazi) felaket"}),
    17673: (T + "word in example", {"t_tr": "açık bırakmak, (giysiyi) çıkarmamak"}),
    17687: (T + "word in example", {"t_tr": "kapatmak, azaltmak, düşürmek"}),
    17719: (T + "word in example", {"t_tr": "gazyağı, (Petroleumlampe) gaz lambası"}),
    17741: (T + "word in example", {"t_tr": "talep, erişim, (auf Abruf) istendiği zaman"}),
    17950: (T + "word in example", {"t_tr": "kütle, kalabalık, (hamur) kıvam"}),
    17960: (T + "word in example", {"t_tr": "unsur, element, (in seinem Element) kendi ortamında"}),
    18028: (T + "word in example", {"t_tr": "araştırmak, aramak"}),
    18243: (T + "word in example", {"t_tr": "bulvar, (Boulevardpresse) magazin basını"}),
    18274: (T + "word in example", {"t_tr": "askı, stand, (Schirmständer) şemsiyelik"}),
}

REPLACE = []
SPLIT_LATER = {}
