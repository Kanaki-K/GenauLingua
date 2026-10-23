"""Вычитка чешского, порция p043 (C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    15160: (T + "«své» — лишнее", {"example_cs": "Máma mě už roky chce dohodit s dcerou kamarádky"}),
    15164: (T + "«jeho tvář vypadá jako děda» — коряво", {"example_cs": "V muzeu visí starý obraz světce a syn si myslí, že má tvář jako děda"}),
    15182: (T + "«syna své sousedky» — тяжело", {"example_cs": "Babička by mě nejradši provdala za milého sousedčina syna"}),
    15191: (T + "«můj» — лишнее", {"example_cs": "Na třídních schůzkách je polovina tátů tetovaná, jen manžel ne"}),
    15192: (T + "«svůj» — лишнее", {"example_cs": "Taxikář mi za dvacet minut vyprávěl celý životní příběh"}),
    15195: (T + "«Náš vánoční večírek» — калька", {"example_cs": "Vánoční večírek se u nás každý rok zvrhne v orgii cukroví a svařáku"}),
    15205: (T + "«mé dcery» — тяжело", {"example_cs": "Na dceřinu oslavu narozenin přijde patnáct dětí a já mám jen dvě ruce"}),
    15208: (T + "«dnes» → «dneska»", {"example_cs": "Na staré fotce je máma brunetka, dneska je blondýnka"}),
    15220: (T + "«mého muže» — тяжело", {"example_cs": "Když k nám přijede celé manželovo příbuzenstvo, nemáme dost židlí"}),
    15256: (T + "«můj strýc» — лишнее", {"example_cs": "V muzeu visí portrét šlechtice, který vypadá úplně jako strejda"}),
    15308: (T + "«můj» — лишнее", {"example_cs": "Po rozvodu se bratr stal pro syna důležitou otcovskou postavou"}),
    15603: (T + "«nedokážu zvládnout» — калька", {"example_cs": "Na zahradě všude roste plevel a nemůžu si s ním poradit"}),
    15624: (T + "«mé malé sestry» — тяжело", {"example_cs": "„Tak co, holubičko, vyspala ses dobře?“ ptá se děda každé ráno malé sestry"}),
    15639: (T + "«dnes» → «dneska»", {"example_cs": "Kvůli sněhové bouři je dneska škola zavřená a děti už v osm staví sněhuláka"}),
    15671: (T + "«moje» — лишнее", {"example_cs": "V horách nosí mezci zavazadla až na chatu a děti se na jednom chtějí za každou cenu svézt"}),
    15692: (T + "«považuje za» — книжно", {"example_cs": "Synovi přijde naše kočka roztomilá, dokud nepřijde s myší v tlamě, pak je pro něj šelma"}),
    15697: (T + "«hledal potravu» — книжно", {"example_cs": "Mýval se nám hrabal v odpadcích a hledal žrádlo"}),
    15704: (T + "«Zdi našeho domu» — тяжело", {"example_cs": "Náš starý hrázděný dům má zdi z hlíny a slámy"}),
    15705: (T + "«Dnes» → «Dneska»", {"example_cs": "Dneska přijde kovář zastřihnout kopyta našemu poníkovi"}),
    15706: (T + "«hynou» — книжно", {"example_cs": "U sousedky se všem pokojovým rostlinám daří, u mě uvadnou"}),
    15707: (T + "«naši» — лишнее", {"example_cs": "Ráno slunce zaplaví celou ložnici"}),
    15710: (T + "«velmi» — книжно", {"example_cs": "Rozhovor s učitelem byl hodně plodný, teď máme plán"}),
    16379: (T + "«našich dětí … mou» — тяжело", {"example_cs": "Pro všechny případy jsme jako poručníka dětí určili sestru"}),
    16383: (T + "«dnes» → «dneska»", {"example_cs": "Před ministerstvem obrany dneska školáci demonstrují za mír"}),
    16394: (T + "смысл и «Moje»", {"example_cs": "Děti chodí do státní školy a peníze, co bychom dali za školné, šetřím na školní výlety"}),
    16395: (T + "«své» — лишнее", {"example_cs": "V seriálu nechá král nepřátele popravit a syn si zakrývá oči"}),
    16398: (T + "«svou daň» — лишнее", {"example_cs": "Tři probdělé noci před zkouškou si vybírají daň, syn usíná v autobuse"}),
    16404: (T + "«mé sestřenice» — тяжело", {"example_cs": "Do sestřeniciny pěstounské rodiny chodí každé tři měsíce někdo z OSPOD"}),
    16416: (T + "«tento» → «tenhle»", {"example_cs": "Sousedka nám tenhle měsíc prominula nájem za zahradu, protože jsme se jí starali o kočku"}),
    16422: (T + "«naše» — лишнее", {"example_cs": "Už několik dní je lednice v obležení, syn roste"}),
    16426: (T + "«Moje» — лишнее", {"example_cs": "Sestřenice je státní zástupkyně a stejně kouká na každou detektivku v televizi"}),
    16441: (T + "«Můj» — лишнее", {"example_cs": "Praděda přijel do Ameriky jako přistěhovalec s jediným kufrem"}),
    16452: (T + "«mé sestřenice» — тяжело", {"example_cs": "Při povodních v USA odvezla národní garda sestřeniciny sousedy na člunech"}),
    16456: (T + "«nazývá … útlakem» — книжно", {"example_cs": "Syn říká zákazu mobilu u jídla útlak a chce v obýváku uspořádat demonstraci"}),
    16465: (T + "«dnes» → «dneska»", {"example_cs": "Sestra je advokátka a dneska má klientku, která se se sousedem hádá o jabloň"}),
    16468: (T + "«nazývá velezradou» — книжно", {"example_cs": "To, že syn prozradil soupeřům naši taktiku, tomu celý tým říká velezrada"}),
    16480: (T + "«dnes» → «dneska»", {"example_cs": "Ve staré pevnosti nad městem dřív sídlila posádka, dneska je tam kavárna s výhledem"}),
    16493: (T + "«mé dcery» — тяжело", {"example_cs": "Dceřino ztracené kolo stálo po dvou dnech na dvoře policejní stanice"}),
    16497: (T + "«se považuje za» — книжно", {"example_cs": "S dětským odznakem si syn připadá jako nejdůležitější strážce zákona v ulici"}),
    16504: (T + "«naše auto» — лишнее", {"example_cs": "Kvůli pouliční slavnosti uzavřeli naši ulici na celou sobotu a auto nám uvízlo v garáži"}),
    16539: (T + "«svým» — лишнее", {"example_cs": "Bratr mě spoilerem připravil o všechno napětí, teď znám konec seriálu"}),
    16547: (T + "«dnes» → «dneska»", {"example_cs": "Po hodině dějepisu chce syn vědět, kolik zemí má dneska jaderné zbraně"}),
    16557: (T + "«Moje tajná zbraň … je» — калька", {"example_cs": "Když děti nechtějí nastoupit do auta, mám tajnou zbraň: sáček gumových medvídků"}),
}

REPLACE = []

SPLIT_LATER = {}
