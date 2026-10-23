"""Вычитка турецкого, порция p016 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    7748: (T + "«Hâlâ kamyonu boşaltmamız» — «noch» = «ещё и»", {"example_tr": "Bir de kamyonu boşaltmamız lazım"}),
    7815: (T + "«borç verebileceğim maksimum» — порядок слов", {"example_tr": "Sana borç verebileceğim maksimum bu"}),
    7879: (T + "«Kendimi … sınırlıyorum» — калька", {"example_tr": "Sadece en önemli şeylerle sınırlı tutuyorum"}),
    7892: (T + "«Bu, … yapılır» — тяжело", {"example_tr": "Bu iş göz açıp kapayıncaya kadar biter"}),
    8063: (T + "warm — с отоплением, не «aidatlar dahil»", {"example_tr": "Kira ısınma dahil 800 euro tutuyor"}),
    8075: (T + "«yüz bin nüfusu var» — коряво", {"example_tr": "Şehrimizin nüfusu yüz bin"}),
    8182: (T + "книги «yatıyor» — лежат, по-турецки «duruyor»", {"example_tr": "Kitaplar masada üst üste duruyor"}),
    8188: (T + "«daha fazla dinamik var» — калька", {"example_tr": "Yeni antrenörle takım çok daha dinamik"}),
    8240: (T + "«ellerim hep pürüzlü» — сухо", {"example_tr": "Kışın ellerim hep pürüz pürüz oluyor"}),
    8337: (T + "«hâlâ ispirto lazım» — «noch» = «ещё и»", {"example_tr": "Kamp ocağı için bir de ispirto lazım"}),
    8409: (T + "«şimdi sonbaharda» — подстрочник", {"example_tr": "Sonbahar geldi, yapraklar dökülüyor"}),
    8541: (T + "«etabı Portekiz'e gidiyor» — коряво", {"example_tr": "Yolculuğumuzun bir sonraki etabı Portekiz"}),
    8639: (T + "«pasif şekilde» — тяжело", {"example_tr": "Pasif pasif televizyon izleyeceğine biraz dışarı çık"}),
    8765: (T + "«ofis olarak hizmet ediyor» — калька", {"example_tr": "Bu oda ofis olarak kullanılıyor"}),
    8766: (T + "«O bizim grubumuzun lideri» — подстрочник", {"example_tr": "Grubumuzun lideri o"}),
    8801: (T + "«O gerçek bir savaşçı» — лишнее «O»", {"example_tr": "Gerçek bir savaşçıdır, asla pes etmez"}),
    8807: (T + "«O gerçek bir profesyonel» — лишнее «O»", {"example_tr": "Gerçek bir profesyonel"}),
    8808: (T + "зарплата «yatıyor», не «geliyor»", {"example_tr": "Maaşım hep ay sonunda yatıyor"}),
    8821: (T + "«O, İtalyan mutfağı uzmanı» — тяжело", {"example_tr": "İtalyan mutfağında uzmandır"}),
    8834: (T + "квартира — через «emlak ajansı»", {"example_tr": "Daireyi bir emlak ajansı aracılığıyla bulduk"}),
    8847: (T + "beschäftigt mich — не «интересует», а «не даёт покоя»", {"example_tr": "Bu konu kafamı çok meşgul ediyor"}),
}

REPLACE = []

SPLIT_LATER = {}
