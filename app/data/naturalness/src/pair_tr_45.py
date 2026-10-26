"""Шаг 2, tr, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    8082: (T + "word in example", {"t_tr": "serinlemek, keyiflenmek, keyfini çıkarmak"}),
    8136: (T + "word in example", {"t_tr": "pek çok, yığın yığın, kitlesel"}),
    8218: (T + "word in example", {"t_tr": "sıralanmak, dizilmek, oluşturmak"}),
    8219: (T + "word in example", {"t_tr": "buradaki, yerel, yöresel"}),
    8225: (T + "grammar", {"x_tr": "Çocuğunuz duvarı boyayla kirletti"}),
    8296: (T + "word in example", {"t_tr": "arıza, iptal, gelememe"}),
    8384: (T + "word in example", {"t_tr": "(auf Anhieb) ilk denemede, bir seferde"}),
    8543: (T + "word in example", {"t_tr": "apaçık, aşikâr, açık"}),
    8553: (T + "word in example", {"t_tr": "havai fişek atmak, patlatmak, yanıp kül olmak"}),
    18804: (T + "word in example", {"t_tr": "uygunsuz, zamansız, uygun olmayan"}),
}

REPLACE = []
SPLIT_LATER = {}
