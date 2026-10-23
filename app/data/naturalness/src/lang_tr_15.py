"""Вычитка турецкого, порция p015 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    6827: (T + "«Onun fikri» — лишнее «onun»", {"example_tr": "Fikri gerçekten parlaktı"}),
    6893: (T + "«Prensipte» — по-турецки «prensip olarak»", {"example_tr": "Prensip olarak haklısın"}),
    6924: (T + "«tamamen olasılıksız» — книжно", {"example_tr": "Bu hiç olası değil"}),
    6925: (T + "«hemen hemen bir garanti» — подстрочник", {"example_tr": "Bu neredeyse garanti"}),
    6927: (T + "«çay için iyi bir ikame» — канцелярит", {"example_tr": "Kahve, çayın yerini tutabilir"}),
    6934: (T + "«derste mevcut muydu» — протокол", {"example_tr": "Bütün öğrenciler derse katıldı mı?"}),
    6938: (T + "Treffen с ней — встреча, не «toplantı» (совещание)", {"example_tr": "Onunla bir buluşma ayarlayabilir misin?"}),
    6960: (T + "«bir özür uygun olurdu» — подстрочник", {"example_tr": "Şimdi bir özür dilemek yerinde olurdu"}),
    6969: (T + "«tespit ettim» — протокол", {"example_tr": "Gelmeyeceğini fark ettim"}),
    6974: (T + "«onu yıkamalıyım» — лишнее «onu»", {"example_tr": "Araba çok kirli, yıkamam lazım"}),
    6979: (T + "«Fiyat kalite için uygun» — подстрочник", {"example_tr": "Kaliteye göre fiyat makul"}),
    6990: (T + "«atlatabileceğimi umarım» — тяжело", {"example_tr": "Bu zor dönemi atlatırım umarım"}),
    6994: (T + "«İpimdeki» — лишнее притяжательное", {"example_tr": "İpteki düğüm çok sıkı"}),
    7006: (T + "«geleceğini tahmin ediyorum» — подстрочник", {"example_tr": "Sanırım birazdan gelir"}),
    7012: (T + "в магазине «просто смотрю» — «bakınıyorum»", {"example_tr": "Sadece biraz bakınıyorum"}),
    7023: (T + "«sarımsaktan güçlü kokuyor» — калька", {"example_tr": "Yemek ağır sarımsak kokuyor"}),
    7037: (T + "zueinander halten — держаться друг за друга", {"example_tr": "Ne olursa olsun birbirlerine destek olurlar"}),
    7053: (T + "«bir taksiyi hazır tut» — неестественно", {"example_tr": "İhtiyacım olursa diye bir taksi hazırda beklesin lütfen"}),
    7054: (T + "Schläger — хулиганы, не «çete»", {"example_tr": "Serseriler adamı sokakta dövdü"}),
    7056: (T + "«O bağımsız olmak ve…» — тяжело", {"example_tr": "Bağımsız olmak, artık evde yaşamamak istiyor"}),
    7066: (T + "«panik tetikleyebilir» — калька", {"example_tr": "Bu onu paniğe sokabilir"}),
    7080: (T + "«Haberden dolayı çok mutlu» — подстрочник", {"example_tr": "Habere çok sevinmiş görünüyorlar"}),
    7214: (T + "«problem … çözülüyor» — время и слово", {"example_tr": "Bu sorun nispeten kolay çözülür"}),
    7249: (T + "«rapor oluşturmak» — канцелярит", {"example_tr": "Bir rapor hazırlamam gerekiyor"}),
    7294: (T + "«olasılığı dışlayamayız» — калька", {"example_tr": "Bu ihtimali göz ardı edemeyiz"}),
    7311: (T + "«Onun kırmızı ceketi» — лишнее «onun»", {"example_tr": "Kırmızı ceketi hemen göze çarpıyor"}),
    7394: (T + "«Bebek beş kilo» — без глагола", {"example_tr": "Bebek beş kilo geliyor"}),
}

REPLACE = []

SPLIT_LATER = {}
