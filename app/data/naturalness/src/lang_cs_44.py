"""Вычитка чешского, порция p044 (C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    16468: (T + "«To… tomu» — коряво (после p043)", {"example_cs": "Celý tým říká velezrada tomu, že syn prozradil soupeřům naši taktiku"}),
    16564: (T + "«Můj pradědeček» — лишнее", {"example_cs": "Praděda byl za války dezertér a v rodině o tom dlouho nikdo nemluvil"}),
    16567: (T + "«svou» — лишнее", {"example_cs": "Dcera přichází ze školy s celou družinou, pět kamarádek u nás chce jíst"}),
    16571: (T + "«Můj» — лишнее", {"example_cs": "Mladší brácha je hrozný slídil, tajně mi čte deník"}),
    16572: (T + "«skutečná» — книжно", {"example_cs": "Elektrika v našem starém domě je hotová časovaná bomba"}),
    16579: (T + "«našeho města … dnes» — тяжело", {"example_cs": "U nás na náměstí stojí pomník válečného hrdiny, kterého už dneska nikdo nezná"}),
    16581: (T + "«Na základě» — канцелярит", {"example_cs": "Podle soudního rozhodnutí musí soused konečně zkrátit živý plot na dva metry"}),
    16590: (T + "«občanský průkaz» — книжно", {"example_cs": "Na novou občanku potřebuju tři termíny — ta byrokracie je tady neuvěřitelná"}),
    16605: (T + "«Můj» — лишнее", {"example_cs": "Malý synovec je hotový vyděrač: bez zmrzliny si bundu neobleče"}),
    16607: (T + "«doprovázíme» — калька", {"example_cs": "V dokumentu o Africe sledujeme strážce, kteří v noci hledají pytláky"}),
    16612: (T + "«naše kočka» — лишнее", {"example_cs": "Při krádeži sušenek z plechovky je kočka moje komplicka"}),
    16833: (T + "«dnes» → «dneska»", {"example_cs": "Když dneska malému dovolíme zmrzlinu k snídani, vytvoříme precedens"}),
    16834: (T + "«tento» → «tenhle»", {"example_cs": "Městská knihovna má tenhle týden amnestii: kdo vrátí staré knihy, neplatí pokutu"}),
    16849: (T + "«v našem městě» — калька", {"example_cs": "Podle statistik počet násilných trestných činů u nás ve městě klesl"}),
    16915: (T + "«probíhá skutečná» — книжно", {"example_cs": "Mezi kočkami z naší ulice je hotová válka gangů o nejlepší revír"}),
    16927: (T + "«barel s vodou» — не то", {"example_cs": "Zástupci rodičů vymohli, že škola dostane výdejník vody"}),
    16988: (T + "«Můj … respekt» — падеж", {"example_cs": "Děda nikdy neměl moc respektu před vrchností, ani před farářem"}),
    17223: (T + "«K zlaté» → «Ke zlaté»", {"example_cs": "Ke zlaté svatbě dáváme rodičům plavbu po Dunaji"}),
    17240: (T + "«můj telefon» — калька", {"example_cs": "Při lezení mi naštěstí spadl jen telefon, ne já"}),
    17257: (T + "«svých» — лишнее", {"example_cs": "Syn počítá dráhu letu papírových vlaštovek, jako by pracoval v NASA"}),
    17279: (T + "«můj» — лишнее", {"example_cs": "Ve veslařském klubu je synovec kormidelník, protože je nejlehčí"}),
    17281: (T + "«moc miluje» — калька", {"example_cs": "Tuhle pasáž z knihy čtu dceři každý večer, protože ji má tak ráda"}),
    17314: (T + "«moje máma» — лишнее", {"example_cs": "Když volá máma, manžel pokaždé udělá elegantní úhybný manévr a podá mi telefon"}),
    17602: (T + "«Můj» — лишнее", {"example_cs": "Nový notebook má jen dva porty a pořád potřebuju nějakou redukci"}),
    17629: (T + "«převodovka našeho auta» — тяжело", {"example_cs": "Od zimy dělá převodovka v našem starém autě divné zvuky, ale táta to nechce slyšet"}),
    17638: (T + "«svou» — лишнее", {"example_cs": "Při vánoční hře přeruší zvonění mobilu přesně místo, kde dcera říká jedinou větu"}),
    17652: (T + "«svou» — лишнее", {"example_cs": "Táta má v obýváku pořád starou hi-fi věž z osmdesátek"}),
    17653: (T + "«musí naše auto» — калька", {"example_cs": "Kvůli svolávací akci musíme příští týden s autem do servisu"}),
    17704: (T + "«můj» — лишнее", {"example_cs": "V kanceláři se notebook automaticky připojí k velkému monitoru"}),
    17829: (T + "«v našem městě» — тяжело", {"example_cs": "Zoo se teď u nás ve městě propaguje na každém autobuse obrovským obrázkem tučňáka"}),
    17980: (T + "«mé dcery» — тяжело", {"example_cs": "Na dceřině posteli bydlí celá legie plyšáků, pro ni samotnou skoro není místo"}),
    18000: (T + "«nad jeho postelí» — калька", {"example_cs": "Syn vyrobil celou sluneční soustavu z polystyrenových koulí a teď mu visí nad postelí"}),
    18005: (T + "«právě» → «zrovna»", {"example_cs": "Nová čistička vzduchu v dětském pokoji ukazuje, kolik částic je zrovna ve vzduchu"}),
    18022: (T + "«Můj» — лишнее", {"example_cs": "Kadeřník rád experimentuje, proto mám teď modré vlasy"}),
    18031: (T + "«naladěni na» — калька", {"example_cs": "S novou kolegyní jsme hned na stejné vlnové délce"}),
    18291: (T + "«své» — лишнее", {"example_cs": "Před svatbou děda dvě hodiny leštil staré boty"}),
    18332: (T + "«kdo je chycen» — пассив", {"example_cs": "Na dětské oslavě je sklep naše kobka a koho chytí, musí zazpívat písničku"}),
    18335: (T + "«Můj oblíbený svetr» — калька", {"example_cs": "Oblíbený svetr mi byl v sušičce jen deset minut a teď je akorát dceři"}),
    18356: (T + "«Moje láhev» — калька", {"example_cs": "Láhev na pití je netěsná a teď mám v batohu mokré všechny sešity"}),
    18365: (T + "«Na mém» — калька", {"example_cs": "Na nočním stolku se mi kupí pět rozečtených knih"}),
    18794: (T + "«mé sousedky» — тяжело", {"example_cs": "Sousedčin životní styl je pro mě záhada: pracuje v noci a běhá ve dvě odpoledne"}),
}

REPLACE = []

SPLIT_LATER = {}
