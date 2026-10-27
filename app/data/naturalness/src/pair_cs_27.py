"""Шаг 2, cs, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    7102: (T + "в примере čeká nás", {"t_cs": "náležet, přiblížit se, (auf jdn. zukommen) čekat koho"}),
    7105: (T + "в примере прилагательное nenápadné", {"t_cs": "nenápadně, nenápadný"}),
    7129: (T + "в примере vyjít (s penězi)", {"t_cs": "projít, zvládnout, (mit Geld) vyjít"}),
    7145: (T + "в примере nehnout se od", {"t_cs": "ustupovat, couvat, (nicht von der Seite weichen) nehnout se od"}),
    7171: (T + "в примере nádherně", {"t_cs": "nádherný, skvostný, nádherně"}),
    7176: (T + "в примере dokázat zázraky", {"t_cs": "způsobit, docílit, (Wunder bewirken) dokázat zázraky"}),
    7232: (T + "в примере přesně", {"t_cs": "přesný, přesně"}),
    7307: (T + "в примере identicky", {"t_cs": "totožný, identický, identicky"}),
    7371: (T + "в примере bezdůvodně", {"t_cs": "bezdůvodný, bezdůvodně"}),
    7386: (T + "в примере neslyšně", {"t_cs": "neslyšný, tichý, neslyšně"}),
    7390: (T + "в примере skoro, не téměř", {"x_cs": "Téměř všechny moje kamarádky už mají děti"}),
}

REPLACE = []
SPLIT_LATER = {}
