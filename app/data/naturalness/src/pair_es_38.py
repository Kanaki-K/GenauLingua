"""Шаг 2, es, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    7366: (T + "в примере de verdad", {"t_es": "verdaderamente, de verdad"}),
    7663: (T + "в примере en mal momento", {"t_es": "desfavorable, poco oportuno, en mal momento"}),
    7665: (T + "в примере tener piedad", {"t_es": "reinar, (Gnade walten lassen) tener piedad"}),
    7685: (T + "в примере echarse atrás", {"t_es": "la marcha atrás, (einen Rückzieher machen) echarse atrás"}),
    7704: (T + "в примере en último caso", {"t_es": "si hace falta, en último caso"}),
    7731: (T + "está desaparecido desde — неестественно", {"x_es": "El mando lleva desaparecido desde el domingo, y todos juran que no lo tenían"}),
    7737: (T + "в примере venir aquí", {"t_es": "hacia aquí, aquí"}),
    18783: (T + "нет Edad Media; pan de pita — калька", {"x_es": "En la feria de la Edad Media del pueblo los niños comen pan recién hecho y miran a los caballeros"}),
}

REPLACE = []
SPLIT_LATER = {}
