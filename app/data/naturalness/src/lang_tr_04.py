"""Вычитка турецкого, порция p004 (A2), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    57: (T + "«mesleki eğitim yapıyor» — так не говорят", {"example_tr": "Aşçılık üzerine mesleki eğitim alıyor"}),
    170: (T + "«Bununla ne istersin?» — подстрочник", {"example_tr": "Yanında ne istersin?"}),
    289: (T + "«Çok seviniyorum» — неестественно", {"example_tr": "Çok sevindim"}),
    730: (T + "«Kilogram başına … tutuyor» — тяжело", {"example_tr": "Kilo başına beş euro"}),
    731: (T + "о еде — «tadına bakmak»", {"example_tr": "Tadına bakmak ister misin?"}),
    1013: (T + "«bozdurmak» — разменять; валюту «çevirmek»", {"example_tr": "Euromu dolara çevirmek istiyorum"}),
    1081: (T + "«sonra çalışmak» — инфинитив звучит как инструкция", {"example_tr": "Önce kahvaltı, sonra iş"}),
    1093: (T + "«Hiç yemek istiyor musun?» — «ты вообще…» = «…ki?»", {"example_tr": "Sen aslında yemek istiyor musun ki?"}),
}

REPLACE = []

SPLIT_LATER = {}
