"""Вычитка турецкого, порция p033 (B2), 23.10: здоровье, одежда, общение — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    12910: (T + "«elinde yanık oluştu» — канцелярит", {"example_tr": "Kocam mangal yaparken elini yaktı, şimdi suyla soğutuyor"}),
    12918: (T + "«kış lastiklerinden tasarruf etmek» — коряво", {"example_tr": "Tasarrufu tam da kış lastiklerinden yapmak oldukça kısa görüşlü"}),
    12923: (T + "«gerçek bir histeri koptu» — калька", {"example_tr": "Küçük bir fare yüzünden ofiste tam bir histeri yaşandı"}),
    12929: (T + "«elektrik çarpması yaşadım» — калька", {"example_tr": "Lambayı değiştirirken sigortayı kapatmayı unuttuğum için beni elektrik çarptı"}),
    12941: (T + "«normal şekilde» — тяжело", {"example_tr": "Kan bağışında kan kaybı o kadar az ki sonra gayet normal çalışabiliyorum"}),
    12958: (T + "«konuşmak gerekiyor» — тяжело", {"example_tr": "Büyükannemle yüksek sesle konuşmak lazım, biraz ağır işitiyor ama kabul etmiyor"}),
    12974: (T + "«etkinleştirilmesi için … gerekiyor» — канцелярит", {"example_tr": "Yeni SIM kartı etkinleştirmek için kimliğim ve yarım saat sabır lazım"}),
    12980: (T + "длинная цепочка «-duğunu ve -duğunu»", {"example_tr": "Kan testine göre kızamığa karşı yeterli antikorum var, aşı olmama gerek yok"}),
    12989: (T + "«çok sakin bir şekilde açıkladı» — тяжело", {"example_tr": "Doktor gayet sakin bir şekilde belsoğukluğunun bugün antibiyotikle kolayca tedavi edildiğini anlattı"}),
    12992: (T + "«kurtarma operasyonunda … gerekti» — коряво", {"example_tr": "Ağaçtaki kedimizin kurtarma operasyonu için iki itfaiyeci ve uzun bir merdiven gerekti"}),
    13030: (T + "время — «tat alamayacağım»", {"example_tr": "Sıcak pizzayla damağımı yaktım, şimdi iki gün hiçbir tat alamayacağım"}),
    13080: (T + "Dampfbad в бассейне — «buhar odası», не «hamam»", {"example_tr": "Ağır bir soğuk algınlığında havuzdaki buhar odası bana her ilaçtan daha iyi geliyor"}),
    13137: (T + "«kanepede üç güne ihtiyacı var» — калька", {"example_tr": "Maratondan sonra kocam kendini toparlamak için üç gün kanepeden kalkmıyor"}),
    13157: (T + "reif für die Nervenklinik — идиома", {"example_tr": "Beş torunla üç haftalık tatilden sonra büyükannem \"Benim yerim artık akıl hastanesi\" diyor"}),
    13516: (T + "«haberdar olmamalı» — книжно", {"example_tr": "Karım bundan hiçbir şey duymamalı, bu bir sürpriz"}),
    13525: (T + "«Burada köyde» — калька", {"example_tr": "Bu köyde herkes herkesi tanır"}),
    13543: (T + "wider Erwarten — «beklenenin aksine»", {"example_tr": "Beklenenin aksine küçük takımımız maçı kazandı"}),
    13679: (T + "«yıkanabiliyor» — правило ухода", {"example_tr": "İpek bluz sadece elde, soğuk suyla yıkanır"}),
    13682: (T + "«Soğuk olduğu için» — тяжело", {"example_tr": "Hava soğuk, kalın bir kazak giyiyorum"}),
    13690: (T + "«Ayakkabılarımdaki topuklar» — коряво", {"example_tr": "Ayakkabılarımın topukları çok yüksek"}),
    13698: (T + "«bin parçaya ayırdı» — коряво", {"example_tr": "Biz yokken köpek gazeteyi parça parça etti"}),
    13777: (T + "«en çok … çıkarmamak istiyor» — калька am liebsten", {"example_tr": "Oğlum bütün pazar pijamasını hiç çıkarmamak istiyor"}),
    14007: (T + "«parkta çöpe karşı» — коряво", {"example_tr": "Belediye parktaki çöplere karşı bir kampanya yürütüyor"}),
    14009: (T + "angewiesen — «muhtaç»", {"example_tr": "Benim yardımıma muhtaç"}),
    14016: (T + "«Bardak masaya koyduğumda» — грамматика", {"example_tr": "Bardağı masaya koyunca şıngırdıyor"}),
    14017: (T + "«O bizim grubumuzun» — лишнее", {"example_tr": "Grubumuzun sözcüsü o"}),
    14019: (T + "«Onun el yazısı» — лишнее; книжно", {"example_tr": "El yazısı hiç okunmuyor"}),
    14020: (T + "noch etwas übrig — не «hâlâ»", {"example_tr": "Pastadan biraz kaldı mı?"}),
    14026: (T + "«Benim açımdan … itirazım» — повтор", {"example_tr": "Benim açımdan plana bir itiraz yok"}),
    14036: (T + "«tartışma vardı» — калька es gab", {"example_tr": "Akşam yemeğinde yine bir tartışma çıktı: telefon masada yasak mı olmalı?"}),
    14054: (T + "«Talebin nedir? Sadece söyle» — канцелярит", {"example_tr": "İsteğin ne? Çekinmeden söyle"}),
    14060: (T + "«O geldiğinde» — лишнее «O»", {"example_tr": "Gelir gelmez bana hemen haber ver"}),
    14077: (T + "«her zaman küfreder» — коряво", {"example_tr": "Bir şey ters gidince hep küfrediyor"}),
    14111: (T + "«istenen çekiciliği kazanıyor» — калька", {"example_tr": "Kırmızı şal sade elbiseye tam istediği çekiciliği katıyor"}),
    14115: (T + "«uyarı yapmadan … kapıya geldi» — коряво", {"example_tr": "Ev sahibi hiçbir uyarı olmadan cumartesi sabahı kapıya dikildi"}),
    14160: (T + "«kanıta ihtiyacın var» — калька", {"example_tr": "Böyle bir iddia için kanıt lazım, yoksa kimse sana inanmaz"}),
    14220: (T + "«yemeyi tercih ediyorum» — калька lieber", {"example_tr": "Ofis mutfağındaki dedikodulara hiç havam yok, o yüzden öğlenleri dışarıda yiyorum"}),
    14236: (T + "viel zu lang — «fazlasıyla»", {"example_tr": "Yeni anıtın açılışında belediye başkanı fazlasıyla uzun bir konuşma yaptı"}),
}

REPLACE = []

SPLIT_LATER = {}
