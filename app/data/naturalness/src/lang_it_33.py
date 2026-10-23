"""Вычитка итальянского, порция p033 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    12947: (T + '«Il bambino è sanissimo» — учебниково', {"example_it": 'Il medico dice che il piccolo è sanissimo'}),
    13519: (T + "повтор 13552 «un'ora e mezza»", {"example_it": "Il film dura un'ora e mezza"}),
    13520: (T + '«Andiamo verso sud» — учебниково', {"example_it": 'In autunno gli uccelli volano verso sud'}),
    13682: (T + '«perché fa freddo» — учебниково', {"example_it": 'Prendi un maglione, la sera fa fresco'}),
    13777: (T + 'повтор 13719 «pigiama tutta la domenica»', {"example_it": 'Puoi tenere addosso il cappotto, qui fa freddo'}),
    14010: (T + 'повтор 13979 «Non mentirmi»', {"example_it": 'Mente a tutti, persino a sua madre'}),
    14020: (T + 'повтор «è rimasta della torta» (6383)', {"example_it": 'Puoi tenere i soldi rimasti'}),
    14060: (T + 'повтор 14055 «avvisami quando arriva»', {"example_it": "Bisogna avvisare la famiglia dell'incidente"}),
    14078: (T + 'повтор 10161 «maledetto computer»', {"example_it": 'Questo maledetto autobus è di nuovo in ritardo'}),
}

REPLACE = []

SPLIT_LATER = {}
