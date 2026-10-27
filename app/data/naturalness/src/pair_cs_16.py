"""Шаг 2, cs, порция 16: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    7725: (T + "в примере rychle", {"t_cs": "rychlý, elegantní, rychle"}),
    7735: (T + "в примере za nic nestojí", {"t_cs": "hodit se, být k něčemu, (nichts taugen) za nic nestát"}),
    8058: (T + "в примере radikálně", {"t_cs": "radikální, zásadní, radikálně"}),
    8115: (T + "в примере paralelně", {"t_cs": "paralelní, souběžný, paralelně"}),
    8245: (T + "в примере napevno", {"t_cs": "napnutý, pevný, napevno"}),
    8316: (T + "в примере nepřímo", {"t_cs": "nepřímý, nepřímo"}),
    8611: (T + "в примере růžově", {"t_cs": "růžový, slibný, růžově"}),
    8671: (T + "в примере rušno", {"t_cs": "rušný, živý, (es ist belebt) je rušno"}),
    8682: (T + "в примере svisle", {"t_cs": "svislý, svisle"}),
    8838: (T + "в примере výbor", {"t_cs": "představenstvo, vedení, (im Verein) výbor"}),
}

REPLACE = []
SPLIT_LATER = {}
