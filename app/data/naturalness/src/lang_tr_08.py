"""Вычитка турецкого, порция p008 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    777: (T + "«hâlâ kremaya ihtiyacımız var» — подстрочник «noch»", {"example_tr": "Sos için bir de krema lazım"}),
    1095: (T + "«Mir fehlt die Übung» — «не хватает практики»", {"example_tr": "Henüz pratiğim eksik"}),
    1192: (T + "«görev» — служебное задание; здесь «iş»", {"example_tr": "Bu iş için zaman yeterli değil"}),
    1226: (T + "«talebinizi işliyorum» — машинный перевод", {"example_tr": "Talebinizle şu anda ilgileniyorum"}),
    1378: (T + "«gönüllü olarak katılıyorum» — калька", {"example_tr": "Çevre koruma için gönüllü çalışıyorum"}),
}

REPLACE = []

SPLIT_LATER = {}
