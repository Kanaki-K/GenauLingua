"""Вычитка турецкого, порция p024 (B1), 23.10: суд, полиция, транспорт — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    15933: (T + "«Bu polisiye bir cinayet hakkında» — калька", {"example_tr": "Bu polisiyede bir cinayet anlatılıyor"}),
    15958: (T + "«O tamamen masum» — лишнее «O»", {"example_tr": "Tamamen masum"}),
    15968: (T + "Prozess здесь — заседание суда, «duruşma»", {"example_tr": "Duruşma iki saattir sürüyor"}),
    16045: (T + "Verfassung — состояние, не спортивная форма", {"example_tr": "Bugün hiç iyi durumda değil"}),
    16049: (T + "«Dede vasiyetini» — нужно «dedem»", {"example_tr": "Dedem vasiyetini değiştirdi"}),
    16051: (T + "«Masumiyetini iddia ediyor» — книжно", {"example_tr": "Masum olduğunu söyleyip duruyor"}),
    16063: (T + "«serbestlikle serbest» — тавтология", {"example_tr": "Denetimli serbestlikle dışarıda"}),
    16099: (T + "Privatsphäre — «özel hayat», не «gizlilik»", {"example_tr": "Özel hayatımı korumak istiyorum"}),
    16102: (T + "«çünkü para borcu var» — непонятно, кто кому должен", {"example_tr": "Borcunu ödemediği için ona dava açmak istiyor"}),
    16104: (T + "festnehmen — «gözaltına almak»", {"example_tr": "Polis adamı gözaltına almak zorunda kaldı"}),
    16108: (T + "«Ortaçağda» — пишется «Orta Çağ'da»", {"example_tr": "Cellat Orta Çağ'da korkulan bir figürdü"}),
    16136: (T + "«kaos hüküm sürüyor» — калька", {"example_tr": "Burası tam bir kaos!"}),
    16249: (T + "Bund — федеральное правительство, не «федерация»", {"example_tr": "Federal hükümet yeni yasalar çıkardı"}),
    16278: (T + "«Çoğunluk lehte» — книжно", {"example_tr": "Çoğunluk bundan yana"}),
    16319: (T + "«başvuru yapmak üzere … gitmeliyim» — канцелярит", {"example_tr": "Pasaport başvurusu için konsolosluğa gitmem lazım"}),
    16343: (T + "«Kadın hâkim» — род не нужен", {"example_tr": "Hâkim akıllıca bir karar verdi"}),
    16365: (T + "«talepte bulunuyor» — канцелярит", {"example_tr": "Hep bir şeyler talep ediyor"}),
    16914: (T + "«O Alman vatandaşı ve…» — подстрочник", {"example_tr": "Alman vatandaşı, burada öğretmenlik yapıyor"}),
    17057: (T + "an Bord — «на борту», не «на палубе»", {"translation_tr": "gemi içi, güverte", "example_tr": "Gemideyiz"}),
    17079: (T + "«limana gidiyor» — входит в порт", {"example_tr": "Gemi limana giriyor"}),
    17121: (T + "«hâlâ 20 km uzakta» — подстрочник", {"example_tr": "En yakın benzin istasyonuna daha 20 km var"}),
}

REPLACE = []

SPLIT_LATER = {}
