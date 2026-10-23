"""Вычитка турецкого, порция p047 (C2), 23.10: характер, еда, спорт, здоровье, общение — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    11489: (T + "«O gerçekten … ve» — подстрочник", {"example_tr": "Gerçekten sorumluluk sahibi biri, iş arkadaşlarıyla ilgileniyor"}),
    11504: (T + "«berbat bir şekilde donuyorum» — калька", {"example_tr": "Ceketsiz otobüs durağında perişan bir hâlde donuyorum"}),
    11595: (T + "«O çok kolay inanır ve» — подстрочник", {"example_tr": "Çok saf, her numaraya kanıyor"}),
    11610: (T + "«sadece saçma» — калька einfach", {"example_tr": "Bu fikir düpedüz saçma"}),
    11613: (T + "«O gerçek bir hayırsever ve» — подстрочник", {"example_tr": "Gerçek bir insan dostu, herkese seve seve yardım ediyor"}),
    11983: (T + "«patates püresi ile lezzetli köfte» — коряво", {"example_tr": "Büyükannem patates püreli nefis köfte yapıyor"}),
    12342: (T + "«Çocuk doğum gününün» — коряво", {"example_tr": "Doğum günü partisinin en büyük atraksiyonu bahçedeki şişme kale"}),
    12357: (T + "«menzilinin dışında kalmayı tercih» — калька", {"example_tr": "Ağabeyim keyifsizken atış menzilinden uzak duruyorum"}),
    12912: (T + "«tımarhane gibi bir ortam oluyor» — тяжело", {"example_tr": "Sabahları okuldan önce ev tımarhaneye dönüyor"}),
    12993: (T + "«Onun körlüğü» — лишнее «onun»", {"example_tr": "Körlüğü, başarılı bir hayat sürmesine engel olmadı"}),
    13021: (T + "«ölüm belgesine ihtiyacı var» — калька", {"example_tr": "Cenaze için cenaze şirketine önce ölüm belgesi lazım"}),
    13032: (T + "noch — «daha», не «hâlâ»", {"example_tr": "Gece saat on birde oğlum birden tamamen uyanık ve daha oyun oynamak istiyor"}),
    13123: (T + "«olmayan biridir» — тяжело", {"example_tr": "Kırk derecede koşuya çıkan birinin akli dengesi yerinde değildir!"}),
    13588: (T + "«herkes hepsini yedi» — коряво", {"example_tr": "Kek biraz yandı, yine de herkes yiyip bitirdi"}),
    14247: (T + "«hafife söylemek olur» — коряво", {"example_tr": "'Fena değil' demek az bile, film harikaydı!"}),
}

REPLACE = []

SPLIT_LATER = {}
