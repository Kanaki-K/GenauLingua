"""Шаг 2, pl, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    7102: (T + "word in example", {"t_pl": "należeć się, zbliżać się, (auf jemanden zukommen) czekać kogoś"}),
    7108: (T + "word in example", {"t_pl": "udzielać, przyznawać, dawać"}),
    7120: (T + "word in example", {"t_pl": "aprobować, pochwalać"}),
    7129: (T + "word in example", {"t_pl": "przebrnąć, dać sobie radę, przetrwać"}),
    7145: (T + "word in example", {"t_pl": "cofać się, ustępować, (nicht von der Seite weichen) nie odstępować"}),
    7176: (T + "word in example", {"t_pl": "powodować, sprawiać, zdziałać"}),
    7189: (T + "word in example", {"t_pl": "skradać się, zakradać się, przemykać"}),
    7206: (T + "word in example", {"t_pl": "wynieść, wypuścić, wydać (płytę)"}),
    7220: (T + "word in example", {"t_pl": "niejasny, (es ist unklar) nie jest jasne"}),
    7227: (T + "word in example", {"t_pl": "minimalny, najmniejszy, (das Mindeste) najmniej"}),
    7258: (T + "word in example", {"t_pl": "wynieść, odnieść, odwieźć"}),
    7278: (T + "word in example", {"t_pl": "pozostawić, zostawić"}),
    7306: (T + "word in example", {"t_pl": "niejasny, mglisty, mgliście"}),
}

REPLACE = []
SPLIT_LATER = {}
