"""Вычитка турецкого, порция p010 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    1797: (T + "«daha çok temizlik işi var» — двусмысленно («больше»)", {"example_tr": "Tadilattan sonra hâlâ yapılacak çok temizlik var"}),
    1801: (T + "«seyahat hedefi» — канцелярит", {"translation_tr": "gidilecek yer, tatil yeri", "example_tr": "Yaz için gideceğimiz yer henüz belli değil, belki Hırvatistan"}),
    1821: (T + "griechischer Salat — «Yunan salatası», не «çoban salatası»", {"example_tr": "Yunan salatası için daha koyun peyniri lazım"}),
    1877: (T + "«O dikkatli çalışıyor» — лишнее «O»", {"example_tr": "Çok özenli çalışıyor"}),
    1883: (T + "«Bir yürüyüş yapıyoruz» — калька", {"example_tr": "Yürüyüşe çıkıyoruz"}),
    1919: (T + "«yol parçası» — канцелярит; Strecke = «güzergâh»", {"example_tr": "Bu güzergâhta sık sık trafik oluyor"}),
    1928: (T + "«O iyi bir dansçı» — лишнее «O»", {"example_tr": "İyi bir dansçı"}),
    1933: (T + "«Değiştirebilir miyiz?» — неясно", {"example_tr": "Değişelim mi?"}),
    1954: (T + "«Bayern'e oynuyorum» = «ставлю деньги»; tippen = угадывать", {"example_tr": "Tahminim Bayern şampiyon olacak"}),
    2024: (T + "«yarın erken çalışıyorum» — подстрочник", {"example_tr": "Maalesef artık vedalaşmam lazım, yarın işe erken gidiyorum"}),
    2134: (T + "«O çok güvenilir» — лишнее «O»", {"example_tr": "Çok güvenilir biridir"}),
    2136: (T + "zwischendurch — «между делом», не «изредка»", {"example_tr": "Arada bir elma yiyorum"}),
    2145: (T + "Absage — отказ, а не «отменить»", {"example_tr": "Cumartesi için maalesef sana hayır demek zorundayım"}),
}

REPLACE = []

SPLIT_LATER = {}
