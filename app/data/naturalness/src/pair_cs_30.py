"""Шаг 2, cs, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    10472: (T + "в примере tlačit na koho", {"t_cs": "naléhat, pobízet, tlačit (na koho)"}),
    10481: (T + "в примере blazeovaně", {"t_cs": "blazeovaný, povýšený, blazeovaně"}),
    10543: (T + "в примере sklíčeně", {"t_cs": "sklíčený, sklíčeně"}),
    10581: (T + "в примере padouch, не lump", {"x_cs": "Ten lump mi prostě vyfoukl parkovací místo!"}),
    10594: (T + "в примере sklíčeně", {"t_cs": "sklíčený, sklíčeně"}),
    10640: (T + "в примере vyděšeně", {"t_cs": "vyděšený, polekaný, vyděšeně"}),
    10660: (T + "в примере rozjařeně", {"t_cs": "rozjařený, rozdováděný, rozjařeně"}),
    10661: (T + "в примере strnule", {"t_cs": "strnulý, ztuhlý, strnule"}),
    10684: (T + "в примере lákavě", {"t_cs": "lákavý, lákavě"}),
    10686: (T + "в примере nerušeně", {"t_cs": "nerušený, v klidu, nerušeně"}),
    10710: (T + "в примере zahanbeně", {"t_cs": "zahanbený, zahanbeně"}),
    10734: (T + "в примере láskyplně", {"t_cs": "láskyplný, láskyplně"}),
    10739: (T + "вежливое Vás с большой буквы", {"x_cs": "To je od Vás velmi laskavé, že mi pomáháte s kufrem"}),
    10740: (T + "в примере tajemně", {"t_cs": "tajemný, záhadný, tajemně"}),
}

REPLACE = []
SPLIT_LATER = {}
