"""Вычитка чешского, порция p049 (C2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    16724: (T + "«třída mé dcery» — тяжело", {"example_cs": "V památníku viděla dceřina třída i plynovou komoru, potom dlouho nikdo nepromluvil"}),
    16733: (T + "«Pro své zpoždění» — калька", {"example_cs": "Na zpoždění má syn vždycky připravenou výmluvu: jednou autobus, jindy pes"}),
    16741: (T + "«moje» — лишнее", {"example_cs": "Dokud je šéf na dovolené, má velení v kanceláři kolegyně"}),
    16743: (T + "«nazývá … pokusem» — книжно", {"example_cs": "Bratr říká mému chili se třemi papričkami pokus o vraždu"}),
    16751: (T + "«své» — лишнее", {"example_cs": "Syn si z kartonu a ruliček od toaletního papíru postavil raketomet pro figurky z lega"}),
    16752: (T + "«Moje» — лишнее", {"example_cs": "Polská kolegyně vypráví, jak její rodiče v roce 1981 žili za stanného práva"}),
    16753: (T + "«mými dvěma» — лишнее", {"example_cs": "Mezi oběma dětmi je od snídaně příměří"}),
    16754: (T + "«dnes» → «dneska»", {"example_cs": "Na letišti dneska platí nejvyšší bezpečnostní stupeň, kontroly trvají věčnost"}),
    16777: (T + "«Moje» — лишнее", {"example_cs": "Teta sedí v zastupitelstvu a její frakce se na každém zasedání hádá o cyklostezky"}),
    16837: (T + "«považuje za» — книжно", {"example_cs": "V muzeu stojí skutečná gilotina, synovi přijde strašidelná i napínavá zároveň"}),
    16848: (T + "«právě» → «zrovna»", {"example_cs": "V angličtině se dcera zrovna učí o Prvním dodatku americké ústavy"}),
    16862: (T + "«Můj» — лишнее", {"example_cs": "Daňový poradce vždycky najde nějakou kličku, aby mi vyšla menší daň"}),
    16863: (T + "«Můj … dnes» — книжно", {"example_cs": "Kolega vyrůstal v ghettu v Chicagu, dneska je dětský lékař"}),
    16876: (T + "«svého» — лишнее", {"example_cs": "Firma vyšle na konferenci zástupce"}),
    16879: (T + "«Moje» — лишнее", {"example_cs": "Sousedka pracuje na ministerstvu financí a na podzim často chodí domů až pozdě"}),
    16883: (T + "«Můj … dnes» — книжно", {"example_cs": "Strejda byl jako fotograf v mnoha válečných zónách, dneska fotí už jen svatby"}),
    16894: (T + "«tajná … tajně» — повтор", {"example_cs": "V muzeu Stasi je vidět, jak tajná policie potají otevírala dopisy"}),
    16901: (T + "«Moji» — лишнее", {"example_cs": "Prarodiče se seznámili v roce 1946 v uprchlickém táboře"}),
    16904: (T + "«mého» — лишнее", {"example_cs": "U strejdy se i grilování stává ideologií: jen dřevěné uhlí, nikdy plyn"}),
    16906: (T + "«raději» → «radši»", {"example_cs": "Bulvár rád píše „pedofil“, policie radši mluví o pachatelích zneužívání"}),
    16908: (T + "«Můj» — лишнее", {"example_cs": "Bratr je vykonavatelem dědovy závěti a stará se o všechno"}),
    16931: (T + "«svou» — лишнее", {"example_cs": "Čtvrtého července slaví Američané Deklaraci nezávislosti z roku 1776"}),
    16947: (T + "«Můj» — лишнее", {"example_cs": "Americký švagr volí republikány, sestra demokraty"}),
    16950: (T + "«můj» — лишнее", {"example_cs": "V dětském pokoji je syn malý anarchista: tam neplatí žádná pravidla"}),
    16958: (T + "«můj» — лишнее", {"example_cs": "Po osmi letech v Německu žádá kolega o německé státní občanství"}),
    16961: (T + "«je považován za» — книжно", {"example_cs": "Ve firmě se šéfovu synovi už dlouho říká korunní princ"}),
    16967: (T + "«Můj … svých» — лишнее", {"example_cs": "Strejda je obhájce v trestních věcech a u jídla nikdy nemluví o případech"}),
    16975: (T + "«moje žena» — лишнее", {"example_cs": "Na třídních schůzkách láme manželka kopí za mladou učitelku"}),
    17344: (T + "«této» → «téhle»", {"example_cs": "Na téhle dálnici je maximální rychlost 130 kilometrů za hodinu"}),
    17353: (T + "«dnes» → «dneska»", {"example_cs": "Kvůli dopravní nehodě na mostě dneska všichni přijdou pozdě do práce"}),
    17363: (T + "«svým» — лишнее", {"example_cs": "V neděli si děda rád udělá projížďku veteránem po vesnicích"}),
    17380: (T + "«zahajuje» — книжно", {"example_cs": "Letadlo začíná přiblížení na přistání, za 15 minut přistaneme"}),
    17385: (T + "«která je dnes muzeem» — тяжело", {"example_cs": "V San Diegu je ze staré letadlové lodi muzeum"}),
    17402: (T + "«opravdová» — книжно", {"example_cs": "Deštivý červen je pro naše grilovací plány pořádná studená sprcha"}),
    17660: (T + "«Můj» — лишнее", {"example_cs": "Učitel fyziky postavil ze starého rádia malý vysílač"}),
    17667: (T + "«dnes» → «dneska»", {"example_cs": "Výtah je dneska kvůli údržbě mimo provoz, musíme jít po schodech"}),
    17670: (T + "«Můj» — лишнее", {"example_cs": "Mobil automaticky šifruje všechny fotky"}),
    17689: (T + "«moje» — лишнее", {"example_cs": "Trojan mi napadl počítač a ukradl všechna data"}),
    17736: (T + "«v mé kapse» — калька", {"example_cs": "Pager v kapse vždycky pípá v nevhodnou chvíli"}),
    17865: (T + "«moje» — лишнее", {"example_cs": "Kvůli inflaci stojí oblíbená houska v pekárně skoro euro"}),
    17876: (T + "«svým» — лишнее", {"example_cs": "„Čas na spaní není k jednání,“ říká sestra dětem"}),
    17877: (T + "«moje» — лишнее", {"example_cs": "Pro děti je sekání trávníku za dvě eura na hodinu čisté vykořisťování"}),
    17885: (T + "«moje kondice je» — калька", {"example_cs": "Po třech patrech nemůžu popadnout dech, kondici mám katastrofální"}),
    18052: (T + "«své» — лишнее", {"example_cs": "Ve staré detektivce, kterou babička miluje, otráví dvě milé tety hosty arsenem"}),
}

REPLACE = []

SPLIT_LATER = {}
