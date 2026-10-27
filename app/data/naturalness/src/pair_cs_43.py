"""Шаг 2, cs, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    15595: (T + "в примере vymřelá", {"t_cs": "vyhynulý, liduprázdný, vymřelý"}),
    15648: (T + "в примере глагол zamrzlo", {"t_cs": "zamrzlý, zmrazený, (zufrieren) zamrznout"}),
    16422: (T + "в примере obležení", {"t_cs": "obléhání, obležení"}),
    16425: (T + "в примере civilizovaně", {"t_cs": "civilizovaný, kultivovaný, civilizovaně"}),
    16552: (T + "в примере křivě přísahá", {"t_cs": "křivá přísaha, (einen Meineid schwören) křivě přísahat"}),
}

REPLACE = []
SPLIT_LATER = {}
