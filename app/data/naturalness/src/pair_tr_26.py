"""Шаг 2, tr, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    18309: (T + "word in example", {"x_tr": "Yeni bir mutfak monte ettiriyoruz"}),
    18346: (T + "word in example", {"x_tr": "Hadi canım, doğru küçük yatağına!"}),
    18410: (T + "word in example", {"x_tr": "Gelin, sıcak odaya girin, dışarıda kar yağıyor"}),
    18665: (T + "word in example", {"t_tr": "geçenlerde, son zamanlarda, kısa süre önce"}),
}

REPLACE = []
SPLIT_LATER = {}
