"""Вычитка чешского, порция p037 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    17305: (T + "«Můj zpáteční let odlétá» — калька", {"example_cs": "Zpáteční let mám příští úterý ve 14 hodin"}),
    17313: (T + "«Na mém starém mopedu» — калька", {"example_cs": "Na starém mopedu mám zase ucpaný karburátor"}),
    17326: (T + "«Moje kóje» — калька", {"example_cs": "Kóje na lodi je hodně malá, ale útulná"}),
    17349: (T + "«Moje němčina byla» — калька", {"example_cs": "Němčinu jsem měl zpočátku tak kostrbatou, že mi pekař vždycky odpovídal anglicky"}),
    17536: (T + "«této» — книжно", {"example_cs": "Frekvence téhle rozhlasové stanice je 88 megahertzů"}),
    17538: (T + "«Web mé firmy» — калька", {"example_cs": "Naše firma má úplně nový web a vypadá super"}),
    17561: (T + "«Moje babička» — книжно", {"example_cs": "Babička má ještě ve sklepě starý psací stroj"}),
    17591: (T + "«Písmo mého lékaře» — тяжело", {"example_cs": "Doktorovo písmo nedokáže rozluštit ani lékárnice"}),
    17666: (T + "«Ve hře mého syna» — тяжело", {"example_cs": "V synově hře má každý druhý nepřítel plamenomet"}),
    17678: (T + "«Algoritmus mého video portálu» — тяжело", {"example_cs": "Algoritmus videoportálu už zná můj vkus líp než já sám"}),
    17794: (T + "«Tento … se svými» — книжно", {"example_cs": "Tenhle měsíc musíme s prostředky šetřit"}),
    17812: (T + "«velmi» — книжно", {"example_cs": "Účast ve volbách byla tentokrát hodně nízká"}),
    17813: (T + "«mé tety» — тяжело", {"example_cs": "Po pandemii byla tetina cestovní kancelář v bankrotu"}),
    17817: (T + "«mé» — лишнее", {"example_cs": "Pro prarodiče bylo vlastní auto tehdy známkou blahobytu"}),
    17857: (T + "«Můj společník a já» — калька", {"example_cs": "Se společníkem vedeme ten podnik spolu"}),
    17942: (T + "«velmi» — книжно", {"example_cs": "Záření z jaderné elektrárny je hodně nebezpečné"}),
    17957: (T + "«Tato» — книжно", {"example_cs": "Tahle látka je jedovatá"}),
    17971: (T + "«mnoho» — книжно", {"example_cs": "Po fúzi s konkurencí se spousta kolegů bojí o práci"}),
    17973: (T + "«mé … velmi» — книжно", {"example_cs": "Pro prarodiče je bydlení s cizími lidmi hodně zvláštní způsob života"}),
    17974: (T + "«Můj děda» — книжно", {"example_cs": "Děda sloužil za války u dělostřelectva a od té doby špatně slyší"}),
    18044: (T + "«tohoto» — книжно", {"example_cs": "Houby z tohohle lesa se nemají jíst, jsou pořád trochu radioaktivní"}),
    18221: (T + "«příliš» — книжно", {"example_cs": "Zahradní hadice je na rostliny moc krátká"}),
    18237: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju lopatu, abych odklidil sníh"}),
}

REPLACE = []

SPLIT_LATER = {}
