"""Шаг 2, pl, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    10536: (T + "word in example", {"t_pl": "litość, zmiłowanie, (Erbarmen haben) zlitować się"}),
    10602: (T + "word in example", {"t_pl": "opanowanie, wersja, (aus der Fassung bringen) wyprowadzić z równowagi"}),
    10606: (T + "word in example", {"t_pl": "lękliwy, strasznie, (bange sein) mieć stracha"}),
    10622: (T + "word in example", {"t_pl": "wariować, zwariować, świrować"}),
    10633: (T + "word in example", {"t_pl": "spokojny, spokojnie, bez obaw"}),
    10645: (T + "word in example", {"t_pl": "nudny, pusty, pusto"}),
    10661: (T + "word in example", {"t_pl": "nieruchomy, nieruchomo, sztywny"}),
    10672: (T + "word in example", {"t_pl": "niemądry, niemądrze, nierozsądny"}),
    10684: (T + "word in example", {"t_pl": "kuszący, kusząco"}),
    10692: (T + "word in example", {"t_pl": "robić w pośpiechu, działać pochopnie, (sich überstürzen) śpieszyć się"}),
    10734: (T + "word in example", {"t_pl": "troskliwy, troskliwie, czuły"}),
    10739: (T + "word in example", {"t_pl": "uprzejmy, uprzejmie, miły"}),
    10740: (T + "word in example", {"t_pl": "tajemniczy, tajemniczo"}),
    10746: (T + "word in example", {"t_pl": "oryginalny, oryginalnie, pomysłowy"}),
}

REPLACE = []
SPLIT_LATER = {}
