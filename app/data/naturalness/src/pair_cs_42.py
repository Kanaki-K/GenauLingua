"""Шаг 2, cs, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    12820: (T + "в примере křečovitě", {"t_cs": "křečovitý, ztuhlý, křečovitě"}),
    12882: (T + "в примере о собаке — z tlamy", {"t_cs": "zápach z úst, (bei Tieren) zápach z tlamy"}),
    12901: (T + "в примере mořská nemoc", {"t_cs": "trpící mořskou nemocí, (seekrank werden) dostat mořskou nemoc"}),
    12906: (T + "в примере onemocněla", {"t_cs": "nemocný, onemocnělý, (erkranken) onemocnět"}),
    12909: (T + "в примере psychicky", {"t_cs": "psychický, duševní, psychicky"}),
    13567: (T + "в примере leckdo", {"t_cs": "leckterý, některý, (manch einer) leckdo"}),
    13584: (T + "в примере na neurčito", {"t_cs": "neurčitý, (auf unbestimmte Zeit) na neurčito"}),
    13750: (T + "в примере oblečený", {"t_cs": "oblékat, zastávat (úřad), (bekleidet) oblečený"}),
    14121: (T + "в примере nezřetelně", {"t_cs": "nezřetelný, nejasný, nezřetelně"}),
    14162: (T + "в примере hebrejsky", {"t_cs": "hebrejský, hebrejština, hebrejsky"}),
    14603: (T + "в примере slavnostně", {"t_cs": "slavnostní, slavnostně"}),
    14658: (T + "в примере poeticky", {"t_cs": "poetický, básnický, poeticky"}),
}

REPLACE = []
SPLIT_LATER = {}
