"""Вычитка французского, порция p022 (B1), 23.10: речь, культура, семья — повторы, кальки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    14046: (T + "нет слова карточки «aborder»", {"example_fr": "Je vais aborder le sujet avec lui demain"}),
    14061: (T + "«Sincères félicitations pour l'examen réussi» — калька", {"example_fr": "Félicitations pour ton examen !"}),
    14095: (T + "«Nous avons trouvé» — книжно", {"example_fr": "On a enfin trouvé un compromis"}),
    14235: (T + "«Nous l'avons scellé» — книжно", {"example_fr": "On a conclu l'affaire par une poignée de main"}),
    14374: (T + "повтор «se comporte comme» (14794, 14814)", {"example_fr": "Ma fille veut une robe de princesse pour son anniversaire"}),
    14390: (T + "повтор 12141 «ont applaudi fort»", {"example_fr": "À la fin du spectacle, tout le public était debout"}),
    14405: (T + "«Je veux filmer ça» — калька", {"example_fr": "Attends, je filme ça !"}),
    14411: (T + "повтор 14437 «Nous avons visité le vieux…»", {"example_fr": "En Thaïlande, il y a des temples partout"}),
    14437: (T + "повтор 14411 «Nous avons visité le vieux…»", {"example_fr": "Les moines du monastère font leur propre bière"}),
    14418: (T + "«nous répétons» — книжно", {"example_fr": "Ce soir, on répète la pièce de théâtre"}),
    14448: (T + "«château de sable» — не то значение", {"example_fr": "On a visité un château fort du Moyen Âge"}),
    14449: (T + "«Les sons de la musique» — калька", {"example_fr": "J'adore le son de cette vieille guitare"}),
    14451: (T + "«une personne bénie» — калька", {"example_fr": "Avec trois petits-enfants, je suis vraiment comblée"}),
    14466: (T + "«narrateur très talentueux» — не то значение", {"example_fr": "Dans ce livre, le narrateur est un chat"}),
    14469: (T + "нет слова карточки «le tube»", {"example_fr": "Cette chanson est devenue le tube de l'été"}),
    14502: (T + "«faire du ballet» — калька", {"example_fr": "Ma fille fait de la danse classique depuis ses cinq ans"}),
    14937: (T + "«où es-tu» — книжно; повтор 14896", {"example_fr": "Le petit pleure, il veut sa maman"}),
    14942: (T + "«nous allons» — книжно", {"example_fr": "Dimanche, on va sur la tombe de mamie"}),
    14953: (T + "«très importante pour moi» — калька", {"example_fr": "Notre amitié dure depuis l'école primaire"}),
    14976: (T + "«et il est très poli» — тавтология", {"example_fr": "C'est un vrai gentleman, il m'ouvre toujours la porte"}),
    15006: (T + "«Comment est votre relation» — калька", {"example_fr": "J'ai de bons rapports avec mes voisins"}),
    15013: (T + "«Nous sommes apparentés» — книжно", {"example_fr": "On est apparentés, mais de loin"}),
    15016: (T + "«Nous passons» — книжно", {"example_fr": "On part en lune de miel à Hawaï"}),
    15034: (T + "«L'évêque a visité l'église» — учебниково", {"example_fr": "L'évêque vient bénir la nouvelle église"}),
}

REPLACE = []

SPLIT_LATER = {}
