"""Шаг 2, tr, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    7476: (T + "word in example", {"t_tr": "hak etmek, layık olmak, (Dank gebührt) borçlu olmak"}),
    7498: (T + "word in example", {"t_tr": "neden olmak, yapılmasını sağlamak, yönlendirmek"}),
    7504: (T + "word in example", {"x_tr": "On dört yaşındaki oğlum şimdiden yaşıtlarının elit sporcuları arasında, eyalet kadrosunda oynuyor"}),
    7507: (T + "word in example", {"t_tr": "tesadüfen, acaba"}),
    7519: (T + "word in example", {"t_tr": "ıskalamak, kaçırmak, (Thema verfehlen) konu dışına çıkmak"}),
    7584: (T + "word in example", {"t_tr": "yerini belirlemek, bulmak"}),
    7622: (T + "word in example", {"t_tr": "öncelik, (Vorrang haben) önce gelmek"}),
    8156: (T + "word in example", {"t_tr": "aydınlatıcı, çok şey anlatan"}),
    8213: (T + "word in example", {"t_tr": "tahmin etmek, önceden söylemek"}),
    8373: (T + "word in example", {"t_tr": "ortaya çıkmak, anlaşılmak"}),
    8399: (T + "word in example", {"t_tr": "kalacak yer bulmuş, kalmış"}),
    8459: (T + "word in example", {"t_tr": "kısıtlamak, azaltmak, kısmak"}),
    8570: (T + "word in example", {"t_tr": "kaplamak, sarmak, (Lust) canı çekmek"}),
    8618: (T + "word in example", {"t_tr": "plan kurmak, bir şeyler çevirmek"}),
    8697: (T + "word in example", {"t_tr": "yeniden, yine"}),
}

REPLACE = []
SPLIT_LATER = {}
