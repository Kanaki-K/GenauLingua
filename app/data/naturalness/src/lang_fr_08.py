"""Вычитка французского, порция p008 (B1), 23.10: «nous» → «on», нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    772: (T + "нет слова карточки «vider»", {"example_fr": "On doit vider l'appartement d'ici vendredi"}),
    862: (T + "«émoussé» — книжно", {"example_fr": "Mon crayon est usé, tu as un taille-crayon ?"}),
    969: (T + "нет слова карточки «la visite médicale»", {"example_fr": "La visite médicale n'a duré que dix minutes"}),
    1192: (T + "«Le temps n'est pas suffisant» — калька", {"example_fr": "Je n'ai pas suffisamment de temps pour cette tâche"}),
    1230: (T + "«Le serveur nous sert bien» — коряво", {"example_fr": "On est bien servis ici"}),
    1249: (T + "«Nous te fournissons» — книжно", {"example_fr": "On te fournit tout le matériel nécessaire"}),
    1263: (T + "«nous» → «on»", {"example_fr": "On en discute demain"}),
    1323: (T + "нет слова карточки «le pouce»", {"example_fr": "Il s'est coincé le pouce dans la porte"}),
    1347: (T + "нет слова карточки «le couple marié»", {"example_fr": "À côté de chez nous habite un vieux couple marié"}),
}

REPLACE = []

SPLIT_LATER = {}
