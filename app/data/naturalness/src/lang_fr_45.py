"""Вычитка французского, порция p045 (C1/C2), 23.10: «nous» → «on», «réfrigérateur» → «frigo», кальки"""

T = "вычитка французского: "

FIXES = {
    18939: (T + "«réfrigérateur» — книжно", {"example_fr": "Après cela, la pâte repose une heure au frigo"}),
    8124: (T + "«nous faisons» — книжно", {"example_fr": "Demain, on fait mesurer le terrain"}),
    8286: (T + "«aidé volontiers» — калька", {"example_fr": "Il m'a aidé de bon cœur"}),
    8359: (T + "повтор 10364 «résister au chocolat»", {"example_fr": "Il a fini par succomber à la tentation"}),
    8393: (T + "нет слова карточки «obligatoire»", {"example_fr": "La présence n'est pas obligatoire"}),
    8457: (T + "«Dissipons» — книжно", {"example_fr": "Il faut dissiper ce malentendu avant l'arrivée des invités"}),
    8487: (T + "«Tu dois vraiment» — калька", {"example_fr": "Arrête de fouiner dans mes affaires !"}),
    8498: (T + "«Fixons … notre rencontre» — книжно", {"example_fr": "On fixe une date ?"}),
    8501: (T + "«que nous nous soyons retrouvés» — книжно", {"example_fr": "C'est un heureux hasard qu'on se soit retrouvés"}),
    8568: (T + "«Nous avons besoin» — книжно", {"example_fr": "Il nous faut une aide extérieure pour régler ce problème"}),
    8572: (T + "«Nous devons» — книжно", {"example_fr": "Il faut modifier le plan pour le rendre plus réaliste"}),
}

REPLACE = []

SPLIT_LATER = {}
