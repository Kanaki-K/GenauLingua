"""Шаг 2, pl, порция 44: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    16603: (T + "word in example", {"t_pl": "uwięzić, osadzić w areszcie, przetrzymywać w areszcie"}),
    17218: (T + "word in example", {"t_pl": "zamorskie kraje, zagranica za oceanem, (aus Übersee) zza oceanu"}),
    17830: (T + "word in example", {"t_pl": "ruina, upadek, (in den Ruin treiben) zrujnować"}),
    17831: (T + "word in example", {"t_pl": "pozostały, opóźniony, (zurückgeblieben sein) zostać"}),
    17845: (T + "word in example", {"t_pl": "wynegocjować, wytargować, negocjować"}),
}

REPLACE = []
SPLIT_LATER = {}
