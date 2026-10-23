"""Вычитка турецкого, порция p050 (C2), 23.10: наука, дом, время — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    18069: (T + "«ışık üretir» — книжно", {"example_tr": "Bu lamba 800 lümen ışık veriyor"}),
    18085: (T + "«gerekiyor» → «lazım»", {"example_tr": "Duştaki derzleri silikonla yeniden kapatmam lazım"}),
    18086: (T + "noch — не «hâlâ»", {"example_tr": "Firma yeni dondurulmuş pizzası için denek arıyor"}),
    18097: (T + "«hissediyorsunuz» — коряво", {"example_tr": "Hızlı tren istasyondan geçerken peronda basınç dalgası hissediliyor"}),
    18386: (T + "«gerek» → «lazım»", {"example_tr": "Misafirler gelmeden önce odayı hazırlamam lazım"}),
    18387: (T + "Absteige — дешёвый отель, не «batakhane»", {"example_tr": "Bir gece için istasyonun yanındaki ucuz bir otel de olur, yeter ki ucuz olsun"}),
    18391: (T + "«pretzel var» — калька", {"example_tr": "Arada fuayede köpüklü şarap ve brezel satılıyor"}),
    18452: (T + "«her zaman … zamanında» — повтор", {"example_tr": "Evdeki kiracım kirayı hep ayın birinde ödüyor"}),
    18468: (T + "«saklanmayı seviyor» — смысл", {"example_tr": "Yaz ortasında aşçılar biraz serinlemek için soğuk odaya kaçıyor"}),
    18491: (T + "«konforludur» — книжно", {"example_tr": "Otelin mekânları geniş ve konforlu"}),
    18860: (T + "«her zaman» → «hep»", {"example_tr": "Babamın ölüm yıldönümünde annem hep bir mum yakar"}),
    18865: (T + "«arasındadır» — книжно", {"example_tr": "Hastanede ziyaret saati 15 ile 19 arası"}),
    18911: (T + "«bunlar mutlu yıllardı» — калька", {"example_tr": "Geriye dönüp bakınca mutlu yıllarmış"}),
}

REPLACE = []

SPLIT_LATER = {}
