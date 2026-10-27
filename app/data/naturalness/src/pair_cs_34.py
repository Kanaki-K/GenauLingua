"""Шаг 2, cs, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    14539: (T + "в примере papír, не rukopis", {"x_cs": "Bez rukopisu nedokážu mít projev, jinak všechno zapomenu"}),
    14542: (T + "в примере očarovat", {"t_cs": "kouzlo, klatba, (in seinen Bann ziehen) očarovat"}),
    15091: (T + "в примере mladistvě", {"t_cs": "mladistvý, mladistvě"}),
    15101: (T + "в примере seznámit se", {"t_cs": "známost, seznámení, (Bekanntschaft machen) seznámit se"}),
    15114: (T + "в примере osiřet", {"t_cs": "sirotek, (Waise werden) osiřet"}),
}

REPLACE = []
SPLIT_LATER = {}
