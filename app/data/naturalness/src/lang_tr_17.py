"""Вычитка турецкого, порция p017 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    8851: (T + "«binadaki ısıtma» — по-турецки «kalorifer»", {"example_tr": "Kapıcı binanın kaloriferiyle ilgileniyor"}),
    8854: (T + "«tutukluları gözetliyor» — «шпионит»", {"example_tr": "Gardiyan mahkumlara göz kulak oluyor"}),
    8856: (T + "«arkadaş canlısı ve yardımcı» — о персонале «güler yüzlü»", {"example_tr": "Uçağın mürettebatı çok güler yüzlü ve yardımsever"}),
    8879: (T + "«Kadın çalışan … görev yapıyor» — канцелярит", {"example_tr": "Bu şirkette on yıldır çalışıyor"}),
    8910: (T + "к официанту — «Garson bey»", {"example_tr": "Garson bey, hesap lütfen!"}),
    8959: (T + "Portier в отеле — «kapı görevlisi»", {"example_tr": "Otelin kapı görevlisi bavullarımı taşımama yardım etti"}),
    9118: (T + "«O diplomat değil» — подстрочник", {"example_tr": "Diplomat değil ki, düşündüğünü hep açıkça söylüyor"}),
    9173: (T + "«kişisel olarak tanır» — калька", {"example_tr": "Meyhane sahibesi bütün müdavimlerini tek tek tanır"}),
    9471: (T + "«O tarih hakkında çok bilgili» — тяжело", {"example_tr": "Tarihi çok iyi bilen, bilgili bir adamdır"}),
    9480: (T + "«Yeni başlayan olarak» — не хватает «biri»", {"example_tr": "Yeni başlayan biri olarak yavaş antrenman yapmalısın"}),
    9592: (T + "«mürekkep gerekli» — книжно", {"example_tr": "Dolma kalemim boş, yeni mürekkep lazım"}),
    9593: (T + "в турецкой школе лучшая оценка — «pekiyi»", {"translation_tr": "en yüksek not, pekiyi", "example_tr": "Karnesinde hep pekiyi vardı"}),
    9781: (T + "«yemek için yalvarıyor» — о собаке «dileniyor»", {"example_tr": "Köpek mama dileniyor"}),
    9783: (T + "«Senin kitabını» — лишнее «senin»", {"example_tr": "Kitabını ödünç alabilir miyim?"}),
    9878: (T + "«Hâlâ halletmem gereken» — «noch» = «ещё»", {"example_tr": "Halletmem gereken birkaç ufak işim daha var"}),
    9915: (T + "«Senin hesap numaran nedir?» — книжно", {"example_tr": "Hesap numaran ne?"}),
    9948: (T + "«baksam iyi olur» — смысл «лучше посмотрю»", {"example_tr": "Alışverişten önce bir hesap bakiyeme bakayım"}),
}

REPLACE = []

SPLIT_LATER = {}
