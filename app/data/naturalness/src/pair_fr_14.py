"""Шаг 2, fr, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    6383: (T + "в примере il reste", {"t_fr": "restant, en trop, (übrig sein) rester"}),
    6418: (T + "в примере ne pas y croire", {"t_fr": "concevoir, saisir, (es nicht fassen können) ne pas y croire"}),
    6486: (T + "в примере veiller", {"t_fr": "monter la garde, surveiller, veiller"}),
    6583: (T + "в примере mutuellement", {"t_fr": "réciproque, mutuel, mutuellement"}),
    6600: (T + "в примере chacun de son côté", {"t_fr": "séparément, en morceaux, chacun de son côté"}),
    6621: (T + "в примере la moindre", {"t_fr": "quelque, n'importe, (irgendeine Ahnung) la moindre"}),
    6687: (T + "в примере en apparence", {"t_fr": "apparemment, en apparence"}),
    6761: (T + "в примере impliqué", {"t_fr": "mêlé, compliqué, impliqué"}),
    6784: (T + "в примере mettre en service", {"t_fr": "employer, utiliser, mettre en service"}),
    6813: (T + "в примере transférer", {"t_fr": "retransmettre, transmettre, transférer"}),
}

REPLACE = []
SPLIT_LATER = {}
