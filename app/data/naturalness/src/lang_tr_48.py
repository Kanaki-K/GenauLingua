"""Вычитка турецкого, порция p048 (C2), 23.10: общение, культура, семья, природа, право — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    14701: (T + "«anısına bir anma töreni» — тавтология", {"example_tr": "Okulun yüzüncü yılında kurucusu için bir anma töreni düzenleniyor"}),
    14705: (T + "«çok satan bir kitap» — коряво", {"example_tr": "Donna Leon'un yeni kitabı çok satanlar listesinde"}),
    14717: (T + "«günah affı verdi» — книжно", {"example_tr": "En sevdiği vazoyu kırdıktan sonra annem gülümseyerek günahımı affetti"}),
    14731: (T + "«ama sadece kalorifer» — без подлежащего", {"example_tr": "Teyzem eski evinde geceleri paranormal sesler duyuyor ama o sadece kalorifer"}),
    14795: (T + "по-турецки «kalp/acı» не рифмуются — оставить немецкие слова", {"example_tr": "Neredeyse her şlagerde 'Herz' ile 'Schmerz' kafiyeli"}),
    15147: (T + "«iyi bir zevki olduğunu» — коряво", {"example_tr": "Evi iyi bir zevke sahip olduğunu gösteriyor"}),
    15339: (T + "«her zaman» → «hep»", {"example_tr": "Bizde ilk çocuk hep arabada önde oturabiliyor"}),
    15783: (T + "«Cezirde» — без пояснения непонятно", {"example_tr": "Cezirde, deniz çekilince plajda yürüyebiliyoruz"}),
    15801: (T + "«hep aynı gün» — оборвано", {"example_tr": "Her sabah banyo yüzünden aynı kavga, her gün aynı gün tekrar ediyor"}),
    16626: (T + "«Büyükannemle büyükbabam» — тяжело", {"example_tr": "Dedemler eski rejim dönemini bugün bile konuşmak istemiyor"}),
    16638: (T + "«aramam gerekiyor» — тяжело", {"example_tr": "Teraryumumuzdaki bukalemun kendini o kadar iyi kamufle ediyor ki bazen onu aramak zorunda kalıyorum"}),
    16674: (T + "«kilit altına almam gerekiyor» — тяжело", {"example_tr": "Çikolatayı kocamdan saklayıp kilitlemem lazım, yoksa bir saatte biter"}),
    16705: (T + "«gerekiyor» → «lazım»", {"example_tr": "Çekilişi başlatmadan önce hukuk departmanının katılım koşullarını kontrol etmesi lazım"}),
    16712: (T + "«reçete almam gerekiyor» — тяжело", {"example_tr": "Fizik tedavi için aile hekiminden reçete lazım"}),
    16721: (T + "Wurst — не «sucuk»", {"example_tr": "Suçlu köpeğimiz çıktı: Masadaki sosisi araklamış"}),
}

REPLACE = []

SPLIT_LATER = {}
