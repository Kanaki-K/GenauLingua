"""Вычитка турецкого, порция p001 (A1), 23.10: кальки и книжные обороты → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    14: (T + "«Yani» — «то есть»; в начале фразы «also» = «peki»", {"example_tr": "Peki, saat üçte gidiyoruz"}),
    50: (T + "«görev» — задание по службе; школьное — «ödev»", {"example_tr": "Bu ödev zor değil"}),
    103: (T + "«O kesinlikle gelir» — книжно", {"example_tr": "Kesin gelir"}),
    160: (T + "«O burada» — подстрочник", {"example_tr": "Burada"}),
    205: (T + "«Görev kolay» — не школьное слово", {"example_tr": "Bu alıştırma kolay"}),
    213: (T + "«Roma'da bulundum» — канцелярит", {"example_tr": "Bir kere Roma'ya gittim"}),
    284: (T + "«Bir soru var mı?» так не спрашивают", {"example_tr": "Soracağın bir şey var mı?"}),
    295: (T + "слово — «eskiden», в примере было «önceden»", {"example_tr": "Eskiden Berlin'de yaşıyordu"}),
    316: (T + "«gefällt mir» — «hoşuma gidiyor»", {"example_tr": "Bu çok hoşuma gidiyor"}),
    330: (T + "«seve seve içerim» — «с радостью выпью», не «люблю пить»", {"example_tr": "Çay içmeyi severim"}),
    362: (T + "«Zaten iyi Almanca konuşuyorsun» — подстрочник", {"example_tr": "Almancan şimdiden çok iyi!"}),
    443: (T + "«sıcak ceket» — горячая куртка", {"example_tr": "Kalın, sıcak tutan bir mont giyiyor"}),
    486: (T + "«Bu benim için açık» — калька", {"example_tr": "Bu bence gayet açık"}),
}

REPLACE = []

SPLIT_LATER = {}
