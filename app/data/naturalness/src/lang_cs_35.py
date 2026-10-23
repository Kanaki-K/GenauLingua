"""Вычитка чешского, порция p035 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    15253: (T + "«Moje svědkyně» — книжно", {"example_cs": "Svědkyně zapomněla na úřadě prstýnky, tak jsme vzali dva gumové medvídky"}),
    15313: (T + "«Moje sestra» — книжно", {"example_cs": "Sestra je hnědovlasá, já jsem blond"}),
    15316: (T + "«se svým nenarozeným dítětem» — тяжело", {"example_cs": "Sestra každý večer mluví s nenarozeným miminkem a pouští mu hudbu"}),
    15545: (T + "«velmi» — книжно", {"example_cs": "Býk na pastvině vypadá hodně divoce"}),
    15570: (T + "«sladký tvor» — калька", {"example_cs": "Naše nové koťátko je takový malý, roztomilý tvoreček"}),
    15588: (T + "«velmi» — книжно", {"example_cs": "Na téhle pláži je koupání zakázané, protože proud je hodně nebezpečný"}),
    16150: (T + "«Ty táhneš chlast» — коряво", {"example_cs": "Táhne z tebe chlast! Kolik jsi vypil?"}),
    16188: (T + "«Můj děda» — книжно", {"example_cs": "Děda sloužil dva roky v armádě a pořád o tom vypráví"}),
    16199: (T + "«mnoho» — книжно", {"example_cs": "Iniciativa proti dětské práci získala spoustu příznivců"}),
    16203: (T + "«velmi» — книжно", {"example_cs": "Vyšetřovatel ten případ hodně důkladně zkoumá"}),
    16205: (T + "«Moje studium» — калька", {"example_cs": "Studium mi zaplatila nadace, jinak bych si ho nemohl dovolit"}),
    16206: (T + "«velmi» — книжно", {"example_cs": "Trest za jeho špatné chování byl hodně přísný"}),
    16210: (T + "«mnoho» — книжно", {"example_cs": "Ve Velké Británii je spousta policistů na ulici neozbrojených"}),
    16225: (T + "«Můj malý bratr» — книжно", {"example_cs": "Malý brácha si nejradši hraje na policajta a banditu, a vždycky je bandita on"}),
    16240: (T + "«velmi» — книжно", {"example_cs": "Římská říše byla hodně mocná"}),
    16246: (T + "«Můj strýc» — книжно", {"example_cs": "Strýc pracuje třicet let v justici, nejdřív jako soudce, teď jako státní zástupce"}),
    16253: (T + "слово карточки «loupežné přepadení»", {"example_cs": "V bance došlo k loupežnému přepadení"}),
    16258: (T + "«Můj praděda» — книжно", {"example_cs": "Praděda sloužil ve stejném pluku jako jeho otec"}),
}

REPLACE = []

SPLIT_LATER = {}
