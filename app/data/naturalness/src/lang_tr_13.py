"""Вычитка турецкого, порция p013 (B1), 23.10: неверные слова и кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    2762: (T + "Reportage — не «röportaj» (по-турецки обычно интервью)", {"translation_tr": "belgesel haber, röportaj", "example_tr": "Bu akşam bakım çalışanlarıyla ilgili bir belgesel haber var"}),
    2773: (T + "Rücksicht nehmen — «думать о других», не «быть внимательным»", {"example_tr": "Başkalarını biraz daha düşünmelisin"}),
    2808: (T + "«Bu zaten doğal» — подстрочник", {"example_tr": "Bu gayet doğal"}),
    2824: (T + "«küçük güneş ışığımsın» — калька", {"example_tr": "Sen benim güneşimsin"}),
    2848: (T + "слово «mali müşavir», в примере «vergi danışmanı»", {"example_tr": "Vergi beyannamem için bir mali müşavire ihtiyacım var"}),
    2972: (T + "«anlayış gösteriyorum» — калька", {"example_tr": "Bunu anlayışla karşılıyorum"}),
    2973: (T + "«hâlâ takviyeye ihtiyacımız var» — подстрочник «noch»", {"example_tr": "Cumartesi taşınma için daha takviye lazım"}),
    2981: (T + "Semmelknödel — «ekmek köftesi»", {"example_tr": "Bayat ekmeği ekmek köftesi yapmak için değerlendiriyorum, böylece hiçbir şey atmıyorum"}),
    2999: (T + "висящее «ki»", {"example_tr": "Etrafına çok sıcaklık yayıyor"}),
    3000: (T + "«lavabo odası» — так не говорят", {"translation_tr": "lavabolar, yıkanma yeri", "example_tr": "Kamp alanındaki lavabolar çok temiz"}),
    3025: (T + "«bebeğin bebek bezini» — тавтология", {"example_tr": "Bebeğin bezini değiştirebilir misin?"}),
}

REPLACE = []

SPLIT_LATER = {}
