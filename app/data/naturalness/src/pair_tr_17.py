"""Шаг 2, tr, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    8848: (T + "word in example", {"t_tr": "güvenlik görevlileri, güvenlik servisi, güvenlik"}),
    8959: (T + "word in example", {"t_tr": "kapıcı, kapı görevlisi, hamal"}),
    9165: (T + "word in example", {"t_tr": "yetkili, görevli, sorumlu"}),
    9468: (T + "word in example", {"t_tr": "ders vermek, öğretmek, öğretmenlik yapmak"}),
    9948: (T + "grammar", {"x_tr": "Alışverişten önce hesap bakiyeme bir bakayım"}),
}

REPLACE = []
SPLIT_LATER = {}
