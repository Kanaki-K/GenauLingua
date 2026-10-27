"""Шаг 2, cs, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    163: (T + "в примере poděkování", {"t_cs": "dík, vděk, poděkování"}),
    195: (T + "в примере нет ty", {"x_cs": "A ty? Půjdeš dnes večer s námi?"}),
    196: (T + "в примере stmívá se", {"t_cs": "tmavý, (es wird dunkel) stmívá se"}),
    203: (T + "в примере vajíčko", {"t_cs": "vejce, vajíčko"}),
    250: (T + "в примере наречие špatně", {"t_cs": "špatný, chybný, špatně"}),
    310: (T + "в примере podáš, не dát", {"x_cs": "Dáš mi vodu?"}),
    363: (T + "в примере глагол platí", {"x_cs": "Je tahle jízdenka ještě platná?"}),
    384: (T + "в примере только úkoly", {"x_cs": "Už máš hotové domácí úkoly?"}),
    428: (T + "в примере возвратное svými", {"t_cs": "její, jejich, (auf das Subjekt bezogen) svůj"}),
    456: (T + "в примере kafe", {"t_cs": "káva, kafe"}),
}

REPLACE = []
SPLIT_LATER = {}
