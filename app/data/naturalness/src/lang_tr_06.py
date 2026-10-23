"""Вычитка турецкого, порция p006 (A2), 23.10: кальки и неестественные обороты → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    6528: (T + "«Para az» — подстрочник", {"example_tr": "Bu ay para kıt"}),
    6628: (T + "«Şu anda ekmek kesiyorum» — тяжело", {"example_tr": "Ekmeği kesiyorum"}),
    6915: (T + "в примере «ayrılmış», а слово только «rezerve»", {"translation_tr": "rezerve, ayrılmış"}),
    7051: (T + "«O, kayıp kedisini…» — лишнее «O,»", {"example_tr": "Kayıp kedisini bütün mahallede aradı"}),
    8857: (T + "«Kadın patron» — по-турецки род не нужен", {"example_tr": "Patron bütün çalışanları ofise çağırdı"}),
    8916: (T + "слово «şantiye», в примере «inşaat alanı»", {"example_tr": "Şantiye yüzünden trafik tamamen tıkandı"}),
    10075: (T + "«Bu benden aptalca oldu» — калька", {"example_tr": "Aptalca bir şey yaptım"}),
    10210: (T + "«Makul ol ve beni dinle» — сухо", {"example_tr": "Makul ol da beni bir dinle"}),
    11707: (T + "«Öğle yemeği için … ile hamburger» — тяжело", {"example_tr": "Öğle yemeğinde patates kızartmalı hamburger yiyorum"}),
    11772: (T + "«öğlen yemeği» — правильно «öğle yemeği»", {"example_tr": "Kafeteryada öğle yemeği yiyoruz"}),
    12461: (T + "о бабушке «öldü» — грубо, говорят «vefat etti»", {"example_tr": "Babaannem geçen yıl 95 yaşında vefat etti"}),
    13315: (T + "«ondan yarısını çoktan yedim» — неестественно", {"example_tr": "Pizza aldım, ondan yarısını yedim bile"}),
    13346: (T + "«Burada evde kimse yok» — тавтология", {"example_tr": "Evde kimse yok"}),
    13811: (T + "«Tanrım, bunu unuttum» — книжно", {"example_tr": "Allah'ım, bunu unutmuşum!"}),
    13815: (T + "«Ah tamam» — неестественно", {"example_tr": "Ha, öyle mi, şimdi anladım!"}),
    14035: (T + "смешение «sen» и «buyrun»", {"example_tr": "İşte kahven, buyur"}),
    15944: (T + "в примере второе значение «компания» — его нет в переводе", {"translation_tr": "toplum, arkadaşlık"}),
    17160: (T + "вещи в отпуск «toplamak», не «paketlemek»", {"example_tr": "Tatil için eşyalarımı topluyorum"}),
}

REPLACE = []

SPLIT_LATER = {}
