"""Вычитка турецкого, порция p009 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    1403: (T + "«hâlâ yardımcıya ihtiyacımız var» — подстрочник «noch»", {"example_tr": "Etkinlik için daha yardımcı lazım"}),
    1419: (T + "«Onu bulamıyorum» — лишнее «onu»", {"example_tr": "Yangın söndürücü nerede? Bulamıyorum"}),
    1464: (T + "«O ünlü bir kemancı» — лишнее «O»", {"example_tr": "Ünlü bir kemancı"}),
    1492: (T + "«30 yaşında zaten keldi» — «zaten» не то", {"example_tr": "Daha 30 yaşındayken kafası kelleşmişti"}),
    1519: (T + "«Kapıcı onu tamir ediyor» — «это починит дворник»", {"example_tr": "Onu kapıcı tamir eder"}),
    1532: (T + "um … herum fahren — объезжать, «etrafından»", {"example_tr": "Şehrin etrafından dolaşıyoruz"}),
    1544: (T + "ноги — «yukarı kaldırmak», не «koymak»", {"translation_tr": "yukarı kaldırmak", "example_tr": "Bacaklarını yukarı kaldırmalısın"}),
    1615: (T + "«kopyalamak» — о бумаге «fotokopisini çekmek»", {"example_tr": "Bunun fotokopisini çekebilir misin?"}),
}

REPLACE = []

SPLIT_LATER = {}
