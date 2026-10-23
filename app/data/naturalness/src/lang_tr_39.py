"""Вычитка турецкого, порция p039 (C1), 23.10: глаголы, наречия, профессии — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    7758: (T + "«ustaya ihtiyacımız var» — калька", {"example_tr": "Çamaşır makinesi su akıtıyor, mümkün olan en kısa sürede bir usta lazım, yoksa mutfağı su basacak"}),
    7770: (T + "вставка-перечисление ломает фразу", {"example_tr": "Yağmura, trafiğe, yırtık çadıra, bütün bunlara rağmen en güzel kamp tatilimizdi"}),
    7805: (T + "«kısmen altı, kısmen sekiz» — калька", {"example_tr": "Oğlumun sınıfındaki çocukların kimi altı, kimi şimdiden sekiz yaşında"}),
    7848: (T + "«gerekiyor» → «lazım»", {"example_tr": "Zımparadan sonra ahşap zemine bir de koruyucu vernik atmamız lazım, yoksa her leke görünür"}),
    7852: (T + "«Büyükanne» без принадлежности", {"example_tr": "Babaanneleri çocuklara gizlice şeker verince koyduğumuz her kuralı baltalıyor"}),
    7857: (T + "«Büyükanneye» без принадлежности", {"example_tr": "Babaanneme gidiş süresini tamamen yanlış tahmin ettim, şimdi bir saattir trafikteyiz"}),
    7909: (T + "überfüllt — «tıklım tıklım»", {"example_tr": "İlk sıcak cumartesi açık havuz o kadar tıklım tıklım ki havlumuzu serecek yer zor buluyoruz"}),
    7915: (T + "«istemem gerekecek» — тяжело", {"example_tr": "Turşu kavanozunun kapağı öyle sıkışmış ki komşudan yardım isteyeceğim"}),
    7919: (T + "«yapmasına izin veriliyor» — канцелярит", {"example_tr": "Kampta çocuklar küçük baltayla çıra yapabiliyor, ama sadece eldivenle"}),
    7929: (T + "«güçlerimizi birleştirip» — пафосно для подарка", {"example_tr": "Veda hediyesi için hepimiz bir araya gelip ona bir hediye çeki alıyoruz"}),
    7933: (T + "«pastayla ziyarette bulunuyoruz» — канцелярит", {"example_tr": "Taşındıktan sonra yeni komşuları elimizde bir pastayla ziyaret ediyoruz"}),
    7936: (T + "«köşeye sıkıştırma» — не то значение", {"example_tr": "Belki cumartesi gelirim ama lütfen bunu söz olarak alma"}),
    7947: (T + "«gerekiyor» → «lazım»", {"example_tr": "Eski buzdolabını dışarı çıkarmamız lazım"}),
    7950: (T + "«her zaman» → «hep»", {"example_tr": "Annem telefonda hep ne yediğini ayrıntılı olarak anlatıyor"}),
    7956: (T + "без глагола — «matlaştı»", {"example_tr": "Denizde geçen yazdan sonra saçlarım iyice matlaştı"}),
    7957: (T + "«Büyükannemlerin» — «dedemlerin»", {"example_tr": "Dedemlerin eski köy evi kimse oturmadığı için yavaş yavaş çöküyor"}),
    7968: (T + "«az da olsa benzer bir yanı yok» — коряво", {"example_tr": "Broşürdeki fotoğraf otel odamıza azıcık bile benzemiyor"}),
    7972: (T + "«gerekiyor» → «lazım»", {"example_tr": "Martta yine bütün saatleri ayarlamamız lazım"}),
    7993: (T + "«gerekiyor» → «lazım»", {"example_tr": "Dalış kursundan önce bir sağlık muayenesinden geçmem lazım"}),
    8015: (T + "«Yeğenine» — падеж (yeğenime)", {"example_tr": "Yeğenime karnesini sorunca yılan balığı gibi kıvranıyor"}),
    8018: (T + "«gerekiyor» → «lazım»", {"example_tr": "Parayı ay sonuna kadar iyi bölüştürmem lazım"}),
    8215: (T + "Schöffe — «jüri üyesi» (как в 16245)", {"example_tr": "Babam jüri üyesi olarak gelecek hafta bir duruşmada hazır bulunmak zorunda"}),
    8991: (T + "«zammı aldım … aldım» — повтор", {"example_tr": "Üç yıl sonra nihayet maaşıma zam geldi, hemen yeni bir çamaşır makinesi aldım"}),
    9023: (T + "«büyükannedeki» — без принадлежности", {"example_tr": "Çocuklar daha ocakta babaannelerindeki yaz tatili için plan yapıyor"}),
    9028: (T + "«binme izni verildi» — канцелярит", {"example_tr": "Çiftlikte oğlum bir kez traktöre binebildi ve o günden beri başka bir şey konuşmuyor"}),
    9045: (T + "«tamamen aşırı yüklenmiş» — коряво", {"example_tr": "Noel öncesinde kuryeler aşırı yük altında, paketimiz bir haftadır depoda"}),
}

REPLACE = []

SPLIT_LATER = {}
