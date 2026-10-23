"""Вычитка турецкого, порция p043 (C1), 23.10: семья, природа, право — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    15160: (T + "«tanıştırıp çöpçatanlık yapmaya çalışıyor» — тяжело", {"example_tr": "Annem yıllardır beni arkadaşının kızıyla evlendirmek için çöpçatanlık yapıyor"}),
    15164: (T + "«… düşünüyor» — тяжело; Antlitz — «çehre»", {"example_tr": "Müzede bir azizin eski tablosu var, oğluma göre çehresi tıpkı dedesine benziyor"}),
    15172: (T + "«daraltması gerekiyor» — тяжело", {"example_tr": "Terzi gelinliği belden biraz daha daraltacak"}),
    15182: (T + "«en çok … evlendirmek istiyor» — калька am liebsten", {"example_tr": "Büyükannemin elinde olsa beni komşusunun kibar oğluyla evlendirirdi"}),
    15185: (T + "«Opera yine aldatma hakkında» — коряво", {"example_tr": "Operada yine bir aldatma hikâyesi var ve büyükannem on dakikada bir 'Skandal' diye fısıldıyor"}),
    15190: (T + "«evde itmemizi» — калька schieben", {"example_tr": "Ufaklık çamaşır sepetine oturmuş, onu evin içinde gezdirmemizi istiyor"}),
    15603: (T + "«kontrol edemiyorum» — калька", {"example_tr": "Bahçede her yerde yabani otlar büyüyor ve baş edemiyorum"}),
    15608: (T + "«zıplamasına izin veriliyor» — канцелярит", {"example_tr": "Çiftlikte çocuklar her yerleri kaşınana kadar taze samanda zıplayabiliyor"}),
    15662: (T + "«Sevgi hayvanat bahçesinde» — калька Streichelzoo", {"example_tr": "Hayvan sevme bahçesinde bir lama kocamın tam yüzüne tükürdü ve çocuklar hâlâ gülüyor"}),
    15683: (T + "«sahibi» без принадлежности", {"example_tr": "Binicilik çiftliğinin sahibi kızıma ata dizginin nasıl takıldığını gösteriyor"}),
    15684: (T + "«Büyükanne ve büyükbabanın» — тяжело", {"example_tr": "Dedemlerin çiftliğinde yaşlı kısrak bir tay doğurdu, çocuklar ona isim koyacak"}),
    15695: (T + "«küvete girmesi gerekiyor» — коряво", {"example_tr": "Köpeğimiz yürüyüşte leşin üstünde yuvarlanmaya bayılıyor, sonra da onu küvete sokmak zorunda kalıyoruz"}),
    16374: (T + "«savunma yapıyor» — калька", {"example_tr": "Yaşlı kedimiz yeni yavru köpeğe karşı kendini cesurca savunuyor"}),
    16385: (T + "«grup şeker istiyor» — коряво", {"example_tr": "Cadılar Bayramı'nda mahalleden koca bir çocuk grubu kapıya dikilip şeker istiyor"}),
    16394: (T + "Schulgeld — сэкономленная плата, не «okul ücreti»", {"example_tr": "Çocuklarım devlet okuluna gidiyor, özel okula vereceğim parayı da sınıf gezileri için biriktiriyorum"}),
    16416: (T + "erlassen — «bağışlamak», не «affetmek»", {"example_tr": "Komşu kedisine baktığımız için bu ayki bahçe kirasını bize bağışladı"}),
    16483: (T + "«Çocuk doğum gününden» — коряво", {"example_tr": "Doğum günü partisinden sonra masa katliam sonrası gibi görünüyor, her yer kırmızı reçel"}),
    16506: (T + "«konuşmasına izin verildi» — канцелярит", {"example_tr": "Açık kapı gününde oğlum polis telsizinden konuşabildi ve 'Merhaba anne' dedi"}),
    16512: (T + "«dehşete düşmüş» — время", {"example_tr": "Bu filmde aile dizisindeki o sevimli oyuncu birden silah tüccarını oynuyor ve annem dehşete düştü"}),
    16518: (T + "«onayına ihtiyacı var» — калька", {"example_tr": "Kızım on dört yaşında, kulak deldirmek için hâlâ anne ya da babasının onayı lazım"}),
    16538: (T + "«raporuna ihtiyacımız var» → «lazım»", {"example_tr": "Bisiklet hırsızlığından sonra sigorta için polis raporu lazım, yoksa hiçbir şey ödemiyorlar"}),
}

REPLACE = []

SPLIT_LATER = {}
