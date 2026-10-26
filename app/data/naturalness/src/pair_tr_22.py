"""Шаг 2, tr, порция 22: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    14391: (T + "word in example", {"t_tr": "şeytan, iblis, cin"}),
    14451: (T + "word in example", {"t_tr": "kutsanmış, mübarek, şanslı"}),
    14974: (T + "word in example", {"t_tr": "figür, karakter, vücut"}),
}

REPLACE = []
SPLIT_LATER = {}
