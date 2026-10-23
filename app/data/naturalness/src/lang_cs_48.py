"""Вычитка чешского, порция p048 (C2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    14701: (T + "«se koná … na počest» — книжно", {"example_cs": "Ke stému výročí školy bude vzpomínková slavnost na její zakladatelku"}),
    14702: (T + "«můj» — лишнее", {"example_cs": "Při ladění kytary učitel hned slyší, jestli je kvinta čistá"}),
    14731: (T + "«svém» — лишнее", {"example_cs": "Teta slyší v noci ve starém domě paranormální zvuky, ale je to jen topení"}),
    14739: (T + "«dnes» → «dneska»", {"example_cs": "Staré opatství na kopci je dneska hotel a snídá se v křížové chodbě"}),
    14740: (T + "«jeho» — лишнее", {"example_cs": "Pro syna je sbírka fotbalových kartiček posvátná věc"}),
    14756: (T + "«právě» → «zrovna»", {"example_cs": "V náboženství se dcera zrovna učí, jak vzniklo křesťanství"}),
    14764: (T + "«velmi» — книжно", {"example_cs": "Refrén té písničky je hodně chytlavý"}),
    14766: (T + "«mé» — лишнее", {"example_cs": "Na svatbě kolegyně měl imám krátký proslov i v němčině"}),
    14767: (T + "«Moji … svého» — лишнее", {"example_cs": "Rodiče se každý večer dívají na díl tureckého seriálu"}),
    14777: (T + "«Svou» — лишнее", {"example_cs": "Starou desku Beatles si pořád rád pouští"}),
    14797: (T + "«Moje poznámky» — калька", {"example_cs": "Poznámky z přednášek mám pro všechny ostatní jako hieroglyfy"}),
    14821: (T + "«jakési» — книжно", {"example_cs": "Před každou písemkou z matiky syn mumlá nějaké zaříkávání"}),
    15216: (T + "«Můj» — лишнее", {"example_cs": "Brácha dvojče mi vždycky zavolá, když jsem nemocný, jako by to cítil"}),
    15223: (T + "«na mou klávesnici» — калька", {"example_cs": "Náš kocour mi sedne zadkem přímo na klávesnici"}),
    15225: (T + "«svého» — лишнее", {"example_cs": "Malý jezevčík táhne páníčka na vodítku přes celou ulici"}),
    15230: (T + "«svého otce» — книжно", {"example_cs": "Syn je přesná kopie táty"}),
    15251: (T + "«můj … skutečný» — книжно", {"example_cs": "S třiceti lety ve firmě je kolega pravý veterán, zná každý fígl"}),
    15267: (T + "«Moje … a já» — калька", {"example_cs": "S nejlepší kamarádkou jsme spřízněné duše, často si voláme ve stejnou chvíli"}),
    15278: (T + "«svého» — лишнее", {"example_cs": "Bez medvídka malý prostě neusne"}),
    15284: (T + "«ve své chatě» — лишнее", {"example_cs": "Od důchodu žije strýc jako poustevník na chatě na horách"}),
    15285: (T + "«svou» — лишнее", {"example_cs": "Táta chrání starou motorku jako oko v hlavě"}),
    15293: (T + "«dnes» → «dneska»", {"example_cs": "V místních novinách je dneska krásný nekrolog naší staré učitelky ze základní školy"}),
    15305: (T + "«můj» — лишнее", {"example_cs": "Ve finské sauně nahota nikomu nevadí, jen americký kolega byl v šoku"}),
    15329: (T + "«Z mého syna … opravdový» — тяжело", {"example_cs": "Ze syna je teď pořádný čahoun, jak rychle roste"}),
    15330: (T + "«Můj» — лишнее", {"example_cs": "Praděda v devadesáti není žádný nemohoucí stařec, pořád jezdí každý den na kole"}),
    15747: (T + "«moje schránka» — калька", {"example_cs": "Od té doby, co jsem dala inzerát na bazar, mám schránku zaplavenou e-maily"}),
    15785: (T + "«Můj» — лишнее", {"example_cs": "Praděda zažil jako dítě hladomor a dodnes nevyhodí ani kousek chleba"}),
    15788: (T + "«naše … opravdu» — книжно", {"example_cs": "Po třech týdnech u moře vypadá sousedka fakt kvetoucí"}),
    15796: (T + "«svého» — лишнее", {"example_cs": "V zimě se s dekou a čajem stáhnu do kokonu na gauči"}),
    15830: (T + "«její … moje» — лишнее", {"example_cs": "Když jde o děti, jinak mírná sestra se mění ve lvici"}),
    15834: (T + "«své» — лишнее", {"example_cs": "Kvůli nové silnici přicházejí žáby u rybníka o stanoviště"}),
    16622: (T + "«naší» — лишнее", {"example_cs": "Dodání nové pohovky se o dva týdny zpozdí"}),
    16623: (T + "«svůj» — лишнее", {"example_cs": "Teta mi odkázala starý šicí stroj, pořád jede jako nový"}),
    16626: (T + "«Moji» — лишнее", {"example_cs": "Prarodiče dodnes neradi mluví o době za starého režimu"}),
    16645: (T + "«právě» → «zrovna»", {"example_cs": "V rádiu ministr spravedlnosti zrovna mluvil o novém nájemním zákoně"}),
    16672: (T + "«právě» → «zrovna»", {"example_cs": "V dějepisu se dcera zrovna učí, jak se v Itálii dostali k moci fašisté"}),
    16675: (T + "«své» — лишнее", {"example_cs": "Naše starostka za funkční období nechala postavit tři nová hřiště"}),
    16676: (T + "«Můj» — лишнее", {"example_cs": "Praděda byl za války partyzánem v horách, nikdy o tom nerad mluvil"}),
    16684: (T + "«Moji» — лишнее", {"example_cs": "Rodiče vyrostli v socialismu a ještě si pamatují fronty před obchody"}),
    16712: (T + "«potřebuji» → «potřebuju»", {"example_cs": "Na fyzioterapii potřebuju předpis od praktického lékaře"}),
}

REPLACE = []

SPLIT_LATER = {}
