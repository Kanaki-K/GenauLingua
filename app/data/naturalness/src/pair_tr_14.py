"""Шаг 2, tr, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    3070: (T + "word in example", {"t_tr": "ek, ilave, ayrıca"}),
    6398: (T + "word in example", {"t_tr": "doğru olmak, uyuşmak, oy vermek"}),
    6418: (T + "word in example", {"t_tr": "tutmak, kavramak, (nicht fassen können) aklı almamak"}),
    6427: (T + "word in example", {"t_tr": "etkilenmiş, hayran kalmış, (angetan sein) bayılmak"}),
    6462: (T + "word in example", {"t_tr": "vazgeçmek, pes etmek, postaya vermek"}),
    6486: (T + "word in example", {"t_tr": "nöbet tutmak, (bei jemandem wachen) başında beklemek"}),
    6519: (T + "word in example", {"t_tr": "siper, korunak, (in Deckung gehen) sığınmak"}),
    6525: (T + "word in example", {"t_tr": "kocaman, devasa, çok büyük"}),
    6593: (T + "word in example", {"t_tr": "sözde, iddiaya göre, güya"}),
    6603: (T + "word in example", {"t_tr": "ortaya çıkarmak, sonuç vermek, göstermek"}),
    6620: (T + "word in example", {"t_tr": "(zurechtfinden) yolunu bulmak, (zurechtkommen) başa çıkmak"}),
    6672: (T + "word in example", {"t_tr": "teşhis etmek, tanımak, kimliğini belirlemek"}),
    6710: (T + "word in example", {"t_tr": "pılı pırtı, şeyler, iş"}),
    6728: (T + "word in example", {"t_tr": "var olmak, (nicht existieren) yok olmak"}),
    6758: (T + "word in example", {"t_tr": "oldukça, kesinlikle, pekâlâ"}),
    6784: (T + "word in example", {"t_tr": "kullanmak, devreye sokmak, (sefer) koymak"}),
}

REPLACE = []
SPLIT_LATER = {}
