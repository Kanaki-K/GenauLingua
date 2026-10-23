"""Вычитка французского, порция p018 (B1), 23.10: чувства и характер — кальки, повторы, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    10035: (T + "«que diable fais-tu là» — книжно", {"example_fr": "Il fait un froid du diable aujourd'hui"}),
    10054: (T + "«Je vais seul» — порядок слов", {"example_fr": "Je vais au cinéma tout seul"}),
    10112: (T + "«Tu en es responsable» — книжно", {"example_fr": "C'est toi le responsable"}),
    10150: (T + "«réclame vengeance pour tout» — коряво", {"example_fr": "Il ne pense qu'à la vengeance"}),
    10152: (T + "«complètement en désordre» — без ситуации", {"example_fr": "Après la fête, tout l'appartement est en désordre"}),
    10184: (T + "«Je peux sentir» — калька", {"example_fr": "Tu sens ce courant d'air ?"}),
    10190: (T + "«Nous prions» — книжно", {"example_fr": "Ma grand-mère prie tous les soirs"}),
    10208: (T + "«ma plus grande force» — калька", {"example_fr": "La cuisine, c'est mon point fort"}),
    10215: (T + "«La perte me rend triste» — калька", {"example_fr": "La perte de son chien l'a beaucoup touchée"}),
    10218: (T + "«Tu dois mieux te comporter» — калька", {"example_fr": "Tiens-toi bien chez mamie, d'accord ?"}),
    10220: (T + "«L'enfant est» — учебниково", {"example_fr": "Le petit a été très sage aujourd'hui"}),
    10230: (T + "нет слова карточки «habituel»", {"example_fr": "On se retrouve à l'heure habituelle, devant le café ?"}),
    10241: (T + "«courageusement sauté» — коряво", {"example_fr": "Les enfants ont été courageux chez le dentiste"}),
    10256: (T + "«Moi, l'idiot» — калька", {"example_fr": "Et moi, comme un idiot, j'ai laissé la lumière allumée"}),
    10267: (T + "нет слова карточки «point faible»", {"example_fr": "Le chocolat, c'est mon point faible"}),
    10285: (T + "«Quel était ton motif» — без ситуации", {"example_fr": "La police cherche encore le mobile du crime"}),
    10288: (T + "повтор 10164 «gênant pour moi»", {"example_fr": "Le bruit de la perceuse est très désagréable"}),
    10296: (T + "повтор 10098 «contre ma volonté»", {"example_fr": "Avec un peu de volonté, tu vas y arriver"}),
    10298: (T + "«vision claire de ma vie» — калька", {"example_fr": "La nouvelle directrice a une vision claire pour l'entreprise"}),
    10318: (T + "«Partageons» — книжно", {"example_fr": "On partage le gâteau de façon équitable"}),
    10321: (T + "«Tu voulais me faire peur» — неживо", {"example_fr": "Tu m'as fait peur !"}),
    10335: (T + "«sent dégoûtant» — калька", {"example_fr": "Il y a une odeur dégoûtante dans le frigo"}),
    10338: (T + "повтор 10295 «c'est dégoûtant»", {"example_fr": "Beurk, elle est dégueulasse, cette soupe !"}),
    10341: (T + "«Nous devons» — книжно", {"example_fr": "Il faut respecter sa décision"}),
    10342: (T + "«nous avons gagné» — книжно", {"example_fr": "Hourra, on a gagné !"}),
    10347: (T + "«C'est vraiment la racaille» — коряво", {"example_fr": "Ces types, c'est de la racaille"}),
    10349: (T + "нет слова карточки «uni»", {"example_fr": "Après la dispute, la famille est de nouveau unie"}),
    10356: (T + "«Avec de la nourriture, tu» — коряво", {"example_fr": "Avec un peu de jambon, on attire le chat dans la maison"}),
    10371: (T + "«contre le harcèlement» — книжно", {"example_fr": "Il faut te défendre, ne te laisse pas faire"}),
    10372: (T + "«Rien ne m'effraie si facilement» — коряво", {"example_fr": "Les orages effraient beaucoup mon chien"}),
    10373: (T + "«l'aide face aux problèmes» — книжно", {"example_fr": "Son intelligence impressionne tous ses professeurs"}),
    10404: (T + "учебниково", {"example_fr": "Sans discipline, on n'arrive à rien"}),
    10405: (T + "«de façon très concentrée» — калька", {"example_fr": "Ne le dérange pas, il est très concentré"}),
    10406: (T + "«attitude face au travail» — книжно", {"example_fr": "Elle a toujours une attitude positive"}),
    10409: (T + "повтор 10179 «jalouse de sa sœur»", {"example_fr": "Il est un peu envieux de ma nouvelle voiture"}),
}

REPLACE = []

SPLIT_LATER = {}
