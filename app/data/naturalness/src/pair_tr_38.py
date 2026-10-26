"""Шаг 2, tr, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    7598: (T + "word in example", {"t_tr": "eski haline getirmek, onarmak, yeniden sağlamak"}),
    7626: (T + "word in example", {"t_tr": "-ebilmek, gücü yetmek, başarabilmek"}),
    7648: (T + "word in example", {"t_tr": "kabul ettirmek, (sich durchsetzen) dediğini yaptırmak"}),
    7733: (T + "word in example", {"t_tr": "örtmek, kaplamak, kapatmak"}),
    7744: (T + "word in example", {"t_tr": "götürmek, (wo soll das hinführen) nereye varmak"}),
    7754: (T + "word in example", {"t_tr": "almak, talep etmek, kaplamak"}),
    18657: (T + "word in example", {"t_tr": "sonsuzluk, (eine Ewigkeit) asırlar"}),
}

REPLACE = []
SPLIT_LATER = {}
