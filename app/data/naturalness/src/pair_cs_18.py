"""Шаг 2, cs, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    10048: (T + "в примере upřímně", {"t_cs": "upřímný, poctivý, upřímně"}),
    10197: (T + "вежливое Vás с большой буквы", {"x_cs": "Jsem velmi rád, že Vás poznávám"}),
    10230: (T + "в примере obvykle", {"t_cs": "zvyklý, obvyklý, (wie gewohnt) jako obvykle"}),
    10247: (T + "в примере strašidelně", {"t_cs": "strašidelný, strašně, strašidelně"}),
    10294: (T + "в примере mýlíš se", {"t_cs": "omyl, chyba, (im Irrtum sein) mýlit se"}),
    10318: (T + "в примере spravedlivě", {"t_cs": "spravedlivý, spravedlivě"}),
    10326: (T + "в примере pořádně", {"t_cs": "slušný, pořádný, pořádně"}),
    10335: (T + "в примере odporně", {"t_cs": "odporný, hnusný, odporně"}),
    10343: (T + "mít úlevu — неестественно", {"x_cs": "S úlevou vidím, že všechno dobře dopadlo"}),
    10349: (T + "в примере spojená", {"t_cs": "sjednocený, jednotný, spojený"}),
    10361: (T + "вежливое Vám с большой буквы", {"x_cs": "Mohu Vám být nápomocný?"}),
    10382: (T + "в примере temno", {"t_cs": "temný, ponurý, (es ist düster) je temno"}),
    10415: (T + "в примере uboze", {"t_cs": "ubohý, mizerný, uboze"}),
}

REPLACE = []
SPLIT_LATER = {}
