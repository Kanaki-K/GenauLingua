"""Шаг 2, tr, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    7756: (T + "word in example", {"t_tr": "başına gelmek, (wie ergeht es dir) nasıl gitmek"}),
    7805: (T + "word in example", {"t_tr": "kısmen, bir kısmı, kimi"}),
    7809: (T + "word in example", {"t_tr": "atmak, kâr getirmek, (ürün) vermek"}),
    7820: (T + "word in example", {"t_tr": "açılışını yapmak, ilk kez kullanmak, sırrı paylaşmak"}),
    7848: (T + "word in example", {"t_tr": "mühürlemek, yalıtmak, vernikle kaplamak"}),
    7849: (T + "word in example", {"t_tr": "serbest bırakmak, onaylamak, izin vermek"}),
    7929: (T + "word in example", {"t_tr": "güçlerini birleştirmek, bir araya gelmek"}),
    7936: (T + "word in example", {"t_tr": "çivilemek, köşeye sıkıştırmak, (auf etwas festnageln) söz olarak almak"}),
    7955: (T + "word in example", {"t_tr": "yetişmek, açığı kapatmak, geçmek"}),
    7968: (T + "word in example", {"t_tr": "kısmen, az da olsa, azıcık"}),
    9008: (T + "word in example", {"t_tr": "istifa, görevi bırakma"}),
}

REPLACE = []
SPLIT_LATER = {}
