"""Шаг 2, pl, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    2806: (T + "word in example", {"t_pl": "od tego czasu, od tamtej pory, odkąd"}),
    2812: (T + "word in example", {"t_pl": "obniżać, zmniejszać, (die Stimme senken) ściszyć"}),
    2819: (T + "word in example", {"t_pl": "sensowny, rozsądny, rozsądnie"}),
    2824: (T + "word in example", {"t_pl": "słońce, blask słońca, (czule) słoneczko"}),
    2828: (T + "word in example", {"t_pl": "zmartwienie, troska, (sich Sorgen machen) martwić się"}),
    2876: (T + "word in example", {"t_pl": "zwierzęcy, okropny, okropnie"}),
    2909: (T + "word in example", {"t_pl": "kontakt, obchodzenie się z czymś, obsługa"}),
    2922: (T + "word in example", {"t_pl": "niecierpliwy, zniecierpliwiony, (ungeduldig sein) niecierpliwić się"}),
    2923: (T + "word in example", {"t_pl": "niezdrowy, niezdrowo"}),
    2925: (T + "word in example", {"t_pl": "niepotrzebny, zbędny, niepotrzebnie"}),
    2976: (T + "word in example", {"t_pl": "znosić, tolerować, dogadywać się"}),
}

REPLACE = []
SPLIT_LATER = {}
