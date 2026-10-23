"""Вычитка турецкого, порция p025 (B1), 23.10: транспорт, техника, наука, дом — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    17148: (T + "«Nehri geçmek için … karşı tarafa gidiyoruz» — тавтология", {"example_tr": "Feribotla nehrin karşı yakasına geçiyoruz"}),
    17193: (T + "«hızlı bir şekilde yakıt almam» — канцелярит", {"example_tr": "Yola çıkmadan önce bir benzin almam lazım"}),
    17198: (T + "«Trafik sıkışıklığındayım» — калька", {"example_tr": "Trafikte kaldım, geç kalacağım"}),
    17255: (T + "«Arabama dizel gerekiyor» — подстрочник", {"example_tr": "Arabam benzinle değil, dizelle çalışıyor"}),
    17319: (T + "«handa geceliyoruz» — архаично", {"example_tr": "İtalya yolunda bir pansiyonda kalıyoruz"}),
    17370: (T + "«Otobüsün kadın şoförü» — род не нужен", {"example_tr": "Otobüsün şoförü her sabah bütün çocukları selamlıyor"}),
    17375: (T + "«Aracımı» — канцелярит", {"example_tr": "Arabamı düzenli olarak oto yıkamaya götürüyorum"}),
    17401: (T + "«yemek satın alabilirsiniz» — подстрочник", {"example_tr": "Trenin yemekli vagonunda sıcak yemek yiyebilirsiniz"}),
    17486: (T + "«Kod nedir?» — книжно", {"example_tr": "Kod ne?"}),
    17533: (T + "«Büyük bir ağın parçasıyım» — непонятно", {"example_tr": "İş hayatında geniş bir bağlantı ağım var"}),
    17585: (T + "«onu düzgün tak» — лишнее «onu»", {"example_tr": "Fiş gevşek, iyice tak"}),
    17592: (T + "«onun blogunu» — лишнее «onun»", {"example_tr": "Blogunu her gün okuyorum"}),
    17700: (T + "«Benim favori radyo istasyonum» — калька", {"example_tr": "En sevdiğim radyo kanalı hep güzel müzik çalıyor"}),
    17833: (T + "«O satışta çalışıyor» — подстрочник", {"example_tr": "Satış bölümünde çalışıyor"}),
    17978: (T + "«fazla büyük» — калька", {"example_tr": "Vida birkaç milimetre büyük geliyor"}),
    17992: (T + "«On kilometrelik yarıçapta» — книжно", {"example_tr": "On kilometre çevrede hiç süpermarket yok"}),
    18030: (T + "«Fayanslar küçük mavi beyaz kareler» — без сказуемого", {"example_tr": "Fayanslar mavi beyaz küçük karelerden oluşuyor"}),
    18187: (T + "Haus здесь — многоквартирный дом, «bina»", {"example_tr": "Binanın sakinleri çok cana yakın"}),
    18191: (T + "«Gece için konaklama arıyoruz» — канцелярит", {"example_tr": "Gece kalacak bir yer arıyoruz"}),
    18203: (T + "в доме/квартире — «oturmak»", {"example_tr": "Dar bir sokakta oturuyorum"}),
}

REPLACE = []

SPLIT_LATER = {}
