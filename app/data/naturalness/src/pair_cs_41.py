"""Шаг 2, cs, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    11056: (T + "в примере nestydatě", {"t_cs": "nestydatý, drzý, nestydatě"}),
    11071: (T + "в примере lehkomyslně", {"t_cs": "lehkomyslný, nerozvážný, lehkomyslně"}),
    11077: (T + "в примере о вине — sladký", {"t_cs": "líbezný, půvabný, (Wein) sladký"}),
    11079: (T + "в примере sebejistě", {"t_cs": "sebejistý, sebejistě"}),
    11080: (T + "в примере sebevědomě", {"t_cs": "sebevědomý, sebevědomě"}),
    11099: (T + "в примере nečinně", {"t_cs": "nečinný, se založenýma rukama, nečinně"}),
    11105: (T + "в примере nesobecky", {"t_cs": "nesobecký, obětavý, nesobecky"}),
    11147: (T + "в примере horlivě", {"t_cs": "horlivý, pilný, horlivě"}),
    11150: (T + "в примере povýšeně", {"t_cs": "povýšený, blahosklonný, povýšeně"}),
    11162: (T + "в примере nejbolestněji", {"t_cs": "bolestný, trpký, bolestně"}),
    11163: (T + "в примере instinktivně", {"t_cs": "instinktivní, bezděčný, instinktivně"}),
    11164: (T + "в примере hrdinsky", {"t_cs": "hrdinský, hrdinný, hrdinsky"}),
    11166: (T + "в примере věrohodně", {"t_cs": "věrohodný, přesvědčivý, věrohodně"}),
    11168: (T + "в примере necitlivě", {"t_cs": "necitlivý, netaktní, necitlivě"}),
    11172: (T + "в примере stylově", {"t_cs": "stylový, vkusný, stylově"}),
    11176: (T + "в примере děsivě", {"t_cs": "děsivý, hrůzostrašný, děsivě"}),
    11260: (T + "в примере bezbranně", {"t_cs": "bezbranný, bezbranně"}),
    11358: (T + "в примере půvabně", {"t_cs": "půvabný, ladný, půvabně"}),
    12252: (T + "в примере autodráha", {"t_cs": "závodiště, (Spielzeug) autodráha"}),
    12755: (T + "в примере fyzicky", {"t_cs": "fyzický, fyzicky"}),
    12809: (T + "в примере leukemie, в переводе leukémie", {"x_cs": "Na školním charitativním běhu sbírají děti peníze pro oddělení nemocnice, kde léčí leukémii"}),
}

REPLACE = []
SPLIT_LATER = {}
