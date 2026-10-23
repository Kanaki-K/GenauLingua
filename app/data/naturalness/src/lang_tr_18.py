"""Вычитка турецкого, порция p018 (B1), 23.10: чувства — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    10041: (T + "«Buna cesaret edemem» — подстрочник", {"example_tr": "Bir türlü cesaret edemiyorum"}),
    10084: (T + "слово «ruh» потерялось", {"example_tr": "Çok güzel ruhlu biridir"}),
    10112: (T + "«Bunun için sen sorumlusun» — калька", {"example_tr": "Bundan sen sorumlusun"}),
    10125: (T + "«tamamen gülünç» — подстрочник «total»", {"example_tr": "Bu çok gülünç"}),
    10133: (T + "«gülümseyebiliyorsun» — «умеешь улыбаться» звучит странно", {"example_tr": "Ne güzel gülümsüyorsun"}),
    10151: (T + "«Sinir etmeye başlıyorsun» — неестественно", {"example_tr": "Sinirimi bozmaya başladın"}),
    10160: (T + "«Bu bir utanç» — неестественно", {"example_tr": "Bu tam bir rezalet"}),
    10181: (T + "«asla geç kalmaz» — книжно", {"example_tr": "Bu garip, o hiç geç kalmaz"}),
    10194: (T + "«Görevden kafam karıştı» — школьное задание", {"example_tr": "Bu alıştırma kafamı tamamen karıştırdı"}),
    10202: (T + "«Onun büyük bir müzik yeteneği» — лишнее «onun»", {"example_tr": "Müziğe büyük bir yeteneği var"}),
    10218: (T + "sich benehmen — о манерах «terbiyeli»", {"example_tr": "Daha terbiyeli davranmalısın"}),
    10222: (T + "zu allem fähig — «на всё способна» в плохом смысле", {"example_tr": "Ondan her şey beklenir"}),
    10224: (T + "висящее «ki»", {"example_tr": "Videonun altındaki yorumlarda çok fazla nefret var"}),
    10236: (T + "«O tamamen umutsuz» — подстрочник", {"example_tr": "Tamamen çaresiz kalmış"}),
    10246: (T + "«Onun tepkisi çok pozitifti» — калька", {"example_tr": "Tepkisi çok olumluydu"}),
    10254: (T + "ungern — «не люблю», не «isteksizce»", {"example_tr": "Banyo temizlemeyi hiç sevmem"}),
    10270: (T + "«Senin tutumunu» — лишнее «senin»", {"example_tr": "Tutumunu beğenmiyorum"}),
    10285: (T + "слово «neden», в примере «sebep»", {"example_tr": "Bunun için nedenin neydi?"}),
    10288: (T + "«benim için tatsız» — калька", {"example_tr": "Bu beni gerçekten rahatsız ediyor"}),
    10294: (T + "«Orada yanılıyorsun» — «da» не про место", {"example_tr": "Bu konuda yanılıyorsun"}),
    10318: (T + "«adil paylaştıralım» — неверная форма", {"example_tr": "Pastayı adil bir şekilde bölüşüyoruz"}),
    10332: (T + "«zayıf bir teselli» — калька", {"example_tr": "Bu pek teselli etmiyor"}),
    10339: (T + "«Sen sadece korkaksın» — «einfach» ≠ «только»", {"example_tr": "Sen düpedüz korkaksın"}),
    10365: (T + "«O, kendini…» — тяжело", {"example_tr": "Kendini işine adamış bir öğretmendir"}),
    10405: (T + "«odaklanmış çalışıyor» — калька", {"example_tr": "Çok konsantre çalışıyor"}),
    10408: (T + "«Onun argümanı» — лишнее «onun»", {"example_tr": "Argümanı pek ikna edici değildi"}),
    10410: (T + "«O bir yalancı ve…» — книжно", {"example_tr": "Yalancının teki, söylediği tek kelimeye inanılmaz"}),
    10416: (T + "«Onda büyük bir çekicilik var» — калька", {"example_tr": "Çok cazibesi var"}),
    10431: (T + "«Onun sözlerine» — лишнее «onun»", {"example_tr": "Sözlerine şok oldum"}),
}

REPLACE = []

SPLIT_LATER = {}
