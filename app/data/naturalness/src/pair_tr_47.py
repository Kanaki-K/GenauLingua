"""Шаг 2, tr, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    11504: (T + "word in example", {"t_tr": "acınası, berbat, perişan"}),
    11954: (T + "word in example", {"t_tr": "şarap çiftliği, bağ evi, şaraphane"}),
    11957: (T + "word in example", {"t_tr": "doldurulmuş, içi dolu, dolgulu"}),
    13114: (T + "word in example", {"t_tr": "skalp, kafa derisi, (mecazi) kelle"}),
    14247: (T + "word in example", {"t_tr": "hafife söyleme, eksik ifade, (das ist eine Untertreibung) az bile"}),
    14254: (T + "word in example", {"t_tr": "tartışmak, ele almak, konuşmak"}),
}

REPLACE = []
SPLIT_LATER = {}
