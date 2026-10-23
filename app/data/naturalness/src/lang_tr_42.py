"""Вычитка турецкого, порция p042 (C1), 23.10: здоровье, одежда, общение, культура — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    12830: (T + "«önce benim okumam lazım» — оттенок", {"example_tr": "Oğlum dalağın ne işe yaradığını bilmek istiyor, benim de önce bir okumam lazım"}),
    12846: (T + "«Koro şefimiz koroda … söylüyor» — тяжело", {"example_tr": "Koro şefimize göre şarkı söylerken göğüs kafesimizin genişlediğini hissetmeliyiz"}),
    12861: (T + "«gerekiyor» → «lazım»", {"example_tr": "Kenya gezisinden önce aile hekimime sıtma hapı yazdırmam lazım"}),
    12882: (T + "«gerekiyor» → «lazım»", {"example_tr": "Yaşlı köpeğimizin ağız kokusu var, o yüzden onu veterinere götürmemiz lazım"}),
    12889: (T + "«eski alışkanlığına geri döndü» — книжно", {"example_tr": "Üç ay sigara içmeden durduktan sonra amcam düğünde yeniden sigaraya başladı"}),
    13038: (T + "«ateşin olunca … evde muayeneye» — коряво", {"example_tr": "Eski aile doktorumuz ateşin olursa hâlâ eve muayeneye geliyor"}),
    13572: (T + "zumal — «hele»", {"example_tr": "Bugün spor salonuna gitmiyorum, hele yağmur yağarken"}),
    13713: (T + "«takım elbiseyle giyiniyor» — калька", {"example_tr": "Dedem fırına giderken bile takım elbise giyiyor, eskiden böyle yapılırdı diyor"}),
    14123: (T + "«kar geleceği duyurusundan sonra» — тяжело", {"example_tr": "Radyo kar yağacağını duyurunca çocuklar hemen kızakları bodrumdan çıkardı"}),
    14163: (T + "«itiraf etmem gerekiyor» — тяжело", {"example_tr": "Kendime itiraf etmeliyim: navigasyon olmadan yapı marketi bile bulamıyorum"}),
    14184: (T + "Statement — «duruş»", {"example_tr": "Kızım saçlarını yeşile boyuyor ve bunun okul üniformasına karşı bir duruş olduğunu söylüyor"}),
    14584: (T + "«dövüşmesine izin veriliyor» — канцелярит", {"example_tr": "Kalede çocuklar Viking kılığına girip tahta kılıçlarla dövüşebiliyor"}),
    14626: (T + "«nasihat veriyor» — «nasihat ediyor»", {"example_tr": "Babam her seferinde bize tasarrufun ne kadar önemli olduğuna dair nasihat ediyor, sonra kendine yeni bir bisiklet alıyor"}),
    14628: (T + "«Büyükanne ve büyükbabamın» — тяжело", {"example_tr": "Babaannemle dedemin aşk hikâyesi bir otobüs durağında kaybolan bir şemsiyeyle başlıyor"}),
}

REPLACE = []

SPLIT_LATER = {}
