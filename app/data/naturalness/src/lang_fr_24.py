"""Вычитка французского, порция p024 (B1), 23.10: право, власть, транспорт — повторы «prison», «voiture de police», «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    15933: (T + "«Le polar parle d'un meurtre» — учебниково", {"example_fr": "Il y a eu un meurtre dans notre quartier"}),
    15938: (T + "повтор «grand-père dans l'armée» (8744)", {"example_fr": "Mon frère fait son service dans l'armée"}),
    15947: (T + "«J'aime ma liberté» — без ситуации", {"example_fr": "Depuis que j'ai mon permis, j'ai enfin ma liberté"}),
    15950: (T + "нет слова карточки «la taule»", {"example_fr": "Il a fait trois ans de taule"}),
    15951: (T + "«Il me faut une preuve de ça» — коряво", {"example_fr": "Tu as des preuves ?"}),
    15967: (T + "«peut libérer» — калька", {"example_fr": "La police a libéré les otages"}),
    15973: (T + "«Le prisonnier est assis» — учебниково", {"example_fr": "Il a passé la nuit en cellule"}),
    15974: (T + "«défendre mon opinion» — книжно", {"example_fr": "Il défend toujours sa petite sœur"}),
    15985: (T + "«L'empereur a gouverné le pays» — учебниково", {"example_fr": "Napoléon s'est fait couronner empereur"}),
    15988: (T + "«me soupçonnent-ils» — книжно", {"example_fr": "Pourquoi tu me soupçonnes ?"}),
    15993: (T + "«Je suis à disposition» — оборвано", {"example_fr": "Je suis à ta disposition si tu as besoin"}),
    15995: (T + "«Le chien nous attaque» — неживо", {"example_fr": "Le chien des voisins a attaqué notre chat"}),
    15996: (T + "нет слова карточки «le soupçon»", {"example_fr": "J'ai un soupçon, mais pas de preuve"}),
    16009: (T + "«Les témoins doivent témoigner» — тавтология", {"example_fr": "Elle doit témoigner au tribunal la semaine prochaine"}),
    16013: (T + "«l'armée aide» — коряво", {"example_fr": "Après l'inondation, les militaires aident les habitants"}),
    16028: (T + "«L'ancien royaume n'existe plus» — учебниково", {"example_fr": "Dans le conte, tout le royaume est en danger"}),
    16068: (T + "«Nous avons passé» — книжно", {"example_fr": "On a passé un accord sur qui fait quoi"}),
    16086: (T + "«Nous avons eu droit» — книжно", {"example_fr": "À l'hôtel, on a eu droit à un traitement royal"}),
    16099: (T + "«protéger ma vie privée» — калька", {"example_fr": "Je ne poste pas de photos des enfants, c'est leur vie privée"}),
    16101: (T + "повтор 16029 «surveille(nt)»", {"example_fr": "Tu peux garder mes affaires pendant que je nage ?"}),
    16103: (T + "«a été importante pour l'affaire» — книжно", {"example_fr": "L'audition du témoin est prévue demain"}),
    16104: (T + "повтор 16146 «La police a arrêté»", {"example_fr": "On l'a interpellé à la sortie du magasin"}),
    16106: (T + "«Mon quotidien est bien organisé» — книжно", {"example_fr": "Tout est réglé pour le voyage"}),
    16133: (T + "повтор 16152 «le roi … ans»", {"example_fr": "Qui gouverne le pays en ce moment ?"}),
    16134: (T + "повтор 16128 «Il est en prison»", {"example_fr": "Le braquage de la banque a duré dix minutes"}),
    16140: (T + "«Le sceau est important» — коряво", {"example_fr": "La lettre porte le sceau du roi"}),
    16281: (T + "«Votons» — книжно", {"example_fr": "On vote pour savoir où on va ?"}),
    16343: (T + "«un jugement avisé» — книжно", {"example_fr": "La juge a été très sévère avec lui"}),
    16345: (T + "«m'occuper une place» — калька", {"example_fr": "Cette place est occupée ?"}),
    16355: (T + "повтор 16717 «voiture de police devant chez nous»", {"example_fr": "La voiture de police roule avec la sirène allumée"}),
    16702: (T + "повтор 15976 «visite notre école»", {"example_fr": "La ministre de la Santé parle ce soir à la télé"}),
    17057: (T + "повтор 17081 «Nous sommes sur/à bord»", {"example_fr": "Bienvenue à bord !"}),
    17081: (T + "повтор 17057 «Nous sommes … du bateau»", {"example_fr": "Il y a du vent sur le pont, mets une veste"}),
    17090: (T + "«Nous nous sommes perdus» — книжно", {"example_fr": "On s'est complètement perdus en venant"}),
    17094: (T + "«nous dormons» — книжно", {"example_fr": "Ce soir, on dort dans un motel"}),
    17099: (T + "повтор 13462 «À qui est la voiture…»", {"example_fr": "Les véhicules de plus de 3,5 tonnes sont interdits"}),
    17131: (T + "«Nous traversons» — книжно", {"example_fr": "On traverse au feu, pas ailleurs"}),
}

REPLACE = []

SPLIT_LATER = {}
