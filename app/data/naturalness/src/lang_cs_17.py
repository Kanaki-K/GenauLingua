"""Вычитка чешского, порция p017 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    8863: (T + "«velmi» — книжно", {"example_cs": "Malíř namaloval moc krásný obraz"}),
    8879: (T + "«v této» — книжно", {"example_cs": "Zaměstnankyně pracuje v téhle firmě už deset let"}),
    9050: (T + "«Jeho práce … velmi» — книжно", {"example_cs": "Práce učitele ho hodně naplňovala"}),
    9204: (T + "«bude zvýšení» — калька", {"example_cs": "Od ledna nás čeká zvýšení nájmu o padesát eur"}),
    9242: (T + "«přijíždí» — не то", {"example_cs": "Popelář jezdí každé pondělí ráno"}),
    9275: (T + "«velmi» — книжно", {"example_cs": "Dneska jsem byl hodně produktivní a hodně jsem toho stihl"}),
    9446: (T + "«velmi» — книжно", {"example_cs": "Mluví moc dobře francouzsky"}),
    9451: (T + "«své» — лишнее", {"example_cs": "Učím dítě plavat"}),
    9457: (T + "«Právě» — книжно", {"example_cs": "Zrovna čtu první kapitolu"}),
    9536: (T + "«kreslím» — не тот вид", {"example_cs": "Kružítkem nakreslím kruh"}),
    9551: (T + "«můžete» — man", {"example_cs": "V knihkupectví za rohem si můžeš dát i kávu"}),
    9565: (T + "«Vyndávám … vytahuji» — не тот вид", {"example_cs": "Vyndám věci z aktovky a vytáhnu úkoly"}),
    9592: (T + "«pero je prázdné» — калька", {"example_cs": "V plnicím peru mi došel inkoust, potřebuju nový"}),
    9631: (T + "«této … velmi» — книжно", {"example_cs": "Na téhle soukromé škole je školné hodně vysoké"}),
    9632: (T + "«velmi» — книжно", {"example_cs": "Moje oblíbená kniha je hrozně napínavá a čtu ji pořád dokola"}),
    9635: (T + "«velmi» — книжно", {"example_cs": "Výlet do muzea byl pro děti hodně poučný"}),
    9638: (T + "«Můj pravopis» — калька", {"example_cs": "Pravopis nemám vždycky dokonalý"}),
    9733: (T + "«Dostávám» — не тот вид", {"example_cs": "Dostanu šek na 100 eur"}),
    9739: (T + "«svou» — лишнее", {"example_cs": "Za pomoc dostaneš odměnu"}),
    9756: (T + "«Jaké značky je» — калька", {"example_cs": "Jakou značku má tvoje auto?"}),
    9773: (T + "«své» — лишнее", {"example_cs": "V kabelce nikdy nic nenajde"}),
    9852: (T + "«svůj» — лишнее", {"example_cs": "Mrknu se na bankovní účet"}),
    9941: (T + "«téměř» — книжно", {"example_cs": "V obchodě s potravinami za rohem nakupuju skoro každý den"}),
}

REPLACE = []

SPLIT_LATER = {}
