"""Вычитка чешского, порция p040 (C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    9093: (T + "«Můj rozvrh je tento týden» — калька", {"example_cs": "Tenhle týden mám tak nabitý rozvrh, že nemám čas ani na kadeřníka"}),
    9109: (T + "«s jeho» — лишнее", {"example_cs": "Na hrázi často potkáváme ovčáka se dvěma psy"}),
    9145: (T + "«můj» — лишнее", {"example_cs": "Při grilování dělá mladší brácha tátovi pobočníka a podává mu všechny kleště"}),
    9217: (T + "«Ve volbě» — предлог", {"example_cs": "Při volbě předsedy třídy dcera odmítla nominaci, protože se jí nechtělo"}),
    9543: (T + "«svého» — лишнее", {"example_cs": "Na třídním srazu táta nepoznal bývalého souseda z lavice, protože je teď plešatý"}),
    9552: (T + "«zjišťuje recenze» — коряво", {"example_cs": "Než koupíme vysavač, manžel tři večery zjišťuje, co o nich píšou v testech"}),
    9567: (T + "«velmi» — книжно", {"example_cs": "Na staré fotce vypadá babička jako školačka s copánky hrozně vážně"}),
    9848: (T + "«Moje úspory» — калька", {"example_cs": "Úspory mi stačí sotva na dovolenou"}),
    9851: (T + "«svou» — лишнее", {"example_cs": "Syn vyměnil svačinu za dvě sušenky od kamaráda"}),
    9862: (T + "«získal» — книжно", {"example_cs": "Na bleším trhu koupil táta za dvě eura staré rádio, které dokonce ještě funguje"}),
    10814: (T + "«Se svou» — лишнее", {"example_cs": "Se školní francouzštinou jsem se v restauraci v Paříži pořádně ztrapnil"}),
    10823: (T + "«Synovi se povedlo» — тяжело", {"example_cs": "Syn halloweenskou maskou nahnal babičce pořádný strach"}),
    10877: (T + "«s trochou víc» — коряво", {"example_cs": "Po třetí prohře s malou sestrou hraje syn šachy s o trochu větší pokorou"}),
    10906: (T + "«cítí svou mužnost ohroženou» — калька", {"example_cs": "Bratr má pocit, že je ohrožená jeho mužnost, když si má u grilu vzít zástěru"}),
    10909: (T + "«vede existenci» — калька", {"example_cs": "Kočka má nádherný život: spát, žrát a nechat se obsluhovat celým domem"}),
    10910: (T + "«velmi … jejích» — книжно", {"example_cs": "Ve dvanácti je dcera hrozně citlivá, každá poznámka o vlasech ji hluboce zraní"}),
    10919: (T + "«svůj» — лишнее", {"example_cs": "Táta nedokáže zapřít bavorský přízvuk ani po třiceti letech v Hamburku"}),
    10922: (T + "«Můj švagr» — лишнее", {"example_cs": "Švagr je pravý fanatik do fitness, dělá kliky i na svatbě"}),
    10923: (T + "«považují za» — книжно", {"example_cs": "Dětem přijde bezcitné, že pavouka vypustíme z okna, místo abychom mu dali jméno"}),
    10937: (T + "«moje trpělivá žena» — лишнее", {"example_cs": "Při třetím rozlitém džusu za ráno ztratí sebeovládání i jinak trpělivá manželka"}),
    10942: (T + "«považuje za» — книжно", {"example_cs": "Dceři přijde nemorální jíst vejce slepic, které nesmějí volně pobíhat"}),
    10948: (T + "«mými» — лишнее", {"example_cs": "O poslední kousek pizzy je mezi syny skoro pokaždé malá rvačka"}),
    10949: (T + "«Můj … svého» — лишнее", {"example_cs": "Malý syn zbožňuje staršího bratrance a dělá všechno po něm"}),
    10960: (T + "«moje malá sestra» — лишнее", {"example_cs": "V Monopolech je malá sestra nemilosrdná, koupí všechno a ještě se směje"}),
    10964: (T + "«při jídle pizzy» — калька", {"example_cs": "Jen u pizzy jsou všechny tři děti v naprostém souladu"}),
    10970: (T + "«velmi» — книжно", {"example_cs": "Na svatbu si děda koupil hodně noblesní klobouk a teď ho chce nosit každou neděli"}),
    10974: (T + "нет слова карточки", {"example_cs": "Děti se mi vysmívají, protože nevím, jak dát video na internet"}),
    10976: (T + "«náš pes» — порядок слов", {"example_cs": "Pes s velkou touhou sleduje každý kousek salámu, který by mohl spadnout ze stolu"}),
    10993: (T + "«velmi» — книжно", {"example_cs": "Učitelka byla hodně chápavá, když syn po narození sestry zapomněl na úkoly"}),
    10997: (T + "«raději» → «radši»", {"example_cs": "Naše kočka je úplně neposlušná: čím častěji říkáme „Dolů ze stolu!“, tím radši tam skáče"}),
    11010: (T + "«mého» — лишнее", {"example_cs": "V zácpě se u jinak klidného manžela objeví agrese, kterou u něj vůbec neznám"}),
    11013: (T + "«velmi» — книжно", {"example_cs": "Noví sousedé jsou hodně ohleduplní a po desáté večer už neperou"}),
    11016: (T + "«velmi» — книжно", {"example_cs": "Tchyně je hodně věřící a modlí se před každým jídlem, i v restauraci"}),
    11019: (T + "«mého syna» — тяжело", {"example_cs": "Synovo vysvědčení je letos potěšující, hlavně v matematice se zlepšil"}),
    11022: (T + "«tutéž» — книжно", {"example_cs": "Dcera se poprvé trápí z lásky a už tři dny poslouchá pořád stejnou smutnou písničku"}),
    11027: (T + "«svůj» — лишнее", {"example_cs": "Na pozvánce stojí „kostým vítán“ a manžel od včerejška hledá pirátský klobouk"}),
}

REPLACE = []

SPLIT_LATER = {}
