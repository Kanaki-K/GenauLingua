"""Шаг 2, cs, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    2153: (T + "в примере pestře", {"t_cs": "rozmanitý, pestrý, pestře"}),
    2217: (T + "в примере pozorně", {"t_cs": "pozorný, ohleduplný, pozorně"}),
    2254: (T + "в примере nadšený", {"t_cs": "nadchnout, uchvátit, (begeistert sein) být nadšený"}),
    2298: (T + "в примере být si vědom", {"t_cs": "vědomý, úmyslný, (sich bewusst sein) být si vědom"}),
    2303: (T + "в примере ekologicky", {"t_cs": "biologický, ekologický, ekologicky"}),
    2337: (T + "в примере demokraticky", {"t_cs": "demokratický, demokraticky"}),
    2353: (T + "в примере dvojnásobek", {"t_cs": "dvojnásobný, dvojitý, (das Doppelte) dvojnásobek"}),
    2371: (T + "в примере samostatně", {"t_cs": "samostatný, odpovědný, samostatně"}),
    2394: (T + "в примере přistěhování", {"t_cs": "přistěhovalectví, přistěhování"}),
}

REPLACE = []
SPLIT_LATER = {}
