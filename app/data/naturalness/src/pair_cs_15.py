"""Шаг 2, cs, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    6841: (T + "в примере báječně", {"t_cs": "báječný, skvělý, báječně"}),
    6842: (T + "в примере důkladně", {"t_cs": "důkladný, pečlivý, důkladně"}),
    6848: (T + "в примере jemně", {"t_cs": "jemný, něžný, jemně"}),
    6855: (T + "в примере udělat chybu, не spáchat", {"t_cs": "spáchat, oslavit, (einen Fehler begehen) dopustit se chyby", "x_cs": "Dopustil jsem se velké chyby a musím se omluvit"}),
    6882: (T + "в примере mezi tím", {"t_cs": "mezitím, mezi tím, uprostřed"}),
    6898: (T + "в примере udělat si čas", {"t_cs": "opatřit, zajistit, (sich Zeit verschaffen) udělat si čas"}),
    6954: (T + "в примере vzít si zpátky", {"t_cs": "vrátit, přinést zpátky, vzít si zpátky"}),
    7001: (T + "в примере v úzkých", {"t_cs": "kaše, svorka, (in der Klemme sein) být v úzkých"}),
    7005: (T + "в примере přibližně", {"t_cs": "hrubý, přibližný, přibližně"}),
    7023: (T + "в примере silně", {"t_cs": "silný, výrazný, silně"}),
    7072: (T + "в примере vyčmuchá", {"t_cs": "vypátrat, vystopovat, vyčmuchat"}),
    7076: (T + "в примере šikmá", {"t_cs": "nakřivo, šikmý, divný"}),
    7078: (T + "в примере глагол zrušit", {"t_cs": "zrušený, vrácený zpět, (rückgängig machen) zrušit"}),
    7140: (T + "в примере kroutit hlavou", {"t_cs": "třást, potřást, (den Kopf schütteln) kroutit hlavou"}),
    7214: (T + "в примере relativně", {"t_cs": "poměrně, relativní, relativně"}),
    7291: (T + "в примере jednotlivě", {"t_cs": "jednotlivý, samostatný, jednotlivě"}),
    7315: (T + "в примере obecně", {"t_cs": "všeobecný, obecný, obecně"}),
    7456: (T + "в примере neoficiálně", {"t_cs": "neoficiální, neoficiálně"}),
    7461: (T + "в примере sekvence", {"t_cs": "sled, pořadí, sekvence"}),
    7573: (T + "в примере upraveně", {"t_cs": "udržovaný, upravený, upraveně"}),
    7594: (T + "в примере barevně", {"t_cs": "barevný, pestrý, barevně"}),
    7696: (T + "в примере křivě", {"t_cs": "křivý, zahnutý, křivě"}),
}

REPLACE = []
SPLIT_LATER = {}
