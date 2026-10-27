"""Шаг 2, cs, порция 44: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    16603: (T + "в примере být ve vazbě", {"t_cs": "uvěznit, zadržet, (inhaftiert sein) být ve vazbě"}),
    17601: (T + "в примере režie (TV)", {"t_cs": "velín, řídicí místnost, (im Fernsehen) režie"}),
    17828: (T + "в примере úspěšnost", {"t_cs": "kvóta, podíl, (Erfolgsquote) úspěšnost"}),
    17831: (T + "в примере zůstali", {"t_cs": "zbylý, zaostalý, (zurückbleiben) zůstat"}),
}

REPLACE = []
SPLIT_LATER = {}
