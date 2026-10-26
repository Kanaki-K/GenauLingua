"""Шаг 2, pl, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    1794: (T + "word in example", {"t_pl": "mnóstwo, obfity, aż nadto"}),
    1827: (T + "word in example", {"t_pl": "elegancki, szykowny, elegancko"}),
    1877: (T + "word in example", {"t_pl": "staranny, dokładny, starannie"}),
    1886: (T + "word in example", {"t_pl": "specjalny, szczególny, osobliwy"}),
    1915: (T + "word in example", {"t_pl": "awaria, przeszkadzanie, (Entschuldigung für die Störung) przepraszam, że przeszkadzam"}),
    1968: (T + "word in example", {"t_pl": "oddzielać, rozstawać się, (Müll trennen) segregować śmieci"}),
    2049: (T + "word in example", {"t_pl": "szalony, zwariowany, (verrückt sein) zwariować"}),
    2145: (T + "word in example", {"t_pl": "odmowa, odwołanie, (eine Absage geben) odmówić"}),
}

REPLACE = []
SPLIT_LATER = {}
