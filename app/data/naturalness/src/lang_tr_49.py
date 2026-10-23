"""Вычитка турецкого, порция p049 (C2), 23.10: право, транспорт, техника, экономика — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    16733: (T + "«her zaman» → «hep»", {"example_tr": "Oğlumun geç kalması için hep hazır bir mazereti var: bazen otobüs, bazen köpek"}),
    16767: (T + "«gerekiyor» → «lazım»", {"example_tr": "Lisans tezinin sonunda yeminli bir beyan imzalamak lazım"}),
    16776: (T + "«bölgeyi devriye geziyor» — падеж", {"example_tr": "Askeri polis bölgede devriye geziyor"}),
    16777: (T + "«ve onun meclis grubu» — коряво", {"example_tr": "Teyzem belediye meclisinde, grubu da her toplantıda bisiklet yolları yüzünden tartışıyor"}),
    16781: (T + "«kanıtlamak gerekiyor» — тяжело", {"example_tr": "Kreşteki iş için sabıka kaydın olmadığını belgelemek lazım"}),
    16799: (T + "«anlatmam gerekti» — тяжело", {"example_tr": "Arkadan çarpma kazasının görgü tanığı olarak polise her şeyi ayrıntılı anlatmak zorunda kaldım"}),
    16810: (T + "«izin almam gerekiyor» → «lazım»", {"example_tr": "Duruşma günü yüzünden perşembe izin almam lazım"}),
    16815: (T + "«doğum günündeki çocuklar» — коряво", {"example_tr": "Dondurma bitince doğum günü partisindeki çocuklar küçük bir isyan başlattı"}),
    16832: (T + "«istismarı cezalandırılır» — канцелярит", {"example_tr": "Hayvanlara kötü muamele etmek suçtur"}),
    16884: (T + "«yüzünden … yüzünden» — повтор", {"example_tr": "Park meselesinden çıkan küçük anlaşmazlıklar yüzünden komşular birbiriyle neredeyse hiç konuşmuyor"}),
    16901: (T + "«Büyükannemle büyükbabam» — тяжело", {"example_tr": "Babaannemle dedem 1946'da bir mülteci kampında tanışmış"}),
    16931: (T + "«Bildirgelerini» — коряво", {"example_tr": "Amerikalılar 4 Temmuz'da 1776'daki bağımsızlık ilanını kutluyor"}),
    16942: (T + "«odasına barikat kuruyor» — калька", {"example_tr": "Sınavdan önce oğlum kendini kitaplarıyla birlikte odasına kapatıyor"}),
    17344: (T + "«maksimum hız … dır» — книжно", {"example_tr": "Bu otoyolda azami hız saatte 130 kilometre"}),
    17364: (T + "«gerekiyor» → «lazım»", {"example_tr": "Gösterge panelinde yine kırmızı bir lamba yanıyor, servise gitmem lazım"}),
    17378: (T + "«babaanneye» — без принадлежности", {"example_tr": "Hırvatistan yolunda Salzburg'da babaanneme uğrayıp mola veriyoruz"}),
    17380: (T + "«iniş yaklaşmasına başlıyor» — технично", {"example_tr": "Uçak alçalmaya başladı, 15 dakika sonra ineceğiz"}),
    17399: (T + "«para koymalıyım» — коряво", {"example_tr": "Kafeye girmeden önce park saatine para atmam lazım"}),
    17667: (T + "«kullanmamız gerekiyor» — тяжело", {"example_tr": "Asansör bugün bakımda, merdivenden çıkmak zorundayız"}),
    17693: (T + "«Lütfen … açabilir misin» — тяжело", {"example_tr": "Işığı bir açar mısın?"}),
    17722: (T + "«gerekiyor» → «lazım»", {"example_tr": "İki bileşenli yapıştırıcıda iki bileşeni de iyice karıştırman lazım"}),
    17725: (T + "«yaklaşmasına izin veriliyor» — канцелярит", {"example_tr": "ESA kontrol merkezi turunda çocuklar ekranlara yaklaşabiliyor"}),
    17736: (T + "«her zaman» → «hep»", {"example_tr": "Çantamdaki çağrı cihazı hep yanlış zamanda çalıyor"}),
}

REPLACE = []

SPLIT_LATER = {}
