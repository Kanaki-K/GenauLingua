"""Вычитка турецкого, порция p035 (B2), 23.10: люди, природа, право — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    15173: (T + "«Büyükannemlerle büyükbabamlar» — тяжело", {"example_tr": "Dedemlerle babaannemler için evlilik öncesi bekâret çok önemliydi, çocuklarım için ise konu bile değil"}),
    15229: (T + "«üst bedenimi soymam gerekiyor» — канцелярит", {"example_tr": "Doktorda göğsümü dinlesin diye belden yukarısını soymam lazım"}),
    15302: (T + "«defni için her şeyi yazdı» — коряво", {"example_tr": "Dedem defniyle ilgili her şeyi şimdiden yazmış, hangi şarkıların çalınacağını bile"}),
    15517: (T + "«çamurda sıkışıp kaldı» — «çamura saplandı»", {"example_tr": "Ayakkabılarım çamura saplandı"}),
    15520: (T + "«rüzgâr esintisi» — тавтология", {"example_tr": "Sadece hafif bir esinti vardı"}),
    15522: (T + "«bir sel gibi e-posta gelmişti» — коряво", {"example_tr": "Tatilden dönünce e-posta seline boğuldum, iki günüm gitti"}),
    15525: (T + "«görebilirsin» — лишнее", {"example_tr": "Ufukta güneş yavaş yavaş batıyor"}),
    15532: (T + "«midilliyle bir tur binebiliyor» — коряво", {"example_tr": "Çiftlikte çocuklar midilliye binip bir tur atabiliyor"}),
    15556: (T + "«ışığına ihtiyacı var» — калька", {"example_tr": "Bitkiler güneş ışığı ister, o yüzden onları pencerenin önüne koyuyorum"}),
    15559: (T + "«büyük gürültü var» — «koptu»", {"example_tr": "Sunucunun yeni saçı yüzünden internette büyük gürültü koptu"}),
    15561: (T + "«bir baykuş duyuyoruz» — коряво", {"example_tr": "Akşamları bahçede sık sık bir baykuşun sesini duyuyoruz"}),
    15576: (T + "«uyumaya devam etmek mümkün değil» — калька", {"example_tr": "Köydeki büyükannemde ilk horoz dörtte ötüyor, uyumak ne mümkün"}),
    15591: (T + "немецкая идиома дословно — по-турецки иначе", {"example_tr": "İkisinin evleneceğini artık kuşlar bile biliyor"}),
    15593: (T + "«gerekiyor» → «lazım»", {"example_tr": "Mayalı hamurun sıcak bir yerde bir saat daha kabarması lazım"}),
    15660: (T + "noch — «daha», не «hâlâ»", {"example_tr": "Dedem çocukken tarlayı daha öküzle sürermiş"}),
    15760: (T + "«Büyükannem ve büyükbabam» — тяжело", {"example_tr": "Dedemler Almanya'nın kuzeybatısında, Kuzey Denizi'ne çok yakın oturuyor"}),
    15797: (T + "«Buzula yürüyüşte» — коряво", {"example_tr": "Buzula yürürken dedem, çocukluğunda buzun otoparka kadar uzandığını anlattı"}),
    15805: (T + "«durdu ve sonunda uyanmasını bekledi» — смысл", {"example_tr": "Oğlum hayvanat bahçesinde pumanın önünde bir saat durup uyanmasını bekledi"}),
    15813: (T + "«Trende o kadar havasızdı» — без подлежащего", {"example_tr": "Tren o kadar havasızdı ki iki saat boyunca açılmayan pencereden başka bir şey düşünemedim"}),
    15883: (T + "«evde geçecek bir güne seviniyor» — калька", {"example_tr": "Kasırga yüzünden yarın bütün trenler iptal, çocuklar da evde kalacakları için seviniyor"}),
    16085: (T + "«on dakika sonra … biliyordum» — коряво", {"example_tr": "Dünkü polisiyede daha onuncu dakikada bahçıvanı kimin öldürdüğünü anlamıştım"}),
    16147: (T + "«gerçek bir … istilası oluyor» — калька", {"example_tr": "Her yaz gölde resmen sivrisinek istilası yaşanıyor"}),
    16148: (T + "«lisansı gerekiyor» — тяжело", {"example_tr": "Bu program için her çalışana ayrı lisans lazım, bu da şirkete çok pahalıya mal oluyor"}),
    16149: (T + "Anklage erheben — «dava açmak»", {"example_tr": "Savcılık dava açtı"}),
    16157: (T + "«öğrenmek istediler» — калька", {"example_tr": "Sokaktaki ankette ne sıklıkla otobüse bindiğimi sordular"}),
    16159: (T + "«hazır bulunuyordu» — канцелярит", {"example_tr": "Başkan yardımcısı da konferanstaydı"}),
    16161: (T + "«yerin her yerine» — повтор", {"example_tr": "Köpek yeni silinmiş yerlerin her yanına pati izi bıraktı"}),
    16174: (T + "«Başkanın suikastından» — грамматика", {"example_tr": "Cumhurbaşkanı öldürüldükten sonra insanlar günlerce sarayın önüne çiçek bıraktı"}),
    16181: (T + "собака «emanet», не «muhafaza»", {"example_tr": "Biz tatildeyken köpek komşuya emanet"}),
    16198: (T + "«taklitti ve polis onu buldu» — коряво", {"example_tr": "Pasaport sahte çıktı, polis de bunu fark etti"}),
    16206: (T + "«verilen ceza çok katıydı» — калька", {"example_tr": "Kötü davranışı yüzünden aldığı ceza çok ağırdı"}),
    16211: (T + "noch — не «hâlâ»", {"example_tr": "Sokak şenliği komitesi mangalda yardım edecek birilerini arıyor"}),
    16212: (T + "обучение «sıkı», не «katı»", {"example_tr": "Askeri eğitim çok sıkı"}),
    16232: (T + "«yirmi yıldan sonra» — коряво", {"example_tr": "Berlin'de geçen yirmi yılın ardından annemle babam taşrada hayatı çok daha sakin buluyor"}),
    16244: (T + "«mobilyaların düzenlemesini» — коряво", {"example_tr": "Karım yeni oturma odasında mobilyaların düzenini her hafta değiştiriyor"}),
    16250: (T + "«her birimiz kendi avukatını tuttu» — согласование", {"example_tr": "Boşanmada ikimiz de ayrı avukat tuttuk"}),
    16252: (T + "«aranması … sürüyor» — канцелярит", {"example_tr": "Hırsız günlerdir aranıyor"}),
    16266: (T + "«daha da çok başı dertte» — порядок", {"example_tr": "Sürücü polise elli avro rüşvet vermek istedi, şimdi başı daha büyük dertte"}),
    16267: (T + "«tahliye oldu» — «yapıldı»", {"example_tr": "Yangın alarmı yüzünden bugün okulda tahliye yapıldı, herkes bir saat bahçede bekledi"}),
    16272: (T + "«hurda ve satılmayacak» — коряво", {"example_tr": "Bu ürün hurda, satılmaz"}),
}

REPLACE = []

SPLIT_LATER = {}
