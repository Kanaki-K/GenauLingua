"""Вычитка турецкого, порция p005 (A2), 23.10: ошибки смысла и кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    1224: (T + "«dikkat etmedi» — «не был внимателен», а смысл «не обратил внимания на меня»", {"translation_tr": "dikkat etmek, umursamak", "example_tr": "Beni hiç umursamadı"}),
    1235: (T + "«gerekçelendirebilir misiniz» — канцелярит", {"example_tr": "Bunun gerekçesini söyleyebilir misiniz?"}),
    1262: (T + "«özellikle lezzetli» — подстрочник", {"example_tr": "Kek bugün özellikle güzel olmuş"}),
    1285: (T + "«sarışın» — о человеке; о волосах «sarı»", {"example_tr": "Sarı saçları var"}),
    1306: (T + "chatten — переписываться", {"example_tr": "Arkadaşlarımla yazışıyorum"}),
    1332: (T + "«ne biçim» — пренебрежительно", {"example_tr": "Bu şey de ne?"}),
    1334: (T + "«tartışılmaz» = «бесспорно» — смысл наоборот", {"example_tr": "Onunla tartışmak mümkün değil"}),
    1658: (T + "Sie liefern — вопрос к продавцу, не пассив", {"example_tr": "Kanepeyi ne zaman teslim edersiniz?"}),
    1819: (T + "«Bunu başarırım» — неестественно", {"example_tr": "Bunu başaracağım"}),
    1922: (T + "«internette geziyorum» — «gezinmek»", {"example_tr": "İnternette geziniyorum"}),
    2160: (T + "«Bu gerçi doğru» — порядок слов", {"example_tr": "Gerçi bu doğru"}),
    2295: (T + "слово «nüfus/halk» потерялось", {"example_tr": "Köy halkının yarısı şenlikteydi"}),
    6212: (T + "«Bütün bu süre boyunca» — тяжело", {"example_tr": "Ben baştan beri bekledim"}),
    6302: (T + "«Kalan senin için» — подстрочник", {"example_tr": "Kalanı senin"}),
}

REPLACE = []

SPLIT_LATER = {}
