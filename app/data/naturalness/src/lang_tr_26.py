"""Вычитка турецкого, порция p026 (B1–B2), 23.10: дом, время — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    18292: (T + "«hızlı bir şekilde» — тяжело", {"example_tr": "Mikrodalgada hemen bir şey ısıtayım"}),
    18309: (T + "«mutfak monte ettiriyoruz» — калька", {"example_tr": "Yeni mutfak yaptırıyoruz"}),
    18346: (T + "«küçük yatağına» — подстрочник уменьшительного", {"example_tr": "Hadi canım, doğru yatağa!"}),
    18349: (T + "Girlanden — «süs zinciri», не «çelenk» (венок)", {"example_tr": "Noel ağacını mumlar ve süs zincirleriyle süslüyoruz"}),
    18410: (T + "«Sıcak odaya gelin» — подстрочник", {"example_tr": "Sıcacık içeri gelin, dışarıda kar yağıyor"}),
    18418: (T + "Jugendherberge — «gençlik yurdu» (как в 2593)", {"example_tr": "Gençlik yurdunda hep birlikte yatakhanede uyuyoruz"}),
    18446: (T + "у учителя — стол, не «kürsü»", {"translation_tr": "kürsü, öğretmen masası", "example_tr": "Öğretmen masasının arkasında duruyor"}),
    18455: (T + "выключатель — «ışık düğmesi»", {"translation_tr": "ışık düğmesi, elektrik anahtarı", "example_tr": "Karanlıkta ışığın düğmesini bulamıyorum"}),
    18459: (T + "«hızla zemini siliyorum» — тяжело", {"example_tr": "Paspası alıp yeri hemen siliyorum"}),
    18460: (T + "«Lütfen … kurulayabilir misin?» — тяжело", {"example_tr": "Tabakları kurular mısın?"}),
    18600: (T + "«Bir an bekle» — неестественно", {"example_tr": "Bir dakika bekle"}),
    18678: (T + "«Önce beklememiz gerek» — abwarten = «подождём, посмотрим»", {"example_tr": "Önce bir bekleyip görelim"}),
    18683: (T + "«yemek yapmaya başlayacağım» — подстрочник", {"example_tr": "Bu arada ben yemeğe başlıyorum"}),
    18686: (T + "«kutlamanın vesilesi nedir?» — книжно", {"example_tr": "Bu kutlama ne vesilesiyle?"}),
    18818: (T + "«Hızla» — книжно", {"example_tr": "Hemen gözyaşlarımı siliyorum"}),
    18935: (T + "«süslerle süsleriz» — тавтология", {"example_tr": "Noel döneminde evi ışıklarla donatırız"}),
    18979: (T + "«Başka sorun olursa» — двусмысленно (sorun = проблема)", {"example_tr": "Aklına takılan bir şey olursa beni rahatça arayabilirsin"}),
    18991: (T + "«valsi hep birlikte dans ediyor» — калька", {"example_tr": "Baloda ilk valsi hep büyükannemle büyükbabam yapar"}),
    18992: (T + "frech о драконе — «yaramaz», не «arsız»", {"example_tr": "Okulda çocuklar yaramaz bir ejderha hakkında bir oyun sahneliyor"}),
    6659: (T + "«seni takip edeceğim» — подстрочник", {"example_tr": "Sen önden git, ben arkandan geliyorum"}),
    7089: (T + "«onarılması gerekiyor» — канцелярит", {"example_tr": "Kırık pencereyi tamir etmemiz lazım"}),
}

REPLACE = []

SPLIT_LATER = {}
