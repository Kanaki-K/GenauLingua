"""Вычитка турецкого, порция p007 (A2–B1), 23.10: кальки и неестественные обороты → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    17864: (T + "«domuz mu?» — нужно «domuz eti»", {"example_tr": "Bu dana eti mi, domuz eti mi?"}),
    17915: (T + "«muayene etmeli» — звучит как приказ врачу", {"example_tr": "Doktorun beni muayene etmesi lazım"}),
    18116: (T + "«O zaman onu alıyorum» — подстрочник", {"example_tr": "Fincan temiz mi? O zaman onu alayım"}),
    18144: (T + "«yan tarafta» — по соседству в доме «yan dairede»", {"example_tr": "Kız arkadaşım yan dairede oturuyor"}),
    18300: (T + "«Evi yazın yeniliyoruz» — ремонт = «tadilat»", {"example_tr": "Yazın evde tadilat yapıyoruz"}),
    18567: (T + "«Ancak dün geldim» — «только вчера» = «daha dün»", {"translation_tr": "daha, ancak", "example_tr": "Daha dün geldim"}),
    18969: (T + "«Onların oğlu» — тяжело", {"example_tr": "Müllerleri tanıyor musun? Oğulları bizimkiyle aynı sınıfta"}),
    18987: (T + "«sen bulmuyor musun?» — подстрочник", {"example_tr": "Yeni filmi bayağı sıkıcı buldum, sence de öyle değil mi?"}),
    85: (T + "Becher — кружка, «kupa»", {"example_tr": "Kahveyi kupadan içiyorum"}),
    154: (T + "«Kendime bir kola sipariş ediyorum» — подстрочник", {"example_tr": "Ben bir kola söyleyeceğim"}),
    182: (T + "слово «görev», в примере «nöbet»", {"example_tr": "Bugün görevde değil"}),
    209: (T + "«bir alışveriş turu yapıyorum» — калька", {"example_tr": "Merkezde alışveriş turuna çıkıyorum"}),
    311: (T + "«Sen aslında nerede doğdun?» — «eigentlich» = «bu arada»", {"example_tr": "Bu arada sen nerede doğdun?"}),
    474: (T + "«Hesabı ödemek istiyoruz» — калька", {"example_tr": "Garsonu çağırır mısın? Hesabı isteyeceğiz"}),
    574: (T + "Brötchen — не «çörek» (сладкая булка)", {"example_tr": "Küçük ekmek en güzel tereyağı ve reçelle olur"}),
    725: (T + "«görevleri açıklıyor» — канцелярит", {"example_tr": "Staj sorumlum her sabah bana o günün işlerini anlatıyor"}),
    754: (T + "«komşular duvardan duyuluyor» — коряво", {"example_tr": "Sıra evde komşuların sesi duvardan geliyor"}),
}

REPLACE = []

SPLIT_LATER = {}
