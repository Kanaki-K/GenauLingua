"""Шаг 2, cs, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    8079: (T + "в примере podívat se", {"t_cs": "nahlédnout, zaskočit, podívat se"}),
    8091: (T + "в примере trojité", {"t_cs": "trojnásobný, trojitý"}),
    8175: (T + "в примере to samé", {"t_cs": "stejný, totéž, to samé"}),
    8254: (T + "в примере věrohodně", {"t_cs": "věrohodný, přesvědčivý, věrohodně"}),
    8267: (T + "в примере nehnout se dál", {"t_cs": "postupovat, pokročit, (nicht vorankommen) nehnout se dál"}),
    8269: (T + "в примере shrbeně", {"t_cs": "shrbený, ohnutý, shrbeně"}),
    8300: (T + "в примере odhánět", {"t_cs": "zahnat, odehnat, odhánět"}),
    8302: (T + "в примере nádherně", {"t_cs": "nádherný, skvostný, nádherně"}),
    8449: (T + "в примере roztroušená skleróza", {"t_cs": "četný, mnohočetný, (multiple Sklerose) roztroušená skleróza"}),
    8497: (T + "в примере podle toho", {"t_cs": "tudíž, odpovídajícím způsobem, podle toho"}),
    8535: (T + "в примере nezadržitelně", {"t_cs": "nezastavitelný, neúprosný, nezadržitelně"}),
    8564: (T + "в примере neslyšně", {"t_cs": "neslyšitelný, neslyšně"}),
    8598: (T + "в примере vkusně", {"t_cs": "vkusný, elegantní, vkusně"}),
    18832: (T + "в примере předčasně", {"t_cs": "předčasný, předčasně"}),
    18843: (T + "в примере ukvapeně", {"t_cs": "ukvapený, unáhlený, ukvapeně"}),
}

REPLACE = []
SPLIT_LATER = {}
