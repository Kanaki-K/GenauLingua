"""Вычитка турецкого, порция p036 (B2), 23.10: право, власть, транспорт — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    16273: (T + "«yeni kuralları onayladı» — определённость", {"example_tr": "Komisyon yeni kurallar kabul etti"}),
    16277: (T + "Mordkommission — «cinayet masası»", {"example_tr": "Cinayet masası dosyayı çok dikkatli inceliyor"}),
    16280: (T + "«Dizi yüzünden» — dizi = сериал", {"example_tr": "Kızım dizindeki sorun yüzünden beden eğitiminden muaf tutuldu"}),
    16287: (T + "«Büyükbabamın mirası» — тяжело", {"example_tr": "Dedemin bize bıraktığı miras eski günlüğüydü"}),
    16290: (T + "«ateşkesi kabul etti» — vereinbaren = договориться", {"example_tr": "İki ülke ateşkes konusunda anlaştı"}),
    16304: (T + "Jugendarrest — «ıslahevi»", {"example_tr": "Genç iki hafta ıslahevinde kalacak"}),
    16318: (T + "«her zaman» → «hep»", {"example_tr": "Paintball'da kardeşim hep bizim keskin nişancımız, neredeyse herkesi vuruyor"}),
    16321: (T + "«daha … bildirmem gerekiyor» — коряво", {"example_tr": "Çalınan bisikletimi bir de karakola bildirmem lazım"}),
    16325: (T + "«O, … tutuluyor» — канцелярит", {"example_tr": "Tek kişilik hücrede yatıyor"}),
    16330: (T + "«Skandalden» — гармония гласных", {"example_tr": "Skandaldan sonra bakan basının yoğun ateşi altında"}),
    16354: (T + "«açılış onayını bekliyor» — коряво", {"example_tr": "Tamirden sonra köprü trafiğe açılması için hâlâ onay bekliyor"}),
    16356: (T + "«evde kalmayı tercih etti» — по-турецки «sandığa gitmedi»", {"example_tr": "Birçok genç seçmen son seçimde sandığa gitmedi"}),
    16359: (T + "«iklimin korunması için» — канцелярит", {"example_tr": "Öğrenciler her cuma belediye binasının önünde iklim için protesto yapıyor"}),
    16363: (T + "«doğrudan üst direğin altından girdi» — коряво", {"example_tr": "Yirmi metreden bir şut ateşledi, top üst direğin hemen altından ağlara gitti"}),
    16387: (T + "«şansına erişti» — книжно", {"example_tr": "Roma ziyaretinde büyükannem Papa'nın huzuruna kabul edildi, çok şanslıydı"}),
    16510: (T + "«yanlışlıkla yanlış» — повтор", {"example_tr": "Kontrolde biletim geçersizdi, çünkü dalgınlıkla yanlış bölgeye bilet almıştım"}),
    16537: (T + "«bugün hâlâ çocukken» — порядок", {"example_tr": "Dedem çocukken her hava saldırısında bodruma nasıl koştuğunu hâlâ anlatır"}),
    16585: (T + "«cezalandırmak istiyor ve … gönderecek» — тяжело", {"example_tr": "Öğretmen herkese ibret olsun istiyor: telefonla yakalanan ilk öğrenciyi müdüre gönderecek"}),
    16632: (T + "«bir dağ kremayla» — коряво", {"example_tr": "Üstü dağ gibi kremayla taçlanmış sıcak bir kakao benim için kışın en güzel şey"}),
    16647: (T + "«…tanıttı, diye anlatıyor» — коряво", {"example_tr": "Büyükannem heyecanla anlatıyor: dolandırıcı kadın telefonda kendini torunu olarak tanıtmış"}),
    16686: (T + "«birinde bir yerde» — повтор", {"example_tr": "Yeni iş için sosyal güvenlik numaram lazım ama mektup taşınma kolilerinden birinde kaldı"}),
    16691: (T + "«Çocuk doğum gününde … oyun oynadık» — коряво", {"example_tr": "Çocukların doğum günü partisinde her yalanda öten oyuncak bir yalan makinesiyle oynadık"}),
    16704: (T + "«Annemin … çantasında» — согласование", {"example_tr": "Annem şehre taşındığından beri çantasında hep küçük bir biber spreyi taşıyor"}),
    16720: (T + "«Büyükanne» без принадлежности", {"example_tr": "Büyükannem kurabiyeleri çıkarır çıkarmaz torunlar dört bir yanını sarıyor"}),
    16731: (T + "«kanunsuz bir düzen başlıyor» — оксюморон", {"example_tr": "Biz evden çıkar çıkmaz çocuk odası kanunsuz bir yere dönüyor"}),
    16756: (T + "«tuvaletleri kabul ettirdi» — коряво", {"example_tr": "Babam hobi bahçesi derneğindeki başkanlığı sırasında nihayet yeni tuvalet yaptırmayı kabul ettirdi"}),
    16764: (T + "«Büyükannemle büyükbabam» — тяжело", {"example_tr": "Dedemler evi daha hayattayken anneme devretmişler"}),
    16786: (T + "«Isırılmış pasta için» — коряво", {"example_tr": "Pastayı kim ısırdı? Baş şüpheli köpeğimiz, burnunda hâlâ krema var"}),
    16789: (T + "«köleleştirilmiş hissediyor» — калька", {"example_tr": "Yeni telefondan beri oğlum kendini sınıf grubundaki mesajların esiri gibi hissediyor"}),
    16798: (T + "«savaşın bitişinden sonra» — тяжело", {"example_tr": "Savaşın sonunda büyük büyükannem Silezya'dan Bavyera'ya kadar yürümek zorunda kalmış"}),
    16806: (T + "порядок «hâlâ Almanya'da» — двусмысленно", {"example_tr": "Büyükannem hâlâ \"Almanya'da taşındıktan sonra iki hafta içinde polise kayıt yaptırmak lazım\" diyor"}),
    16853: (T + "«oturup korkmasına izin verildi» — канцелярит", {"example_tr": "Eski kale turunda çocuklar nezarethaneye oturup biraz korkabildi"}),
    16855: (T + "«taraf değiştiren biri ve» — коряво", {"example_tr": "Ağabeyim Münih'e taşındığından beri ailemizin gözünde taraf değiştirdi, Bayern'i tutuyor"}),
    16893: (T + "«Oğlum diyor ki» — порядок", {"example_tr": "Oğluma göre Wi-Fi olmadan odası hapishane hücresinden farksız"}),
    16899: (T + "«çok fazla mağazadan hırsızlık oluyor» — коряво", {"example_tr": "Bizim süpermarkette artık her yerde kamera var, çünkü mağazadan çok hırsızlık yapılıyor"}),
    16940: (T + "концовка дословно как в 16772", {"example_tr": "Oğlum müzede savaş esirlerinin mektuplarını okudu, akşam boyunca ağzını bile açmadı"}),
    17146: (T + "«Yola çıkışım … yedide» — канцелярит", {"example_tr": "Yarın sabah yedide yola çıkıyorum"}),
    17153: (T + "«beklenenden daha uzundu» — калька", {"example_tr": "Dönüş yolu sandığımızdan uzun sürdü"}),
    17158: (T + "«yakında gelmeli» — калька sollten", {"example_tr": "Misafirler birazdan gelir"}),
    17179: (T + "«iniş yaklaşmasında» — техничный термин", {"example_tr": "Berlin'e inişe geçerken televizyon kulesi daha havadan görünüyor"}),
}

REPLACE = []

SPLIT_LATER = {}
