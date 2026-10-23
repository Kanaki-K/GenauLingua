"""Вычитка турецкого, порция p021 (B1), 23.10: медицина, одежда, речь — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    12984: (T + "«mide yanması oluyor» — калька", {"example_tr": "Kahve içince sık sık midem yanıyor"}),
    12998: (T + "«elektrikli süpürgeyle temizlemem» — тяжело", {"example_tr": "Halıyı süpürmem lazım"}),
    13045: (T + "«mide ağrısı yaşadım» — калька", {"example_tr": "Yemekten sonra midem çok fena ağrıdı"}),
    13060: (T + "«sesi kısıktı» — после концерта «kısılmıştı»", {"example_tr": "Münih'teki konserden sonra sesi kısılmıştı"}),
    13096: (T + "«okula gidemez» — время", {"example_tr": "Çocuğun karnı ağrıyor, okula gidemiyor"}),
    13097: (T + "слово «aile hekimi», в примере «aile doktoru»", {"example_tr": "Hasta olunca aile hekimime gidiyorum"}),
    13107: (T + "«pedikür için gidiyorum» — калька", {"example_tr": "Bugün pediküre gidiyorum"}),
    13394: (T + "«karşı komşuya» — rüber = «заскочу»", {"example_tr": "Bir dakika komşuya geçiyorum"}),
    13434: (T + "«Konu ne hakkında?» — тавтология", {"example_tr": "Konu ne?"}),
    13443: (T + "«Ne hakkında düşünüyorsun?» — калька", {"example_tr": "Ne düşünüyorsun?"}),
    13481: (T + "«dünkü adamla aynı adam» — тавтология", {"example_tr": "Bu, dünkü adamın ta kendisi"}),
    13493: (T + "«Sorduğun soru» — тавтология", {"example_tr": "Sorduğun şeyle ilgili bir şey diyemem"}),
    13508: (T + "«O dördüncü sınıfta» — лишнее «O»", {"example_tr": "Dördüncü sınıfta"}),
    13512: (T + "«Bu hiç de hikayenin sonu değil» — порядок слов", {"example_tr": "Bu, hikâyenin sonu hiç de değil"}),
    13570: (T + "«epeyce aradım» — «много раз»", {"example_tr": "Seni epey kez aradım"}),
    13575: (T + "«onun beşinci galibiyeti» — лишнее «onun»", {"example_tr": "Bu sezonki beşinci galibiyeti"}),
    13631: (T + "«kıyafete ihtiyacı var» — канцелярит", {"example_tr": "Bebek çıplak, bir şey giydirmek lazım"}),
    13643: (T + "«Ben zaten giyindim» — подстрочник", {"example_tr": "Ben giyindim bile"}),
    13688: (T + "«güneş çok güçlü» — калька", {"example_tr": "Şapkanı tak, güneş çok yakıyor"}),
    13710: (T + "«Hızlı bir şekilde» — тяжело", {"example_tr": "Hemen geceliğini giyip yatıyor"}),
    13718: (T + "фартук «bağlamak», не «takmak»", {"example_tr": "Önlük bağla, yoksa kirleneceksin"}),
    13770: (T + "«ev terliğimi» — тавтология после «eve»", {"example_tr": "Eve gelince terliklerimi giyerim"}),
    13821: (T + "«Aslında ne yapıyorsun?» — это вопрос о работе", {"example_tr": "Sen ne iş yapıyorsun aslında?"}),
    13877: (T + "Nee — разговорное «yok», не «hayır»", {"example_tr": "Geliyor musun? – Yok, canım istemiyor"}),
    13924: (T + "«Onun aptal yorumlarını» — лишнее «onun»", {"example_tr": "Aptal yorumlarını rahatça görmezden gelirim"}),
    13934: (T + "gefälligst — резко, не вежливое «lütfen»", {"translation_tr": "artık, lütfen (sert)", "example_tr": "Şunu artık bırak lütfen!"}),
    13936: (T + "«aptal laflar» — по-турецки «boş laf»", {"example_tr": "Bunlar boş laflar"}),
    13954: (T + "«Otelin açıklaması» — описание отеля = «tanıtım»", {"example_tr": "Otelin tanıtımı kulağa harika geliyordu"}),
    13957: (T + "Nö — разговорное «yok»", {"example_tr": "Sinemaya geliyor musun? – Yok, canım istemiyor"}),
    13973: (T + "«beni rahatsız ediyor» — nerven = «бесит»", {"example_tr": "Bu bip sesi sinirimi bozuyor"}),
    13984: (T + "«Bu, ondan güzel bir jestti» — калька", {"example_tr": "Güzel bir jest yaptı"}),
    14000: (T + "«senin konumun için» — калька", {"example_tr": "Bu, senin görüşünü destekleyen güçlü bir argüman"}),
}

REPLACE = []

SPLIT_LATER = {}
