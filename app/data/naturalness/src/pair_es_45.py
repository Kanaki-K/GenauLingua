"""Шаг 2, es, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    8198: (T + "в примере un misterio", {"t_es": "misterioso, enigmático, un misterio"}),
    8470: (T + "в примере rapidísimo", {"t_es": "rápidamente, vertiginosamente, rapidísimo"}),
    8471: (T + "aprovecha … en su provecho — тавтология", {"x_es": "Usa la situación en su provecho para ganar más dinero"}),
    8553: (T + "в примере tiran", {"t_es": "lanzar (fuegos), tirar, quemarse"}),
    8564: (T + "нет inaudible", {"x_es": "Mi gata se acerca de forma casi inaudible y me salta al regazo"}),
    8579: (T + "нет bloquear", {"x_es": "Después de la tormenta un árbol caído bloquea la calle"}),
    8582: (T + "в примере plagado", {"t_es": "estar lleno de, bullir, estar plagado de"}),
    18817: (T + "в примере en una hora", {"t_es": "en el plazo de, dentro de, en"}),
    18826: (T + "в примере retrasarse", {"t_es": "la demora, (in Verzug sein) retrasarse"}),
}

REPLACE = []
SPLIT_LATER = {}
