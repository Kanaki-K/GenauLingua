"""Вычитка турецкого, порция p037 (B2), 23.10: транспорт, техника, экономика, наука, дом — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    17201: (T + "«Ekspres treniyle» — порядок", {"example_tr": "Havaalanına ekspres trenle gidiyorum"}),
    17205: (T + "«araba gezisi yapacağız» — коряво", {"example_tr": "Pazar günü yeni üstü açık arabayla göle doğru küçük bir tur atacağız"}),
    17276: (T + "«station wagon araba lazım» — повтор", {"example_tr": "Üç çocuk ve bir köpekle bize station wagon lazım, yoksa bagaj sığmıyor"}),
    17345: (T + "«hızlanmasında» — коряво", {"example_tr": "Elektrikli araba hızlanırken her seferinde koltuğa yapışıyorum"}),
    17365: (T + "«kısa bir süreliğine uğruyoruz» — тяжело", {"example_tr": "İtalya yolunda hep Innsbruck'taki Erika teyzeye bir uğruyoruz"}),
    17369: (T + "«açıldığı … duyuldu» — коряво", {"example_tr": "İnişte iniş takımları o kadar gürültüyle açıldı ki oğlum kulaklarını kapattı"}),
    17371: (T + "«on dakika sonra uyuyor» — schon", {"example_tr": "Tatilden dönüş yolculuğunda çocuklar arabada hep daha on dakika geçmeden uyuyor"}),
    17403: (T + "«kaza inişi» в переносном смысле — калька", {"example_tr": "Oğlumun ilk keki tam bir felaketti, fırında tamamen çöktü"}),
    17408: (T + "«mahallenin etrafında tam bir tur» — смысл genau einmal", {"example_tr": "Komşum her pazar klasik otomobilini parlatıyor, sonra da sokağın etrafında sadece bir tur atıyor"}),
    17557: (T + "«gerek» → «lazım»", {"example_tr": "Kolu sola itmem lazım"}),
    17568: (T + "«bisikletleri pompalayacağım» — коряво", {"example_tr": "Geziden önce bisikletlerin lastiklerini bir şişireyim"}),
    17589: (T + "«uygulamayla kontrolü var» — калька", {"example_tr": "Kaloriferi artık uygulamadan kontrol edebiliyorum, ofisten bile açabiliyorum"}),
    17598: (T + "«uçurmana izin verilmeden önce» — тяжело", {"example_tr": "Gerçek uçak uçurmadan önce saatlerce simülasyonda pratik yapılıyor"}),
    17688: (T + "«Hurdadan … yeni zincirle» — коряво", {"example_tr": "Çöpten bulduğum eski bisiklet yeni zincir takınca yine tamamen çalışır durumda"}),
    17701: (T + "«bakmam gerekiyor» — тяжело", {"example_tr": "Aile geçmişi araştırması için kütüphanede eski gazeteleri mikrofilmden taramam lazım"}),
    17741: (T + "«arşivde talep üzerine» — канцелярит", {"example_tr": "Yeni bölüm cumadan itibaren internette istendiği zaman izlenebiliyor, o zaman birlikte izleriz"}),
    17804: (T + "«büyük etkiye sahip» — канцелярит", {"example_tr": "Petrol şirketlerinin lobisi çok etkili"}),
    17817: (T + "«Büyükannemle büyükbabam için» — тяжело", {"example_tr": "Dedemlerin zamanında kendi araban olması bir refah göstergesiydi"}),
    17857: (T + "«Ortağım ve ben … işletmeyi» — калька", {"example_tr": "İşi ortağımla birlikte yürütüyoruz"}),
    17886: (T + "«şehre doğru büyümeyi» — коряво", {"example_tr": "Köşedeki fırın o kadar iyi gidiyor ki şimdi komşu şehre doğru büyümeyi, orada şube açmayı planlıyor"}),
    17950: (T + "«pürüzsüz bir kütle» — калька", {"example_tr": "Hamuru pürüzsüz bir kıvama gelene kadar yoğuruyorum"}),
    17956: (T + "«spekülasyon yapıyorlar» — канцелярит", {"example_tr": "Bilim insanları uzaydaki solucan delikleri hakkında kafa yoruyor"}),
    17969: (T + "«tam istenen ekşiliği» — калька", {"example_tr": "Biraz limon sosa tam kararında ekşilik katıyor"}),
    17973: (T + "«Büyükannemle büyükbabam için» — тяжело", {"example_tr": "Dedemlere göre yabancılarla aynı evde yaşamak çok tuhaf bir yaşam biçimi"}),
    18012: (T + "strahlen — «yüzü gülüyor»", {"example_tr": "Kızımız yüzme yarışmasında bronz aldı ve o günden beri yüzü gülüyor"}),
    18028: (T + "«solucan araştırıyor» — коряво", {"example_tr": "Oğlum bahçede solucan araştırması yapıyor, sonra bulduklarını gururla mutfağa getiriyor"}),
    18099: (T + "«saklayarak uyuyor» — коряво", {"example_tr": "Oğlum sahilde küçük bir fosil buldu, şimdi yastığının altına koyup öyle uyuyor"}),
    18183: (T + "«Onun odası tamamen dağınık» — лишнее «onun»", {"example_tr": "Odası darmadağınık"}),
    18211: (T + "«sadece yüksek sesle kapıyı çal» — калька", {"example_tr": "Kapı zili bozuk, kapıyı sert vur"}),
    18213: (T + "«üzerinde yürüyünce» — порядок", {"example_tr": "Üzerinde yürüyünce döşeme tahtaları gıcır gıcır ediyor"}),
    18230: (T + "«değirmende elle öğütüyor» — коряво", {"example_tr": "Dedem her sabah kahvesini eski bir el değirmeniyle öğütüyor"}),
    18237: (T + "«bir küreğe ihtiyacım var» — калька", {"example_tr": "Karı küremek için bir kürek lazım"}),
    18239: (T + "dicht aneinander — «birbirine yapışık»", {"example_tr": "Şehirde evler birbirine yapışık duruyor"}),
    18250: (T + "«gerek» → «lazım»", {"example_tr": "Yara bandı yapıştırmadan önce yarayı iyice temizlemen lazım"}),
    18261: (T + "«almamız gerekecek» — тяжело", {"example_tr": "Bodrumdaki eski kazan o kadar gürültü yapıyor ki yenisini almamız lazım"}),
    18279: (T + "«eğilmek gerekiyor» — тяжело", {"example_tr": "Eski çiftlik evimizde kirişlerin altından eğilmen lazım, yoksa başını çarparsın"}),
}

REPLACE = []

SPLIT_LATER = {}
