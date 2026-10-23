"""Вычитка турецкого, порция p022 (B1), 23.10: культура, семья — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    14044: (T + "«Burada sana karşı çıkmam gerek» — «da» не про место", {"example_tr": "Bu konuda sana itiraz etmek zorundayım"}),
    14061: (T + "«başarıyla tamamladığın için» — канцелярит", {"example_tr": "Sınavı geçtiğin için tebrikler!"}),
    14095: (T + "«Bir uzlaşma bulduk» — калька", {"example_tr": "Orta yolu bulduk"}),
    14169: (T + "«Gitmeliyim» — книжно", {"example_tr": "Hoşça kal, yakında görüşürüz! Gitmem lazım"}),
    14213: (T + "«resmi mi kalalım?» — по-турецки «siz mi diyelim»", {"example_tr": "Birbirimize sen diyebilir miyiz, yoksa siz mi diyelim?"}),
    14235: (T + "«el sıkışarak pekiştirdik» — книжно", {"example_tr": "Bunu el sıkışarak kararlaştırdık"}),
    14251: (T + "«telefon görüşmesi bekliyorum» — калька", {"example_tr": "Hâlâ doktordan telefon bekliyorum"}),
    14271: (T + "«dedem yine hareketli» — калька", {"example_tr": "Diz ameliyatından sonra dedem yine rahatça hareket edebiliyor"}),
    14329: (T + "«senin açısından … abartı» — калька", {"example_tr": "Bu söylediğin büyük bir abartıydı"}),
    14389: (T + "«Bu ses tonuyla değil» — оборвано", {"example_tr": "Benimle bu ses tonuyla konuşma lütfen!"}),
    14406: (T + "«Bu günah değil» — подстрочник «doch»", {"example_tr": "Bunda günah yok ki"}),
    14412: (T + "Segen — «nimet», не «bereket»", {"example_tr": "Yağmur bitkiler için tam bir nimetti"}),
    14425: (T + "«Onun şarkı söylemesi» — тяжело", {"example_tr": "Şarkı söyleyişi çok güzeldi"}),
    14441: (T + "мессу «yönetmek», не «düzenlemek»", {"example_tr": "Kardinal yarın önemli bir ayin yönetiyor"}),
    14449: (T + "«Müziğin sesleri» — Klang = «tını»", {"example_tr": "Müziğin tınıları çok güzeldi"}),
    14451: (T + "«ailesinin olduğu mübarek bir insan» — коряво", {"example_tr": "Allah ona mutlu bir aile vermişti, şanslı bir insandı"}),
    14619: (T + "«Sen gerçek bir şairsin» — подстрочник", {"example_tr": "Sen tam bir şairsin!"}),
    14643: (T + "«Onun tutkusu» — лишнее «onun»", {"example_tr": "Tutkusu fotoğrafçılık, harika fotoğraflar çekiyor"}),
    14684: (T + "«sihirbaz bir kadın» — порядок", {"example_tr": "Çocuk doğum günü partisine kadın bir sihirbaz geliyor"}),
    14697: (T + "без сказуемого", {"example_tr": "Ödül töreninde podyumun en üst basamağında duruyor"}),
    14700: (T + "«favori şarkım» — калька", {"example_tr": "Bu en sevdiğim şarkı, sürekli dinliyorum"}),
    14704: (T + "«Onun anlatısına göre» — книжно", {"example_tr": "Onun anlattığına göre durum tamamen farklıydı"}),
    14765: (T + "Duo — «ikili», «düet» = песня дуэтом", {"example_tr": "Ünlü ikili yarın sahneye çıkacak"}),
    14936: (T + "Fräulein — «küçükhanım», не «bayan»", {"translation_tr": "küçükhanım, genç hanım", "example_tr": "Eskiden genç kadınlara küçükhanım denirdi"}),
    14961: (T + "«O, kulübün üyesi» — лишнее «O»", {"example_tr": "Kulübün üyesi"}),
    14967: (T + "«Meslektaşıyla bir ilişkisi» — сухо", {"example_tr": "İş arkadaşıyla gizli bir ilişkisi var"}),
    14970: (T + "«juniör olarak oynuyor» — калька", {"example_tr": "Takımın gençler kadrosunda oynuyor"}),
    14974: (T + "«Onun ince bir vücudu» — лишнее «onun»", {"example_tr": "İnce bir vücudu var"}),
    14976: (T + "«O gerçek bir centilmen ve…» — подстрочник", {"example_tr": "Tam bir centilmen, çok kibar"}),
    15002: (T + "«onun penisini» — лишнее «onun»", {"example_tr": "Doktor penisini muayene etti"}),
    15074: (T + "«kendi köyünü» — лишнее «kendi»", {"example_tr": "Hikâyenin kadın kahramanı köyünü kurtarıyor"}),
    15110: (T + "«O, doğuştan bir öğretmen» — тяжело", {"example_tr": "Doğuştan öğretmen"}),
}

REPLACE = []

SPLIT_LATER = {}
