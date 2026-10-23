"""Вычитка турецкого, порция p046 (C2), 23.10: глаголы, работа, характер — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    8634: (T + "«kesmesine izin veriliyor» — канцелярит", {"example_tr": "Doğumda göbek bağını baba kesebiliyor"}),
    8636: (T + "«Masada sekiz saatten sonra» — коряво", {"example_tr": "Masa başında sekiz saat oturduktan sonra iyice kamburlaşıyorum"}),
    8661: (T + "«gerekiyor» → «lazım»", {"example_tr": "Trendeki kontrolde biletimi ve kimliğimi göstermem lazım"}),
    8686: (T + "«alışmak gerektiren cinsten» — коряво", {"example_tr": "Kantinimizin yemekleri, hafif tabirle, alışmak ister"}),
    8688: (T + "initiieren — «öncülük etmek»", {"example_tr": "Komşumuz her yıl bütün site için bir sokak şenliğine öncülük ediyor"}),
    8704: (T + "«Prensip olarak taraftarım» — коряво", {"example_tr": "Prensip olarak bundan yanayım ama biraz daha düşünmem lazım"}),
    9135: (T + "«O sadece patronun uşağı ve» — подстрочник", {"example_tr": "Patronun emir kulundan başka bir şey değil, ne derse onu yapıyor"}),
    9188: (T + "«mektubuna ihtiyacı var» — калька", {"example_tr": "Kızımın burs için öğretmeninden tavsiye mektubu alması lazım"}),
    9286: (T + "косвенная речь → прямая, живее", {"example_tr": "Oğlum 'Çöpü atmak benim sorumluluk alanıma girmiyor' diyor"}),
    9611: (T + "«yeterliliğine ihtiyacın var» — калька", {"example_tr": "Bu bölümü okumak için Latince yeterlilik belgesi lazım"}),
    9620: (T + "«yazılı uyarı var» — калька es gibt", {"example_tr": "Derste telefon kullanıldığı için bu sefer yazılı uyarı verilecek"}),
    9917: (T + "«Renovasyon» — калька", {"example_tr": "Tadilat masrafları sandığımızdan yüksek"}),
    11208: (T + "«Onun» — лишнее", {"example_tr": "Sürekli sızlanması sinirimi bozuyor"}),
    11477: (T + "«O çok … ve» — подстрочник", {"example_tr": "Çok disiplinli bir sporcu, her gün antrenman yapıyor"}),
    11482: (T + "«Onun düşüncesiz yorumu onu» — двусмысленно", {"example_tr": "Düşüncesizce yaptığı yorum onu çok kırdı ve öfkelendirdi"}),
}

REPLACE = []

SPLIT_LATER = {}
