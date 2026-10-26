"""Шаг 2, en, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    1148: (T + "word in example", {"t_en": "proposal of marriage, application, (einen Antrag machen) to propose"}),
    1186: (T + "word in example", {"x_en": "After a day at the office, sport is a good balance for me"}),
    1230: (T + "word in example", {"x_en": "The waiter serves us very attentively"}),
    1241: (T + "word in example", {"t_en": "to take (a course), to prove, to sign up for"}),
}

REPLACE = []
SPLIT_LATER = {}
