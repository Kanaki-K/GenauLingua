"""Шаг 2, cs, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    1772: (T + "в примере profesionálně", {"t_cs": "profesionální, profesionálně"}),
    1789: (T + "в примере zpravidla", {"t_cs": "pravidlo, (in der Regel) zpravidla"}),
    1811: (T + "в примере rytmicky", {"t_cs": "rytmický, rytmicky"}),
    1827: (T + "в примере elegantně", {"t_cs": "elegantní, elegantně, šik (hovor.)"}),
    1877: (T + "в примере pečlivě", {"t_cs": "pečlivý, důkladný, pečlivě"}),
    1915: (T + "в примере že ruším", {"t_cs": "porucha, rušení, (Entschuldigen Sie die Störung) promiňte, že ruším"}),
    1949: (T + "в примере teoreticky", {"t_cs": "teorie, (in der Theorie) teoreticky"}),
    1967: (T + "в примере sportuju", {"t_cs": "dělat, hnát, (Sport treiben) sportovat"}),
    2049: (T + "в примере zbláznil ses", {"t_cs": "šílený, bláznivý, (verrückt sein) zbláznit se"}),
    2145: (T + "в примере глагол zrušit", {"t_cs": "odmítnutí, zrušení, (absagen) zrušit"}),
}

REPLACE = []
SPLIT_LATER = {}
