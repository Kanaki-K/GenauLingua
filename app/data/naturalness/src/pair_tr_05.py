"""Шаг 2, tr, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    1484: (T + "word in example", {"t_tr": "sağlıklı, sağlam, sapasağlam"}),
    1530: (T + "word in example", {"t_tr": "içeri, (herein!) girin"}),
    1537: (T + "word in example", {"t_tr": "oraya, (hin und zurück) gidiş dönüş"}),
    1737: (T + "word in example", {"t_tr": "kullanmak, yararlanmak, değerlendirmek"}),
    1819: (T + "word in example", {"t_tr": "başarmak, yetişmek, yapabilmek"}),
    1875: (T + "word in example", {"t_tr": "değil de, bilakis"}),
    2036: (T + "word in example", {"t_tr": "kararlaştırmak, ayarlamak, (Termin vereinbaren) randevu almak"}),
    2106: (T + "word in example", {"t_tr": "herhalde, muhtemelen"}),
    2206: (T + "word in example", {"t_tr": "tür, biçim, yol"}),
    2492: (T + "word in example", {"t_tr": "yönetmek, götürmek, (yol) çıkmak"}),
    2621: (T + "word in example", {"t_tr": "kral (kraliçe), (satrançta) şah"}),
    6212: (T + "word in example", {"x_tr": "Ben tüm bu süre boyunca bekledim"}),
}

REPLACE = []
SPLIT_LATER = {}
