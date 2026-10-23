"""Вычитка турецкого, порция p038 (B2–C1), 23.10: дом, время, бытовые глаголы — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    18321: (T + "«gerekiyor» → «lazım»", {"example_tr": "Banyo tadilatından kalan molozu çöplüğe kendimiz götürmemiz lazım"}),
    18397: (T + "«kaydolmalı» — книжно", {"example_tr": "Ziyaretçiler servise girmeden önce hastanenin giriş kapısında kayıt yaptırmak zorunda"}),
    18422: (T + "«ve çıkamıyor» — связка", {"example_tr": "Restoranda küçük oğlum kendini erkek tuvaletine kilitledi, şimdi de çıkamıyor"}),
    18464: (T + "«akşam yemeği alıyor» — калька", {"example_tr": "Kedimiz her gece yangın merdiveninden komşuya tırmanıyor ve orada ikinci kez akşam yemeği yiyor"}),
    18488: (T + "«mülk daire aldık» — коряво", {"example_tr": "On yıl kirada oturduktan sonra nihayet şehrin kenarında kendimize ait küçük bir daire aldık"}),
    18653: (T + "stets — «daima»", {"example_tr": "Daima geç gelir"}),
    18719: (T + "«kestirme yapıyor» — «bir kestiriyor»", {"example_tr": "Dedem her gün yemekten sonra koltukta bir kestiriyor ve horluyor"}),
    18728: (T + "«organize kalmamı» — калька", {"example_tr": "Günlük rutin düzenli olmama yardım ediyor"}),
    18738: (T + "«hızlıca ekmek alıyorum» — калька schnell", {"example_tr": "Eve dönüş yolunda köşedeki fırından bir ekmek alıveriyorum"}),
    18741: (T + "«yeni başlangıca ihtiyacı var» — калька", {"example_tr": "Taşındıktan sonra yeni bir başlangıç yapması lazım"}),
    18765: (T + "«başvurmam gerekiyor» → «lazım»", {"example_tr": "Pasaportumun süresi mayısta doluyor, yenisine başvurmam lazım"}),
    18790: (T + "«tamirciye ihtiyacımız var» — калька", {"example_tr": "Çamaşır makinesi su kaçırıyor, bir an önce usta lazım"}),
    18846: (T + "«gözümüzü kırpmadık» — не та идиома", {"example_tr": "Bebek bu gece aralıksız ağladı, gözümüze neredeyse hiç uyku girmedi"}),
    18873: (T + "«her çeyrekte» — канцелярит", {"example_tr": "Aile hekiminde her üç ayda bir sigorta kartımı yeniden göstermem lazım"}),
    18883: (T + "«Düğünün arife akşamı» — коряво", {"example_tr": "Düğünden bir önceki akşam bütün aile bizim bahçede mangal yaptı"}),
    18934: (T + "«Onun zaman hissi yok ve» — подстрочник", {"example_tr": "Hiç zaman duygusu yok, hep geç kalıyor"}),
    19012: (T + "«büyük kalabalık oluyor» — калька", {"example_tr": "Cumartesi sabahları süpermarket hep çok kalabalık oluyor"}),
    7540: (T + "«Çocuk doğum gününden» — коряво", {"example_tr": "Çocuğun doğum günü partisinden sonra oturma odasında hâlâ yığınla konfeti buluyoruz, buzdolabında bile"}),
    7553: (T + "место «devretmek» — книжно", {"example_tr": "Uzun yolculuk için cam kenarındaki yerimi sana seve seve bırakıyorum"}),
    7563: (T + "«bir dönüş aldı» — калька", {"example_tr": "Gezi beklenmedik bir yöne döndü: hayvanat bahçesi yerine arı sokması yüzünden kendimizi doktorda bulduk"}),
    7596: (T + "«kesmesine izin veriliyor» — канцелярит", {"example_tr": "Oyun parkının açılışında kırmızı kurdeleyi kızım kesecek"}),
    7636: (T + "Kaffeekanne — не «cezve»", {"example_tr": "Babaannemle dedemin yirmi beşinci evlilik yıl dönümü için gümüş bir kahve demliği hediye ediyoruz"}),
    7642: (T + "«gerekiyor» → «lazım»", {"example_tr": "Gripten sonra kızımın iki haftalık okul konusunu telafi etmesi lazım"}),
    7652: (T + "«Tatil açısından anlaşıyoruz» — коряво", {"example_tr": "Tatil açısından hemfikiriz, sadece nereye gideceğimiz belli değil"}),
    7668: (T + "«zorlamam gerekiyor» — тяжело", {"example_tr": "Gözlüksüz okurken gözlerimi çok zorluyorum"}),
    7686: (T + "«söylememeyi tercih ediyorum» — калька", {"example_tr": "Veli toplantılarında karım bir diplomat gibi hareket ediyor, ben ise hiç ağzımı açmıyorum"}),
    7702: (T + "«yeniden paketliyoruz» — калька", {"example_tr": "Uçurtmayı uçurmak için üç başarısız denemeden sonra onu toplayıp kaldırıyoruz"}),
    7704: (T + "«son çare olarak» — слово не notfalls", {"example_tr": "Otobüs gelmezse gerekirse yürürüz"}),
    7737: (T + "«yardıma ihtiyacım var» → «lazım»", {"example_tr": "Bir dakika bu tarafa gelir misin? Merdivende bebek arabası için yardım lazım"}),
    7739: (T + "«gerekiyor» → «lazım»", {"example_tr": "Kreşte yer için işverenden bir belge sunmamız lazım, yoksa bekleme listesinde kalıyoruz"}),
    7756: (T + "«ses çıkarmadın» — не тот смысл", {"example_tr": "Yeni işinde nasıl gidiyor? Haftalardır hiç aramadın"}),
}

REPLACE = []

SPLIT_LATER = {}
