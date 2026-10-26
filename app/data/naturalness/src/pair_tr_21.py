"""Шаг 2, tr, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    13481: (T + "word in example", {"t_tr": "aynı, aynısı, ta kendisi"}),
    13483: (T + "word in example", {"t_tr": "hiçbir, en ufak bir, hiç"}),
    13835: (T + "word in example", {"t_tr": "eh, işte, ee"}),
    13954: (T + "word in example", {"t_tr": "açıklama, betimleme, tanıtım"}),
    13991: (T + "word in example", {"t_tr": "açıklığa kavuşturmak, netleştirmek, açıkça belirtmek"}),
}

REPLACE = []
SPLIT_LATER = {}
