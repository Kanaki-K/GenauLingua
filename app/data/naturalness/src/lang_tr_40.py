"""Вычитка турецкого, порция p040 (C1), 23.10: работа, учёба, деньги, характер — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    9086: (T + "«Çocuk doğum günündeki» — коряво", {"example_tr": "Doğum günü partisindeki sihirbazlık gösterisinde kızım sihirbaza asistanlık yapacak, çok heyecanlı"}),
    9098: (T + "«gerekiyor» → «lazım»", {"example_tr": "Üç çocuk ve iki işle her pazar bütün haftayı koordine etmemiz lazım"}),
    9112: (T + "«giriş sadece öndeki şoför kapısından» — коряво", {"example_tr": "Bu otobüste giriş sadece ön kapıdan, şoförün yanından"}),
    9131: (T + "«talepler çok daha yüksek» — без принадлежности", {"example_tr": "Yeni okulun talepleri çok daha yüksek, oğlum her akşam ödevlerinin başında oturuyor"}),
    9843: (T + "«Büyükanne ve büyükbabamla» — тяжело", {"example_tr": "Dedemlerle geçirdiğimiz zaman çok değerli, o yüzden her ay onlara gidiyoruz"}),
    9850: (T + "«fazladan ödememiz gerekiyor» — коряво", {"example_tr": "Isınma giderlerinin hesabı geldi, iki yüz avro ek ödeme çıktı"}),
    9885: (T + "«elma bolluğu yaşıyoruz» — калька", {"example_tr": "Sonbaharda elmamız bol oluyor, komşulara dağıtıyoruz"}),
    10822: (T + "«aydınlanma yaşadım» — калька", {"example_tr": "Duşta birden aydınlanma geldi: kayıp araba anahtarının yerini hatırladım"}),
    10829: (T + "«Büyükannenin evinde … evde» — повтор", {"example_tr": "Babaannelerinin yanında çocuklar küçük melekler gibi davranıyor, evde yine haydut kesiliyorlar"}),
    10876: (T + "«ekmeğimin sonucu» — калька", {"example_tr": "İlk ekmeğim hayal kırıklığı oldu, taş gibi sert"}),
    10905: (T + "«…aramayacağımı söylüyor» — тяжело", {"example_tr": "Kız kardeşime göre biraz öz saygım olsa eski sevgilimi üç kez aramazdım"}),
    10944: (T + "«büyükanne» без принадлежности", {"example_tr": "Torunu tabaktaki son kek dilimini kapınca büyükannesi 'Seni küçük hergele!' diye bağırıyor"}),
    10973: (T + "«hep bir tokat var» — калька es gibt", {"example_tr": "Eski filmlerde kahraman yanlış bir şey söylediğinde hep bir tokat atılır, bugün bu bir skandal olurdu"}),
    10976: (T + "Wurst — не «sucuk»", {"example_tr": "Köpeğimiz masadan düşebilecek her sosis parçasına büyük bir arzuyla bakıyor"}),
    11007: (T + "«Kolalı ve pastalı çocuk doğum gününden» — коряво", {"example_tr": "Kola ve pastalı doğum günü partisinden sonra ufaklıklar o kadar coşkulu ki kimse uyumak istemiyor"}),
    11038: (T + "«barışma oldu» — калька", {"example_tr": "On yıllık küslükten sonra annem doğum gününde nihayet kız kardeşiyle barıştı"}),
}

REPLACE = []

SPLIT_LATER = {}
