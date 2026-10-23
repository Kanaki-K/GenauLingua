"""Вычитка турецкого, порция p041 (C1), 23.10: характер, еда, спорт, здоровье — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    11063: (T + "«birlikte bile uyuyorlar» — порядок", {"example_tr": "Köpeğimiz ve komşunun erkek kedisi ayrılmaz ikili, hatta güneşte birlikte uyuyorlar"}),
    11072: (T + "«çok daha fazla özgüveni var» — калька", {"example_tr": "Yeni saç kesiminden sonra arkadaşımın özgüveni birden çok arttı"}),
    11087: (T + "«gitmesi gerektiğinde» — смысл", {"example_tr": "Kızım yatmadan önce üç kez daha tuvalete gitmek istiyorsa sadece zaman kazanmaya çalışıyordur"}),
    11153: (T + "«bana acınmasından» — коряво", {"example_tr": "Grip olup yatsam bile kimsenin bana acımasını istemem"}),
    11157: (T + "«zaferlerine güvenip» — калька идиомы", {"example_tr": "Liseyi bitirdikten sonra büyük oğlumuz başarısının üstüne yattı, öğlene kadar uyuyor"}),
    11162: (T + "«en acı verici şekilde özlediğim» — тяжело", {"example_tr": "Yurt dışında en acı özlediğim şey köşedeki fırının ekmeği"}),
    11180: (T + "«canlı bir hareket var» — калька", {"example_tr": "Anaokulundaki kermeste hep büyük bir hareketlilik oluyor"}),
    11182: (T + "«yenisini koymam gerekiyor» — коряво", {"example_tr": "Şifrem ele geçirilmiş, her yerde değiştirmem lazım"}),
    11602: (T + "«tam bir dehşet» — не то", {"example_tr": "Ütü yapmak benim için kâbus gibi, o yüzden sadece buruşmayan gömlekler alıyorum"}),
    11801: (T + "«her zaman» → «hep»", {"example_tr": "Sabahları hep bir espresso içerim"}),
    11830: (T + "«bitirmeyen tatlı alamıyor» — коряво", {"example_tr": "Büyükannemin evinde tabağını bitirmeyene tatlı yok"}),
    11870: (T + "«yıkamak gerekiyor» — тяжело", {"example_tr": "Çocuklarım kaburgayı hiç çatal bıçak kullanmadan yiyor, sonra da bütün yüzlerini yıkamam lazım"}),
    12246: (T + "«rakip» без связки", {"example_tr": "İki komşu sokaktaki en güzel ön bahçe konusunda birbirinin rakibi"}),
    12249: (T + "Kaffeekanne — не «cezve»", {"example_tr": "Komşum tutkulu bir kahve demliği koleksiyoncusu, mutfağında iki yüzden fazla var"}),
    12750: (T + "«Yaralanan diz» — aufgeschlagen = sıyrılmış", {"example_tr": "Sıyrılan dizi bir haftada iyileşti ama oğlum yara bandını yine de çıkarmak istemiyor"}),
    12766: (T + "«diyetini kontrol etmesi gerekiyor» — калька", {"example_tr": "Dedemin şekeri var, ne yediğine dikkat etmesi lazım"}),
    12769: (T + "«On iki misafirli çocuk doğum günü» — коряво", {"example_tr": "On iki çocuklu doğum günü partisinden sonra başım çatlıyor"}),
    12787: (T + "«büyükanne ve büyükbabada olduğu hafta sonu» — тяжело", {"example_tr": "Çocuklar hafta sonunu dedelerinde geçirince aylardır ilk kez dinlenebildim"}),
}

REPLACE = []

SPLIT_LATER = {}
