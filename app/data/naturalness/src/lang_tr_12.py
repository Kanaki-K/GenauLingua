"""Вычитка турецкого, порция p012 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    2478: (T + "учительская Fortbildung — «hizmet içi eğitim»", {"translation_tr": "hizmet içi eğitim, kurs", "example_tr": "Öğretmen gelecek hafta yok, ilk yardım üzerine hizmet içi eğitime gidiyor"}),
    2480: (T + "«hâlâ gönüllü arıyoruz» — подстрочник «noch»", {"example_tr": "Şenlik için daha gönüllü arıyoruz"}),
    2498: (T + "«işe yaradığını» — время: «сработает»", {"example_tr": "Bunun işe yarayacağını sana garanti ederim"}),
    2530: (T + "разнобой «glüten/glutensiz»", {"example_tr": "Kızım gluten kaldıramıyor, o yüzden doğum günü için glutensiz pasta yapıyorum"}),
    2585: (T + "«Herhangi bir soru var mı?» — неестественно", {"example_tr": "Aklına takılan herhangi bir soru var mı?"}),
    2599: (T + "«İyi bir satın almaydı» — калька", {"example_tr": "İyi bir alışveriş oldu"}),
    2607: (T + "«dağlarda tırmanıyorum» — без дополнения не говорят", {"example_tr": "Hafta sonları dağlarda tırmanış yapıyorum"}),
    2620: (T + "«Çatışmayı çözmek» — «çatışma» = вооружённый конфликт", {"example_tr": "Bu anlaşmazlığı çözmemiz lazım"}),
    2635: (T + "«mutfakla ilgili lezzetleri» — коряво", {"translation_tr": "mutfak, gastronomik", "example_tr": "Lyon kendine özgü mutfağıyla ünlü, orada sadece yemek yedik"}),
    2652: (T + "«canlı bir şekilde» — тяжело", {"example_tr": "Hâlâ çok canlı hatırlıyorum"}),
    2663: (T + "«Teslimat yarın geliyor» — тавтология", {"example_tr": "Teslimat yarın"}),
    2734: (T + "«Protesto olarak» — калька", {"example_tr": "Protesto etmek için gelmedi"}),
}

REPLACE = []

SPLIT_LATER = {}
