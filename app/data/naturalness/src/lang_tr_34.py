"""Вычитка турецкого, порция p034 (B2), 23.10: общение, культура, религия, семья — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    14281: (T + "«anlayabileceğini söylüyor» — тяжело", {"example_tr": "Dedeme göre tokalaşmadan insanın dürüst olup olmadığı hemen anlaşılır"}),
    14284: (T + "«kalbim ağzımda zonkluyor» — коряво", {"example_tr": "Otobüse koştuktan sonra kalbim ağzıma gelmiş gibi zonkluyor"}),
    14285: (T + "«seksenine» — без «yaş günü»", {"example_tr": "Büyükannemin seksen yaş günü için ağabeyim bir şiir yazdı ve ailenin yarısı ağladı"}),
    14296: (T + "Gassi gehen — «gezdirmek»", {"example_tr": "Köpek fikrini destekliyorum ama onu gezdirmeye lütfen başkası çıksın"}),
    14314: (T + "«lütfen tam bir sessizlik» — без глагола", {"example_tr": "Babamın hediyesi konusunda ağzınızı sıkı tutun, hiçbir şeyden şüphelenmemeli!"}),
    14473: (T + "«güzel şekilde süslenmiş» — калька", {"example_tr": "Kilisedeki sunak çok güzel süslenmiş"}),
    14486: (T + "«tencerede davul çalıyor» — коряво", {"example_tr": "Çocuk sopalarla tencereye vurarak davul çalıyor"}),
    14522: (T + "«sagasının» — по-турецки «serisi»", {"example_tr": "Oğlum Harry Potter serisinin bütün kitaplarını üç kez okudu"}),
    14526: (T + "Gläubige в церкви — «cemaat»", {"example_tr": "Papaz yardımcısı kilisede cemaatle konuşuyor"}),
    14538: (T + "«ile karşılaştırır» — по-турецки «benzetiyor»", {"example_tr": "Bu metafor hayatı bir yolculuğa benzetiyor"}),
    14545: (T + "«döşenmesine dair bir gösteri» — канцелярит", {"example_tr": "Yapı marketinde cumartesileri fayansın nasıl döşeneceğini anlatan bir gösteri var"}),
    14555: (T + "«ailelere oğullarının» — по-турецки «anne babaya»", {"example_tr": "Öğretmen büyük bir incelikle anne babaya oğullarının sorunları olduğunu anlattı"}),
    14585: (T + "nachgefahren — «takip etti»", {"example_tr": "Kızım en sevdiği grubu turnede üç şehir boyunca takip etti"}),
    14623: (T + "«bir bis daha yaptı» — коряво", {"example_tr": "Seyirciler grup bis yapana kadar alkışladı"}),
    14649: (T + "«yazılı olduğu bir yazı» — тавтология", {"example_tr": "Alyansımın içinde düğün tarihimizi gösteren bir yazı var"}),
    14714: (T + "«O,» — лишнее", {"example_tr": "On yıldır şov dünyasında çalışıyor"}),
    14718: (T + "«fotoğrafçı bile çok heyecanlı» — калька begeistert", {"example_tr": "Dağlar düğün fotoğrafları için mükemmel bir fon, fotoğrafçı bile bayıldı"}),
    14735: (T + "«Büyükannemle büyükbabam» — тяжело", {"example_tr": "Babaannemle dedem ellili yıllarda swing yaparken tanışmışlar ve hâlâ dans ediyorlar"}),
    14747: (T + "«başlıyor … başlıyor» — повтор", {"example_tr": "Gelin kiliseye girince org çalıyor, annem de hemen ağlamaya başlıyor"}),
    14751: (T + "«ihtiyacımız var» → «lazım»", {"example_tr": "Yeğenimin komünyonu için bütün aile Polonya'dan geliyor, üç masa daha lazım"}),
    14754: (T + "«dolabında onun mason olduğunu gördük» — коряво", {"example_tr": "Dedemin mason olduğunu ancak ölümünden sonra dolabını açınca öğrendik"}),
    14785: (T + "«Dondurmacının … yelpazesi» — коряво", {"example_tr": "Dondurmacıda çok geniş bir çeşit yelpazesi var ama oğlum yine de her seferinde vanilya alıyor"}),
    14800: (T + "«her yerde dallarda» — коряво", {"example_tr": "Paskalya'da oturma odamızda dallarda boyalı yumurtalar asılı"}),
    14812: (T + "«altına kayboluyor» — падеж", {"example_tr": "Büyükannem kedimizin doğaüstü güçleri olduğuna inanıyor, çünkü her fırtınadan önce kanepenin altında kayboluyor"}),
    14826: (T + "«piyano çalma sesi» — коряво", {"example_tr": "Üst kattaki komşunun piyano çalması bizi her pazar sekizde uyandırıyor"}),
    14843: (T + "«seksenine yapılan pasta» — коряво", {"example_tr": "Büyükannemin seksen yaş günü pastası onun meşhur haşhaşlı kek tarifine bir saygı"}),
    15042: (T + "«çok duygusal oldu» — калька", {"example_tr": "Cenaze aile için çok duygusal geçti"}),
    15043: (T + "«Nişanlım ve ben» — калька", {"example_tr": "Nişanlımla gelecek ay evleniyoruz"}),
    15056: (T + "«Babacık yakında» — коряво", {"example_tr": "Babacığın birazdan eve gelir"}),
    15061: (T + "«bir lezbiyen» — лишнее «bir»", {"example_tr": "Arkadaşım lezbiyen"}),
    15078: (T + "«büyükanne ve büyükbabasının» — тяжело", {"example_tr": "Çocuk dedesinin ve babaannesinin himayesinde, emin ellerde"}),
    15086: (T + "«erkeğinin tüyleri renkli» — сухо", {"example_tr": "Bu kuşun erkeği rengârenk tüylü"}),
    15102: (T + "животных «sahiplenmek»; «gerekiyor»", {"example_tr": "Barınaktan hayvan sahiplenirken bir sözleşme imzalamak lazım"}),
    15120: (T + "«sinirlere ihtiyacım var» — калька", {"example_tr": "Kızımın doğum günü partisine on iki çocuk geliyor, sağlam sinir lazım"}),
}

REPLACE = []

SPLIT_LATER = {}
