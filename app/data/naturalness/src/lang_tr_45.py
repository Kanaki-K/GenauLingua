"""Вычитка турецкого, порция p045 (C1–C2), 23.10: время, наречия, глаголы — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    18822: (T + "«futbola asla» — оборвано", {"example_tr": "Ailemin yanına her gidişimizde kocam geç kalıyor ama maça hiç geç kalmıyor"}),
    18828: (T + "«Büyükannemle büyükbabam» — тяжело", {"example_tr": "Babaannemle dedem evliliklerinin ellinci yıldönümünde tıpkı o zamanki gibi kendi şarkılarıyla dans ediyor"}),
    18831: (T + "noch — «daha», не «hâlâ»", {"example_tr": "Kızımın şimdiki en sevdiği renk mor, geçen hafta daha sarıydı"}),
    19013: (T + "Orden — монашеский, «rahibe tarikatı»", {"example_tr": "Teyzem yirmi yaşında bir rahibe tarikatına girdi ve o zamandan beri manastırda yaşıyor"}),
    8136: (T + "«pek çok elma yerde yatıyor» — коряво", {"example_tr": "Sonbaharda bahçemizde yerde yığın yığın elma oluyor"}),
    8219: (T + "hiesig — «oranın», не «buranın»", {"example_tr": "Tatilde hep önce oranın yöresel lezzetlerini deniyoruz"}),
    8296: (T + "«yokluğu nedeniyle … yapılmıyor» — канцелярит", {"example_tr": "İki öğretmen gelemediği için bugün matematik dersi yok"}),
    8307: (T + "«annesi … babasına» — это мы", {"example_tr": "Çocuklar bizi birbirimize karşı kullanıyor: anne hayır derse babaya soruyorlar"}),
    8326: (T + "«yardım etmem gerekiyor» — тяжело", {"example_tr": "Oğlum matematik ödevlerini neredeyse kendi yapıyor, ben sadece biraz el atıyorum"}),
    8346: (T + "«uzatılmış halde oturup» — канцелярит", {"example_tr": "Yogada bacaklarımızı uzatıp oturuyor ve ayak parmaklarımıza dokunmaya çalışıyoruz"}),
    8384: (T + "«ilk kez … ilk denemede» — повтор", {"example_tr": "İlk kez denediğim bir tarif olmasına rağmen pasta bir seferde harika oldu"}),
    8393: (T + "«zorunlu olarak gerekli» — тавтология", {"example_tr": "Bu illa ki gerekli değil"}),
    8469: (T + "«onu zar zor kapatabiliyorum» — тяжело", {"example_tr": "Bavul tıka basa dolu, zar zor kapanıyor"}),
    8520: (T + "«aydınlatır» — сейчас", {"example_tr": "Mumlar odayı sıcak bir ışıkla aydınlatıyor"}),
    8522: (T + "«olmadan olmaz» — коряво", {"example_tr": "Bir haftalık kampın sonunda vardığım sonuç: bir daha asla şişme yataksız gitmem"}),
    8568: (T + "«dış yardıma ihtiyacımız var» — калька", {"example_tr": "Bu sorunu çözmek için dışarıdan yardım lazım"}),
    8571: (T + "«basitleştirilmiş şekilde» — тяжело", {"example_tr": "Anlaman için sana basitçe anlatayım"}),
    8572: (T + "«değiştirmemiz gerekiyor» — тяжело", {"example_tr": "Planı daha gerçekçi yapmak için değiştirmemiz lazım"}),
    8574: (T + "«babaanne» без принадлежности", {"example_tr": "Torunlarla geçen hafta sonundan sonra babaannem posası çıkmış gibi hissediyor"}),
}

REPLACE = []

SPLIT_LATER = {}
