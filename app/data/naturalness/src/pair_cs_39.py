"""Шаг 2, cs, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    7819: (T + "в примере nemyslitelná", {"t_cs": "myslitelný, možný, (undenkbar) nemyslitelný"}),
    7851: (T + "в примере jednomyslně", {"t_cs": "jednomyslný, jednomyslně"}),
    7898: (T + "в примере přiřízl", {"t_cs": "uříznout, přeseknout, přiříznout"}),
    7944: (T + "в примере nepřirozeně", {"t_cs": "nepřirozený, strojený, nepřirozeně"}),
    7965: (T + "в примере konstantně", {"t_cs": "konstantní, stálý, konstantně"}),
    8006: (T + "в примере omezeně", {"t_cs": "omezený, podmíněný, omezeně"}),
    8017: (T + "в примере bezvadně", {"t_cs": "bezvadný, bezchybný, bezvadně"}),
    8038: (T + "в примере trhaně", {"t_cs": "trhaný, přerývaný, trhaně"}),
}

REPLACE = []
SPLIT_LATER = {}
