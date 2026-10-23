"""Вычитка чешского, порция p042 (C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    12822: (T + "«Moje … svou práci» — лишнее", {"example_cs": "Kamarádka pracuje jako sestra na psychiatrickém oddělení a práci miluje"}),
    12851: (T + "«tento» → «tenhle»", {"example_cs": "V těhotenské aplikaci manžel každý týden sleduje, jak velký je plod: tenhle týden jako citron"}),
    12852: (T + "«dnes» → «dneska»", {"example_cs": "Starý lazaret na okraji města je dneska kavárna a na dlaždicích jsou ještě vidět čísla pokojů"}),
    12865: (T + "«moje malá» — лишнее", {"example_cs": "Od té doby, co chodí do školky, je malá hrozně náchylná k nachlazení"}),
    12869: (T + "«jakéhosi» — книжно", {"example_cs": "Při žehlení někdy upadnu do takového transu, že přestanu slyšet děti"}),
    12873: (T + "«Moje chytré hodinky» — калька", {"example_cs": "Chytré hodinky mi měří tep i v noci"}),
    13567: (T + "«můj» — лишнее", {"example_cs": "Leckdo usne ve vlaku a probudí se až na konečné, jako manžel minulý týden"}),
    13571: (T + "«dnes» → «dneska»", {"example_cs": "Autobus nejel, takže dneska přijdu o hodinu později"}),
    13572: (T + "«Dnes» → «Dneska»", {"example_cs": "Dneska do posilovny nejdu, zvlášť když prší"}),
    13715: (T + "«darovali» — книжно", {"example_cs": "Děda nosí každou neděli stejnou košili s modrým károvaným vzorem, už jsme mu dali tři nové"}),
    13722: (T + "«svou» — лишнее", {"example_cs": "Babiččiny svatební šaty visí padesát let ve skříni a sestra si je chce vzít na svatbu"}),
    13729: (T + "«daruju … její» — книжно", {"example_cs": "K desátým narozeninám dám dceři první manikúru a ona si vybrala barvy duhy"}),
    14126: (T + "«svého» — лишнее", {"example_cs": "Dovolenou si syn tentokrát hradí celou z vlastního kapesného"}),
    14133: (T + "«můj muž» — лишнее", {"example_cs": "Že jsou všichni Němci dochvilní, je klišé, manžel chodí vždycky pozdě"}),
    14164: (T + "«mých e-mailů» — тяжело", {"example_cs": "V podpisu e-mailů mám pořád staré telefonní číslo a nikdo se mi nedovolá"}),
    14178: (T + "«svou» — лишнее", {"example_cs": "Táta líčí cestu do Norska tak živě, že bychom tam nejradši hned jeli"}),
    14565: (T + "«své» — лишнее", {"example_cs": "Můžeš mi předvést nové taneční kroky, než přijdou hosté?"}),
    14570: (T + "«Moje rodina je» — калька", {"example_cs": "Jsme katolická rodina a každou neděli chodíme do kostela"}),
    14577: (T + "«svou» — лишнее", {"example_cs": "Každý večer mi syn zahraje na flétnu novou písničku"}),
    14578: (T + "«probíhá natáčení» — книжно", {"example_cs": "V naší ulici je zrovna natáčení detektivky a všichni sousedé stojí u oken"}),
    14586: (T + "«Moji» — лишнее", {"example_cs": "Tři synové si říkají tři mušketýři a bojují v chodbě vařečkami"}),
    14589: (T + "«mé neteře» — тяжело", {"example_cs": "Na neteřino biřmování přijede i arcibiskup a celá rodina se strojí"}),
    14594: (T + "«své» — лишнее", {"example_cs": "Dcera navrhla pro panenky celou kolekci šatů ze starých ponožek"}),
    14598: (T + "«moje» — лишнее", {"example_cs": "Na rodinných oslavách je malá sestra nejradši ve světlech ramp a zpívá pro všechny"}),
    14603: (T + "«Velmi … svůj» — книжно", {"example_cs": "Syn mi úplně slavnostně předává první dárek, který sám vyrobil: korunu z kartonu"}),
    14605: (T + "«v našem sklepě» — калька", {"example_cs": "Syn si myslí, že u nás ve sklepě bydlí něco nadpřirozeného, a přitom je to jen topení"}),
    14628: (T + "«mých prarodičů» — лишнее", {"example_cs": "Milostný příběh prarodičů začal ztraceným deštníkem na autobusové zastávce"}),
    14637: (T + "«darovala» — книжно", {"example_cs": "K narozeninám nám sestra dala lístky do lóže v opeře, jako ve filmu"}),
    14645: (T + "«své» — лишнее", {"example_cs": "Děda píše paměti a po roce je teprve u první krávy"}),
    14647: (T + "«svým» — лишнее", {"example_cs": "Synovec natáčí mobilem krátké filmy s křečkem a už si říká filmař"}),
    14656: (T + "«Moje … velmi» — книжно", {"example_cs": "Babička je hrozně pověrčivá a vyhýbá se černým kočkám"}),
    14667: (T + "«velmi» — книжно", {"example_cs": "Děda jí i pizzu příborem, je to prostě hodně kultivovaný člověk"}),
    14671: (T + "«moje» — лишнее", {"example_cs": "Když vypadne wifi, je to pro děti konec světa"}),
    15139: (T + "«Můj … svým» — лишнее", {"example_cs": "Strejda je homosexuální a třicet let žije s manželem ve stejné vesnici"}),
}

REPLACE = []

SPLIT_LATER = {}
