"""Шаг 2, fr, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    15591: (T + "калька идиомы про воробьёв", {"x_fr": "Les moineaux se disputent les miettes sur la terrasse du café"}),
    16151: (T + "в примере se réfugier", {"t_fr": "fuir, s'enfuir, se réfugier"}),
    16157: (T + "в примере enquête, нет sondage", {"x_fr": "Lors du sondage dans la rue, ils voulaient savoir combien de fois je prends le bus"}),
    16190: (T + "в примере mal entendre", {"t_fr": "interroger, (sich verhören) mal entendre"}),
    16236: (T + "в примере cacher", {"t_fr": "étouffer, dissimuler, cacher"}),
}

REPLACE = []
SPLIT_LATER = {}
